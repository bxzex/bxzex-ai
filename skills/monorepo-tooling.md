---
name: monorepo-tooling
description: Setting up a monorepo with workspaces, shared packages and cached builds using turborepo.
---
# Monorepos and Build Speed

Use a monorepo when several apps share code. For one app, skip it.

1. **Layout.**
   ```
   apps/web      apps/api
   packages/ui   packages/config   packages/utils
   package.json  pnpm-workspace.yaml (or "workspaces" in package.json)
   ```
2. **Workspaces.** pnpm: create `pnpm-workspace.yaml` with `packages: ['apps/*', 'packages/*']`. npm: add `"workspaces": ["apps/*", "packages/*"]` to the root `package.json`. Install once at the root: `pnpm install`.
3. **Shared package.** In `packages/utils/package.json` set `"name": "@acme/utils"`, `"version": "0.0.0"`, `"main"` and `"types"`. In the app depend on it with `"@acme/utils": "workspace:*"` (pnpm) or `"*"` (npm). Either build the package to `dist`, or let the app's bundler compile the source (in Next.js add the package to `transpilePackages`).
4. **Turborepo.** `pnpm add -D turbo -w`, then `turbo.json`:
   ```
   { "tasks": {
       "build": { "dependsOn": ["^build"], "outputs": ["dist/**", ".next/**", "!.next/cache/**"] },
       "lint": {}, "test": {},
       "dev": { "cache": false, "persistent": true } } }
   ```
   `^build` means build dependencies first.
5. **Run.** `npx turbo build`, `npx turbo build --filter=web` (one app and what it needs), `npx turbo dev`. Run it twice: the second run should print `FULL TURBO` and replay from cache.
6. **Remote cache.** `npx turbo login` and `npx turbo link` share the cache between your machine and CI. Cache keys include the env vars you list under `env` or `globalEnv`, so declare the ones that change output.
7. **Shared configs.** Put the tsconfig and eslint base config in `packages/config` and extend it from each app.
8. **Deploying.** On hosts, set the project root directory to `apps/web` and keep "include files outside root" on so shared packages are visible.

**Pitfalls:** a package that is not listed in dependencies "works" locally through hoisting and fails in CI; missing `outputs` means nothing gets cached; two versions of React in the tree cause hook errors, so pin one version at the root.
