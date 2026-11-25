#!/usr/bin/env python3
"""Ledger split, spec §5.1 step 9: prune orphaned footnotes and renumber.

Usage:
    python3 -I scripts/ledger/prune_orphans.py [--dry-run] [PATH ...]   (default: docs/doctrines/)

A PATH may be a file or a directory (recursed for *.html). Stdlib only, deterministic and
idempotent: a second run changes nothing.

On each page with a footnote apparatus it:
  1. finds every inline reference in the body. Two forms are recognised, exactly as CLAUDE.md
     ("Footnotes") writes them:
         <sup id="fnref<K>:X"><a class="footnote-ref" href="#fn:X">N</a></sup>
         <sup><a class="footnote-ref" href="#fn:X">N</a></sup>     (a repeat cite with no id)
  2. removes every Sources <li id="fn:X"> that no inline reference points at;
  3. renumbers the survivors 1..N by first appearance in the body: the <li>s are reordered,
     every inline ref shows its source's new number, and each backref title ("Jump back to
     footnote N in the text") names it. Ids, hrefs and backref targets are left as they are,
     so the slug-based ids, the fnref<K>: occurrence namespaces and any deep links survive.

Only pages that have at least one orphan are rewritten; a page with no orphans is left alone
even if its numbering is off (that is reported, not fixed).

The script is conservative. It skips a page, and says why, rather than guess when it sees:
  - more or fewer than one <div class="footnote"> Sources block, or an <ol> it can't split
    cleanly into <li id="fn:..."> items;
  - a footnote-ref, or any href="#fn:...", that isn't in one of the two forms above (e.g. a
    prose "see note 1" link, whose wording would need changing);
  - an id'd ref whose id slug differs from its href target;
  - a ref to a source that doesn't exist, or two <li>s with the same id;
  - a kept source whose backref points at a ref id that doesn't exist, or that has no
    backref at all;
  - a kept source cited only by plain id-less <sup>s (its backref would have nothing to
    land on: needs a hand fix);
  - a footnote reference inside the Sources list itself.
"""

import os
import re
import sys

RE_FOOTDIV = re.compile(r'<div class="footnote">\s*<hr>\s*<ol>(?P<body>.*?)</ol>\s*</div>', re.S)
RE_LI = re.compile(r'<li id="fn:(?P<id>[^"]+)">(?P<inner>.*?)</li>', re.S)
RE_REF_ID = re.compile(
    r'<sup id="fnref(?P<k>\d*):(?P<rid>[^"]+)"><a class="footnote-ref" href="#fn:(?P<t>[^"]+)">'
    r'(?P<n>\d+)</a></sup>'
)
RE_REF_PLAIN = re.compile(r'<sup><a class="footnote-ref" href="#fn:(?P<t>[^"]+)">(?P<n>\d+)</a></sup>')
RE_ANY_FN_HREF = re.compile(r'href="#fn:[^"]*"')
RE_FOOTREF_CLASS = re.compile(r'class="footnote-ref"')
RE_BACKREF = re.compile(
    r'<a class="footnote-backref" href="#fnref(?P<k>\d*):(?P<t>[^"]+)" '
    r'title="Jump back to footnote (?P<n>\d+) in the text">'
)
RE_ANY_BACKREF = re.compile(r'class="footnote-backref"')
RE_ID = re.compile(r'\bid="([^"]+)"')


class Skip(Exception):
    pass


def short(inner, width=90):
    txt = re.sub(r"<[^>]+>", "", inner)
    txt = re.sub(r"&#160;|&nbsp;", " ", txt)
    txt = re.sub(r"&#8617;", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt if len(txt) <= width else txt[: width - 1] + "…"


def process(text):
    """Return (new_text or None, report dict). Raises Skip."""
    divs = list(RE_FOOTDIV.finditer(text))
    if not divs:
        if 'id="fn:' in text or "footnote-ref" in text:
            raise Skip('footnote markup present but no <div class="footnote"><hr><ol> block')
        return None, None
    if len(divs) > 1:
        raise Skip(f"{len(divs)} footnote blocks")
    div = divs[0]
    if text.count('<div class="footnote">') != 1:
        raise Skip('more than one <div class="footnote">')
    ol = div.group("body")
    ol_start = div.start("body")

    # --- split the <ol> into items, insisting nothing else is in it ---
    items = list(RE_LI.finditer(ol))
    if not items:
        raise Skip("Sources <ol> has no <li id=\"fn:...\"> items")
    pieces = []
    pos = 0
    seps = []
    for m in items:
        gap = ol[pos:m.start()]
        if gap.strip():
            raise Skip(f"unexpected text in Sources <ol> before fn:{m.group('id')}: {gap.strip()[:60]!r}")
        seps.append(gap)
        pos = m.end()
    tail = ol[pos:]
    if tail.strip():
        raise Skip(f"unexpected text at end of Sources <ol>: {tail.strip()[:60]!r}")
    for m in items:
        if "<li" in m.group("inner"):
            raise Skip(f"nested <li> inside fn:{m.group('id')}")
        if RE_ANY_FN_HREF.search(m.group("inner")) or RE_FOOTREF_CLASS.search(m.group("inner")):
            raise Skip(f"fn:{m.group('id')} contains a footnote reference")
    if ol.count("<li") != len(items):
        raise Skip("Sources <ol> has <li> items without an fn: id")
    head_sep = seps[0]
    inner_seps = set(seps[1:])
    if len(inner_seps) > 1:
        raise Skip("inconsistent whitespace between Sources items")
    joiner = inner_seps.pop() if inner_seps else "\n"

    li_ids = [m.group("id") for m in items]
    if len(set(li_ids)) != len(li_ids):
        dup = sorted({i for i in li_ids if li_ids.count(i) > 1})
        raise Skip(f"duplicate source ids: {', '.join(dup)}")
    li_inner = {m.group("id"): m.group("inner") for m in items}

    # --- inline refs in the body (everything outside the Sources <ol>) ---
    body_before = text[:ol_start]
    body_after = text[ol_start + len(ol):]
    refs = []  # (abs_start, abs_end, kind, k, target, num)
    for seg, off in ((body_before, 0), (body_after, ol_start + len(ol))):
        spans = []
        for m in RE_REF_ID.finditer(seg):
            if m.group("rid") != m.group("t"):
                raise Skip(f"ref id fnref{m.group('k')}:{m.group('rid')} points at #fn:{m.group('t')}")
            spans.append((m.start() + off, m.end() + off, "id", m.group("k"), m.group("t"), m.group("n")))
        for m in RE_REF_PLAIN.finditer(seg):
            spans.append((m.start() + off, m.end() + off, "plain", None, m.group("t"), m.group("n")))
        n_classes = len(RE_FOOTREF_CLASS.findall(seg))
        n_hrefs = len(RE_ANY_FN_HREF.findall(seg))
        if n_classes != len(spans) or n_hrefs != len(spans):
            raise Skip(
                f"{n_hrefs} href=\"#fn:\" / {n_classes} footnote-ref in the body, but only "
                f"{len(spans)} in a recognised <sup> form"
            )
        refs.extend(spans)
    refs.sort()
    if not refs and not items:
        return None, None

    for r in refs:
        if r[4] not in li_inner:
            raise Skip(f"dangling ref to #fn:{r[4]}")

    referenced = {r[4] for r in refs}
    orphans = [i for i in li_ids if i not in referenced]
    report = {"orphans": [(i, short(li_inner[i])) for i in orphans]}

    # first-appearance order of the survivors
    order = []
    for r in refs:
        if r[4] not in order:
            order.append(r[4])
    newnum = {t: str(i + 1) for i, t in enumerate(order)}

    # is the current numbering already right?
    cur_ok = all(r[5] == newnum[r[4]] for r in refs) and [i for i in li_ids if i in referenced] == order
    report["numbering_ok"] = cur_ok
    if not orphans:
        return None, report

    # --- integrity of the survivors' backrefs ---
    body_ids = set(RE_ID.findall(body_before)) | set(RE_ID.findall(body_after))
    idref_targets = {r[4] for r in refs if r[2] == "id"}
    for t in order:
        inner = li_inner[t]
        brs = list(RE_BACKREF.finditer(inner))
        if len(brs) != len(RE_ANY_BACKREF.findall(inner)):
            raise Skip(f"fn:{t} has a backref not in the standard form")
        if not brs:
            raise Skip(f"fn:{t} has no backref")
        for b in brs:
            if b.group("t") != t:
                raise Skip(f"fn:{t} backref points at #fnref{b.group('k')}:{b.group('t')}")
            if f"fnref{b.group('k')}:{t}" not in body_ids:
                raise Skip(f"fn:{t} backref #fnref{b.group('k')}:{t} has no target")
        if t not in idref_targets:
            raise Skip(f"fn:{t} is cited only by id-less <sup>s (hand fix needed)")

    # --- rebuild ---
    def fix_li(t):
        inner = RE_BACKREF.sub(
            lambda b: b.group(0).replace(
                f'title="Jump back to footnote {b.group("n")} in the text"',
                f'title="Jump back to footnote {newnum[t]} in the text"',
            ),
            li_inner[t],
        )
        return f'<li id="fn:{t}">{inner}</li>'

    new_ol = head_sep + joiner.join(fix_li(t) for t in order) + tail

    out = []
    pos = 0
    renumbered = 0
    for start, end, kind, k, t, n in refs:
        out.append(text[pos:start])
        old = text[start:end]
        new = old[: old.rfind(f">{n}</a></sup>")] + f">{newnum[t]}</a></sup>"
        if new != old:
            renumbered += 1
        out.append(new)
        pos = end
    out.append(text[pos:])
    rebuilt = "".join(out)
    # splice the new <ol> in: the refs never overlap the <ol>, so its offset only moves by
    # the length change of refs before it
    before_len_change = 0
    for start, end, kind, k, t, n in refs:
        if end <= ol_start:
            before_len_change += len(newnum[t]) - len(n)
    o0 = ol_start + before_len_change
    assert rebuilt[o0:o0 + len(ol)] == ol
    rebuilt = rebuilt[:o0] + new_ol + rebuilt[o0 + len(ol):]
    report["renumbered_refs"] = renumbered
    report["kept"] = len(order)
    report["moved_items"] = sum(1 for a, b in zip([i for i in li_ids if i in referenced], order) if a != b)
    return rebuilt, report


def crude_orphans(text):
    """For a skipped page: how many fn: ids have no href="#fn:id" anywhere outside their own <li>."""
    n = 0
    for m in RE_LI.finditer(text):
        rest = text[:m.start()] + text[m.end():]
        if f'href="#fn:{m.group("id")}"' not in rest:
            n += 1
    return n


def iter_html(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs.sort()
                for f in sorted(files):
                    if f.endswith(".html"):
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            yield p
        else:
            print(f"warning: no such path: {p}", file=sys.stderr)


def main(argv):
    dry = "--dry-run" in argv
    paths = [a for a in argv if not a.startswith("--")] or ["docs/doctrines"]
    n_pages = n_removed = 0
    skipped = []
    misnumbered = []
    for path in iter_html(paths):
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        try:
            new, rep = process(text)
        except Skip as e:
            skipped.append((path, f"{e} [{crude_orphans(text)} source(s) with no href to them]"))
            continue
        if rep is None:
            continue
        if new is None:
            if not rep["numbering_ok"]:
                misnumbered.append(path)
            continue
        n_pages += 1
        n_removed += len(rep["orphans"])
        print(f"{path}: remove {len(rep['orphans'])}, keep {rep['kept']}, "
              f"renumber {rep['renumbered_refs']} ref(s), reorder {rep['moved_items']} item(s)")
        for fid, desc in rep["orphans"]:
            print(f"    - fn:{fid}  {desc}")
        if not dry:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            # idempotence check
            again, rep2 = process(new)
            assert again is None and rep2["numbering_ok"], f"{path}: second pass not clean"
    for path, why in skipped:
        print(f"SKIPPED {path}: {why}")
    for path in misnumbered:
        print(f"NOTE {path}: no orphans, but numbering is not by first appearance (left alone)")
    verb = "would remove" if dry else "removed"
    print(f"Summary: {verb} {n_removed} orphan footnote(s) on {n_pages} page(s); "
          f"{len(skipped)} page(s) skipped; {len(misnumbered)} page(s) misnumbered without orphans.")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
