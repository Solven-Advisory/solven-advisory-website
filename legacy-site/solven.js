/* Solven Advisory: interaction & motion layer
   ----------------------------------------------------------------------
   Invariants (do not break):
   1. Visible by default. Hidden states exist ONLY behind a JS-applied
      class (.pending, body.intro-armed) that always has a release path.
   2. Reduced motion is a hard stop: nothing below the `if (reduce)` line
      binds; CSS resting states are the finished design.
   3. Transitions (not keyframe clocks) drive load-critical reveals, with
      timed rescues, so a stalled clock can never strand content.
   ---------------------------------------------------------------------- */
(function () {
  "use strict";

  var de = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Capability classes (single source of truth for CSS gating) ---- */
  if (!reduce) de.classList.add("anim");                       // master motion switch
  if (!reduce && window.matchMedia("(hover: hover) and (pointer: fine)").matches)
    de.classList.add("has-pointer");                           // gates magnetic CTA

  /* ---- Decorative overlays (pure enhancement; absent if JS fails) ---- */
  function inject(cls) {
    var el = document.createElement("div");
    el.className = cls;
    el.setAttribute("aria-hidden", "true");
    document.body.appendChild(el);
    return el;
  }
  inject("grain");
  var srule = inject("scroll-rule");

  /* ---- Mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---- Line-mask splitter ----
     Wraps each visual line of a plain-text headline in
     .lm__mask > .lm__line so the lines can wipe up. Runs after layout;
     skipped under reduced motion and never run twice. */
  function lineMask(el) {
    if (!el || reduce || el.dataset.lmDone) return;
    var text = el.textContent.replace(/\s+/g, " ").trim();
    if (!text) return;
    var words = text.split(" ");
    el.textContent = "";
    var probes = [];
    var frag = document.createDocumentFragment();
    words.forEach(function (w, i) {
      var s = document.createElement("span");
      s.textContent = w + (i < words.length - 1 ? " " : "");
      s.style.display = "inline-block";   // measurable while probing
      frag.appendChild(s);
      probes.push(s);
    });
    el.appendChild(frag);
    // Group words into visual lines by their vertical offset.
    var lines = [], cur = [], top = null;
    probes.forEach(function (s) {
      var t = s.offsetTop;
      if (top === null || Math.abs(t - top) < 2) cur.push(s);
      else { lines.push(cur); cur = [s]; }
      top = t;
    });
    if (cur.length) lines.push(cur);
    // Rebuild as masked block lines.
    el.textContent = "";
    lines.forEach(function (group, li) {
      var mask = document.createElement("span");
      mask.className = "lm__mask";
      var line = document.createElement("span");
      line.className = "lm__line";
      line.style.setProperty("--li", li);
      group.forEach(function (s) { s.style.display = ""; line.appendChild(s); });
      mask.appendChild(line);
      el.appendChild(mask);
    });
    el.classList.add("lm");
    el.dataset.lmDone = "1";
  }

  /* ---- Hero intro (transition-based, never leaves content hidden) ---- */
  if (!reduce && document.body.hasAttribute("data-intro")) {
    // Split hero line-mask headlines BEFORE arming, so their lines exist
    // to be hidden by intro-armed.
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-intro] .line-mask"),
      function (h) { lineMask(h); }
    );
    // Measure the hero chevron's stroke for an exact draw (home only).
    var cs = document.querySelector(".hero__chev .cs");
    if (cs && "getTotalLength" in cs) {
      try { cs.style.setProperty("--chev-len", cs.getTotalLength().toFixed(1)); } catch (e) {}
    }
    var b = document.body;
    b.classList.add("intro-armed");                 // hide instantly (no transition)
    var release = function () { b.classList.add("intro-go"); };
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(release);        // paint hidden once, then release
    });
    window.setTimeout(release, 90);
    window.setTimeout(release, 1200);
    window.setTimeout(function () { b.classList.add("intro-rescue"); }, 2000);
  }

  if (reduce) return; // everything below is enhancement only

  /* ---- Measure the executed signature so its ink can draw on reveal ---- */
  var sig = document.querySelector(".party--solven .ink");
  if (sig && "getTotalLength" in sig) {
    try { sig.style.setProperty("--sig-len", sig.getTotalLength().toFixed(1)); } catch (e) {}
  }

  /* ---- Reveal engine: IntersectionObserver + reveal:in event bus ----
     Preserves the original contract: only elements that START below the
     fold are hidden; a 2500ms safety net reveals anything left. */
  var all = Array.prototype.slice.call(
    document.querySelectorAll(".reveal, .draw-rule, [data-stagger], .band-curtain")
  );
  var vh = window.innerHeight || de.clientHeight;

  // Index children of stagger containers for CSS delay math.
  document.querySelectorAll("[data-stagger]").forEach(function (c) {
    Array.prototype.forEach.call(c.children, function (el, i) {
      el.style.setProperty("--i", i);
    });
  });

  var pending = [];
  all.forEach(function (el) {
    if (el.getBoundingClientRect().top > vh * 0.85) {
      el.classList.add("pending");
      pending.push(el);
    }
  });

  function fire(el) {
    el.classList.add("in");
    el.dispatchEvent(new CustomEvent("reveal:in", { bubbles: true }));
  }

  if ("IntersectionObserver" in window && pending.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { fire(e.target); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.01 });
    pending.forEach(function (el) { io.observe(el); });
  } else if (pending.length) {
    // Fallback: rAF-throttled scroll listener.
    var ticking = false;
    var check = function () {
      var h = window.innerHeight || de.clientHeight;
      var trigger = h * 0.88;
      for (var i = pending.length - 1; i >= 0; i--) {
        var r = pending[i].getBoundingClientRect();
        if (r.top < trigger && r.bottom > 0) { fire(pending[i]); pending.splice(i, 1); }
      }
      if (!pending.length) {
        window.removeEventListener("scroll", onScroll);
        window.removeEventListener("resize", onScroll);
      }
    };
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { check(); ticking = false; });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    check();
  }

  // Safety net, two layers. At 2500ms, rescue only what the viewer can
  // already see; content still below the fold keeps its observer so its
  // reveal actually plays on arrival (the drawn chart, the signature, the
  // cascades). A throttled scroll belt then catches anything the observer
  // somehow missed once it is well inside the viewport, so nothing can
  // strand hidden even if IntersectionObserver misbehaves.
  window.setTimeout(function () {
    var vhNow = window.innerHeight || de.clientHeight;
    for (var i = pending.length - 1; i >= 0; i--) {
      var el = pending[i];
      if (el.classList.contains("in")) { pending.splice(i, 1); continue; }
      if (el.getBoundingClientRect().top < vhNow + 120) {
        fire(el);
        pending.splice(i, 1);
      }
    }
  }, 2500);
  (function () {
    var belt = false;
    window.addEventListener("scroll", function () {
      if (belt || !pending.length) return;
      belt = true;
      window.requestAnimationFrame(function () {
        var vhNow = window.innerHeight || de.clientHeight;
        for (var i = pending.length - 1; i >= 0; i--) {
          var el = pending[i];
          if (el.classList.contains("in")) { pending.splice(i, 1); continue; }
          if (el.getBoundingClientRect().top < vhNow * 0.6) {
            fire(el);
            pending.splice(i, 1);
          }
        }
        belt = false;
      });
    }, { passive: true });
  })();

  /* ---- Cadence cascade (home frontier timeline) ----
     Sequences ticks/dots/diamonds left→right by their left% so the
     weekly-vs-monthly rhythm reads through the motion itself. */
  var cad = document.querySelector(".cadence");
  if (cad) {
    cad.addEventListener("reveal:in", function () {
      function cascade(sel, base, step) {
        Array.prototype.slice.call(cad.querySelectorAll(sel))
          .sort(function (a, b) { return parseFloat(a.style.left) - parseFloat(b.style.left); })
          .forEach(function (el, i) { el.style.setProperty("--d", (base + i * step) + "ms"); });
      }
      cascade(".cadence__week", 0, 34);
      cascade(".cadence__cap", 480, 80);
      cascade(".cadence__session", 980, 150);
    });
  }

  /* ---- Magnetic primary CTA (fine-pointer only) ---- */
  if (de.classList.contains("has-pointer")) {
    document.querySelectorAll(".btn--solid, .btn--dark").forEach(function (btn) {
      var raf = null;
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        var dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        var mx = Math.max(-1, Math.min(1, dx)) * 6;   // cap 6px
        var my = Math.max(-1, Math.min(1, dy)) * 4;   // cap 4px
        if (raf) return;
        raf = window.requestAnimationFrame(function () {
          btn.style.setProperty("--mx", mx.toFixed(1) + "px");
          btn.style.setProperty("--my", my.toFixed(1) + "px");
          raf = null;
        });
      });
      btn.addEventListener("pointerleave", function () {
        btn.style.setProperty("--mx", "0px");
        btn.style.setProperty("--my", "0px");
      });
    });
  }

  /* ---- Scroll-progress hairline (tracks 1:1, no easing) ---- */
  (function () {
    var t = false;
    function upd() {
      var max = de.scrollHeight - de.clientHeight;
      var p = max > 0 ? (window.pageYOffset || de.scrollTop) / max : 0;
      srule.style.transform = "scaleX(" + Math.min(1, Math.max(0, p)).toFixed(4) + ")";
      t = false;
    }
    window.addEventListener("scroll", function () {
      if (!t) { t = true; window.requestAnimationFrame(upd); }
    }, { passive: true });
    window.addEventListener("resize", upd);
    upd();
  })();

  /* ---- Subtle parallax on background chevrons (cinematic depth) ---- */
  var px = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  if (px.length) {
    var pxTicking = false;
    function pxUpdate() {
      var vh2 = window.innerHeight || de.clientHeight;
      px.forEach(function (el) {
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.06;
        var anchor = el.offsetParent || el.parentElement;
        if (!anchor) return;
        var rect = anchor.getBoundingClientRect();
        var offset = (rect.top + rect.height / 2 - vh2 / 2);
        el.style.transform = "translate3d(0," + (-offset * speed).toFixed(1) + "px,0)";
      });
    }
    window.addEventListener("scroll", function () {
      if (pxTicking) return;
      pxTicking = true;
      window.requestAnimationFrame(function () { pxUpdate(); pxTicking = false; });
    }, { passive: true });
    window.addEventListener("resize", pxUpdate);
    pxUpdate();
  }

  /* ---- Living hero chevron (home only) ----
     Once the intro construction has seated, the watermark frontier mark
     becomes a quiet, explorable object: it eases toward the cursor and wakes
     slightly while the pointer is inside the hero, and a click re-inks it.
     Bound after the intro/rescue window (2200ms) so it never competes with
     the construction, and only when has-pointer is set (fine pointer + motion
     and never under reduced motion). Pure enhancement: navigation and the
     resting 5% watermark are untouched if this never runs. */
  var heroChev = document.querySelector(".hero__chev");
  var heroSec = document.querySelector(".hero");
  if (heroChev && heroSec && de.classList.contains("has-pointer")) {
    window.setTimeout(function () {
      heroChev.classList.add("live");
      var craf = null, rect = null;
      heroSec.addEventListener("pointerenter", function () {
        rect = heroSec.getBoundingClientRect();
        heroChev.classList.add("awake");
      });
      heroSec.addEventListener("pointermove", function (e) {
        if (craf) return;
        craf = window.requestAnimationFrame(function () {
          craf = null;
          if (!rect) rect = heroSec.getBoundingClientRect();
          var dx = (e.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);
          var dy = (e.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);
          dx = Math.max(-1, Math.min(1, dx));
          dy = Math.max(-1, Math.min(1, dy));
          heroChev.style.transform =
            "translate3d(" + (dx * 7).toFixed(1) + "px," + (dy * 5).toFixed(1) +
            "px,0) rotate(" + (dx * 2.4).toFixed(2) + "deg)";
        });
      });
      heroSec.addEventListener("pointerleave", function () {
        heroChev.classList.remove("awake");
        heroChev.style.transform = "";
      });
      // Click the hero backdrop (not a control) to re-ink the mark.
      heroSec.addEventListener("click", function (e) {
        if (e.target.closest("a, button, input, textarea, select, label")) return;
        heroChev.classList.remove("reinking");
        void heroChev.offsetWidth;                 // restart the keyframe
        heroChev.classList.add("reinking");
      });
      heroChev.addEventListener("animationend", function (e) {
        if (e.animationName === "hero-chev-reink") heroChev.classList.remove("reinking");
      });
    }, 2200);
  }
})();
