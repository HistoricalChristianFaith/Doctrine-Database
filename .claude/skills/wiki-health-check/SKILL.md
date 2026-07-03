---
name: wiki-health-check
description: Do a consistency-and-connections pass over the whole wiki — surface cross-page inconsistencies (contradictory facts/dates/ratings, stale cross-links, index-vs-summary drift, orphaned pages) and spot latent connections between pages worth teeing up as new research leads. Use when the user invokes /wiki-health-check, or asks for a wiki audit / consistency pass / "anything worth researching" sweep.
---

Do a health-check pass over the wiki: **find inconsistencies across pages**, and **spot connections
worth teeing up as new research leads**. This is a survey-and-report skill — it does *not* author
timeline/person/argument pages on the spot (that's what the leads are for), and it does *not* commit
unless the user asks. Its two deliverables are (1) a report of inconsistencies (with fixes proposed,
and mechanical ones optionally applied) and (2) new `todo/` files for the research leads it surfaces.

Ground everything in `CLAUDE.md` (the operating schema) — the checks below are all violations of, or
opportunities within, that schema.

## 0. Orient

Read the shape of the site before judging it:

- `docs/index.html` — the concept-family `<h2>` groups, each doctrine's `<h3>` block, its one-liner,
  and its arguments (grouped `<h4>` "Related arguments" clusters first, then standalone `<ul>`).
- Every `docs/doctrines/<slug>.html` summary — the intro, the `Related doctrines:` breadcrumb, the
  chronological witness blocks, and the "Arguments" section.
- Spot-read the person-detail and argument pages a check points you at (don't pre-read all of them).
- `people.md`, `log.md`, and `todo/` (existing leads — so you don't file a duplicate).

Fan this out with subagents (e.g. one per doctrine, or one per check category) when the site is large;
you keep the conclusions, not the file dumps.

## 1. Inconsistency checks (things that are *wrong* and should be reconciled)

Look for genuine cross-page contradictions and drift, not style nits:

- **Fact/date contradictions.** A person's `Dates: c. <year>` on their detail page vs. the year implied
  by their slot in the summary timeline (rule 1: earliest-first); a date or claim on a person page that
  contradicts `people.md` or the same person's page under another doctrine; a quote attributed
  differently in two places.
- **Assessment drift.** An argument's `assessment` on its own page vs. the `(assessment: <rating>)` label
  on the home summary, the `<strong>rating</strong>` on the index, and **every cross-doctrine cross-ref**
  to it. These must agree (or be deliberately *scoped* — see `steelman-framing` step 5). Grep each
  argument slug across `docs/` and compare the rating wherever it appears.
- **Index ↔ summary drift.** Every doctrine/argument on a summary should be surfaced on the index under
  the right family, and vice-versa; argument-group `<h4>` clusters and their order (groups first, then
  standalone) should match between index and summary; a new argument missing its index `<li>`.
- **Broken or stale cross-links.** Relative-link targets that don't resolve (wrong depth, renamed file,
  typo'd slug); `Related doctrines:` / `Related arguments:` breadcrumbs that aren't reciprocal (member A
  links B but B doesn't link A); a `DOCTRINE_NAMES` entry missing in `toc.js` for a doctrine (breadcrumb
  label gap); an argument group with fewer than 2 members actually present on a summary (rule 3).
- **Schema/plumbing leaks.** Reader-facing pages that name the source DBs as infrastructure, the meta
  files, or the `todo/` queue (hard rules 8–9); a summary claim without a footnote (rule 2). (Deep
  footnote-apparatus linting is `/footnote-check`'s job — flag obvious breaks here, defer the mechanical
  audit to that skill rather than duplicating it.)
- **Orphans.** A person/argument page not linked from any summary; a summary not reachable from the index.

For each finding: name the pages, quote the conflicting bits, say which is right (or that it needs
research), and propose the minimal fix. **Mechanical, unambiguous fixes** (a stale rating label, a
broken relative link, a missing `DOCTRINE_NAMES` entry, a non-reciprocal breadcrumb) you may apply
directly, respecting all hard rules (verbatim quotes, exact footnote markup, depth-relative links,
append-don't-overwrite) — then run `python3 .claude/skills/footnote-check/check.py <file>` on anything
touched. **Substantive fixes** (which of two dates is correct, whether a rating should change) become
research leads, not silent edits.

## 2. Connection checks (things worth *researching* — tee up as leads)

Hunt for latent structure the wiki hasn't yet captured:

- **Shared witnesses across doctrines.** A father who appears on doctrine A's timeline and is relevant to
  doctrine B but absent there — a lead to survey his corpus for B.
- **Shared proof-texts / mechanisms.** The same verse or the same interpretive move doing work in two
  doctrines or two arguments — a candidate **argument group** (≥2 members, one doctrine) or **doctrine
  cluster**, or a lead to check whether a witness on one applies to the other.
- **Ungrouped clusters.** Two+ existing argument pages under one doctrine sharing a proof-text/theme that
  aren't yet an argument group; two+ summaries sharing witnesses/texts not yet a doctrine cluster.
- **Thin or one-sided spots.** A doctrine with a lone early witness and a long silence; an argument rated
  without its strongest counter-witness considered; a `⚠ unverified` claim whose primary is locatable — a
  primary-hunt lead (rule 4).
- **Absent obvious voices.** A major father who *should* have said something on a doctrine and isn't
  there — a lead to check the Commentaries/Writings DBs (and the web) for him.

## 3. File the leads

Turn each connection/research item into a `todo/` file per `CLAUDE.md` ("Import X" conventions + hard
rules on `todo/`):

- One file per lead, named `YYYY-MM-DD-HHMM-<slug>.md` (real current date; stagger the `HHMM` so they
  sort). Get the timestamp from `date`.
- Say enough to be actioned cold: the pages that sparked it, the specific `(person/claim, source)` pair
  or the grouping/cluster hypothesis, **where to look** (verse URLs, `Commentaries-Database` /
  `Writings-Database` paths, or web), and the lead type (**primary-hunt** vs **argument** vs
  structural/grouping). Point at sources; **don't dictate the exact page edits** — the executing agent
  investigates and decides for itself (per the "Import X" rule).
- Check existing `todo/` files first so you don't duplicate a pending lead.

## 4. Report

Give the user a tight summary, not a wall of text:

- **Inconsistencies** — grouped by severity, each with the pages, the conflict, and whether you *fixed it*
  (mechanical) or *filed it* (substantive). List every file you edited.
- **Connections / leads filed** — each new `todo/` file with a one-line hook.
- **Judgment calls** — anything ambiguous you want the user to weigh in on.

Don't commit unless asked. If you applied mechanical fixes, note that `log.md` should get an entry (append
one per rule 7 if you made real edits; skip it for a pure read-only report).
