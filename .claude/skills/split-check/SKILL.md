---
name: split-check
description: Audit argument pages against CLAUDE.md's "one advocated claim per page — split rivals, fold defeaters" rule — flag pages that bury an independently-advocated rival (should split out), standalone pages that are really just defeaters with no proponent (should fold back in), and dual-panel "contested" pages hosting two advocated readings (should split into two). Use when the user invokes /split-check, or asks to check/audit argument-page decomposition, or whether any pages need splitting/folding in light of the split-rivals-fold-defeaters rule.
---

Run a **decomposition audit** over the wiki's argument pages against the `CLAUDE.md` rule (under
**Assessments → "One advocated claim per page — split rivals, fold defeaters"**):

> An argument page states **one** advocated interpretation in steelman form, with the counterpoints *to
> its own evidence* folded in and one `assessment`. A counter-position gets its **own** page when it is
> *independently advocated* (named proponents + its own proof-texts); it is **folded in** when it is a
> mere *defeater* — a limit on the evidence nobody holds as a positive thesis. Trigger = "**is it
> advocated?**", not "is it correct?" (a popular-but-failing argument still earns its own rated page).
> Two genuinely-advocated rival readings → **two advocacy pages**, grouped + cross-linked, not one
> dual-panel page.

This is a **report-first** skill. It classifies pages and proposes the fix; it does **not** silently
restructure — splitting/folding an argument page is substantive (new files, re-grouping, re-footnoting,
index/summary/cross-ref propagation). What happens **after approval depends on scope**:

- **whole-wiki or doctrine scope** → approved findings are **teed up as `todo/` leads only, never executed
  inline** (§3). A wide sweep can surface many restructures; the queue lets each be actioned and reviewed
  on its own (via `/next`).
- **single-page scope** → approved fix is **executed inline** in the same run (§4).

It does not commit unless asked.

**Calibration.** The `perpetual-virginity` argument set is the model of a **compliant** decomposition
(the Helvidian and Epiphanian rival readings each get their own advocacy page; the *suggenēs* defeater
earns a page because Svendsen/White press it). `mary-new-eve`'s `christology-vs-mariology` is the known
**dual-panel** case (two advocated readings — Christological-only vs. implicit-Marian — in one page).
Use these as your yardsticks.

## Parameter — scope

`$ARGUMENTS` sets the scope; default is the whole wiki.

- **empty** → audit **every** argument page under `docs/doctrines/*/arguments/`. Fan out with subagents
  (one per doctrine) when large; you keep the classifications, not the file dumps.
- **a doctrine slug** (`perpetual-virginity`) → just that doctrine's argument set.
- **a single argument page** (slug / doctrine-qualified slug / full path) → audit that one page and, if
  the user approves, **execute** its fix in the same run (the steelman-framing pattern).

## 0. Orient

- Re-read the rule in `CLAUDE.md` (quoted above) and the **Argument groups** section — a split usually
  creates or grows an argument group (`<h3 id="group-…">` on the summary, `<h4>` on the index,
  `Related arguments:` breadcrumbs); a fold may shrink one below its 2-member minimum (rules 1 & 3 there).
- For each page in scope read its `<h1>`/`Assessment:` line, its **"Who advances it"** section, and its
  **"Adversarial assessment" / counterpoint** sections — that's where the buried rivals and the
  no-proponent defeaters show up.

## 1. The three failure modes (with detection heuristics)

**(a) Under-split — a rival is buried.** The page folds in a counter-position that is *independently
advocated*. Tells: the counterpoint section **names a proponent or camp** who holds the opposing view as
a *positive thesis* (not just "critics object"); the counter-position could stand as its own titled
question (`Does X?`) with its **own evidence-for section and proof-texts**; the page's own `assessment`
is quietly doing double duty (rating both a claim and its live rival). → **Split** the rival out into its
own advocacy page, rate it on its own, group + cross-link the two.

**(b) Over-split — a defeater is masquerading as a thesis.** A *standalone* argument page whose "claim"
is really a limit on someone else's evidence, held by no one as a positive position. Tells: a **thin or
absent "Who advances it"** (no named proponent, or only "some object that…"); a purely **negative** claim
(`X does not follow`, `Y fails to prove Z`) that exists only to rebut another page; a **sub-variant** that
merely refines another page's proof-text without an independent champion. → **Fold** it back into the page
it defeats (as a counterpoint in that page's adversarial section), delete the file, de-group if needed.
*Guard:* "advocated ≠ correct" — a page can be rated `weak`/`unsupported` and still legitimately stand
alone **if it has real proponents** (the *suggenēs* page is the paradigm: weak, but Svendsen/White press
it). Weakness alone is **never** grounds to fold; absence of a proponent is.

**(c) Dual-panel — two advocated readings in one page.** A single page with two parallel "evidence for A
/ evidence for B" panels, two named camps, usually rated `contested` (the `christology-vs-mariology`
shape). → Candidate to **split into two advocacy pages**, each rated on its own, grouped + cross-linked
(the Helvidian/Epiphanian precedent). *Judgment call:* if the two readings share **all** the same
evidence and differ only in how they read it — so two pages would just mirror each other — a single
`contested` page may be correct. Split when each side has its **own** distinct positive case; flag
borderline ones to the user rather than splitting mechanically.

## 2. Classify

Sort every in-scope page into: **compliant** · **under-split (a)** · **over-split (b)** · **dual-panel
(c)** · **borderline (judgment call)**. For each non-compliant page record: the pages/sections involved,
which counterpoint or panel is the offending rival/defeater, whether it has a **named proponent** (the
deciding fact), and the proposed decomposition (split into `<new-slug>` / fold into `<target>`). Note
whether the fix creates, grows, or shrinks an **argument group**.

## 3. Report

Give the user a tight, ranked list — clearest violations first:

- **Under-split** — page, the buried rival, its proponent, proposed new page slug + group.
- **Over-split** — page, why it has no independent proponent, the fold-in target.
- **Dual-panel** — page, the two readings + camps, proposed two-page split (or why it should stay).
- **Borderline** — the call you couldn't make alone, framed for a yes/no.

Don't execute yet — ask which findings to proceed with. Then fork by scope:

- **Whole-wiki / doctrine scope** → for each approved finding, **file one structural `todo/` lead** (per
  `CLAUDE.md` "Import X" + `todo/` rules) and **stop there — never restructure inline**. Each lead:
  `YYYY-MM-DD-HHMM-<slug>.md` (real timestamp from `date`; stagger `HHMM` so they sort); enough context to
  action cold — the pages/sections involved, the offending rival/defeater, the **proponent-test result**
  (the deciding fact), the proposed decomposition (split into `<new-slug>` / fold into `<target>`) and its
  argument-group impact, and where the sources live. Point at the pages/sources; **don't dictate the exact
  edits** — the executing agent (`/next`) investigates and decides. Check existing `todo/` files first so
  you don't duplicate a pending lead.
- **Single-page scope** → offer to **execute the fix inline now** (§4).

## 4. Execute inline — single-page scope only (on approval)

Reached **only** when the skill was invoked on one named page and the user approved the fix. Whole-wiki
and doctrine sweeps never get here — their approved findings become `todo/` leads in §3.

**Splitting out a rival / a dual panel:**

1. **Author the new advocacy page** — `docs/doctrines/<doctrine>/arguments/<new-slug>.html` from
   [`templates/argument.html`](../../../templates/argument.html): title it for the *interpretation* (not
   the proponent), state the one claim, its strongest evidence, the counterpoints *to that evidence*
   folded in, and its own `Assessment:` line + `Assessment` section. Verbatim quotes in `<blockquote>`
   (hard rule 3); exact footnote markup with `<new-slug>` ids; link every source you have a URL for
   (rule 10). Steelman it per `CLAUDE.md` (this often pairs with `/steelman-framing`).
2. **Trim the origin page** — remove the extracted rival's positive case, leaving (where apt) a one-line
   `see also` to the new page; re-sequence its footnotes (sequential by first appearance) and drop now-orphaned `<li>`s.
3. **Wire the argument group** (the two are now ≥2 related): add/extend the `<h3 id="group-<slug>">`
   `Related arguments — <theme>` block on the **summary**, the `<h4>` bare-theme group on the **index**,
   and a `Related arguments:` breadcrumb on **each** member linking the summary anchor + siblings (per the
   **Argument groups** section — groups lead the doctrine's arguments on summary and index alike).
4. **Surface the new page** — its `<h3>`/`<h4>` heading + blurb + `(assessment: <rating>)` on the summary
   (with a Sources footnote), and its `<li> … — <strong>rating</strong>` on the index under the right family.

**Folding a defeater back in:**

1. **Merge** its substantive counterpoint into the target page's adversarial section (as prose, not a new
   thesis), carrying any unique sources into the target's Sources block; re-sequence the target's footnotes.
2. **Delete** the folded page's file.
3. **De-surface it** everywhere: remove its summary heading/blurb/footnote, its index `<li>`, and every
   `Related arguments:` breadcrumb / `see also` / cross-doctrine cross-ref pointing at it (grep the slug
   across `docs/` first). If its group now has **< 2 members**, dissolve the group (demote the lone
   survivor back to a flat `<h3>`/`<ul>`, drop the group heading + breadcrumbs) per Argument-groups rule 1.

**Both paths, always:**

- Keep ratings coherent across **all** surfaces (page ↔ summary ↔ index ↔ every cross-ref) — the
  assessment-drift check in `/wiki-health-check` step 1 applies; scope a cross-ref label when a sibling
  rates a neighbouring claim differently, don't blind-swap the word.
- Run the footnote healthcheck on **every** file touched and fix to clean:
  `python3 .claude/skills/footnote-check/check.py <files>` (use the `fnref2:`/`fnref3:` namespace for
  repeat citations; no duplicate ids).
- **`log.md`** — append a dated entry (real current date, hard rule 7): the pages split/folded, the
  proponent-test that decided it, the group changes, and every file touched. Don't commit unless asked.

Respect all `CLAUDE.md` hard rules throughout (no internal plumbing on reader-facing pages, verbatim
quotes, depth-relative links, append-don't-overwrite, a footnote on every summary claim).
