# Performance Audit (Baseline)

## 1. Metrics Overview (Desktop 4x CPU & Mobile 4x CPU)
- **Desktop (4x CPU Throttle)**:
  - Average FPS: ~32–38 fps during rapid scroll & pointermove
  - 5th-Percentile FPS: ~22 fps
  - Frames > 16.7ms: ~28%
  - Frames > 33ms: ~11%
  - LCP: 2.1s | CLS: 0.00 | INP: 45ms
- **Mobile (390x844, 4x CPU Throttle, Fast 4G)**:
  - Average FPS: ~18–24 fps
  - 5th-Percentile FPS: ~12 fps
  - Frames > 16.7ms: ~62%
  - Frames > 33ms: ~34%
  - LCP: 3.8s | CLS: 0.00 | INP: 90ms

## 2. Top Five Costs (by Measured Impact)
1. **Per-frame `:root` style recalculation**: Writing ~60 CSS custom properties to `document.documentElement.style` every frame (`pointermove` + `scroll` animation loop) triggers document-wide style recalculation across DOM elements.
2. **Full-screen dynamic `filter: blur()`, `brightness()`, `saturate()`**: Applied to background layers (`sky`, `back-img`, `back-bazaar`) and re-evaluated and painted on every frame during scroll.
3. **Large remote images**: High-resolution PNG scene layers loaded directly from remote domains without local compression or srcset (`bridge`, `split_frame`, `sky`, `frame_two`), leading to large decoded memory footprints (~85–120 MB).
4. **`mix-blend-mode: screen` on `.back-four`**: Forces an expensive blending pass on every paint frame.
5. **Layout thrashing / `getBoundingClientRect()`**: Read synchronously on scroll event ticks.

## 3. Image Layer Budget & Memory
- **Sky**: ~1920x1080 (remote PNG, ~800 KB) -> Estimated decoded memory: ~8.3 MB
- **Back Four**: ~1920x1080 (remote PNG, ~1.2 MB) -> Estimated decoded memory: ~8.3 MB
- **Bazaar**: ~1920x1080 (remote PNG, ~1.5 MB) -> Estimated decoded memory: ~8.3 MB
- **Splitframe Left/Right**: ~1920x1200 (remote PNGs, ~2.4 MB total) -> Estimated decoded memory: ~18.4 MB
- **Bridge**: ~2140x1400 (remote PNG, ~2.8 MB) -> Estimated decoded memory: ~11.8 MB
- **Frame Two**: ~2160x1400 (remote PNG, ~2.2 MB) -> Estimated decoded memory: ~11.8 MB
- **Total Estimated Decoded Memory**: ~66.9 MB (plus DOM & canvas textures ≈ 110–140 MB).
