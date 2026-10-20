/* Solven Advisory: consent gate & analytics loader
   ----------------------------------------------------------------------
   Invariants (do not break):
   1. No analytics script is fetched and no analytics cookie is written
      until the visitor actively chooses "accept". Silence is not consent,
      and neither is scrolling, clicking, or closing the banner.
   2. Declining costs exactly one click, carries the same visual weight as
      accepting, and is remembered. Global Privacy Control and Do Not Track
      are honoured as a standing decline; those visitors never see a banner.
   3. Consent is withdrawable. Any [data-cookie-settings] control reopens
      the banner, and withdrawing purges the cookies the vendors set.
   4. The choice itself lives in localStorage, not a cookie, and is the only
      thing this file stores without being asked.
   5. If no vendor below is configured, the banner never shows. A site that
      sets no cookies must not claim to.
   ---------------------------------------------------------------------- */
(function () {
  "use strict";

  /* ---- Vendors. Blank string disables that vendor entirely. ---------- */
  var VENDORS = {
    posthog: "",   // PostHog EU project key, e.g. "phc_AbC123..."
    clarity: ""    // Microsoft Clarity project id, e.g. "a1b2c3d4e5"
  };

  var STORE = "solven.consent";     // "granted" | "denied"
  var VERSION = "2026-07";          // bump to re-ask after a material change
  var STORE_V = "solven.consent.v";

  /* ---- Storage helpers (private browsing can throw on access) -------- */
  function read(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function write(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* no-op */ }
  }

  function state() {
    if (read(STORE_V) !== VERSION) return null;   // stale or absent choice
    var v = read(STORE);
    return v === "granted" || v === "denied" ? v : null;
  }

  /* ---- Signals that count as a standing refusal ---------------------- */
  function refusedByBrowser() {
    return navigator.globalPrivacyControl === true ||
           navigator.doNotTrack === "1" ||
           window.doNotTrack === "1";
  }

  var configured = Object.keys(VENDORS).filter(function (k) { return VENDORS[k]; });

  /* ---- Loading the vendors ------------------------------------------ */
  var loaded = false;

  function loadAnalytics() {
    if (loaded) return;
    loaded = true;

    if (VENDORS.posthog) {
      !function (t, e) {
        var o, n, p, r;
        e.__SV || (window.posthog = e, e._i = [], e.init = function (i, s, a) {
          function g(t, e) {
            var o = e.split(".");
            2 == o.length && (t = t[o[0]], e = o[1]);
            t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); };
          }
          (p = t.createElement("script")).type = "text/javascript";
          p.async = !0;
          p.src = s.api_host.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js";
          (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(p, r);
          var u = e;
          for (void 0 !== a ? u = e[a] = [] : a = "posthog", u.people = u.people || [],
               u.toString = function (t) {
                 var e = "posthog";
                 return "posthog" !== a && (e += "." + a), t || (e += " (stub)"), e;
               }, u.people.toString = function () { return u.toString(1) + ".people (stub)"; },
               o = "init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),
               n = 0; n < o.length; n++) g(u, o[n]);
          e._i.push([i, s, a]);
        }, e.__SV = 1);
      }(document, window.posthog || []);

      window.posthog.init(VENDORS.posthog, {
        api_host: "https://eu.i.posthog.com",
        ui_host: "https://eu.posthog.com",
        person_profiles: "always",
        capture_pageview: true,
        capture_pageleave: true,
        autocapture: true,
        session_recording: { maskAllInputs: true, maskTextSelector: "[data-private]" },
        persistence: "localStorage+cookie"
      });
    }

    if (VENDORS.clarity) {
      (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      })(window, document, "clarity", "script", VENDORS.clarity);
      window.clarity("consent");
    }
  }

  /* ---- Purging on withdrawal ---------------------------------------- */
  var VENDOR_COOKIES = /^(_clck|_clsk|CLID|MUID|ANONCHK|SM|SRM_B|ph_)/;

  function purge() {
    if (window.posthog && typeof window.posthog.opt_out_capturing === "function") {
      try { window.posthog.opt_out_capturing(); } catch (e) { /* no-op */ }
    }

    var host = location.hostname;
    var domains = ["", host, "." + host];
    var parts = host.split(".");
    if (parts.length > 2) domains.push("." + parts.slice(-2).join("."));

    document.cookie.split(";").forEach(function (raw) {
      var name = raw.split("=")[0].trim();
      if (!name || !VENDOR_COOKIES.test(name)) return;
      domains.forEach(function (d) {
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" +
          (d ? "; domain=" + d : "");
      });
    });

    try {
      Object.keys(window.localStorage).forEach(function (k) {
        if (k.indexOf("ph_") === 0 || k.indexOf("_clck") === 0) window.localStorage.removeItem(k);
      });
    } catch (e) { /* no-op */ }
  }

  /* ---- Copy, in the language of the page ----------------------------- */
  var pt = (document.documentElement.lang || "en").toLowerCase().indexOf("pt") === 0;

  var COPY = pt ? {
    title: "Cookies neste site",
    body: "Usamos cookies de análise para perceber como este site é lido: que páginas prendem a atenção, onde as pessoas param e que percursos levam a uma conversa. Nada é vendido e nada serve para publicidade. Recusar não altera o funcionamento do site.",
    accept: "Aceitar análise",
    decline: "Recusar",
    more: "Política de privacidade",
    region: "Escolha sobre cookies"
  } : {
    title: "Cookies on this site",
    body: "We use analytics cookies to understand how this site is read: which pages hold attention, where people stop, and which routes lead to a conversation. Nothing is sold and nothing feeds advertising. Decline and the site works exactly as it does now.",
    accept: "Accept analytics",
    decline: "Decline",
    more: "Privacy notice",
    region: "Cookie choice"
  };

  /* ---- The banner ---------------------------------------------------- */
  var banner = null;

  function decide(choice) {
    write(STORE, choice);
    write(STORE_V, VERSION);
    if (choice === "granted") loadAnalytics(); else purge();
    if (banner) {
      banner.classList.remove("is-open");
      window.setTimeout(function () {
        if (banner && banner.parentNode) banner.parentNode.removeChild(banner);
        banner = null;
      }, 320);
    }
  }

  function build() {
    if (banner) return;

    banner = document.createElement("div");
    banner.className = "consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-modal", "false");
    banner.setAttribute("aria-label", COPY.region);

    var inner = document.createElement("div");
    inner.className = "consent__inner";

    var text = document.createElement("div");
    text.className = "consent__text";

    var h = document.createElement("p");
    h.className = "consent__title";
    h.textContent = COPY.title;

    var p = document.createElement("p");
    p.className = "consent__body";
    p.textContent = COPY.body + " ";

    var link = document.createElement("a");
    link.href = "/privacy";
    link.textContent = COPY.more;
    p.appendChild(link);

    text.appendChild(h);
    text.appendChild(p);

    var actions = document.createElement("div");
    actions.className = "consent__actions";

    var no = document.createElement("button");
    no.type = "button";
    no.className = "consent__btn";
    no.textContent = COPY.decline;
    no.addEventListener("click", function () { decide("denied"); });

    var yes = document.createElement("button");
    yes.type = "button";
    yes.className = "consent__btn consent__btn--solid";
    yes.textContent = COPY.accept;
    yes.addEventListener("click", function () { decide("granted"); });

    actions.appendChild(no);
    actions.appendChild(yes);

    inner.appendChild(text);
    inner.appendChild(actions);
    banner.appendChild(inner);
    document.body.appendChild(banner);

    // Transition in on the next frame so the class change is animatable.
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        if (banner) banner.classList.add("is-open");
      });
    });
  }

  /* ---- Withdrawal controls ------------------------------------------- */
  document.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-cookie-settings]");
    if (!trigger) return;
    e.preventDefault();
    if (!configured.length) return;
    build();
  });

  /* ---- Boot ----------------------------------------------------------- */
  if (!configured.length) return;          // nothing to consent to

  var choice = state();

  if (choice === "granted") {
    loadAnalytics();
  } else if (choice === null && !refusedByBrowser()) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", build);
    } else {
      build();
    }
  }
})();
