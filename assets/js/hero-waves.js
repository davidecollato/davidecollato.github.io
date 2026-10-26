/*
 * Animated hero banner: time-harmonic plane wave scattered by a sound-soft disk.
 *
 * The complex field u(x) is precomputed by scripts/make_hero_field.py and stored
 * in images/hero/field.png (R = Re u, G = Im u). Each frame draws
 * Re(u e^{-i omega t}) = Re(u) cos(omega t) + Im(u) sin(omega t) with viridis.
 * Without JavaScript, or with prefers-reduced-motion, the static poster stays.
 */
(function () {
  var PERIOD_MS = 3000;
  var FRAME_MS = 1000 / 30;
  var OBSTACLE = "rgb(24, 26, 33)"; // keep in sync with scripts/make_hero_field.py
  var VIRIDIS = ["#440154", "#472d7b", "#3b528b", "#2c728e", "#21918c",
                 "#28ae80", "#5ec962", "#addc30", "#fde725"];

  var canvas = document.getElementById("hero-waves");
  if (!canvas || !canvas.getContext) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  // Colour table packed as RGBA uint32 (little-endian byte order): 256 viridis
  // entries plus LUT_PAD copies of the end colours on each side, so the inner
  // loop needs no clamping (quantisation can push |value| slightly above 1).
  var LUT_PAD = 2;
  function buildLut() {
    var stops = VIRIDIS.map(function (h) {
      return [1, 3, 5].map(function (i) { return parseInt(h.substr(i, 2), 16); });
    });
    var lut = new Uint32Array(256 + 2 * LUT_PAD);
    for (var j = 0; j < lut.length; j++) {
      var i = Math.max(0, Math.min(255, j - LUT_PAD));
      var t = i / 255 * (stops.length - 1);
      var k = Math.min(Math.floor(t), stops.length - 2);
      var f = t - k, a = stops[k], b = stops[k + 1];
      var rgb = [0, 1, 2].map(function (c) { return Math.round(a[c] + (b[c] - a[c]) * f); });
      lut[j] = (255 << 24) | (rgb[2] << 16) | (rgb[1] << 8) | rgb[0];
    }
    return lut;
  }

  var img = new Image();
  img.onload = function () {
    var w = img.naturalWidth, h = img.naturalHeight;
    var tmp = document.createElement("canvas");
    tmp.width = w; tmp.height = h;
    var tctx = tmp.getContext("2d");
    tctx.drawImage(img, 0, 0);
    var src = tctx.getImageData(0, 0, w, h).data;

    var n = w * h;
    // Re u, Im u rescaled to [-127.5, 127.5], i.e. already in colour-table units
    var re = new Float32Array(n), im = new Float32Array(n);
    for (var p = 0; p < n; p++) {
      re[p] = src[4 * p] - 127.5;
      im[p] = src[4 * p + 1] - 127.5;
    }
    var offset = 127.5 + 0.5 + LUT_PAD;

    canvas.width = w; canvas.height = h;
    var ctx = canvas.getContext("2d");
    var frame = ctx.createImageData(w, h);
    var out = new Uint32Array(frame.data.buffer);
    var lut = buildLut();

    var cx = parseFloat(canvas.dataset.cx) * w;
    var cy = parseFloat(canvas.dataset.cy) * h;
    var r = parseFloat(canvas.dataset.r) * w;

    function draw(t) {
      var phase = 2 * Math.PI * t / PERIOD_MS;
      var c = Math.cos(phase), s = Math.sin(phase);
      for (var p = 0; p < n; p++) {
        out[p] = lut[(re[p] * c + im[p] * s + offset) | 0];
      }
      ctx.putImageData(frame, 0, 0);
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, 2 * Math.PI);
      ctx.fillStyle = OBSTACLE;
      ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = "#fff";
      ctx.stroke();
    }

    var visible = true, running = false, last = 0, elapsed = 0;
    function loop(now) {
      if (!visible) { running = false; return; }
      if (now - last >= FRAME_MS) {
        elapsed += Math.min(now - last, 100);
        last = now;
        draw(elapsed);
      }
      requestAnimationFrame(loop);
    }
    function start() {
      if (running) return;
      running = true;
      last = performance.now();
      requestAnimationFrame(loop);
    }

    draw(0);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        if (visible) start();
      }).observe(canvas);
    } else {
      start();
    }
  };
  img.src = canvas.dataset.field;
})();
