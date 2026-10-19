---
name: payments-stripe
description: Taking payments with Stripe Checkout and webhooks, in test mode first, without trusting the browser.
---
# Stripe payments

1. **Test mode only until the user says otherwise.** Keys starting `sk_test_` and `pk_test_` come from the Stripe dashboard. Put the secret key in `.env` as `STRIPE_SECRET_KEY`, never in client code, never in git, never printed. Real `sk_live_` keys are the user's to add.
2. **Install.** `npm i stripe` or `pip install stripe`.
3. **Create a Checkout Session on the server.**
   ```
   const session = await stripe.checkout.sessions.create({
     mode: "payment",
     line_items: [{ price: "price_123", quantity: 1 }],
     success_url: `${BASE}/thanks?session_id={CHECKOUT_SESSION_ID}`,
     cancel_url: `${BASE}/cart`,
     metadata: { orderId },
   });
   // redirect the browser to session.url
   ```
   Create products and prices in the dashboard or with `stripe products create`. Look up the price on the server, never accept an amount from the browser.
4. **Never trust the client.** The success page URL proves nothing. Mark an order paid only when your webhook receives `checkout.session.completed` (check `payment_status === "paid"`).
5. **Webhook endpoint with signature check.** Use the raw request body, not parsed JSON:
   ```
   const event = stripe.webhooks.constructEvent(rawBody, req.headers["stripe-signature"], process.env.STRIPE_WEBHOOK_SECRET);
   ```
   Return 400 if it throws. Return 200 quickly, do slow work after. In Next.js route handlers use `await req.text()` for the raw body.
6. **Be idempotent.** Stripe can send an event twice. Store `event.id` or the session id and skip repeats.
7. **Test locally with the Stripe CLI** (`brew install stripe/stripe-cli/stripe`):
   ```
   stripe login
   stripe listen --forward-to localhost:3000/api/webhook
   stripe trigger checkout.session.completed
   ```
   `listen` prints a `whsec_...` secret, use it as `STRIPE_WEBHOOK_SECRET` locally. Test card: `4242 4242 4242 4242`, any future date, any CVC.
8. **Go live** (user does this): swap in live keys, create a live webhook endpoint in the dashboard, set its own signing secret.

Pitfalls: parsing the body before verifying the signature, using the test webhook secret in production, storing card data yourself (never), forgetting refunds and failed payments, amounts are in the smallest unit (cents).
