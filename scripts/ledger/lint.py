#!/usr/bin/env python3
"""Neutral-voice lint for the historical ledger (spec §6).

Usage: python3 -I scripts/ledger/lint.py [paths...]   (default: docs/)
Errors fail the run (exit 1). Warnings are printed for a human or agent to judge:
words like "contested" or "weak" have legitimate plain-English uses.
Text inside <blockquote>, <q> and HTML comments is exempt.
"""
import html
import os
import re
import sys

ERRORS = [
    (r"\(assessment:", "rating label"),
    (r"\bAssessment:", "rating label"),
    (r"granted-premise", "premise box"),
    (r"\bPresupposition:", "premise box"),
    (r"\bthis wiki (rates|holds|does not discount|judges|finds)", "self-reference as authority"),
    (r"<strong>\s*(sound|plausible|contested|weak|unsupported)\s*</strong>", "bold rating word"),
    (r"<h[2-4][^>]*>\s*(Adversarial assessment|What holds|What is overstated|Assessment)\b", "evaluative heading"),
    (r"\b(proves|refutes|debunks?|debunked)\b", "verdict verb"),
]
WARNINGS = [
    (r"\b(contested|weak|plausible|unsupported|verdict|overstat\w*|overread\w*|flagged|on balance|the stronger reading|the better reading|clearly)\b", "possible evaluative word"),
    (r"\bthe first [^.<]{0,60}\bto\b", "'the first … to' (prefer 'earliest extant')"),
    (r"\bscholars (agree|disagree)\b(?![^.]*<sup)", "unattributed 'scholars agree/disagree'"),
    (r"\b(heretic|heretical|orthodox)\b", "narrator label (allowed only when reporting a judgement)"),
]

EXEMPT = re.compile(r"<!--.*?-->|<blockquote\b.*?</blockquote>|<q\b.*?</q>", re.S | re.I)


HREF = re.compile(r'\b(href|src|id)="[^"]*"', re.I)


def strip_exempt(doc):
    # Replace exempt spans with same number of newlines so line numbers stay right.
    # Attribute values (filenames, anchors, ids) are not prose, so blank them too.
    doc = EXEMPT.sub(lambda m: "\n" * m.group(0).count("\n"), doc)
    return HREF.sub(lambda m: m.group(1) + '=""', doc)


def reading_balance(doc):
    secs = re.findall(r'<h2 class="reading"[^>]*>(.*?)</h2>(.*?)(?=<h2|\Z)', doc, re.S)
    if len(secs) < 2:
        return ["interpretation page has fewer than two readings"] if "arguments/" in doc_path_ctx[0] else []
    words = [len(re.sub(r"<[^>]+>", " ", body).split()) for _, body in secs]
    out = []
    if max(words) > 2 * max(1, min(words)):
        out.append(f"reading lengths unbalanced: {words}")
    for title, body in secs:
        if "Held by:" not in body:
            out.append(f"reading '{html.unescape(re.sub('<[^>]+>', '', title)).strip()}' has no 'Held by:' line")
    return out


doc_path_ctx = [""]


def lint_file(path):
    doc = open(path, encoding="utf-8").read()
    body = strip_exempt(doc)
    errs, warns = [], []
    for i, line in enumerate(body.split("\n"), 1):
        for pat, label in ERRORS:
            for m in re.finditer(pat, line, re.I):
                errs.append((i, label, m.group(0)))
        for pat, label in WARNINGS:
            for m in re.finditer(pat, line, re.I):
                warns.append((i, label, m.group(0)))
    if "/arguments/" in path:
        doc_path_ctx[0] = path
        for msg in reading_balance(doc):
            (errs if "fewer than two" in msg or "Held by" in msg else warns).append((0, "structure", msg))
    return errs, warns


def main(argv):
    paths = argv or ["docs"]
    files = []
    for p in paths:
        if os.path.isdir(p):
            for d, _, fs in os.walk(p):
                files += [os.path.join(d, f) for f in fs if f.endswith(".html")]
        else:
            files.append(p)
    n_err = n_warn = 0
    for f in sorted(files):
        errs, warns = lint_file(f)
        for i, label, txt in errs:
            print(f"ERROR {f}:{i}: {label}: {txt}")
        for i, label, txt in warns:
            print(f"warn  {f}:{i}: {label}: {txt}")
        n_err += len(errs)
        n_warn += len(warns)
    print(f"-- {len(files)} files, {n_err} errors, {n_warn} warnings")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
