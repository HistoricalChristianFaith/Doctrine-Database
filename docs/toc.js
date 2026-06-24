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

  function build() {
    // Headings in document order, excluding the title (h1) and the Sources/footnote block.
    var all = Array.prototype.slice.call(document.querySelectorAll("h2, h3, h4"));
    var headings = all.filter(function (h) {
      if (h.closest(".footnote")) return false;
      var t = (h.textContent || "").trim();
      return t.toLowerCase() !== "sources";
    });

    if (headings.length < 3) return; // too short to be worth a TOC

    // Ensure every target has a unique id (without clobbering existing footnote ids).
    var used = {};
    document.querySelectorAll("[id]").forEach(function (el) { used[el.id] = true; });

    var details = document.createElement("details");
    details.className = "toc";
    details.id = "toc";
    details.open = true;

    var summary = document.createElement("summary");
    summary.className = "toc-title";
    summary.textContent = "Contents";
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
      // Drop a trailing "(assessment: …)" tag from the TOC label only — it clutters the
      // list; the heading itself keeps it.
      a.textContent = (h.textContent || "").trim().replace(/\s*\(assessment:[^)]*\)\s*$/i, "");
      li.appendChild(a);
      ul.appendChild(li);
      byId[id] = a;
    });

    nav.appendChild(ul);
    details.appendChild(nav);

    // Insert after the page h1 if present, else at the top of <body>.
    var h1 = document.querySelector("h1");
    if (h1 && h1.parentNode) {
      h1.parentNode.insertBefore(details, h1.nextSibling);
    } else {
      document.body.insertBefore(details, document.body.firstChild);
    }

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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
