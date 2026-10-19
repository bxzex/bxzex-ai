---
name: file-storage
description: Storing user uploads in object storage with signed URLs and size and type checks, not in the repo.
---
# File Storage for Uploads

Do not keep uploads in the git repo or on a serverless disk. Use object storage: an S3-compatible bucket (S3, R2, Backblaze, MinIO) or your platform's blob store.

1. **Create a bucket.** Keep it private by default. Save the endpoint, bucket name and keys in env vars, server side only.
2. **Upload path A: direct to storage with a signed URL (best for big files).**
   - Client asks your API: `POST /api/upload-url` with file name, type and size.
   - Server checks the user is logged in, checks the limits, builds an object key like `uploads/<userId>/<uuid>.<ext>` and returns a presigned PUT URL that expires in 5 minutes.
   - Client does `fetch(url, {method:'PUT', body:file, headers:{'content-type': type}})`.
   - Save the key (not the full URL) in your database.
3. **Upload path B: through your server (small files only).** Accept multipart, stream to storage. Serverless request bodies are often capped near 4.5 MB.
4. **Checks before accepting.**
   - Size limit (for example 10 MB) and a file count limit.
   - Allowlist of types: `image/png`, `image/jpeg`, `image/webp`, `application/pdf`. Check the extension and sniff the first bytes, because the content-type header can lie.
   - Generate your own file names. Never use the user's name in the path.
   - Never allow `.html`, `.svg` or scripts to be served from your own domain.
5. **Reading files.** For private files, return a presigned GET URL with a short expiry. For public images, use a public bucket path or CDN in front.
6. **Browser uploads need CORS** on the bucket: allow your site origin and the `PUT` method.
7. **Cleanup.** Add a lifecycle rule to delete temp uploads, and delete the object when its database row is deleted.

**Check:** upload a test file with `curl -X PUT -T test.png "<signed-url>"`, then fetch it with a signed GET. An unsigned GET on a private bucket should return 403.

**Pitfalls:** public buckets by accident; no size limit; expired signed URLs cached by the page; storing the full signed URL instead of the key.
