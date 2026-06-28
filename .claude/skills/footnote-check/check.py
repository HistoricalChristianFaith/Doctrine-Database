#!/usr/bin/env python3
"""Footnote healthcheck for the Doctrine Across Time wiki.

Detection only — this script never edits a page. It sweeps the hand-authored
static HTML under docs/ and reports integrity problems in the footnote
apparatus (inline <sup id="fnref:X"><a href="#fn:X">N</a></sup> refs paired with
a bottom Sources <ol> of <li id="fn:X">…<a class="footnote-backref"
href="#fnref:X">). The AI driving the /footnote-check skill reads this report
and fixes the pages by hand.

Usage:
    python3 check.py [PATH ...]      # default: docs/
    python3 check.py --errors-only   # suppress warnings
    python3 check.py --quiet         # summary line only, no per-file detail

A PATH may be a file or a directory (recursed for *.html). Exit code is
non-zero iff any ERROR was found (warnings alone exit 0).

Checks
  ERROR E1  ref id != its own href target   (<sup id="fnref:X"> ... href="#fn:Y">, X!=Y)
  ERROR E2  dangling ref: target has no matching <li id="fn:..">
  ERROR E3  orphan source: <li id="fn:X"> has no inline ref pointing to it
  ERROR E4  duplicate source definition: two <li id="fn:X"> with same X
  ERROR E5  numbering: a source cited under two numbers, two sources sharing one
            number, or the numbers not forming a contiguous 1..N
  ERROR E6  broken intra-page anchor: href="#fn:.."/"#fnref:.." to a non-existent id
  ERROR E7  backref id mismatch: <li id="fn:X"> backref points to #fnref:Y, X!=Y
  WARN  W1  source <li> has no external source URL (only its backref / # fragments)
  WARN  W2  backref title "…footnote N…" where N != the source's number
"""

import os
import re
import sys

# --- markup patterns (the apparatus is machine-consistent; anchored regex is enough) ---
#
# Inline refs live in up to four parallel namespaces — fnref:, fnref2:, fnref3:,
# fnref4: — one per *occurrence* of the same source in the body (a source cited
# three times has fnref:X / fnref2:X / fnref3:X, each pointing at the one #fn:X,
# and the <li id="fn:X"> carries three backrefs). Sources are always one fn:
# namespace. The slug captured below is the part AFTER the fnref<N>: prefix, so
# fnref2:foo-3 and fnref:foo-3 both have slug "foo-3" — they're occurrences of the
# same footnote. (The malformed "-1b"/"-2c" *suffix* variants, by contrast, change
# the slug and so trip E1.)

# Inline ref: <sup id="fnref<N>:SLUG"> ... <a class="footnote-ref" href="#fn:TARGET">N</a> ... </sup>
RE_REF = re.compile(
    r'<sup\s+id="fnref\d*:(?P<id>[^"]+)"\s*>'
    r'(?P<inner>.*?)'
    r'</sup>',
    re.DOTALL,
)
RE_REF_A = re.compile(
    r'<a\s+class="footnote-ref"\s+href="#fn:(?P<target>[^"]+)"\s*>(?P<num>.*?)</a>',
    re.DOTALL,
)

# Source list item: <li id="fn:ID"> ... </li>
RE_FN_LI = re.compile(r'<li\s+id="fn:(?P<id>[^"]+)"\s*>(?P<inner>.*?)</li>', re.DOTALL)

# Backref inside a source item (any fnref<N>: namespace).
RE_BACKREF = re.compile(
    r'<a\s+class="footnote-backref"\s+href="#fnref\d*:(?P<target>[^"]+)"'
    r'(?:\s+title="(?P<title>[^"]*)")?',
    re.DOTALL,
)
RE_TITLE_NUM = re.compile(r'footnote\s+(\d+)\b')

# Any <a href> inside a source item (used to detect a real external source URL).
RE_ANY_A = re.compile(r'<a\s+[^>]*href="(?P<href>[^"]*)"', re.DOTALL | re.IGNORECASE)

# Any intra-page anchor reference anywhere on the page (all fnref<N>: namespaces).
RE_ANCHOR_REF = re.compile(r'href="#(fn:[^"]+|fnref\d*:[^"]+)"')

# All defined ids on the page (for broken-anchor detection).
RE_ANY_ID = re.compile(r'\bid="([^"]+)"')


def line_of(text, pos):
    """1-based line number of byte offset *pos*."""
    return text.count("\n", 0, pos) + 1


def strip_num(html):
    """Visible text of a ref number: drop tags/entities, keep digits."""
    txt = re.sub(r"<[^>]+>", "", html)
    return txt.strip()


class Finding:
    __slots__ = ("sev", "line", "code", "msg")

    def __init__(self, sev, line, code, msg):
        self.sev = sev  # "ERROR" | "WARN"
        self.line = line  # int or None
        self.code = code  # e.g. "E1"
        self.msg = msg


def check_page(path, text):
    """Return a list of Finding for one page."""
    findings = []

    # --- collect inline refs ---
    refs = []  # dicts: id, target (or None), num, line
    for m in RE_REF.finditer(text):
        rid = m.group("id")
        line = line_of(text, m.start())
        a = RE_REF_A.search(m.group("inner"))
        if a:
            target = a.group("target")
            num = strip_num(a.group("num"))
        else:
            target = None
            num = None
        refs.append({"id": rid, "target": target, "num": num, "line": line})

    # --- collect source items ---
    sources = []  # dicts: id, line, backref_target, backref_title, has_url
    fn_id_lines = {}  # id -> [lines] for duplicate detection
    for m in RE_FN_LI.finditer(text):
        fid = m.group("id")
        inner = m.group("inner")
        line = line_of(text, m.start())
        fn_id_lines.setdefault(fid, []).append(line)
        br = RE_BACKREF.search(inner)
        backref_target = br.group("target") if br else None
        backref_title = br.group("title") if br else None
        # an external source URL = any <a href> that isn't a # fragment
        has_url = any(
            not a.group("href").startswith("#") for a in RE_ANY_A.finditer(inner)
        )
        sources.append(
            {
                "id": fid,
                "line": line,
                "backref_target": backref_target,
                "backref_title": backref_title,
                "has_url": has_url,
            }
        )

    # Page with no apparatus at all -> nothing to validate.
    if not refs and not sources:
        return findings

    fn_ids = {s["id"] for s in sources}

    # --- E1: ref self-consistency (id == target) ---
    for r in refs:
        if r["target"] is None:
            findings.append(
                Finding("ERROR", r["line"], "E1",
                        f"fnref:{r['id']} has no inner footnote-ref <a href=\"#fn:..\">")
            )
        elif r["id"] != r["target"]:
            findings.append(
                Finding("ERROR", r["line"], "E1",
                        f"ref id≠href  fnref:{r['id']} → #fn:{r['target']}")
            )

    # --- E2: dangling ref (target missing from sources) ---
    for r in refs:
        t = r["target"]
        if t is not None and t not in fn_ids:
            findings.append(
                Finding("ERROR", r["line"], "E2",
                        f"dangling ref  fnref:{r['id']} → #fn:{t} (no such source)")
            )

    # --- E3: orphan source (defined but never referenced) ---
    referenced = {r["target"] for r in refs if r["target"] is not None}
    for s in sources:
        if s["id"] not in referenced:
            findings.append(
                Finding("ERROR", s["line"], "E3",
                        f"orphan source  fn:{s['id']} (no inline ref points to it)")
            )

    # --- E4: duplicate source definition ---
    for fid, lines in fn_id_lines.items():
        if len(lines) > 1:
            extra = ", ".join(f"L{l}" for l in lines[1:])
            findings.append(
                Finding("ERROR", lines[0], "E4",
                        f"duplicate source def  fn:{fid} (also at {extra})")
            )

    # --- E5: numbering. The visible number belongs to the SOURCE, not the order a
    # ref happens to appear in the body (the wiki numbers by Sources-list order, and
    # the same source cited twice legitimately shows one number twice). So the
    # invariant is a bijection: every ref to a source shows that source's one number,
    # distinct sources have distinct numbers, and the numbers form a contiguous 1..N.
    num_of = {}  # target -> the single visible number (str) it should carry
    for t in fn_ids:
        seen = {(r["num"], r["line"]) for r in refs if r["target"] == t and r["num"] is not None}
        nums = {n for n, _ in seen}
        if not nums:
            continue
        if len(nums) > 1:
            shown = "; ".join(f"\"{n}\"@L{l}" for n, l in sorted(seen, key=lambda x: x[1]))
            line = min(l for _, l in seen)
            findings.append(
                Finding("ERROR", line, "E5",
                        f"inconsistent number  #fn:{t} cited as {shown}")
            )
        num_of[t] = sorted(nums)[0]

    # collisions: one visible number used by two different sources
    by_num = {}
    for t, n in num_of.items():
        by_num.setdefault(n, []).append(t)
    for n, tgts in by_num.items():
        if len(tgts) > 1:
            line = min((r["line"] for r in refs if r["target"] in tgts), default=None)
            findings.append(
                Finding("ERROR", line, "E5",
                        f"number {n} used by {len(tgts)} sources: {', '.join('fn:' + t for t in sorted(tgts))}")
            )

    # contiguity: the distinct numbers should be exactly 1..N
    try:
        ints = sorted(int(n) for n in num_of.values())
    except ValueError:
        ints = None
    if ints is not None and ints and ints != list(range(1, len(ints) + 1)):
        have = set(ints)
        missing = [i for i in range(1, max(ints) + 1) if i not in have]
        gap = f"missing {missing}" if missing else f"runs 1..{max(ints)} with duplicates"
        findings.append(
            Finding("ERROR", None, "E5",
                    f"footnote numbers not contiguous 1..{len(ints)} ({gap})")
        )

    # --- E6: broken intra-page anchors (any href="#fn.."/"#fnref.." to a missing id) ---
    all_ids = set(RE_ANY_ID.findall(text))
    for m in RE_ANCHOR_REF.finditer(text):
        ref_id = m.group(1)  # e.g. "fn:foo-1" or "fnref:foo-1"
        if ref_id not in all_ids:
            findings.append(
                Finding("ERROR", line_of(text, m.start()), "E6",
                        f"broken anchor  href=\"#{ref_id}\" (no element with that id)")
            )

    # --- E7: backref self-consistency ---
    for s in sources:
        bt = s["backref_target"]
        if bt is None:
            findings.append(
                Finding("ERROR", s["line"], "E7",
                        f"fn:{s['id']} has no footnote-backref link")
            )
        elif bt != s["id"]:
            findings.append(
                Finding("ERROR", s["line"], "E7",
                        f"backref id≠  fn:{s['id']} → #fnref:{bt}")
            )

    # --- W1: source with no external URL ---
    for s in sources:
        if not s["has_url"]:
            findings.append(
                Finding("WARN", s["line"], "W1",
                        f"no source URL  fn:{s['id']}")
            )

    # --- W2: backref title number mismatch ---
    # The backref title ("Jump back to footnote N…") should name the source's number.
    for s in sources:
        if s["backref_title"] is None or s["id"] not in num_of:
            continue
        tm = RE_TITLE_NUM.search(s["backref_title"])
        if tm and tm.group(1) != num_of[s["id"]]:
            findings.append(
                Finding("WARN", s["line"], "W2",
                        f"backref title says footnote {tm.group(1)} but fn:{s['id']} is footnote {num_of[s['id']]}")
            )

    return findings


def iter_html(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                for f in sorted(files):
                    if f.endswith(".html"):
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            yield p
        else:
            print(f"warning: no such path: {p}", file=sys.stderr)


def main(argv):
    errors_only = "--errors-only" in argv
    quiet = "--quiet" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        paths = ["docs"]

    files = list(iter_html(paths))
    n_files = 0
    n_with_apparatus = 0
    files_with_errors = 0
    files_with_warnings = 0
    total_errors = 0
    total_warnings = 0

    for path in files:
        n_files += 1
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"warning: cannot read {path}: {e}", file=sys.stderr)
            continue

        findings = check_page(path, text)
        has_apparatus = ('id="fnref:' in text) or ('id="fn:' in text)
        if has_apparatus:
            n_with_apparatus += 1

        errs = [f for f in findings if f.sev == "ERROR"]
        warns = [f for f in findings if f.sev == "WARN"]
        if errs:
            files_with_errors += 1
        if warns:
            files_with_warnings += 1
        total_errors += len(errs)
        total_warnings += len(warns)

        shown = errs if errors_only else findings
        if not shown or quiet:
            continue

        # ERROR before WARN, then by line.
        shown.sort(key=lambda f: (0 if f.sev == "ERROR" else 1, f.line or 0))
        print(path)
        for f in shown:
            loc = f"L{f.line}" if f.line else "—"
            print(f"  {f.sev:<5} {loc:<7} {f.code}  {f.msg}")
        print()

    print(
        f"Summary: {n_files} files scanned ({n_with_apparatus} with footnotes), "
        f"{files_with_errors} with errors, {files_with_warnings} with warnings; "
        f"{total_errors} errors / {total_warnings} warnings total."
    )

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
