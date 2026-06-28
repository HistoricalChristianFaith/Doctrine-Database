---
name: footnote-check
description: Healthcheck the footnote apparatus on the wiki's pages — runs a deterministic checker over docs/ (inline fnref ↔ Sources fn pairing, numbering, hrefs, backrefs, source URLs), then fixes the flagged defects by hand. Use when the user invokes /footnote-check, or asks to lint/healthcheck/audit footnotes or find broken footnote links.
---

Lint and repair the footnote apparatus on the static HTML pages under `docs/`.

Division of labour: a deterministic Python checker **detects** problems (it never edits a page); **you
interpret the findings and fix the pages by hand**, then re-run the checker to confirm each page is
clean. The script is the eyes; you are the hands.

## 1. Detect

Run the checker (stdlib Python, no deps):

```
python3 .claude/skills/footnote-check/check.py [PATH]
```

- **No argument** → sweeps all of `docs/` (the default full health pass; ~225 pages with footnotes,
  runs in well under a second).
- **A slug** like `ot-canon` → resolve it to `docs/doctrines/ot-canon.html` and pass that.
- **A path** (file or directory) → passed through as-is. Flags: `--errors-only`, `--quiet`.

It prints findings grouped by file with `Lnnn` line numbers and an `Exxx`/`Wxxx` code, then a summary
line, and exits non-zero iff any **error** was found. Read the report.

What the codes mean:

| code | severity | meaning |
|------|----------|---------|
| **E1** | error | an inline `<sup id="fnref…:X">` whose inner `href="#fn:Y"` has `X ≠ Y` (the id and its target disagree) |
| **E2** | error | an inline ref points at `#fn:X` but there is no `<li id="fn:X">` |
| **E3** | error | a source `<li id="fn:X">` that no inline ref points at (orphan) |
| **E4** | error | two `<li id="fn:X">` with the same id (duplicate source definition) |
| **E5** | error | numbering: a source cited under two different visible numbers, two sources sharing one number, or the numbers not forming a contiguous `1..N` |
| **E6** | error | a `href="#fn:…"`/`href="#fnref…:…"` anchor whose id doesn't exist on the page |
| **E7** | error | a source `<li id="fn:X">`'s backref points to `#fnref…:Y` with `X ≠ Y` |
| **W1** | warn | a source `<li>` with no external source URL (only its backref / `#` fragments) — wants a real link per the wiki's rule 10 |
| **W2** | warn | a backref `title="… footnote N …"` whose N disagrees with the source's actual number |

Conventions the checker already understands (so it does **not** flag them):
- **Repeat-citation namespaces** `fnref:` / `fnref2:` / `fnref3:` / `fnref4:` — the *correct* way to
  cite one source several times: each occurrence is `fnref<n>:X` pointing at the one `#fn:X`, and the
  `<li id="fn:X">` carries one backref per occurrence. Same slug `X` across them ⇒ no E1.
- **Numbering by Sources-list order** rather than strict body order — fine, as long as each source has
  one consistent number and the set is contiguous `1..N`.

## 2. Triage & fix (you do the editing — never the script)

For each finding, open the page, read the surrounding markup to understand the *intended* footnote,
and correct it by hand. The right fix depends on intent, so use judgment:

- **E1 / E7 malformed reuse** — the common `…-1b` / `…-2c` *suffix* ids (e.g.
  `fnref:gregory-naz-1b → #fn:gregory-naz-1`) are a botched second citation of one source. Normalise to
  the real convention: make the second occurrence `fnref2:<slug>` (third `fnref3:`, …) of the **same**
  slug, pointing at the same `#fn:<slug>`, and give the `<li id="fn:<slug>">` an extra backref to it.
  A cross-namespace pair like `fnref:…-sum-N ↔ fn:…-N` is the same problem — realign both sides to one
  slug. If context shows a genuinely *new* source was meant, instead add the missing `<li id="fn:…">`
  and fix the href.
- **E2 / E6 dangling ref or broken anchor** — either the source `<li>` is missing (add it) or the
  href has a typo (point it at the source that exists). Decide from context.
- **E3 orphan source** — either an inline ref was dropped (restore it) or the source is dead (remove
  the `<li>`); re-sequence afterwards.
- **E4 duplicate definition** — merge the two `<li>` into one (keep the fuller citation), and make sure
  every backref/number still resolves.
- **E5 numbering** — fix so each source shows one number, numbers are unique across sources, and run
  `1..N`. Renumbering **cascades**: visible `<n>`, the `<li>` order, and every backref `title` move
  together — re-sequence the whole page, don't patch one number.
- **W1 missing source URL** — link the actual edition/work if you can find it quickly (prefer a stable,
  specific URL). If it needs real research, **leave the claim and surface it to the user** — never
  fabricate a link (rule 10). A bare bibliographic citation is the only acceptable URL-less form.
- **W2 backref title** — mechanical: set the title number to the source's real number.

Respect the wiki's hard rules while editing (verbatim quotes inside `<blockquote>`, append-don't-
overwrite, depth-relative links, etc. — see `CLAUDE.md`).

## 3. Verify

Re-run the checker on the same path and iterate until it exits clean (0 errors). Then report, per
file, what you changed, and explicitly flag anything you deliberately left for the user (e.g. a W1
needing a source). When a finding's correct fix is genuinely ambiguous, **surface it — don't guess.**

This skill only edits when it is repairing a flagged defect; it does not otherwise touch pages, and it
does not commit (leave that to the user unless they ask).
