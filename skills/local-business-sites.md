---
name: local-business-sites
description: Building a one-page website for a local business in a named trade (barber, plumber, restaurant, auto shop, dentist and similar).
---
# Local business sites

A local site has one job: get a nearby person to call, book or walk in. Build for that.

1. **Get the facts first.** Business name, trade, address, phone, hours, services, and any real photos or reviews the owner has. If something is missing, leave it out or ask. Never invent it.
2. **Pick sections for the trade.**
   - Barber, salon: services with prices, book button, gallery of real work, hours.
   - Plumber, electrician, HVAC: phone number at the top, service area, "24/7" only if true, license number, services list.
   - Restaurant, cafe: menu (as text, not a PDF image), hours, address, reservations or order link, photos of the food.
   - Auto shop: services, brands serviced, warranty, hours, drop-off info, phone.
   - Dentist, clinic: services, insurance accepted, new patient info, booking, address with parking notes.
3. **Make contact one tap.** Use `<a href="tel:+15555550123">` for the phone, a sticky call button on mobile, and `mailto:` only as a backup. Put the phone in the header and the footer.
4. **Real map and hours.** Embed the business location with a map iframe or link to the maps listing. Write hours as a list per day, and mark holidays if known.
5. **Look like the trade.** A barber shop can be dark, bold and condensed type. A dentist should be clean, bright and calm. A plumber should be plain and trustworthy. Pick fonts and colors from the shop itself: its sign, logo, or van. Do not reuse one template for every trade.
6. **Write like the owner talks.** Short, specific lines: "Fades from $25, walk-ins welcome." Not "premier grooming experience".
7. **Proof, honestly.** Use only real reviews with the reviewer's permission, or link to the real listing. No fake star counts, no invented "500+ happy customers", no stock-photo staff.

Checks before you finish:
- Phone number is correct and works with `tel:`.
- Address, hours and map match each other.
- Title tag has the trade and the town: "Mike's Barbershop, Fresno CA".
- Add LocalBusiness JSON-LD with name, address, phone and hours.
- Test at 375px wide and check text contrast.
- Page loads fast: compress photos, keep it under about 1 MB.

Also load ui-design and no-ai-slop before finishing.
