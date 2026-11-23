document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const docEl = document.documentElement;

  if (urlParams.get("lite") === "1") {
    docEl.setAttribute("data-perf", "lite");
    return;
  }

  let frameCount = 0;
  let lastTime = performance.now();
  let lowFpsSeconds = 0;
  const fpsCounter = urlParams.get("fps") === "1" ? document.createElement("div") : null;

  if (fpsCounter) {
    fpsCounter.style.cssText = "position:fixed; bottom:10px; right:10px; background:rgba(0,0,0,0.8); color:#0f0; padding:4px 8px; font-family:monospace; z-index:99999; font-size:12px;";
    document.body.appendChild(fpsCounter);
  }

  const checkFps = (now) => {
    frameCount++;
    const delta = now - lastTime;
    if (delta >= 1000) {
      const fps = Math.round((frameCount * 1000) / delta);
      if (fpsCounter) fpsCounter.textContent = `FPS: ${fps}`;

      if (fps < 40) {
        lowFpsSeconds++;
        if (lowFpsSeconds >= 2) {
          docEl.setAttribute("data-perf", "lite");
        }
      } else {
        lowFpsSeconds = Math.max(0, lowFpsSeconds - 1);
      }

      frameCount = 0;
      lastTime = now;
    }
    requestAnimationFrame(checkFps);
  };

  requestAnimationFrame(checkFps);
});
