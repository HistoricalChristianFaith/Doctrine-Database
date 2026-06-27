/* toc.js — builds a Wikipedia-style table of contents from the page's headings.
 * Shared across every page, linked like style.css (depth-relative src). No deps.
 * - Collects h2/h3 in the content (skips the page h1 and the Sources/footnotes block).
 * - Floats in the left gutter on wide viewports; collapses to a block at the top otherwise
 *   (positioning is entirely in style.css; this file only builds the markup + scroll-spy).
 */
(function () {
  "use strict";

  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^\w]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60) || "section";
  }

  // A "home" link back to the site root (index.html). The href reuses the page's own
  // depth-relative stylesheet prefix (style.css → index.html), so it is correct at any
  // depth without counting path segments. Returns null on the root page (empty prefix)
  // or if no stylesheet is found.
  function makeHome() {
    var links = document.querySelectorAll('link[rel~="stylesheet"]');
    var prefix = null;
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href") || "";
      var m = href.match(/^(.*?)style\.css(?:[?#].*)?$/);
      if (m) { prefix = m[1]; break; }
    }
    if (!prefix) return null; // no stylesheet, or already at the root
    var a = document.createElement("a");
    a.className = "toc-home";
    a.href = prefix + "index.html";
    a.textContent = "⌂ Doctrine Across Time";
    return a;
  }

  function insertAfterH1(node) {
    var h1 = document.querySelector("h1");
    if (h1 && h1.parentNode) h1.parentNode.insertBefore(node, h1.nextSibling);
    else document.body.insertBefore(node, document.body.firstChild);
  }

  function build() {
    var home = makeHome();

    // Headings in document order, excluding the Sources/footnote block. The page h1 leads
    // the list (top-level, styled as the title); h2–h4 nest beneath it.
    var all = Array.prototype.slice.call(document.querySelectorAll("h1, h2, h3, h4"));
    var headings = all.filter(function (h) {
      if (h.closest(".footnote")) return false;
      var t = (h.textContent || "").trim();
      return t.toLowerCase() !== "sources";
    });

    if (headings.length < 3) {
      // Too short for a TOC, but the home link still belongs on the page — drop it in
      // standalone (inline at the top) so every page can get back to the root.
      if (home) { home.classList.add("toc-home--solo"); insertAfterH1(home); }
      return;
    }

    // Ensure every target has a unique id (without clobbering existing footnote ids).
    var used = {};
    document.querySelectorAll("[id]").forEach(function (el) { used[el.id] = true; });

    var details = document.createElement("details");
    details.className = "toc";
    details.id = "toc";

    // Default open when floating in the side gutter, collapsed when inline at the top.
    // The query MUST match the float breakpoint in style.css (.toc @media min-width).
    // Re-applies when the viewport crosses the breakpoint, unless the user has toggled it.
    var sideMode = window.matchMedia ? window.matchMedia("(min-width: 78.5em)") : null;
    var userToggled = false, suppressToggle = false;
    details.open = sideMode ? sideMode.matches : true;
    details.addEventListener("toggle", function () {
      if (!suppressToggle) userToggled = true;
    });
    if (sideMode && sideMode.addEventListener) {
      sideMode.addEventListener("change", function () {
        if (userToggled) return;
        suppressToggle = true;
        details.open = sideMode.matches;
        suppressToggle = false;
      });
    }

    var summary = document.createElement("summary");
    summary.className = "toc-title";
    var summaryText = document.createElement("span");
    summaryText.textContent = "Table of Contents";
    summary.appendChild(summaryText); // span lets us gap the text off the disclosure marker
    details.appendChild(summary);

    var nav = document.createElement("nav");
    nav.setAttribute("aria-label", "Table of contents");
    var ul = document.createElement("ul");

    var byId = {};
    headings.forEach(function (h) {
      var id = h.id;
      if (!id) {
        id = slugify(h.textContent || "");
        var base = id, n = 2;
        while (used[id]) { id = base + "-" + n++; }
        h.id = id;
      }
      used[id] = true;

      var li = document.createElement("li");
      li.className = "toc-" + h.tagName.toLowerCase();
      var a = document.createElement("a");
      a.href = "#" + id;
      // Trim the TOC label only — the headings themselves keep their full text:
      //  • drop a trailing "(assessment: …)" tag, and
      //  • drop the leading "Related arguments —" prefix from argument-group h4s,
      // both of which just clutter the list.
      a.textContent = (h.textContent || "").trim()
        .replace(/\s*\(assessment:[^)]*\)\s*$/i, "")
        .replace(/^Related arguments\s*[—–-]\s*/i, "");
      li.appendChild(a);
      ul.appendChild(li);
      byId[id] = a;
    });

    nav.appendChild(ul);
    details.appendChild(nav);

    // Home link rides at the top of the TOC box, above the "Table of Contents" toggle.
    if (home) details.insertBefore(home, details.firstChild);

    insertAfterH1(details);

    setupScrollSpy(headings, byId, details, summary);
  }

  function setupScrollSpy(headings, byId, box, titleEl) {
    if (!("IntersectionObserver" in window)) return;
    var current = null;

    function setActive(id) {
      if (id === current) return;
      if (current && byId[current]) byId[current].classList.remove("toc-active");
      current = id;
      var link = byId[id];
      if (!link) return;
      link.classList.add("toc-active");
      // Keep the active link visible inside the TOC's own scroll box (float mode only;
      // never scrolls the window — we only nudge box.scrollTop). Offset the sticky title
      // so the active link doesn't end up hidden behind it.
      var lr = link.getBoundingClientRect(), br = box.getBoundingClientRect();
      var titleH = titleEl ? titleEl.getBoundingClientRect().height : 0;
      if (lr.top < br.top + titleH) box.scrollTop -= (br.top + titleH - lr.top) + 8;
      else if (lr.bottom > br.bottom) box.scrollTop += (lr.bottom - br.bottom) + 8;
    }

    // A heading becomes "current" once it reaches the top ~15% of the viewport.
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) setActive(e.target.id);
      });
    }, { rootMargin: "0px 0px -85% 0px", threshold: 0 });

    headings.forEach(function (h) { io.observe(h); });
  }

  // Announce this page's path to a parent viewer shell (historicalchristian.faith
  // /doctrine), so it can mirror the location in its address bar for deep-linking.
  // No-ops when the page is viewed standalone on GitHub Pages (parent === self), and
  // the pinned targetOrigin means the message reaches only that one shell.
  function postLocationToParent() {
    if (window.parent === window) return; // not framed
    var base = "/Doctrine-Database/"; // GitHub Pages repo root
    var path = location.pathname;
    var rel =
      path.indexOf(base) === 0 ? path.slice(base.length) : path.replace(/^\/+/, "");
    var msg = { type: "doctrine-nav", page: rel + location.search, hash: location.hash };
    // Trusted parent shells this page may be embedded in. postMessage takes a single
    // targetOrigin, so we post once per allowed origin — the browser delivers only to the
    // frame whose origin matches and silently drops the rest. Pinned (never "*") to keep
    // the message from leaking to an unexpected embedder.
    var ALLOWED_PARENTS = [
      "https://historicalchristian.faith",
      "http://localhost:8888" // local dev shell
    ];
    ALLOWED_PARENTS.forEach(function (origin) {
      window.parent.postMessage(msg, origin);
    });
  }

  function init() {
    build();
    postLocationToParent();
  }

  window.addEventListener("hashchange", postLocationToParent);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
