/* Solven Advisory · site v4 preview. Two small behaviours, both instant, no animation. */

/* Header button: an outline while the page's hero is in view, solid once it has gone. */
(function () {
  var header = document.querySelector(".header");
  var hero = document.querySelector(".hero");
  if (!header) return;
  if (!hero) { header.classList.remove("cta-quiet"); return; }
  function update() { header.classList.toggle("cta-quiet", hero.getBoundingClientRect().bottom > 80); }
  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
})();

/* Calçada: the stones under the pointer read darker. Sets the pointer position and marks the hero lit;
   the CSS does the rest. Mouse and pen only: off on touch and under prefers-reduced-motion. */
(function () {
  var hero = document.querySelector(".hero");
  var layer = hero && hero.querySelector(".hero__calcada");
  if (!layer || !window.matchMedia) return;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var still = window.matchMedia("(prefers-reduced-motion: reduce)");
  function allowed(e) { return fine.matches && !still.matches && e.pointerType !== "touch"; }
  function move(e) {
    if (!allowed(e)) { hero.classList.remove("is-lit"); return; }
    var r = hero.getBoundingClientRect();
    layer.style.setProperty("--mx", (e.clientX - r.left) + "px");
    layer.style.setProperty("--my", (e.clientY - r.top) + "px");
    hero.classList.add("is-lit");
  }
  function leave() { hero.classList.remove("is-lit"); }
  hero.addEventListener("pointermove", move);
  hero.addEventListener("pointerleave", leave);
  hero.addEventListener("pointercancel", leave);
})();

/* Language switch: the other language opens at the same place in the page. Both languages share one
   template, so the first block that starts in view is found by its position among the page's blocks and
   put back at the same height. If the blocks do not match (a page with no counterpart), the same share of
   the page's length is used instead. Instant, no scrolling animation. */
(function () {
  var KEY = "solven-lang-scroll";
  var main = document.querySelector("main");
  if (!main || !window.sessionStorage) return;
  var BLOCKS = "h1, h2, h3, h4, p, li, figure, img, blockquote, table, tr, dt, dd, form, section, article";
  function blocks() {
    return Array.prototype.filter.call(main.querySelectorAll(BLOCKS), function (el) { return el.getClientRects().length; });
  }
  function room() { return document.documentElement.scrollHeight - window.innerHeight; }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".lang a[href]");
    if (!a || a.getAttribute("aria-current") || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var list = blocks(), at = -1, top = 0;
    for (var i = 0; i < list.length; i++) {
      top = list[i].getBoundingClientRect().top;
      if (top >= 0) { at = i; break; }
    }
    try {
      sessionStorage.setItem(KEY, JSON.stringify({ path: new URL(a.href).pathname, count: list.length, at: at, top: top,
                                                   share: room() > 0 ? window.scrollY / room() : 0 }));
    } catch (err) {}
  });

  var saved;
  try { saved = JSON.parse(sessionStorage.getItem(KEY)); sessionStorage.removeItem(KEY); } catch (err) { return; }
  if (!saved || saved.path !== location.pathname || location.hash) return;
  function restore() {
    var list = blocks();
    if (list.length === saved.count && saved.at >= 0) {
      window.scrollTo({ top: window.scrollY + list[saved.at].getBoundingClientRect().top - saved.top, behavior: "instant" });
    } else {
      window.scrollTo({ top: saved.share * room(), behavior: "instant" });
    }
  }
  restore();
  window.addEventListener("load", restore, { once: true });
})();
