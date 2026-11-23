document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const tallVideo = document.querySelector(".photo-img--tall");
  const wideVideo = document.querySelector(".photo-img--wide");

  const playVideo = (v) => {
    if (!v || reduceMotion.matches) return;
    v.play().catch(() => {
      // Autoplay blocked by browser policy; kickstart on first user interaction
      const kickstart = () => {
        v.play().catch(() => {});
        window.removeEventListener("pointerdown", kickstart);
        window.removeEventListener("keydown", kickstart);
        window.removeEventListener("touchstart", kickstart);
      };
      window.addEventListener("pointerdown", kickstart, { once: true });
      window.addEventListener("keydown", kickstart, { once: true });
      window.addEventListener("touchstart", kickstart, { once: true });
    });
  };

  const updateVideos = () => {
    const isPortrait = window.matchMedia("(max-aspect-ratio:51/50)").matches || window.innerWidth < 700;
    if (tallVideo && wideVideo) {
      if (isPortrait) {
        tallVideo.style.display = "none";
        wideVideo.style.display = "block";
        wideVideo.preload = "auto";
        tallVideo.preload = "none";
        tallVideo.pause();
        playVideo(wideVideo);
      } else {
        tallVideo.style.display = "block";
        wideVideo.style.display = "none";
        tallVideo.preload = "auto";
        wideVideo.preload = "none";
        wideVideo.pause();
        playVideo(tallVideo);
      }
    }
  };

  if (reduceMotion.matches) {
    if (tallVideo) tallVideo.pause();
    if (wideVideo) wideVideo.pause();
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      if (tallVideo) tallVideo.pause();
      if (wideVideo) wideVideo.pause();
    } else {
      updateVideos();
    }
  });

  window.addEventListener("resize", updateVideos, { passive: true });
  updateVideos();
});
