document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".cinema-scroll");
  if (!section) return;

  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const isFinePointer = matchMedia("(pointer: fine)");
  const docEl = document.documentElement;
  const sightsControls = document.querySelector(".sights-controls");
  const originalCards = Array.from(document.querySelectorAll(".sight-card"));
  const track = document.querySelector(".sights-track");

  let targetMouseX = 0, targetMouseY = 0;
  let mouseX = 0, mouseY = 0;
  let targetScroll = 0, smoothScroll = 0;
  let initialized = false, rafPending = false;
  let sightCards = [];
  let originalSightCount = originalCards.length;
  let activeSight = originalSightCount;

  const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v));
  const smoothstep = (e0, e1, v) => {
    const x = clamp((v - e0) / (e1 - e0));
    return x * x * (3 - 2 * x);
  };
  const lerp = (a, b, t) => a + (b - a) * t;

  const segmentInOut = (s, a, b, c, d) => {
    const enter = smoothstep(a, b, s), exit = smoothstep(c, d, s);
    return { enter, exit, active: enter * (1 - exit) };
  };

  const getScrollDistance = () => {
    if (!section) return 0;
    return clamp(-section.getBoundingClientRect().top, 0, section.offsetHeight - window.innerHeight);
  };

  const setupSightSlider = () => {
    if (!track || originalCards.length === 0) return;
    track.replaceChildren();
    for (let setIndex = 0; setIndex < 3; setIndex++) {
      originalCards.forEach((card, cardIndex) => {
        const clone = card.cloneNode(true);
        clone.dataset.sightIndex = setIndex * originalSightCount + cardIndex;
        clone.setAttribute("tabindex", "0");
        clone.setAttribute("role", "button");
        clone.addEventListener("click", () => selectSightCard(clone));
        clone.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            selectSightCard(clone);
          }
        });
        track.appendChild(clone);
      });
    }
    sightCards = Array.from(track.querySelectorAll(".sight-card"));
    activeSight = originalSightCount;
    track.addEventListener("transitionend", normalizeSightSlider);
    updateSightSlider();
  };

  const updateSightSlider = () => {
    if (!sightCards.length) return;
    const cardWidth = sightCards[0].offsetWidth;
    const gap = parseFloat(getComputedStyle(track).columnGap || "0");
    docEl.style.setProperty("--sights-shift", `${-(cardWidth + gap) * activeSight}px`);
    sightCards.forEach((card, idx) => {
      card.classList.toggle("is-active", idx === activeSight);
    });
  };

  const moveSightSlider = (dir) => {
    activeSight += dir;
    updateSightSlider();
  };

  const selectSightCard = (card) => {
    const idx = Number(card.dataset.sightIndex);
    if (Number.isFinite(idx)) {
      activeSight = idx;
      updateSightSlider();
    }
  };

  const jumpSightSlider = (i) => {
    track.classList.add("is-jumping");
    activeSight = i;
    updateSightSlider();
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        track.classList.remove("is-jumping");
      });
    });
  };

  const normalizeSightSlider = () => {
    if (activeSight >= originalSightCount * 2) {
      jumpSightSlider(activeSight - originalSightCount);
    } else if (activeSight < originalSightCount) {
      jumpSightSlider(activeSight + originalSightCount);
    }
  };

  let cachedProps = {};
  const setProp = (prop, val) => {
    if (cachedProps[prop] === val) return;
    cachedProps[prop] = val;
    docEl.style.setProperty(prop, val);
  };

  const update = () => {
    rafPending = false;
    targetScroll = getScrollDistance();

    if (!initialized || reduceMotion.matches) {
      smoothScroll = targetScroll;
      initialized = true;
    } else {
      smoothScroll = lerp(smoothScroll, targetScroll, 0.2);
    }
    if (Math.abs(smoothScroll - targetScroll) < 0.08) smoothScroll = targetScroll;

    if (isFinePointer.matches) {
      mouseX = lerp(mouseX, targetMouseX, 0.12);
      mouseY = lerp(mouseY, targetMouseY, 0.12);
    }

    const frame2 = segmentInOut(smoothScroll, 560, 900, 1300, 1620);
    const frame3 = segmentInOut(smoothScroll, 1760, 2140, 2540, 2700);
    const progress = clamp(smoothScroll / 2700);
    const introExit = smoothstep(90, 650, smoothScroll);
    const sightsEnterRaw = smoothstep(2760, 3560, smoothScroll);
    const sightsEnter = Math.pow(sightsEnterRaw, 1.55);
    const sightsControlsEnter = smoothstep(3360, 3660, smoothScroll);
    const blurActive = clamp(frame2.active + frame3.active);
    const frame2Opacity = frame2.active * (1 - frame3.enter);
    const splitDrift = Math.pow(frame2.enter, 1.5);
    const panel2Opacity = frame2.active * (1 - frame2.exit);
    const panel3Opacity = frame3.active * (1 - frame3.exit);
    const backScale = 0.76 + progress * 0.2 + frame2.enter * 0.18 + frame3.enter * 0.16;
    const sharedHeroY = progress * -74;
    const sharedHeroScale = progress * 0.23;
    const sightsScreenTop = Math.min(220, Math.max(112, window.innerHeight * 0.19)) - 50;
    const sightsParentTop = window.innerHeight - (window.innerHeight - sightsScreenTop) / backScale;

    setProp("--mx", reduceMotion.matches ? "0" : mouseX.toFixed(4));
    setProp("--my", reduceMotion.matches ? "0" : mouseY.toFixed(4));
    setProp("--back-opacity", (1 - frame2.active * 0.06).toFixed(4));
    setProp("--back-x", `${(mouseX * -12).toFixed(2)}px`);
    setProp("--back-y", `${(mouseY * -4).toFixed(2)}px`);
    setProp("--back-scale", backScale.toFixed(4));
    setProp("--four-y", `${(10 + progress * 10).toFixed(2)}vh`);
    setProp("--four-scale", (0.78 + progress * 0.16).toFixed(4));
    setProp("--bazaar-y", `${(20 - progress * 8).toFixed(2)}vh`);
    setProp("--blur-px", `${(blurActive * 14).toFixed(2)}px`);
    setProp("--back-brightness", (1 - blurActive * 0.255).toFixed(4));
    setProp("--bazaar-blur-px", `${(frame2.active * 14).toFixed(2)}px`);
    setProp("--bazaar-brightness", (1 - frame2.active * 0.255 - frame3.active * 0.06).toFixed(4));
    setProp("--bazaar-saturation", (1 + frame3.active * 0.18).toFixed(4));
    setProp("--shade-opacity", "1");
    setProp("--shade-z", frame2.active > 0.02 ? "2" : "0");
    setProp("--shade-top-alpha", (blurActive * 0.465).toFixed(4));
    setProp("--shade-mid-alpha", (blurActive * 0.42).toFixed(4));
    setProp("--shade-bottom-alpha", (blurActive * 0.51).toFixed(4));

    setProp("--title-y", `${(introExit * -210).toFixed(2)}px`);
    setProp("--title-scale", (1 - introExit * 0.08).toFixed(4));
    setProp("--title-opacity", (1 - introExit).toFixed(4));

    setProp("--bridge-x", `calc(-50% + ${(mouseX * 18).toFixed(2)}px)`);
    setProp("--bridge-y", `${(mouseY * 8 + sharedHeroY - frame2.exit * 760).toFixed(2)}px`);
    setProp("--bridge-bottom", `${(5 - frame2.enter * 13).toFixed(2)}vh`);
    setProp("--bridge-width", `${(67.2 + frame2.enter * 37.8).toFixed(2)}vw`);
    setProp("--bridge-scale", (1.02 + sharedHeroScale + frame2.exit * 0.46).toFixed(4));

    setProp("--split-left-x", `calc(-50% + ${(-splitDrift * 46).toFixed(2)}vw + ${(mouseX * 22).toFixed(2)}px)`);
    setProp("--split-left-y", `${(mouseY * 10 + sharedHeroY - splitDrift * 180).toFixed(2)}px`);
    setProp("--split-left-scale", (1 + sharedHeroScale + frame2.enter * 0.74).toFixed(4));
    setProp("--split-right-x", `calc(-50% + ${(splitDrift * 46).toFixed(2)}vw + ${(mouseX * 22).toFixed(2)}px)`);
    setProp("--split-right-y", `${(mouseY * 10 + sharedHeroY - splitDrift * 180).toFixed(2)}px`);
    setProp("--split-right-scale", (1 + sharedHeroScale + frame2.enter * 0.74).toFixed(4));

    setProp("--frame2-opacity", frame2Opacity.toFixed(4));
    setProp("--frame2-x", `calc(-50% + ${(mouseX * 10).toFixed(2)}px)`);
    setProp("--frame2-y", `calc(-50% + ${(mouseY * 8 - frame2.exit * 150).toFixed(2)}px)`);
    setProp("--frame2-scale", (1.06 + frame2.enter * 0.08 + frame2.exit * 0.08).toFixed(4));

    setProp("--intro-copy-y", `${(introExit * 90).toFixed(2)}px`);
    setProp("--intro-copy-opacity", (1 - introExit).toFixed(4));
    setProp("--panel2-opacity", panel2Opacity.toFixed(4));
    setProp("--panel2-y", `calc(-50% + ${(-frame2.exit * 86 + (1 - frame2.enter) * 58).toFixed(2)}px)`);
    setProp("--panel3-opacity", panel3Opacity.toFixed(4));
    setProp("--panel3-y", `calc(-50% + ${(-frame3.exit * 86 + (1 - frame3.enter) * 58).toFixed(2)}px)`);

    setProp("--sights-opacity", sightsEnter.toFixed(4));
    setProp("--sights-controls-opacity", sightsControlsEnter.toFixed(4));
    if (sightsControls) {
      sightsControls.classList.toggle("is-ready", sightsControlsEnter > 0.98);
    }
    setProp("--sights-visibility", sightsEnter > 0.01 ? "visible" : "hidden");
    setProp("--sights-y", "0px");
    setProp("--sights-enter-x", `${((1 - sightsEnter) * 420).toFixed(2)}vw`);
    setProp("--sights-scale", (1 / backScale).toFixed(4));
    setProp("--sights-top", `${sightsParentTop.toFixed(2)}px`);
    setProp("--sights-screen-top", `${sightsScreenTop.toFixed(2)}px`);

    if (
      Math.abs(smoothScroll - targetScroll) > 0.08 ||
      Math.abs(mouseX - targetMouseX) > 0.001 ||
      Math.abs(mouseY - targetMouseY) > 0.001
    ) {
      requestTick();
    }
  };

  const requestTick = () => {
    if (!rafPending) {
      rafPending = true;
      requestAnimationFrame(update);
    }
  };

  window.addEventListener("scroll", requestTick, { passive: true });
  window.addEventListener("resize", () => {
    updateSightSlider();
    requestTick();
  });

  if (isFinePointer.matches) {
    window.addEventListener("pointermove", (e) => {
      targetMouseX = e.clientX / window.innerWidth - 0.5;
      targetMouseY = e.clientY / window.innerHeight - 0.5;
      requestTick();
    }, { passive: true });
  }

  const btnPrev = document.querySelector(".sight-prev");
  const btnNext = document.querySelector(".sight-next");
  if (btnPrev) btnPrev.addEventListener("click", () => moveSightSlider(-1));
  if (btnNext) btnNext.addEventListener("click", () => moveSightSlider(1));

  setupSightSlider();
  requestTick();
});
