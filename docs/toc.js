/* toc.js — builds a Wikipedia-style table of contents from the page's headings.
 * Shared across every page, linked like style.css (depth-relative src). No deps.
 * - Collects h2–h4 in the content (skips the Sources/footnotes block). On the root index
 *   page it stops at h3 (families + doctrines) — the per-argument h4 groups would just
 *   duplicate the directory below; deeper pages keep their h4 sub-sections.
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

  // Doctrine slug → concise display label for the breadcrumb's middle crumb. The label
  // is the only crumb not derivable from the path (an argument page's h1 is the argument,
  // not the doctrine), so it lives here. Add an entry when you add a doctrine (see CLAUDE.md).
  var DOCTRINE_NAMES = {
    "canon": "The Biblical Canon",
    "ot-canon": "The Old Testament Canon",
    "septuagint-origin": "The Septuagint",
    "rabbinic-corruption": "The Rabbinic Corruption of Scripture",
    "intermediate-state": "The Intermediate State",
    "purgatory": "Purgatory",
    "prayer-to-saints": "Prayer to the Saints",
    "dream-apparitions-of-the-dead": "Dream-apparitions of the Dead",
    "discernment-of-dreams": "The Discernment of Dreams",
    "real-presence": "The Real Presence in the Eucharist",
    "ministerial-priesthood": "The Ministerial Priesthood",
    "nephilim": "The Sons of God and the Nephilim",
    "flood": "Noah's Flood",
    "conquest-of-canaan": "The Conquest of Canaan",
    "first-language": "The First Language of Mankind",
    "baptist-successionism": "Baptist Successionism",
    "infant-baptism": "Infant Baptism",
    "church-buildings": "The Place of Christian Worship",
    "perpetual-virginity": "The Perpetual Virginity of Mary",
    "mary-new-eve": "Mary as the New Eve",
    "theotokos": "Theotokos (Mother of God)",
    "immaculate-conception": "The Immaculate Conception of Mary",
    "assumption": "The Assumption / Dormition of Mary",
    "writing-on-the-ground": "What Jesus Wrote on the Ground",
    "astrology": "Astrology and the Stars",
    "pillars-of-seth": "The Pillars of Seth",
    "mythical-beasts": "Dragons, Unicorns & Mythical Beasts",
    "goliath-slayer": "Who Killed Goliath?",
    "goliath-height": "How Tall Was Goliath?",
    "revelation-date": "The Date of Revelation",
    "mark-of-the-beast": "The Mark of the Beast and the Number 666",
    "origenist-controversy": "The Origenist Controversy (Jerome and Rufinus)",
    "jerome-augustine": "Jerome and Augustine: a correspondence across the Mediterranean"
  };

  // The page's depth-relative path prefix ("", "../", "../../", "../../../"), read from its
  // own stylesheet href (style.css). Lets every crumb URL be built without counting path
  // segments. Returns null on the root page (empty prefix) or if no stylesheet is found.
  function getPrefix() {
    var links = document.querySelectorAll('link[rel~="stylesheet"]');
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href") || "";
      var m = href.match(/^(.*?)style\.css(?:[?#].*)?$/);
      if (m) return m[1];
    }
    return null;
  }

  function prettifySlug(slug) {
    return slug.replace(/-/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  // Build the breadcrumb trail (Home › Doctrine › leaf) entirely from the path + the map
  // above — no network. Returns a <nav> for any non-root page, or null on index.html / when
  // the path doesn't sit under doctrines/. Crumbs: linked ancestors as <a>, the current page
  // as a non-link <span aria-current="page"> (separators are CSS-generated, not in markup).
  function buildBreadcrumb() {
    var prefix = getPrefix();
    if (!prefix) return null; // root page (or no stylesheet) — no breadcrumb

    var segs = location.pathname.split("/").filter(Boolean);
    var di = segs.lastIndexOf("doctrines");
    if (di === -1 || di + 1 >= segs.length) return null;
    var next = segs[di + 1];
    var isSummary = /\.html$/i.test(next);
    var isArgument = segs.indexOf("arguments") > di;
    var slug = next.replace(/\.html$/i, "");

    var crumbs = [
      { href: prefix + "index.html", text: "⌂ Doctrine Across Time" }
    ];
    var doctrineName = DOCTRINE_NAMES[slug] || prettifySlug(slug);
    if (isSummary) {
      crumbs.push({ text: doctrineName }); // the summary itself — current, no link
    } else {
      crumbs.push({ href: prefix + "doctrines/" + slug + ".html", text: doctrineName });
      crumbs.push(leafCrumb(doctrineName, isArgument));
    }

    var nav = document.createElement("nav");
    nav.className = "breadcrumb";
    nav.setAttribute("aria-label", "Breadcrumb");
    var ol = document.createElement("ol");
    crumbs.forEach(function (c) {
      var li = document.createElement("li");
      var el;
      if (c.href) {
        el = document.createElement("a");
        el.href = c.href;
      } else {
        el = document.createElement("span");
        el.setAttribute("aria-current", "page");
      }
      el.textContent = c.text;
      if (c.title) el.title = c.title;
      li.appendChild(el);
      ol.appendChild(li);
    });
    nav.appendChild(ol);
    return nav;
  }

  // The trailing (current-page) crumb for a person or argument page, derived from the h1:
  //  • person h1 "Jerome on the Old Testament Canon" → "Jerome" (strip the doctrine phrase),
  //  • argument h1 (a long question) → truncated, with the full text on hover.
  // The " on …" strip is person-only — an argument h1 can legitimately contain " on " (e.g.
  // "Does X depend on Y?"), so argument pages are never stripped, only truncated.
  function leafCrumb(doctrineName, isArgument) {
    var h1 = document.querySelector("h1");
    var text = h1 ? (h1.textContent || "").trim() : "";
    if (!isArgument) {
      // Try the mapped doctrine name first, then a generic trailing " on …".
      var escaped = doctrineName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      var stripped = text.replace(new RegExp("\\s+on\\s+" + escaped + "\\s*$", "i"), "");
      if (stripped === text) stripped = text.replace(/\s+on\s+.+$/i, "");
      if (stripped !== text && stripped) return { text: stripped };
    }
    if (text.length > 60) return { text: text.slice(0, 57).trim() + "…", title: text };
    return { text: text };
  }

  function insertAfterH1(node) {
    var h1 = document.querySelector("h1");
    if (h1 && h1.parentNode) h1.parentNode.insertBefore(node, h1.nextSibling);
    else document.body.insertBefore(node, document.body.firstChild);
  }

  function build() {
    // Breadcrumb rides at the very top of every non-root page, independent of the TOC —
    // so even a short, TOC-less page (and a deep-linked one) can climb the hierarchy.
    var crumbs = buildBreadcrumb();
    if (crumbs) document.body.insertBefore(crumbs, document.body.firstChild);

    // Headings in document order, excluding the Sources/footnote block. The page h1 leads
    // the list (top-level, styled as the title); h2–h4 nest beneath it. On the root index
    // (empty prefix) we stop at h3 so the TOC lists families + doctrines only — its h4
    // argument-groups would merely restate the rated directory printed below it.
    var levels = getPrefix() === "" ? "h1, h2, h3" : "h1, h2, h3, h4";
    var all = Array.prototype.slice.call(document.querySelectorAll(levels));
    var headings = all.filter(function (h) {
      if (h.closest(".footnote")) return false;
      var t = (h.textContent || "").trim();
      return t.toLowerCase() !== "sources";
    });

    if (headings.length < 3) return; // too short for a TOC (breadcrumb already handles up-nav)

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

  function init() {
    build();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
