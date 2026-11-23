(function() {
  var REF_W=1464, REF_H=949, PHOTO_W=836, PANE_W=628, CARD_W=613, CARD_H=922;
  var CONTENT_H=697;
  var IMG_W=1177, IMG_H=1336, IMG_REF_SCALE=836/1177;
  var PANE_RATIO=PANE_W/REF_W;
  var HERO_W=681, HERO_H=219;
  var REF_CARD_ASPECT=692/855;
  var RAMP_HI=1280, RAMP_LO=1000, PHOTO_MIN=0.42;
  var RAMP_LO2=820, PHOTO_MIN2=0.36;
  var TP={"pad":0.1076,"h1Top":0.08656,"h1Fs":0.06839,"subTop":0.17368,"subFs":0.0309,"emTop":0.25435,"emH":0.10257,"emR":0.0202,"ephFs":0.02702,"ephPad":0.0332,"pwTop":0.36851,"pwH":0.10839,"btnTop":0.50435,"btnH":0.10981,"btnFs":0.0275,"arrow":0.026,"btnGap":0.02,"divTop":0.68222,"orFs":0.02245,"orPad":0.051,"divH":0.0026,"gTop":0.76445,"gH":0.09966,"gIcon":0.032,"gtFs":0.03205,"gGap":0.026,"btTop":0.89668,"btFs":0.1058,"badgeH":0.0742,"heroLh":1.1246,"heroBot":0.06493,"heroGap":-0.30423,"heroSide":0.0525};

  var mqLandscape = window.matchMedia('(min-width:700px) and (min-aspect-ratio:51/50)');
  var mqPortrait  = window.matchMedia('(min-width:700px) and (max-aspect-ratio:51/50)');

  var photo = document.querySelector('.photo');
  var pane = document.querySelector('.pane');
  var card = document.querySelector('.card');
  var cardIn = document.querySelector('.card-in');
  var hero = document.getElementById('hero');
  var tallVideo = document.querySelector('.photo-img--tall');
  var wideVideo = document.querySelector('.photo-img--wide');

  function clearInline() {
    if (photo) photo.style.cssText = '';
    if (pane) pane.style.cssText = '';
    if (card) card.style.cssText = '';
    if (cardIn) cardIn.style.cssText = '';
    if (hero) hero.style.cssText = '';
  }

  function photoRatio(vw) {
    if (vw >= RAMP_HI) return 1 - PANE_RATIO;
    if (vw >= RAMP_LO) {
      var t = (vw - RAMP_LO) / (RAMP_HI - RAMP_LO);
      return PHOTO_MIN + t * ((1 - PANE_RATIO) - PHOTO_MIN);
    }
    if (vw >= RAMP_LO2) {
      var t = (vw - RAMP_LO2) / (RAMP_LO - RAMP_LO2);
      return PHOTO_MIN2 + t * (PHOTO_MIN - PHOTO_MIN2);
    }
    return PHOTO_MIN2;
  }

  function headlineMeasure() {
    var dummy = document.createElement('span');
    dummy.style.visibility = 'hidden';
    dummy.style.position = 'absolute';
    dummy.style.fontFamily = 'Eloquia, sans-serif';
    dummy.style.fontSize = '69.14px';
    dummy.style.fontWeight = '578';
    dummy.style.whiteSpace = 'nowrap';
    dummy.innerText = 'Find Signal to Action Instantly';
    document.body.appendChild(dummy);
    var w = dummy.getBoundingClientRect().width;
    document.body.removeChild(dummy);
    return w;
  }

  function playActiveVideo() {
    var isPortrait = window.matchMedia('(max-aspect-ratio:51/50)').matches || window.innerWidth < 700 || mqPortrait.matches;
    var activeV = isPortrait ? wideVideo : tallVideo;
    var inactiveV = isPortrait ? tallVideo : wideVideo;

    if (inactiveV) {
      inactiveV.pause();
    }
    if (activeV) {
      activeV.play().catch(function() {
        var kickstart = function() {
          activeV.play().catch(function(){});
          window.removeEventListener('pointerdown', kickstart);
          window.removeEventListener('touchstart', kickstart);
          window.removeEventListener('keydown', kickstart);
        };
        window.addEventListener('pointerdown', kickstart, { once: true });
        window.addEventListener('touchstart', kickstart, { once: true });
        window.addEventListener('keydown', kickstart, { once: true });
      });
    }
  }

  function layout() {
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    clearInline();

    if (vw < 700) {
      document.body.classList.remove('tabport');
      document.body.classList.add('stacked');
      if (tallVideo) tallVideo.style.display = 'none';
      if (wideVideo) wideVideo.style.display = 'block';
      playActiveVideo();
      return;
    }

    document.body.classList.remove('stacked');

    if (mqPortrait.matches) {
      document.body.classList.add('tabport');
      if (tallVideo) tallVideo.style.display = 'none';
      if (wideVideo) wideVideo.style.display = 'block';

      var bandH = Math.round(vh * 0.425);
      var sideMargin = Math.round(vw * 0.0525);
      if (photo) photo.style.height = bandH + 'px';
      if (hero) {
        hero.style.bottom = Math.round(vh * 0.0297) + 'px';
        hero.style.left = sideMargin + 'px';
        hero.style.right = sideMargin + 'px';
        hero.style.width = 'auto';
        hero.style.height = 'auto';
      }
      var measuredW = headlineMeasure();
      var wrap = document.querySelector('.hl-wrap');
      if (wrap) wrap.style.maxWidth = Math.round(measuredW * 0.61) + 'px';

      var cardHVal = vh - bandH;
      if (card) card.style.height = cardHVal + 'px';
      if (pane) pane.style.top = bandH + 'px';
      if (cardIn) cardIn.style.inset = '0';
      playActiveVideo();
      return;
    }

    // Mode A: Land
    document.body.classList.remove('tabport');
    if (tallVideo) tallVideo.style.display = 'block';
    if (wideVideo) wideVideo.style.display = 'none';

    var r = photoRatio(vw);
    var photoW = vw * r;
    var paneW = vw - photoW;

    if (photo) photo.style.width = (r * 100) + '%';
    if (pane) pane.style.left = (r * 100) + '%';

    var cs = Math.min(paneW / PANE_W, vh / CONTENT_H);
    var gapL = 1 * cs;
    var mT = 14 * cs;
    var mB = 13 * cs;
    var mR = 14 * cs;

    var cw = Math.max(CARD_W * cs, paneW - gapL - mR);
    var ch = vh - mT - mB;

    if (card) {
      card.style.left = gapL + 'px';
      card.style.top = mT + 'px';
      card.style.width = cw + 'px';
      card.style.height = ch + 'px';
      card.style.borderRadius = (26 * cs) + 'px';
      card.style.borderWidth = Math.max(1, cs) + 'px';
    }

    if (cardIn) {
      var tx = (cw - CARD_W * cs) / 2;
      cardIn.style.transform = 'translate(' + tx + 'px, 0) scale(' + cs + ')';
    }

    var bandH = vh;
    var imgScale = Math.max(photoW / IMG_W, bandH / IMG_H);
    var s = Math.min(imgScale / IMG_REF_SCALE, photoW * 0.92 / HERO_W);
    if (hero) {
      hero.style.transform = 'scale(' + s + ')';
    }
    playActiveVideo();
  }

  // Entrance Animation
  function runEntrance() {
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion || typeof Element.prototype.animate !== 'function') {
      releaseEntrance();
      return;
    }

    var compact = window.matchMedia('(max-width:699px)').matches;
    var ease = 'cubic-bezier(.16,1,.3,1)';
    var softEase = 'cubic-bezier(.22,1,.36,1)';

    var targets = [
      { el: document.querySelector('.card'), delay: 40, duration: 820, easing: ease, from: { opacity: 0, transform: compact ? 'translateY(14px)' : 'translateY(12px) scale(.988)' } },
      { el: document.querySelector('.badge'), delay: 120, duration: 480, easing: softEase, from: { opacity: 0, transform: 'translateY(8px)' } },
      { el: document.getElementById('hl1'), delay: 240, duration: 760, easing: ease, from: { opacity: 0, transform: compact ? 'translateY(12px)' : 'translateY(16px)', clipPath: 'inset(100% 0 0 0)' } },
      { el: document.getElementById('hl2'), delay: 330, duration: 760, easing: ease, from: { opacity: 0, transform: compact ? 'translateY(12px)' : 'translateY(16px)', clipPath: 'inset(100% 0 0 0)' } },
      { el: document.getElementById('h1'), delay: 470, duration: 620, easing: ease, from: { opacity: 0, transform: 'translateY(10px)' } },
      { el: document.getElementById('sub'), delay: 570, duration: 560, easing: ease, from: { opacity: 0, transform: 'translateY(10px)' } },
      { el: document.getElementById('email'), delay: 720, duration: 520, easing: softEase, from: { opacity: 0, transform: 'translateY(8px)' } },
      { el: document.getElementById('pw'), delay: 790, duration: 520, easing: softEase, from: { opacity: 0, transform: 'translateY(8px)' } },
      { el: document.getElementById('loginBtn'), delay: 930, duration: 560, easing: ease, from: { opacity: 0, transform: 'translateY(8px)' } },
      { el: document.querySelector('.divider'), delay: 1060, duration: 440, easing: softEase, from: { opacity: 0, transform: 'translateY(6px)' } },
      { el: document.getElementById('gBtn'), delay: 1150, duration: 540, easing: ease, from: { opacity: 0, transform: 'translateY(8px)' } },
      { el: document.getElementById('bottom'), delay: 1260, duration: 500, easing: softEase, from: { opacity: 0, transform: 'translateY(6px)' } }
    ];

    var anims = [];
    targets.forEach(function(item) {
      if (!item.el) return;
      var to = { opacity: 1, transform: 'none' };
      if (item.from.clipPath) to.clipPath = 'inset(0 0 0 0)';

      var anim = item.el.animate([item.from, to], {
        delay: item.delay,
        duration: item.duration,
        easing: item.easing,
        fill: 'both'
      });
      anims.push(anim);
    });

    document.documentElement.classList.remove('entry-pending');

    Promise.allSettled(anims.map(function(a) { return a.finished; })).then(function() {
      anims.forEach(function(a) { a.cancel(); });
      releaseEntrance();
    });
  }

  function releaseEntrance() {
    if (window.__entryFallback) {
      clearTimeout(window.__entryFallback);
      window.__entryFallback = null;
    }
    document.documentElement.classList.remove('entry-pending');
  }

  window.addEventListener('resize', layout, { passive: true });
  window.addEventListener('orientationchange', layout);
  if (mqLandscape.addEventListener) {
    mqLandscape.addEventListener('change', layout);
    mqPortrait.addEventListener('change', layout);
  }

  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise(function(r){ setTimeout(r, 650); })]).then(function() {
      requestAnimationFrame(function() {
        requestAnimationFrame(runEntrance);
      });
    });
  } else {
    setTimeout(runEntrance, 100);
  }

  layout();
  playActiveVideo();
})();
