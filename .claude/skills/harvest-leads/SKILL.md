---
name: harvest-leads
description: Scan one already-researched area of the wiki (a doctrine slug, a concept-family, or a person) and spin up new todo/ research leads for the connections and unturned stones that the existing research surfaced but never queued. Use when the user invokes /harvest-leads <area>, or asks to harvest / spin up / generate follow-on research leads for a specific doctrine or area.
---

Take **one area** the user names — a doctrine slug (`balaam`), a concept-family (`family-primeval` /
"Primeval history"), or a person (`ambrose-of-milan`) — and **scan the whole of it** to harvest new
`todo/` research leads: the connections, absent voices, ungrouped clusters, and unturned stones that the
*existing* research on that area opened up but nobody queued. Research tends to finish a lead without
spinning up the follow-ons it exposed; this skill closes that gap for one area at a time.

This is a **generative, scoped** skill, deliberately different from `/wiki-health-check`:

- **Scope is the area the user passes, not the whole wiki.** You go *deep* on one patch, not broad across
  all of `docs/`. Don't wander outside the area except to check whether a lead already exists elsewhere.
- **It scans the whole area, not "recent" work.** There is no recency filter — read the area's pages as
  they stand today and ask "what did all this research open up?" regardless of when it was done.
- **The only deliverable is new `todo/` files** (plus a short report). It does **not** author or edit
  timeline/person/argument pages, does **not** fix inconsistencies (that's `/wiki-health-check`), and does
  **not** commit. It mines for leads, drops one file per lead, and stops — the "Import X" discipline.

Ground everything in `CLAUDE.md` (the operating schema): every lead is an opportunity *within* that schema
(a missing witness, an ungrouped argument group, a locatable primary, an unadjudicated sub-claim).

## 1. Resolve the area

Figure out what the argument names and gather the pages in scope:

- **Doctrine slug** (`balaam`) → its summary `docs/doctrines/<slug>.html`, every person-detail and argument
  page under `docs/doctrines/<slug>/`, and its `<h3>` block on the index.
- **Concept-family** (a family name or `family-<slug>`) → every doctrine `<h3>` under that family's `<h2>`
  on the index, and each of those doctrines' summaries (spot-read their sub-pages as leads point you at
  them). A family-level scan leans toward *cross-doctrine* leads (clusters, shared witnesses).
- **Person** (`ambrose-of-milan`) → every person-detail page with that slug across all doctrines
  (`docs/doctrines/*/<person>.html`), plus that person's entries in `people.md`. A person-level scan leans
  toward "where else should this witness appear?" leads.

If the argument is ambiguous or matches nothing, say so and ask which the user meant rather than guessing.

Read the pages in scope fully — you are going deep on a small set. Fan out with subagents (e.g. one per
sub-page) only if the area is large; you keep the conclusions, not the file dumps.

## 2. Harvest the leads

Hunt for latent structure and unfinished threads the existing research exposed. Categories to sweep:

- **Absent obvious voices.** A father who *should* have weighed in on this doctrine and isn't on the
  timeline — a lead to survey the Commentaries/Writings DBs (and the web) for him. On a person scan: a
  doctrine this witness plainly touches but where his page is missing.
- **Shared witnesses across doctrines.** Someone on this area's timeline who is relevant to a neighbouring
  doctrine but absent there — a lead to survey his corpus for it.
- **Shared proof-texts / mechanisms.** The same verse or interpretive move doing work in two pages here —
  a candidate **argument group** (≥2 members, one doctrine) or **doctrine cluster**, or a lead to test
  whether a witness on one applies to the other.
- **Ungrouped clusters.** Two+ existing argument pages under this doctrine sharing a proof-text/theme not
  yet made an argument group; two+ summaries in the family sharing witnesses/texts not yet a cluster.
- **Unadjudicated sub-claims.** A claim asserted in prose on a summary or person page that is really an
  **argument** (interest = "does it hold?") and deserves its own rated page.
- **Locatable primaries.** A `⚠ unverified` claim whose primary source looks findable — a **primary-hunt**
  lead (rule 4).
- **Thin or one-sided spots.** A lone early witness and a long silence; a transmission link asserted at
  both ends but never traced through the middle (e.g. a tradition present in an early source *and* a late
  one, with the intervening carriers unqueried); an argument rated without its strongest counter-witness.
- **Unfinished threads the pages themselves flag.** Prose that says "beyond our scope," "not pursued
  here," "a separate question," or names a work/figure it doesn't chase — each is a lead sitting in plain
  sight.

## 3. The quality bar (non-negotiable — this is what keeps it from being lead-spam)

A candidate is only worth a file if it is **specific and actionable cold**. Before you write one, it must
clear all three:

1. **Named target.** It names a specific `(person/claim, plausible source)` pair, a specific
   sub-claim to adjudicate, or a specific grouping/cluster hypothesis with its ≥2 named members. "Explore
   the reception of X," "research more on Y," or "consider whether Z is relevant" is **not** a lead — cut it.
2. **A place to look.** You can point the executing agent at where to start: a father/work in the
   Commentaries/Writings DBs, key verse URL(s), a named external work, or the specific pages to wire
   together. A lead with no "where to look" is a wish, not a lead.
3. **Not already covered.** It is not already a pending file in `todo/`, and the page/argument/group it
   proposes does not already exist. **Check both before writing:** glob `todo/*.md` for the slug/theme, and
   check `docs/` for an existing page or an already-rendered group/cluster. Re-proposing existing work is
   the main failure mode of this skill — guard against it every time.

When in doubt, cut. A short list of sharp, actionable leads is the goal; a long list of vague ones poisons
the queue that `/next` grinds through.

## 4. File the leads

For each survivor, drop a `todo/` file per `CLAUDE.md` + `todo/README.md`:

- One file per lead, named `YYYY-MM-DD-HHMM-<slug>.md`. Use the **real current date** (get it from `date`)
  and stagger the `HHMM` so the files sort distinctly.
- Follow the body template in `todo/README.md`: `# <short title>` then `**Doctrine:**`, `**Type:**`
  (primary-hunt | argument | structural), `**Claim/lead:**`, `**Source it came from:**`, `**Next action:**`.
- Make it **self-contained** — actionable without re-reading this area. Name the pages that sparked it, the
  specific target, and **where to look** (verse URLs, `Commentaries-Database` / `Writings-Database` paths,
  or a web source). For `**Source it came from:**` write `harvest-leads scan of <area> <date>`.
- **Point at sources; don't dictate the exact page edits.** Per the "Import X" rule, the executing agent
  investigates the sources and the current state of the wiki and decides for itself what to author — make
  clear that's its job, don't pre-write the edits.

## 5. Report

Give the user a tight summary, not a wall of text:

- **Area scanned** and how many pages were in scope.
- **Leads filed** — each new `todo/` file with a one-line hook and its type.
- **Considered but cut** — a brief note on strong-looking candidates you dropped for the quality bar
  (already covered, too vague), so the user sees the area was swept, not skimmed.
- **Judgment calls** — anything ambiguous you want the user to weigh in on.

Do **not** author pages, and do **not** commit — filing the leads is the whole job. (`todo/` is git-ignored,
so the new files won't show in `git status`; that's expected.)
