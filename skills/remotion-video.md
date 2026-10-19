---
name: remotion-video
description: Making designed, animated videos in code with Remotion (React): ads, promos, explainers, captions and data-driven clips.
---
# Videos in code with Remotion

**Remotion or ffmpeg?** Use Remotion when the video is designed: ads, promos, explainers, animated titles, captions, charts, or one template rendered with different data. Use ffmpeg (see media-ffmpeg) for cutting, converting, compressing or joining footage that already exists. Often both: build the scene in Remotion, then post-process with ffmpeg.

**Licensing:** Remotion is free for individuals and companies of up to 3 people. Larger companies need a paid company license. Mention this if the user works for a bigger company.

**New project**
1. `npx create-video@latest` asks questions, and commands here can't answer them, so set the project up by hand (step 2). If the user runs it themselves, they pick the blank template.
2. Hand setup: `npm init -y`, then `npm i remotion @remotion/cli react react-dom typescript @types/react`. Keep every `remotion` and `@remotion/*` package on the exact same version (no `^`). Mismatches cause confusing errors.
3. `src/index.ts`: `import {registerRoot} from 'remotion'; import {Root} from './Root'; registerRoot(Root);`
4. `src/Root.tsx`: return `<Composition id="Promo" component={Promo} durationInFrames={300} fps={30} width={1920} height={1080} />`.
5. Commands change between versions. If unsure, `web_search` or `fetch_page` on remotion.dev/docs before guessing.

**Sizes:** 1920x1080 landscape, 1080x1920 vertical (Reels, TikTok, Shorts), 1080x1080 square. 30 fps is typical. Duration in frames = seconds x fps.

**Core API**
- `useCurrentFrame()` and `useVideoConfig()` give the frame and `{fps, width, height, durationInFrames}`.
- `interpolate(frame, [0, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})` maps frames to values. Always clamp.
- `spring({frame, fps, config: {damping: 200}})` gives a natural 0 to 1 move. Low damping bounces; 200 is smooth.
- `Easing` (for example `Easing.out(Easing.cubic)`) goes in interpolate's `easing` option.
- `<AbsoluteFill>` is a full-frame layer. `<Sequence from={30} durationInFrames={60}>` shows children in a window and resets their frame to 0. `<Series>` plays `<Series.Sequence durationInFrames>` items back to back.
- `@remotion/transitions`: `<TransitionSeries>` with `<TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: 15})} />`; also `slide()`.
- Media: put files in `public/` and load with `staticFile('clip.mp4')`. Use `<Img>`, `<Audio>`, and `<OffthreadVideo>` (preferred over `<Video>` for rendering).
- Fonts: `import {loadFont} from '@remotion/google-fonts/Inter'; const {fontFamily} = loadFont();`

**Example scene**
```tsx
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const Title: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 200}});
  const fadeOut = interpolate(frame, [75, 90], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#0b1220', justifyContent: 'center', alignItems: 'center', opacity: fadeOut}}>
      <h1 style={{color: 'white', fontSize: 120, transform: `translateY(${(1 - pop) * 60}px)`, opacity: pop}}>{text}</h1>
    </AbsoluteFill>
  );
};
```

**Hard rule: everything is driven by the frame.** CSS transitions, CSS animations, `setTimeout` and `requestAnimationFrame` do not render correctly, because each frame is captured separately. Compute every animated value from `useCurrentFrame()`. For async work (fetching data, loading a font) use `delayRender()` then `continueRender(handle)`. For duration that depends on data or a media file, use `calculateMetadata` on the Composition. Pass inputs through `defaultProps`.

**Preview and verify**
1. `npx remotion studio` opens a live preview for the user.
2. Without the studio, check key frames: `npx remotion still Promo out/f0.png --frame=0`, then a middle frame and the last frame. Open each png and look: text cut off, overlaps, wrong colors, empty frames.
3. Fix what you see, then render fully.

**Render**
- `npx remotion render Promo out/video.mp4`
- Options: `--codec=h264` (default), `--crf=18` (lower is better quality), `--concurrency=4`, `--scale=0.5` for a quick draft, `--frames=0-90` for a range, `--props='{"text":"Hello"}'` or a path to a JSON file.
- Music: `<Audio src={staticFile('music.mp3')} volume={(f) => interpolate(f, [0, 30, durationInFrames - 45, durationInFrames], [0, 0.8, 0.8, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />`. The volume callback gets the frame inside the audio's own sequence.

**Troubleshooting**
- Cannot download or launch the headless browser: use an existing one. Find it with `find ~/Library/Caches/ms-playwright ~/.cache/ms-playwright -name chrome-headless-shell -type f 2>/dev/null` (macOS, then Linux), and pass `--browser-executable=/that/path` to `still`, `render` and `studio`.
- Errors about versions or missing modules: align all remotion packages to one version, delete `node_modules` and reinstall.
- Wrong font in the output: load it explicitly with `loadFont` or `@font-face` and wait for it; system fonts differ between machines.
- Render is slow or may hang: render `--frames=0-60` first, lower `--scale`, and avoid huge images or many layered blurs and shadows.
- Video file stutters or is blank: use `<OffthreadVideo>`, and keep source clips in `public/`.

**Finish:** report the absolute path of the mp4 and its length (`ffprobe` gives duration and size). Then offer a vertical 1080x1920 cut: add a second Composition with the same component and new dimensions, and make the layout read width and height from `useVideoConfig()`.
