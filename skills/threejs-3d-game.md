---
name: threejs-3d-game
description: Building 3D browser games with three.js or React Three Fiber: setup, lighting, models, physics, endless runners and phone performance.
---
# 3D browser games with three.js

Use plain three.js for a game with its own loop. Use React Three Fiber (`@react-three/fiber`) with `@react-three/drei` when the app is already React. Check current APIs and versions with `web_search` or `fetch_page` on threejs.org/docs before relying on memory; imports and addon paths change.

**Setup:** `npm create vite@latest game -- --template vanilla`, `npm i three`. Import addons from `three/addons/...`.

**Scene, camera, renderer**
```js
import * as THREE from 'three';
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200);
const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  const dt = Math.min(clock.getDelta(), 0.05);
  update(dt);
  renderer.render(scene, camera);
});
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
```
Everything moves by `speed * dt`, never per frame. Cap `dt`.

**Lighting that looks good cheaply:** one `HemisphereLight` (sky and ground color) plus one `DirectionalLight` with a shadow map of 1024 and a tight shadow camera around the play area. Set `renderer.outputColorSpace` default (sRGB) and add fog (`scene.fog`) matching the background to hide the far edge. Prefer `MeshStandardMaterial` or unlit `MeshBasicMaterial` for stylized looks. Avoid many dynamic lights.

**Models:** use GLB. Compress with `gltf-transform` (`npx @gltf-transform/cli optimize in.glb out.glb`), load with `GLTFLoader` plus `DRACOLoader` (set the decoder path) or `MeshoptDecoder`. Reuse loaded models with `clone()`; animate with `AnimationMixer.update(dt)`.

**Instancing.** For many copies of the same mesh (trees, coins, rocks) use `InstancedMesh`; set each matrix with `setMatrixAt`, then `instanceMatrix.needsUpdate = true`. One draw call instead of hundreds.

**Physics.** Only add it if the game needs it. Rapier: `@dimforge/rapier3d-compat` (await `RAPIER.init()`, step the world with a fixed dt, copy body positions to meshes). cannon-es is simpler for small scenes. For runners and arcade games, hand-written lane and box checks are lighter and more predictable.

**Character and camera follow.** Move a parent group, not the camera directly. Smooth the camera: `camera.position.lerp(target, 1 - Math.exp(-dt * 6))`, then `camera.lookAt(player.position)`. Frame-rate independent smoothing like this avoids jitter.

**Endless runner pattern**
1. Build 3 to 5 track chunks and keep them in a pool.
2. Move chunks toward the player (or the player forward); when a chunk is behind the camera, move it to the front and re-roll its obstacles.
3. Spawn with a seeded random so layouts are fair, ramp speed slowly.
4. Collisions with simple boxes per lane; lanes switch with swipe left/right, jump on swipe up.

**Touch controls:** listen to `pointerdown` and `pointerup`, compare the delta; a swipe is over about 30 px. Add `touch-action: none`. Provide buttons as a fallback.

**Postprocessing:** sparingly. One bloom or vignette at most on desktop; skip on phones. Each pass renders the full screen again.

**Disposing.** When a level ends or objects are removed: `geometry.dispose()`, `material.dispose()`, `texture.dispose()`, and `scene.remove(obj)`. Leaks cause crashes on phones.

**60 fps on phones checklist**
- Pixel ratio capped at 2 (1.5 on weak devices); lower it automatically if frame time rises.
- Draw calls under about 100: merge geometry, instance, share materials.
- Triangles under about 100k visible.
- One shadow-casting light, 1024 map, or fake blob shadows.
- Textures 1024 or smaller, KTX2 compressed where possible (`KTX2Loader`).
- No allocations in the loop: reuse `Vector3`, no `new` per frame.
- Test after a few minutes; phones throttle when hot, so performance drops later.
- Fog and a short far plane to cull distant objects.

**Verify with test_page.** Open as iPhone and Android in portrait and phone-landscape, iPad, and desktop. Check that the canvas actually renders (not black), there are no console errors (WebGL, shader, 404 for models), nothing scrolls sideways, and the screenshots look right. Use `steps` like "click Play", "press Space", "wait 3000" to get into the game and screenshot it in motion.
