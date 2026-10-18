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
