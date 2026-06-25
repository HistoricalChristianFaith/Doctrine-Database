# CLAUDE.md — operating schema for the Doctrine Across Time wiki

This is the terse, load-every-session rule sheet. For the full concept and rationale, read
[`project.md`](project.md) once.

## What this wiki is
For each Christian **doctrine**, a timeline page showing how belief developed across time,
**earliest person first**, where **every claim is footnoted to a source**. The wiki is a set of
**hand-authored static HTML files** under `docs/`, served as-is by GitHub Pages (no build step,
no Markdown, no Jekyll). You edit the `.html` directly.

## Layout
```
docs/                          the published site (GitHub Pages source = /docs)
  index.html                   the reader's home page: doctrine summaries + the cruxes catalog
                                 (NOT a person-page list — witnesses are cataloged on their timeline)
  .nojekyll                    serve raw HTML; do not Jekyll-process
  doctrines/<slug>.html              summary timeline (1 footnoted block/person)
  doctrines/<slug>/<person>.html     detail page (full quotes + context + links)
  doctrines/<slug>/arguments/<arg>.html   argument/crux page (one sub-claim → assessment; OFF-timeline)

project.md   full brief        CLAUDE.md   this file        templates/   HTML page skeletons
log.md       append-only history            TODO.md     pending-leads queue (pending only)
people.md    non-DB people dates/slugs       llm-wiki.md  the general pattern
```
Meta files (this file, `project.md`, `log.md`, `TODO.md`, `people.md`, `templates/`, `README.md`)
live at the repo root and are **not** part of the published site — only `docs/` is served.

Three page types: **doctrine** (summary timeline), **person-doctrine** (a witness's detail page,
slotted on the timeline by year), and **argument** (a single sub-claim adduced for a reading —
proof-text, parallel, or historical thesis — weighed adversarially and given an `assessment` of the
*interpretation* it serves; it cuts *across* the timeline, so it lives in the summary's "Arguments &
cruxes" section, **not** the chronological list, and has no year). Two or more argument pages that share
a proof-text, mechanism, or theme may be grouped into a named **complex** — a grouping convention
realized in visible content (a sub-heading on the summary + index and a `Related cruxes:` breadcrumb on
each member), **not** a fourth page type and **not** a new file. ("Complex" is the internal term only;
the reader-facing label is **"Related cruxes"**.) See "Complexes" under Assessments below.

## Source databases (prefer over web, but still use web)
- `~/Desktop/Commentaries-Database/<Father>/<Book Ch_Vs>.toml` → `[[commentary]]` blocks
  (`quote`, `source_url`, `source_title`). Verse-oriented.
  - ⚠ A verse may live in a **range-named** file (`Book 3_18-19.toml`), not just `Book 3_19.toml`.
    To survey a verse, glob the range too (e.g. `*/"1 Peter 3_1*.toml"`) — exact-name globbing undercounts.
- `~/Desktop/Writings-Database/<Father>/<Work>.html` → full texts; `metadata.toml` has
  `default_year` (timeline anchor) + `wiki`.
- Verse URL: `https://historicalchristian.faith/<book>/<ch>/<vs>` (book = lowercased, no spaces).
- Work URL: `https://historicalchristian.faith/by_father.php?file=<Father>%2F<Work>.html`
  → maps to `Writings-Database/<Father>/<Work>.html` (decode `%2F`→`/`, `%2520`→space).
  - ⚠ **Read the text from the local `Writings-Database` file, never by fetching this URL** (the
    `by_father.php` page doesn't serve the work body to a fetcher). The URL exists only so published
    pages can *link* a local source we can't otherwise hyperlink — build it from the local path.
- Book name spellings: `Commentaries-Database/book_names.json`.
- **Work outside our corpus?** (e.g. a father's work absent from `Writings-Database`) — **search the web
  for it** rather than dropping it as an "open lead"; cite the online source on the page like any other
  (don't tell the reader it's "outside our corpus" — that's internal, not reader-facing).
- **Source-DB gaps → open a GitHub issue.** When research surfaces a fixable gap in the upstream repos —
  a missing work in [`Writings-Database`](https://github.com/HistoricalChristianFaith/Writings-Database),
  a missing import/verse in [`Commentaries-Database`](https://github.com/HistoricalChristianFaith/Commentaries-Database),
  or an OCR/transcription error in either — **file a concise issue on that repo** (`gh issue create`)
  describing the gap and (if known) the correct source/text. Keep doing the wiki work from the web in the
  meantime; the issue just flags the upstream fix.

## HTML conventions
- **Document wrapper** (every page): copy the skeletons in [`templates/`](templates/).
  ```html
  <!doctype html>
  <html lang="en">
  <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><Page title></title>
  <link rel="stylesheet" href="<…/>style.css">
  <script defer src="<…/>toc.js"></script>
  </head>
  <body>
  …
  </body>
  </html>
  ```
  Both the `<link>` href and the `<script src>` are **depth-relative** to `docs/`: `style.css`/`toc.js`
  (index), `../` (summary), `../../` (person-detail), `../../../` (argument). Root-absolute `/style.css`
  would break — the site is published under `…github.io/Doctrine-Database/`.
- **One shared stylesheet** — `docs/style.css`, a single dark, minimal sheet (constrained reading
  column, default serif fonts, styled links/quotes/footnotes). Every page links it (see wrapper
  above). No per-page CSS — keep styling in that one file.
- **One shared script** — `docs/toc.js`, the only JS on the site. Every page loads it (`<script defer
  src="<…/>toc.js">` in the wrapper); it builds a collapsible, Wikipedia-style **table of contents**
  from the page's `h2`–`h4` at view time (skips the `h1` and `Sources`; bails on pages with < 3
  headings) and floats it in the left gutter on wide viewports, scroll-spy included. The TOC is
  generated, **not** authored into the HTML — write normal headings and it appears. TOC styling lives
  in `style.css` (the `.toc*` rules). Keep JS in this one file unless asked otherwise.
- **Metadata is path- and content-derived, not hidden frontmatter:**
  - *type* ← the path; *doctrine slug* ← the path; *person-slug* ← the filename.
  - *year* (for ordering) ← the visible `<strong>Dates:</strong> c. <year>` line on the person page;
    the summary timeline order is maintained **by hand**.
  - *verified?* ← presence/absence of `⚠ unverified` markers on claims (the index does not track this).
  - *assessment* (argument) ← the visible `<strong>Assessment:</strong> …` line.
  - history/recency ← [`log.md`](log.md) (there is no per-page `updated` field).
- **Cross-links are relative `.html`:** summary→detail `<slug>/<person>.html`; detail→summary
  `../<slug>.html`; argument→detail `../<person>.html`; argument→summary `../../<slug>.html`.
  Members of a **complex** are additionally grouped under a shared `<h3 id="complex-<slug>">` heading on
  the summary and an `<h4>` group in the index (both labelled `Related cruxes — <theme>`), and each member
  page carries a `Related cruxes:` breadcrumb linking the home-summary anchor
  (`../../<slug>.html#complex-<slug>`) and its sibling members.
- **Footnotes** use this exact markup (matches every existing page) so numbering and back-links work:
  - Inline ref (visible `<n>` is sequential **by first appearance** on the page; the id uses the
    person-slug): `<sup id="fnref:<person-slug>-1"><a class="footnote-ref" href="#fn:<person-slug>-1">1</a></sup>`
  - Sources block at the bottom of the page (one `<li>` per note, ordered by first appearance):
    ```html
    <h2>Sources</h2>
    <div class="footnote">
    <hr>
    <ol>
    <li id="fn:<person-slug>-1">
    <p><a href="<source URL>">source title</a>&#160;<a class="footnote-backref" href="#fnref:<person-slug>-1" title="Jump back to footnote 1 in the text">&#8617;</a></p>
    </li>
    </ol>
    </div>
    ```

## Hard rules
1. Summary pages list people **earliest year first** (order maintained by hand on insert).
2. **Every** claim on a summary page ends in a footnote (the `<sup>` markup above).
3. Quotes on detail pages are **verbatim** — never paraphrase inside `<blockquote>`.
4. Firsthand quote found → cite the primary URL (page counts as *verified*). Only a secondary
   report → mark the claim `⚠ unverified` inline, cite the secondary work, add a `TODO.md` row.
5. `person-slug` = lowercased full name, spaces→hyphens (mirrors the `Writings-Database` folder)
   and is the page's filename.
6. Appending to an existing detail page → **append/merge**, don't overwrite.
7. Use the real current date for `log.md` entries.
8. **Never mention `TODO.md` in a published page** (summary / person-detail / argument) — it's
   internal bookkeeping. On the page, mark an unsourced claim `⚠ unverified` (or call it an "open
   lead" / "not yet sourced") and cite the secondary work only; still add the backlog row per
   rule 4. Referencing `TODO.md` is fine only in meta files (this file, `project.md`, `log.md`).

## Importing & the TODO queue
- **`TODO.md` is a queue of not-yet-executed leads — pending items only.** It never holds
  "done"/"resolved" entries: when a lead is executed, **delete its row** and record the outcome in
  `log.md` (that is the history). Process rows **one at a time, top-down**; each row must carry enough
  context to be actioned without re-reading the source it came from.
- **"Import X"** (X = a local file or URL) means **extract every lead from X and add a row to
  `TODO.md` for each** — it is *not* a request to author pages on the spot. Mine X for
  `(person/claim, source)` pairs and open cruxes, queue them below, then stop. The leads get
  processed one-by-one in later passes (or when the user says to work the queue).
- Two row types: **primary-hunt** (a secondhand claim needing a primary located in the DBs → resolve
  per rule 4) and **crux** (a sub-claim needing adversarial adjudication → resolve into an argument
  page with an `assessment`). Both end the same way: execute, then delete the row + log it.

## Authoring checklist (see project.md §7 for detail)
1. Identify doctrine(s) + slug + key verses; extract every `(person, claim)`.
2. Date each person (DB `metadata.toml` `default_year`, or research → `people.md`).
3. Verify each claim against the DBs (commentary files by key verse / writings HTML).
4. Write/append the person-detail page `docs/doctrines/<slug>/<person-slug>.html` (full quotes,
   context, links). Copy [`templates/person-detail.html`](templates/person-detail.html).
5. Insert the person's footnoted block into the summary `docs/doctrines/<slug>.html` in
   chronological order; add the matching `<li>` footnotes to its Sources block.
6. Bookkeep: append `log.md`, update `TODO.md`. Touch `docs/index.html` **only** for a new doctrine
   (a row in "Doctrines", with its people count) or a new crux (a row in "Arguments & cruxes") — a new
   *witness* needs no index edit (the index no longer lists person pages; bump the doctrine's people
   count, though). Keep the doctrine row's count current.

If a `(person, claim)` is really a **crux** (interest = "does the argument hold?" not "who held it?"):
skip the timeline — write an **argument page** instead (`arguments/<slug>.html`,
[`templates/argument.html`](templates/argument.html)), weigh it adversarially → `assessment`, surface
it in the summary's + index's "Arguments & cruxes" section, and flag any of the proponent's
overstatements on their detail page. See project.md §4/§7.

## Assessments (argument pages)
The `assessment` rates the **interpretation** the argument serves — *not* whichever proponent we
happened to ingest first. `assessment` ∈ {`sound`, `plausible`, `contested`, `weak`, `unsupported`}:
*sound* = holds up — mainstream / near-consensus, or well-grounded and unrefuted; *plausible* =
coherent and not ruled out, but short of majority support; *contested* = genuinely disputed, no clear
winner (often strong by one discipline's lights, weak by another's); *weak* = does not hold on its
best available case; *unsupported* = no real basis. (There is deliberately **no `mixed`** — that old
value blended the *interpretation's* strength with the *proponent's* framing; rate only the
interpretation, and keep framing problems in the prose and on the proponent's page.) Within these,
distinguish **plausible** (coherent, not ruled out) from **probable** (more likely than not). Frame a
proponent's overreach as a *less-probable reading* or *conjecture beyond the evidence*, not as
"wrong/false" — reserve falsity language for genuinely false claims (e.g. a factual misstatement), and
keep wording-precision issues separate from probability judgments.

**State the finding, don't rebut a label.** Assess the interpretation on its own evidence — plausible,
probable, overstated, with caveats. Do **not** frame the assessment as overturning a label
(especially one *we* assigned: "often called the shakiest claim … but actually," "not a mere
apologetic inference"). Setting up a label only to knock it down reads as dishonest and editorial.
Drop the label; just say what the evidence shows.

**Steelman before you weigh.** The assessment adjudicates the *interpretation*, not the modern
proponent's particular wording of it. When the proponent we're ingesting misstates, overstates, or
rests the reading on a weak or wrong-camp source, but a stronger case for the *same* reading exists
(a better proof-text, a sounder mechanism, a fitter witness in the DBs), reconstruct that strongest
version and judge **that**. Keep two questions separate and answer both: is the proponent's stated
argument sound, and is the interpretation sound on its *best available* case? Flag the proponent's
misstep on their page (always, whatever the assessment) — but title the argument page for the
**interpretation** (not the proponent), and let the assessment track the steelman, not the stumble.
So a reading can stand even where the proponent's prop for it fails, and a page that began as "does
X's argument work?" should be reframed to "is the interpretation true?" once the stronger case is in
view.

## Complexes (grouping argument pages)
A **complex** is a named cluster of **two or more argument/crux pages** (within one doctrine, or
occasionally across two) that share a single proof-text, mechanism, or theme and are best read as a set.
It is a **grouping convention, not a page type**: it has no file of its own and adds no `docs/` entry. A
complex is realized in visible content in three places — a grouped sub-heading in the summary's and
index's "Arguments & cruxes" sections, and a `Related cruxes:` breadcrumb on each member page that names
the group and links its siblings. Like all wiki metadata it is derived from visible content, not hidden
frontmatter.

**Naming — internal term vs. reader-facing label.** The convention is called a *complex* in the plumbing
only: the kebab-case slug (`descent`), the anchor `id="complex-<slug>"`, and these meta files. The reader
never sees the word "complex". Every visible surface is labelled **"Related cruxes"** — the group heading
reads `Related cruxes — <theme>` (summary `<h3>`, index `<h4>`) and the member breadcrumb label is
`Related cruxes:` with the bare theme as its link text (e.g. `the descent`). (NB: "complex" also appears
legitimately in argument *prose* in its religious-studies sense — a "ritual/cultural complex" — which is
content, not this label, and is left as written.) Five rules:

1. **Membership ≥ 2.** A single crux is never a complex; a theme with one member stays a standalone crux.
2. **One home complex per argument.** An argument is *grouped* under at most one home complex (never
   listed twice in a summary/index). Relationships to other complexes are `see also` cross-links, not
   double-grouping.
3. **Grouped surfacing needs ≥ 2 members in that summary.** A complex renders as an `<h3>` group on a
   doctrine summary only where that summary holds two or more of its members. A cross-doctrine pairing
   with one member per side is realized via breadcrumb + `see also` links only — no `<h3>` group (e.g.
   the 1 Peter 3:19 identity crux on `nephilim` ↔ the content-of-the-proclamation crux on
   `intermediate-state`, whose home complex is `descent`).
4. **Slug + display name + anchor.** Each complex has a kebab-case slug (`descent`), a reader-facing
   display name ("Related cruxes — the descent"), and a stable anchor on its home summary:
   `<h3 id="complex-<slug>">`. Member
   breadcrumbs link to `../../<doctrine>.html#complex-<slug>`; on the summary the members demote from
   `<h3>` to `<h4>` under a framing `<p>`; in the index they form an `<h4>` group above a trailing
   unheaded `<ul>` of standalone cruxes. **Complex groups lead the "Arguments & cruxes" section on the
   summary as well as the index** — the complex `<h3 id="complex-<slug>">` group first, the standalone
   `<h3>` cruxes after — so summary and index order agree. Re-sequence footnotes after any reorder
   (numbers are sequential by first appearance).
5. **Standalone cruxes are unchanged.** Cruxes in no complex keep their flat `<h3>` / `<ul>` presentation.
