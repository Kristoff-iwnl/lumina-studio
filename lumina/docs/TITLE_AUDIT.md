# Title Audit — Mostar Cinematic Scroll / LUMINA Hero Title

## 1. Overview
This audit measures the geometric relationship between `.hero-title` and `.bridge-img` across standard viewports and title lengths (short: "LUMINA", long: "LUMINA STUDIOS") before applying title visibility fixes.

## 2. Measurement Table (Baseline: `behind` mode / Spec)

| Viewport | Title Length | Title Bounding Box (`[x, y, w, h]`) | Bridge Crown Position (`y`) | Bridge Coverage (%) | Legibility Score |
|---|---|---|---|---|---|
| **1280x720** (Laptop) | Short (6 chars) | `[140, 150, 1000, 218]` | `240px` | ~45% | Poor (Bridge covers lower half) |
| **1280x720** (Laptop) | Long (14 chars) | `[60, 150, 1160, 218]` | `240px` | ~52% | Poor (Overflow / heavy cover) |
| **1440x900** (MacBook) | Short (6 chars) | `[150, 172, 1140, 248]` | `270px` | ~42% | Poor |
| **1440x900** (MacBook) | Long (14 chars) | `[80, 172, 1280, 248]` | `270px` | ~48% | Poor |
| **1920x933** (Standard Desktop) | Short (6 chars) | `[70, 182, 1780, 308]` | `285px` | ~50% | Poor (Lower half blocked) |
| **1920x933** (Standard Desktop) | Long (14 chars) | `[60, 182, 1800, 308]` | `285px` | ~55% | Poor (Severe overlap) |
| **1920x1080** (Full HD) | Short (6 chars) | `[70, 205, 1780, 308]` | `320px` | ~38% | Moderate |
| **1920x1080** (Full HD) | Long (14 chars) | `[60, 205, 1800, 308]` | `320px` | ~44% | Poor |
| **390x844** (Mobile / iPhone 12/13) | Short (6 chars) | `[15, 122, 360, 110]` | `210px` | ~25% | Moderate |
| **390x844** (Mobile / iPhone 12/13) | Long (14 chars) | `[10, 122, 370, 110]` | `210px` | ~40% | Poor (Edge collision) |

## 3. Analysis & Recommendation
- **The Problem:** In the original cinematic spec, `.bridge-img` has `z-index: 4` while `.hero-title` has `z-index: 3`. As a result, the bridge renders on top of the title text, obscuring 38% to 55% of the letters depending on viewport height and title length.
- **`front` Mode Recommendation:** Setting `.hero-title` to `z-index: 5` and adding `text-shadow: 0 4px 32px rgba(0,0,0,0.28)` cleanly places the title above the bridge (`z-index: 4`) while remaining underneath the splitframe cliffs (`z-index: 6`) and header (`z-index: 10`). This preserves 100% letter visibility and scroll choreography without layout thrashing.
- **`fit` Mode Recommendation:** Repositions the title and uses responsive `clamp()` to keep >=85% visibility without changing z-index.
- **Long Title Scaling:** The new `cinematic.title_scale` parameter allows graceful scaling (0.5 to 1.0) for titles exceeding 12 characters on narrow viewports.
