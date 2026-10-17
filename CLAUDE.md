# CLAUDE.md — operating schema for the Doctrine Across Time wiki

This is the terse, load-every-session rule sheet. For the full concept and rationale, read
[`project.md`](project.md) once.

## What this wiki is
For each Christian **doctrine**, a timeline page showing how belief developed across time,
**earliest person first**, where **every claim is footnoted to a source**. The wiki is a set of
**hand-authored static HTML files** under `docs/`, served as-is (no build step, no Markdown,
no Jekyll). You edit the `.html` directly.

Every `docs/` page is deployed as a **standalone page directly on historicalchristian.faith** — no
iframe, no viewer shell. So **every `docs/` page is reader-facing**: write for the reader, never the
operator (see Hard rule 9). `index.html` is both the reader landing page and the LLM catalog — keep its
intro reader-facing; operator guidance lives in an HTML comment.

## Layout
```
docs/                          the published site (deployed to historicalchristian.faith)
  index.html                   the reader's home page + LLM catalog. ONE rated, doctrine-organised
                                 directory, grouped by concept family (an `<h2 id="family-…">` per
                                 family). Each doctrine is an `<h3 id="<slug>">` heading linking to
                                 its summary, then a one-line description, then the arguments adduced
                                 for it. Browse-nav is the generated TOC (`toc.js`), which on this
                                 root page lists families + doctrines only (h2/h3) — there is no
                                 hand-maintained jump table. (NOT a person-page list — witnesses are
                                 cataloged on their timeline; the index tracks no counts.)
  doctrines/<slug>.html              summary timeline (1 footnoted block/person)
  doctrines/<slug>/<person>.html     detail page (full quotes + context + links)
  doctrines/<slug>/arguments/<arg>.html   argument page (one sub-claim → assessment; OFF-timeline)

project.md   full brief        CLAUDE.md   this file        templates/   HTML page skeletons
log.md       append-only history            todo/       pending-leads queue (one file per lead)
people.md    non-DB people dates/slugs       llm-wiki.md  the general pattern
```
Meta files (this file, `project.md`, `log.md`, `todo/`, `people.md`, `templates/`, `README.md`)
live at the repo root and are **not** part of the published site — only `docs/` is served. Note:
`todo/` and `log.md` are intentionally **git-ignored** (operator bookkeeping) — edit them on disk
as usual, but they won't appear in `git status` and are never part of a commit.

Three page types: **doctrine** (summary timeline), **person-doctrine** (a witness's detail page,
slotted on the timeline by year), and **argument** (a single sub-claim adduced for a reading —
proof-text, parallel, or historical thesis — weighed adversarially and given an `assessment` of the
*interpretation* it serves; it cuts *across* the timeline, so it lives in the summary's "Arguments"
section, **not** the chronological list, and has no year). Two or more argument pages that share
a proof-text, mechanism, or theme may be grouped into a named **argument group** — a grouping convention
realized in visible content (a sub-heading on the summary + index and a `Related arguments:` breadcrumb on
each member), **not** a fourth page type and **not** a new file. ("Argument group" is the internal term;
the reader-facing label is **"Related arguments"**.) See "Argument groups" under Assessments below.
Any of the three page types may also carry a **granted premise** banner: the page is analysed *as if* a stated premise
were true (testing it, or working inside it), or — for a **held presupposition** — the wiki simply holds it and the page
works inside it. It is a modifier, not a page type; see "Granted premise" below.

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
  would break — the `docs/` tree is mounted under a subpath of historicalchristian.faith, not the domain
  root, so depth-relative links stay correct wherever it's mounted.
- **One shared stylesheet** — `docs/style.css`, a single dark, minimal sheet (constrained reading
  column, default serif fonts, styled links/quotes/footnotes). Every page links it (see wrapper
  above). No per-page CSS — keep styling in that one file.
- **One shared script** — `docs/toc.js`, the only JS on the site. Every page loads it (`<script defer
  src="<…/>toc.js">` in the wrapper); it builds a collapsible, Wikipedia-style **table of contents**
  from the page's `h2`–`h4` at view time (skips `Sources`; bails on pages with < 3 headings) and
  floats it in the left gutter on wide viewports, scroll-spy included. **Exception:** on the root
  `index.html` it stops at `h3` (families + doctrines), dropping the per-argument `h4` groups that
  would just restate the rated directory below. The TOC is
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
  Members of an **argument group** are additionally grouped under a shared `<h3 id="group-<slug>">` heading on
  the summary (labelled `Related arguments — <theme>`) and an `<h4>` group on the index (the **bare theme**,
  e.g. `the descent` — no "Related arguments —" prefix; the index drops it since the theme already heads the
  doctrine's own block), and each member page carries a `Related arguments:` breadcrumb linking the
  home-summary anchor (`../../<slug>.html#group-<slug>`) and its sibling members.
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
   report → mark the claim `⚠ unverified` inline, cite the secondary work, add a `todo/` file.
5. `person-slug` = lowercased full name, spaces→hyphens (mirrors the `Writings-Database` folder)
   and is the page's filename.
6. Appending to an existing detail page → **append/merge**, don't overwrite.
7. Use the real current date for `log.md` entries.
8. **Never mention the `todo/` queue in a published page** (summary / person-detail / argument) — it's
   internal bookkeeping. On the page, mark an unsourced claim `⚠ unverified` (or call it an "open
   lead" / "not yet sourced") and cite the secondary work only; still add the backlog file per
   rule 4. Referencing `todo/` is fine only in meta files (this file, `project.md`, `log.md`).
9. **No internal plumbing in reader-facing pages** (index / summary / person / argument — i.e. all of
   `docs/`; extends rule 8). Don't name the **source DBs** *as* infrastructure ("our corpus", "our
   holdings", "the database", "the writings corpus", `Commentaries-Database`, `Writings-Database`) or
   the meta files (`project.md`, `log.md`, `CLAUDE.md`, `people.md`) — cite the actual work/edition
   instead, and scope a negative claim as "surveyed here," not "in the database." Keep the provenance
   (which edition/translation a quote is from); drop only the corpus-membership framing. Operator notes
   go in HTML comments or meta files.
   - **"This wiki" / "the wiki" is fine** — it names the *published* doctrine site (reader-facing), not
     the source DBs. Self-references like "X appears on this wiki also as a witness on the Y timeline,"
     "the wiki does not discount a claim merely because it requires a miracle," or "this wiki rates it
     weak" are acceptable house style. The rule bans naming the **upstream source databases** (or meta
     files) as infrastructure — not the site referring to itself.
10. **Link every citation you have a URL for — scholarship included.** We find most references during
    online research (often a free full copy on archive.org, Google Books, a journal, or a digitized
    edition); whenever a reference has a URL we've seen, **hyperlink the citation directly** in the
    footnote so the reader can verify the claim at the source — including modern scholarship (Metzger,
    Bruce, et al.), not just primary fathers. Prefer the most specific stable target (a page/section
    anchor, e.g. an archive.org page link, over a bare landing page). Only omit the link for a **really
    good reason** — no findable online copy, paywalled with no stable URL, or a deep-link too unstable to
    trust — and a bare bibliographic citation (author, title, publisher, year, page) is the fallback,
    never the default. Don't dress an *unverified* page number as if linked: if you cite a page you
    didn't actually open, don't imply otherwise.
- **`todo/` is a queue of not-yet-executed leads — one file per lead, pending items only.** Each lead is
  its own file named `YYYY-MM-DD-HHMM-<slug>.md`; the queue is processed in **lexical filename order**
  (earliest timestamp first), so new leads can be dropped in asynchronously without editing a shared file.
  It never holds "done"/"resolved" items: when a lead is executed, **delete its file** and record the
  outcome in `log.md` (that is the history). The **`/next`** skill works the queue, one file at a time;
  each file must carry enough context to be actioned without re-reading the source it came from. See
  `todo/README.md`.
- **"Import X"** (X = a local file or URL) means **extract every lead from X and add a `todo/` file for
  each** — it is *not* a request to author pages on the spot. Mine X for `(person/claim, source)` pairs
  and open arguments, drop a file per lead, then stop. The leads get processed one-by-one in later passes
  (or when the user says to work the queue). Vital to include source links from where you found the items (local file paths, external urls) for the agents to tap into later when attributing sources, if necessary. Do not explicitly specify the exact edits the agent needs to make - make it clear that the agent should investigate the sources and where our wiki is at, and determine that for itself.
- **Cap a multi-lead batch with a fan-out harvest lead — when appropriate.** Whenever you queue a *batch*
  of leads that scaffolds a **new doctrine, family, or other substantial topic** (a spine + its initial
  research/argument leads), add one trailing **harvest lead** with the **latest timestamp** in the batch, so
  `/next` reaches it only after the spine and initial leads are worked. Its job: once the fresh pages exist,
  run the **`/harvest-leads`** skill over the new area to spin up follow-on leads from the unturned stones the
  initial research surfaced but never queued (named-but-unslotted witnesses, sub-questions raised in prose but
  not yet given argument pages, cross-links that deepen into their own leads, adjacent doctrines worth their
  own spine). The lead must say **do not action until** the pages it depends on exist (else re-queue later and
  stop), and end the normal way (delete + log). This keeps a topic self-extending instead of stopping at the
  first pass. **Only where it fits** — skip it for a lone primary-hunt, a single argument, or any one-off lead
  that opens no new territory; a harvest lead is for batches that plausibly have a *tail* of further research.
- Two lead types: **primary-hunt** (a secondhand claim needing a primary located in the DBs → resolve
  per rule 4) and **argument** (a sub-claim needing adversarial adjudication → resolve into an argument
  page with an `assessment`). Both end the same way: execute, then delete the file + log it. (A **harvest
  lead** — see above — is a third, *meta* kind that queues more leads rather than authoring a page.)
- **Blocked from a needed doc? Exhaust workarounds first, then escalate to `human_todo/`.** If a
  research agent is denied access to a source it needs, it must first try hard to work around it
  (alternative editions, web copies, other sources that suffice). Only if *no* workaround is found
  does it drop a lead in `human_todo/` (same filename convention) asking the human to pull that
  specific doc; assume the human will fetch it and later queue a fresh `todo/` lead for an agent with
  access. `human_todo/` is git-ignored operator bookkeeping, like `todo/`.

## Authoring checklist (see project.md §7 for detail)
1. Identify doctrine(s) + slug + key verses; extract every `(person, claim)`.
2. Date each person (DB `metadata.toml` `default_year`, or research → `people.md`).
3. Verify each claim against the DBs (commentary files by key verse / writings HTML).
4. Write/append the person-detail page `docs/doctrines/<slug>/<person-slug>.html` (full quotes,
   context, links). Copy [`templates/person-detail.html`](templates/person-detail.html).
5. Insert the person's footnoted block into the summary `docs/doctrines/<slug>.html` in
   chronological order; add the matching `<li>` footnotes to its Sources block.
6. Bookkeep: append `log.md`, update `todo/`. Touch `docs/index.html` **only** for a new doctrine
   (add an `<h3 id="<slug>">` linked heading + one-line description under the right concept-family
   `<h2>` — a new family also needs its own `<h2 id="family-…">`) or a new argument (add its `<li>` —
   `title — <strong>rating</strong>` — under the doctrine's argument group, or its trailing standalone
   `<ul>`). **The index `<li>` link text is the argument's title/question only — never its assessment
   prose.** Don't append a paragraph-length parenthetical mini-essay: the reasoning lives on the argument
   page and (condensed) in the summary's "Arguments" section; duplicating it on the index bloats the
   directory and drifts out of sync. A short parenthetical that is genuinely *part of the question* is
   fine; a rehearsal of the verdict is not. Navigation is the generated TOC (families + doctrines), so there is no hand-maintained jump
   table to update. A new *witness* needs no index edit; the index lists
   no person pages and tracks **no counts** (the old people/argument counts were dropped). For a new
   doctrine also add its `slug → display name` entry to the `DOCTRINE_NAMES` map in `docs/toc.js` so
   its breadcrumb crumb is labelled (the only metadata the breadcrumb can't derive from the path).

If a `(person, claim)` is really an **argument** (interest = "does the argument hold?" not "who held it?"):
skip the timeline — write an **argument page** instead (`arguments/<slug>.html`,
[`templates/argument.html`](templates/argument.html)), weigh it adversarially → `assessment`, surface
it in the summary's "Arguments" section and under its doctrine on the index, and flag any of the
proponent's overstatements on their detail page. See project.md §4/§7.

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

**One advocated claim per page — split rivals, fold defeaters.** An argument page states **one**
interpretation in its steelman form, shows the strongest evidence for it, folds in the counterpoints
*to that evidence*, and rates it. Give a counter-position its **own** argument page when it is
*independently advocated* (has its own proponents and proof-texts); **fold it in** when it is a mere
*defeater* — a limit on the evidence that nobody holds as a positive thesis. The trigger is
"**is it advocated?**", not "is it correct?": a popular-but-failing argument (e.g. "*suggenēs* tells
against the cousin-reading") still earns its own rated page. So two genuinely-advocated rival readings
become **two advocacy pages**, grouped and cross-linked (as the Helvidian and Epiphanian readings each
get their own page under `perpetual-virginity`) — **not** one dual-panel page hosting both. This cut
operates at two levels: page-split for advocated rivals, paragraph-level fold-in for defeaters.

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

**Don't rule out the supernatural a priori.** This wiki takes miracles and the supernatural as
genuinely possible — a claim is **not** weak merely because it requires one, and "no natural process
allows it" is not by itself a refutation (that begs the question the miracle claim openly concedes).
Weigh a miracle claim on its *evidence* — attestation, dating, independence, internal coherence — not
on a naturalistic premise. Keep two things distinct: that God *could* act here does not establish that
He *did* (possibility ≠ proof), so a late, poorly-attested, or self-contradictory miracle story can
still be weak — on the evidence, not on the metaphysics. Reserve "impossible" for what fails *even
granting* the supernatural: a conflation of distinct named persons, a demonstrable chronological or
etymological error, a logical contradiction — not for the bare fact of a miracle.

## Argument groups (grouping argument pages)
An **argument group** is a named cluster of **two or more argument pages** (within one doctrine, or
occasionally across two) that share a single proof-text, mechanism, or theme and are best read as a set.
It is a **grouping convention, not a page type**: it has no file of its own and adds no `docs/` entry. An
argument group is realized in visible content in three places — a grouped sub-heading in the summary's
"Arguments" section and under the doctrine's `<h3>` block on the index, and a `Related arguments:` breadcrumb
on each member page that names the group and links its siblings. Like all wiki metadata it is derived from visible content, not hidden
frontmatter.

**Naming — internal term vs. reader-facing label.** The convention is called an *argument group* in the
plumbing: the kebab-case slug (`descent`), the anchor `id="group-<slug>"`, and these meta files. The
reader-facing surface is labelled **"Related arguments"** — the group heading reads `Related arguments —
<theme>` on the **summary** (`<h3>`), while on the **index** the `<h4>` shows the **bare theme** only (e.g.
`the descent` — the "Related arguments —" prefix is dropped there, since the theme already sits under the
doctrine's own heading). The member breadcrumb label is `Related arguments:` with the bare theme as its link
text (e.g. `the descent`). (NB: the bare word "complex" still appears legitimately
in argument *prose* in its religious-studies sense — a "ritual/cultural complex" — which is content,
unrelated to this grouping convention, and is left as written.) Five rules:

1. **Membership ≥ 2.** A single argument is never a group; a theme with one member stays a standalone argument.
2. **One home group per argument.** An argument is *grouped* under at most one home group (never
   listed twice in a summary/index). Relationships to other groups are `see also` cross-links, not
   double-grouping.
3. **Grouped surfacing needs ≥ 2 members in that summary.** An argument group renders as an `<h3>` group on a
   doctrine summary only where that summary holds two or more of its members. A cross-doctrine pairing
   with one member per side is realized via breadcrumb + `see also` links only — no `<h3>` group (e.g.
   the 1 Peter 3:19 identity argument on `nephilim` ↔ the content-of-the-proclamation argument on
   `intermediate-state`, whose home group is `descent`).
4. **Slug + display name + anchor.** Each argument group has a kebab-case slug (`descent`), a reader-facing
   display name ("Related arguments — the descent" on the summary; the **bare theme** on the index), and a
   stable anchor on its home summary: `<h3 id="group-<slug>">`. Member
   breadcrumbs link to `../../<doctrine>.html#group-<slug>`; on the summary the members demote from
   `<h3>` to `<h4>` under a framing `<p>`; on the index they form an `<h4>` group (bare theme) above a
   trailing unheaded `<ul>` of standalone arguments, all under that doctrine's `<h3>` block. **Argument
   groups lead each doctrine's arguments on the summary and the index alike** — the group(s) first, the
   standalone arguments after — so summary and index order agree. Re-sequence footnotes after any reorder
   (numbers are sequential by first appearance; the index itself carries no footnotes).
5. **Standalone arguments are unchanged.** Arguments in no group keep their flat `<h3>` / `<ul>` presentation.

## Relationship topics (a doctrine-page variant)
A **relationship topic** is a doctrine page whose subject is a *relationship between two people told
across time* — the friendship, quarrel, or correspondence itself — rather than a belief many witnesses
held. It **reuses** the doctrine + person-detail page types (a summary timeline plus one detail page per
party); it is **not** a fourth page type and adds no new file convention. It sits under the "Controversies
among the Fathers" concept-family `<h2>` on the index. First instances: `origenist-controversy` (Jerome ↔
Rufinus) and `jerome-augustine` (Jerome ↔ Augustine). It diverges from an ordinary belief-timeline in
three ways:

1. **Person pages carry life-span dates, not a single event-year.** Both parties are present across the
   whole arc, so the detail head line reads `<strong>Dates:</strong> c. 347&ndash;420` (a span), and the
   `Summary:` line scopes which stretch of the relationship that page covers.
2. **Timeline "witnesses" are dated events, not persons.** Each `<h3>` on the summary is an event, letter,
   or document with a parenthetical date (`<h3>Jerome settles at Bethlehem (386)</h3>`), ordered
   earliest-event-first but tolerant of multi-year topical blocks (event-start-first, with narrative
   latitude). Every event block still ends in a footnote (Hard rule 2); ordering is maintained by hand
   (Hard rule 1).
3. **Both parties get a detail page** under `docs/doctrines/<slug>/`, each telling the arc from that
   person's side and cross-linking the other. The summary intro flags that this timeline is a
   *relationship* told through its dated moments, unlike the belief-timelines elsewhere.

Arguments, argument groups, and the "Related doctrines" cluster convention all apply unchanged. A second
relationship topic under the same family turns it into a **cluster** (≥ 2 members) → add a `Related
doctrines:` breadcrumb to each member summary (see below).

## Biographical tradition-timelines (a doctrine-page variant)
A **biographical tradition-timeline** is a doctrine page whose subject is *a person* — an apostle — rather
than a belief many held. The "belief that developed" is the **tradition about that figure**: how the
church's memory of his origin, mission, and death grew (and got embellished) across the centuries. It
**reuses** the ordinary doctrine + person-detail types unchanged — **not** a new page type. The timeline's
"witnesses" are the datable **sources** that report on him (NT → Papias → Clement of Alexandria →
Irenaeus/Tertullian → Eusebius → the apocryphal *Acts* → Jerome → the Byzantine/Latin apostle-lists →
the *Golden Legend* → modern scholarship), ordered earliest-source-first (Hard rule 1), each block
footnoted (Hard rule 2). Contested identity/mission/death questions (Bartholomew = Nathanael? Thomas in
India? Peter's Roman crucifixion?) become ordinary **argument pages** in the summary's "Arguments" section.
The Twelve, Matthias, and Paul live under the **"The apostles"** concept-family `<h2 id="family-apostles">`
on the index, fronted by the overview hub `doctrines/apostles.html`; slug convention `apostle-<name>`
(e.g. `apostle-peter`, `apostle-james-zebedee`). Once ≥ 2 apostle pages exist the family reads as a
**doctrine cluster** — add the `Related doctrines:` breadcrumb to each member summary and the hub then.

**Reception-history timelines** are the same shape aimed at a *verdict* rather than a life: the subject is a
person, and the "belief that developed" is the church's judgement on him — who called him heretical, on what
charges, on whose authority, and how the charge-sheet changed. Timeline "witnesses" are the datable
**judgements and documents** (a synod, a rival's treatise, a heresy-catalogue, a papal letter, an imperial
edict, a conciliar anathema, a modern monograph), earliest first, each footnoted; contested questions become
ordinary argument pages. Again **not** a new page type — it reuses doctrine + person-detail unchanged, and
sits in whatever concept-family fits its subject. First instance: `origen-condemnation`, under "Controversies
among the Fathers".

## Granted premise (a banner on any page type)
A **granted premise** marks a page that is analysed *as if* a stated premise were true. It is a **modifier, not a page
type and not a doctrine-page variant**: a banner at the top of an ordinary doctrine summary, person-detail, or argument
page. It lets the wiki drive deep into belief structures whose premises are not mainstream, or fit the real-world record
poorly, without the page's findings being mistaken for a verdict on the premise. Like all wiki metadata it is visible
content, not hidden frontmatter: a page *is* premised exactly when it carries the banner. (It replaces the former
"evidential reconstruction" variant, and underlies the scenario ledger and the synthesis narrative below.)

**Markup.** An `<aside class="granted-premise">` placed directly after the `<h1>` (styled in `style.css`):
```html
<aside class="granted-premise">
<p><strong>Granted premise:</strong> that <premise, stated plainly>. <mode sentence>. <link to where the premise
itself is weighed, with its real assessment>.</p>
</aside>
```
A page that grants several premises side by side (a scenario ledger) uses the plural label **Granted premises:**. A page
working inside a **held presupposition** (below) uses the label **Presupposition:** instead, in the same `<aside>`.

**Three modes — the banner must say which.**
- **Testing** — the page grants the premise to see what it predicts and whether the evidence bears it out. Its verdicts
  bear on the premise itself, so the page *is* where the premise is weighed and the banner points at its own Arguments
  section. No page uses this mode at present. Use it only where a page must reason *inside* a premise to derive what it
  predicts; a page that simply gathers the evidence for and against a claim (e.g. `book-of-mormon-historicity`) is an
  ordinary evidence page and carries no banner.
- **Working inside** — the page assumes the premise to explore what follows from it (the "unseen realm" told as one
  story). Its ratings are **conditional** on the premise, and the banner links the page that weighs the premise
  unconditionally.
- **Held presupposition** — the wiki itself *holds* the premise, as the site owner's working presupposition, and does not
  spend pages testing whether it is true: no page argues that it did not happen, and none is kept "for balance." The
  banner (label **Presupposition:**) says "this wiki holds that …" and states what the page asks *inside* it. Ratings are
  conditional on it, as for working-inside pages. Rule 2's "link where it is weighed" is met by linking the belief-history
  page that records how the Church has held it (e.g. `flood`), not an unconditional test. Evidence still gets weighed
  honestly, sorted three ways: (a) **a claimed trace is not what it is claimed to be** (a silt band, landform, skull) —
  rate it weak/unsupported as usual; (b) **evidence that tells against one *model* of the event** (a given date, a
  given mechanism) — say so, scoped to that model; (c) **evidence that presses on the presupposition itself** — present it as an
  **open puzzle inside the presupposition**: state the tension plainly without softening the data, and weigh the
  resolutions proposed by those who hold it (noting where a resolution only works by giving up part of the
  presupposition — e.g. a regional Flood, under a whole-earth presupposition). Never frame (c) as falsifying the
  presupposition, and never frame (b) as a test of it. Rival believing models stay (e.g. scenarios A/B/C, three datings of
  the Flood, on `primeval-scenarios`). **Current held presuppositions:** Noah's Flood happened, **covered the whole earth**,
  and destroyed all humanity outside the ark — its *date* stays open — and the Nephilim were real (`primeval-evidence`, `flood-date`, `primeval-scenarios`, and
  their argument pages); and Israel took Canaan as Joshua and Judges tell it — its *date* stays open, the early (c. 1406 BC)
  and late (c. 1250 BC) datings being rival models, and no "no invasion" reading is carried (`conquest-of-canaan`,
  `conquest-as-written`, and their argument pages; their banners link the belief-history page `conquest-in-tradition`, as
  the Flood pages link `flood`). Extend the list only when the site owner adopts a new one.

**Rules.**
1. **Conditional ratings say so.** On a working-inside page every `Assessment:` means "given the premise." The banner
   scopes them; don't restate the condition on every line, but never present such a rating as unconditional in prose,
   and the page's one-line description on the index must name the premise it grants.
2. **The banner links where the premise is weighed, with its real assessment** (or, for a testing page, its own
   Arguments). A premise that is weighed nowhere yet is a lead to create that page first: a premised page may never be
   the *sole* home of its premise (no laundering an unrated premise by assuming it). A **held presupposition** is the one
   exception: it is held, not weighed, so its banner links the belief-history page that records how the Church has held it
   (see the third mode above), and no page is created to test it.
3. **Argument pages inherit.** Each argument page under a premised summary carries a one-line inherited banner,
   `<aside class="granted-premise"><p><strong>Granted premise:</strong> inherited from <a href="../../<slug>.html">…</a>
   — …</p></aside>`, so a reader who lands there directly sees the scope. Person-detail pages under a premised summary
   report a source and need no banner unless their own prose works inside the premise.
4. **Granting is not assuming the conclusion.** On a testing or working-inside page the intro still says so plainly;
   each line of evidence is rated on its own merits, **possibility ≠ proof**, and such a page may (and often should)
   report that the evidence does not bear the premise out. This is the anti-apologetics guard, the direct extension of
   "don't rule out the supernatural a priori," and it is load-bearing: without it a granted premise is just apologetics
   with a label. On a **held-presupposition** page the guard applies to every *claimed trace and model* (possibility ≠
   proof; a misidentified artifact stays misidentified; tensions are stated, not buried), but not to the presupposition
   itself, which the page holds rather than tests (see the third mode above).
5. **Testing and held-presupposition pages: evidence-dated timelines and two argument modes.** Where such a page's timeline "witnesses" are
   datable evidence-sources (a stratum, tablet, king-list, megalith, hoax, genome study), order them by the age of the
   *evidence*, not of the event it reports, and flag that ordering in the intro. Arguments run *retrospective* ("here is
   an artifact — does it fit?") and *predictive* ("the premise requires X — is X there?"); a predictive page commits to
   what would falsify it and **scopes any failure to the specific model that made it** (a young single-date global
   deluge, a literal eight-person survival), not to the bare premise. Keep at least one honestly-*successful*
   prediction in the set so it is not rigged toward debunking. (On a held-presupposition page, a failed prediction sorts
   into model-choice (b) or open puzzle (c) above, never into a test of the presupposition.)

**Current premised pages.** Held presupposition: `primeval-evidence`, `flood-date` and `primeval-scenarios` (a whole-earth
Flood that destroyed all humanity outside the ark, and real Nephilim); `conquest-of-canaan` (the conquest as Joshua tells
it, date open; Jericho's date, Ai's empty mound and the highland pottery as open puzzles) and `conquest-as-written` (one
dating model inside it, the Bible's own dates, c. 1406 BC, with its fits marked in the scenario-ledger buckets and its bill
at the foot). Testing: none at present. Working inside: `supernatural-worldview` (the unseen-realm reading, in the
narrative format below). Several premises side by side: the other three scenario ledgers below (`primeval-scenarios` compares three models
inside the held presupposition, under the **Presupposition:** label).
Arguments, argument groups, and the "Related doctrines" cluster convention all apply unchanged.

## Comparative scenario-ledger pages (several granted premises side by side)
A **scenario ledger** is a doctrine page that grants **two or more competing premises at once** and reads one shared
body of evidence under each. Each premise is a fixed presupposition-bundle — a "scenario" — and the page carries the
plural **Granted premises:** banner (see "Granted premise" above) — or, when its scenarios are rival models inside a held
presupposition (as on `primeval-scenarios`), the **Presupposition:** banner instead. It **reuses** the ordinary doctrine + person-detail +
argument types unchanged — **not** a new page type, **one aggregate page**, and it **does not clone** the pages it reads:
it *links* the existing argument/evidence pages and holds only the *conditional delta* per item. Instances:
`primeval-scenarios` ("The Flood and the Nephilim: the evidence under competing scenarios", "Primeval history (Genesis
6–9)"); `divorce-scenarios` (the three historic answers on divorce — A Latin/Catholic indissolubility · B the
Erasmian–Protestant dissolution reading · C the Eastern Orthodox *oikonomia* practice — over the Gospel/Pauline
proof-texts, "Marriage, celibacy, and the single life"); `final-state-scenarios` (A eternal conscious torment · B universal
restoration · C conditional immortality, "The living and the dead"); and `chronology-scenarios` (A Masoretic/Ussher · B
Septuagint long · C rabbinic *Seder Olam*, "Reckoning sacred time"). The textual/doctrinal ledgers adapt the △ bucket from
"costs a date" to **"costs a text"** (`chronology-scenarios`, which mixes both kinds of anchor, uses "costs a date or a
text"). The reusable purpose is comparison of *total frameworks*; `perpetual-virginity` (the Helvidian vs. Epiphanian vs.
Hieronymian readings) is a natural future instance. It has four defining features:

1. **Scenarios are named, fixed presupposition-bundles, each stating exactly what it commits to.** A scenario is not a
   mood ("the traditional view") but a spelled-out set of commitments with a **bill** — the specific things that must
   hold true for it, and what would falsify it. E.g. on `primeval-scenarios` the three scored bundles are *(A)* Septuagint
   long chronology + real antediluvian Watcher-arts inherited *through* the Flood, *(B)* Masoretic short / young-earth
   literal global Flood, and *(C)* an open antediluvian age (conventional dates accepted, the genealogy read as open) —
   three rival models inside the wiki's held presupposition of a real Flood and real Nephilim, so no no-Flood column is
   scored or carried as a baseline there; elsewhere a null may be carried either way (see feature 4). Each scored column carries its own falsifiers, not just its friendly fits.
2. **One shared evidence shelf, scored per scenario into four buckets.** The rows are the *same* evidence for every
   column (drawn from the linked argument/evidence pages), and each cell places that item, under that scenario, in one
   bucket: **✓ fits / positively predicted**, **○ neutral (consistent, non-discriminating)**, **△ costs a date** (fits
   only if a *named* dating result is wrong — say which method and how load-bearing), or **✗ unexplained / contradicts**
   (a residue the scenario cannot absorb *even granting its premises* — the honesty anchor). The cell holds a terse
   conditional delta and links the full argument page; it does **not** re-rate that argument (its `assessment` stays the
   neutral one — the ledger reports how it reads *conditional on* each bundle, nothing more). No cloning, no per-page
   codas, no laundering a fit upward because the friendly bundle is assumed.
3. **The honesty floor is mandatory and load-bearing.** Every scenario column **must** publish, from the ledger, (a) its
   **✗ residue** explicitly (what it still cannot explain), and (b) its **△ count** — how many *independent* dating
   results it needs overturned, and whether those failures share one mechanism (correlated — e.g. "all radiometric
   compressible") or are **ad hoc** (many unrelated excuses). The friendly bundle is always shown beside its bill, and a
   scenario ledger **may — and often should — conclude against a bundle**. This extends the "don't launder a fit upward"
   and "symmetry of skepticism" rules: the ✗ residue and △ count are what keep the ledger honest, not a column of friendly
   fits. Keep at least one honest ✓ *and* one honest ✗ per live scored bundle so no column is rigged in either direction.
   (A dedicated naturalistic-null *column* is optional, not required — the null can instead sit as the neutral baseline the
   linked pages establish; the honesty work is done by each live bundle publishing its own residue and bill, not by hosting
   a null column for contrast.)
4. **Confine it to subjects where a presupposition bundle genuinely reorganizes the whole reading.** Requires ≥ 2
   competing bundles and a shared evidence shelf it links rather than restates; the mainstream/naturalistic reading may be
   carried as one scored column *or* folded into the baseline the linked neutral pages already hold — except under a held
   presupposition, where no null is carried at all (as on `primeval-scenarios`, which scores only rival models of the held
   history). Do **not**
   spawn scenario ledgers for every doctrine — the value is systems-level accounting where competing *total* frameworks
   read the *same* data differently.

Reader-facing label **"Scenarios" / "the scenario ledger"**; internal term *scenario ledger* with a kebab-case slug per
instance (`primeval-scenarios`, `divorce-scenarios`, `final-state-scenarios`, `chronology-scenarios`). Arguments, argument groups, and the "Related doctrines" cluster convention all apply
unchanged; the base facts and neutral ratings live once on the linked pages, so the ledger's job is the *delta and the
bill*, kept in one legible place. Skeleton: [`templates/scenario-ledger.html`](templates/scenario-ledger.html).

## Synthesis-narrative pages (a working-inside granted premise, told as one story)
A **synthesis narrative** is the *narrative format* of a working-inside granted premise: a doctrine page that grants a
*whole worldview* and tells it as one connected story — the "big picture" that individual doctrines and arguments only
ever show a fragment of. It carries the **Granted premise:** banner (naming the worldview and pointing at its cost
ledger), and everything below is what distinguishes the narrative format from an ordinary premised page. Many of the
wiki's threads (the divine council, the Genesis-6 rebellion, the Nephilim, the Flood, Babel's disinherited nations, the
conquest giants, the gods-of-the-nations, the modern UFO tail) interlock into a single cohesive account; each leg lives
on its own timeline/argument page and is weighed there, but nowhere does a reader see the arc *as* an arc. A synthesis
narrative draws that arc. It **reuses** the ordinary doctrine + person-detail + argument types unchanged — **not** a new
page type, **one aggregate page** — and it **does not clone** the pages it draws on: it *links* them and holds only the
*connective narration*. First (and so far only) instance: `supernatural-worldview` ("The Supernatural Worldview: How
the Threads Connect"), the Deuteronomy-32 / Heiser "unseen realm" story, under its own "The big picture" family
(`family-big-picture`). It is defined by four features:

1. **It grants the whole reading and narrates in its own voice — it makes NO assessments.** Unlike every other page,
   a synthesis narrative carries **no** `sound`/`plausible`/`contested`/`weak`/`unsupported` judgments and does not
   adjudicate anything in its prose. It states plainly up front that it is a *synthesis, not an assessment*: "granting
   the whole reading, here is the single story its threads tell." The narrative is deliberately kept **clean** — it is
   **not** hedged, tagged, or rebutted at the seams (that staining is exactly what this page-type exists to avoid). The
   honesty is not abandoned; it is **relocated** to (a) an inline link at every load-bearing leg, out to the page that
   weighs it critically, and (b) the mandatory cost ledger at the foot. Those two carry the whole honesty burden, so
   both are non-negotiable.
2. **The cost ledger at the foot is the single honesty floor — mandatory and load-bearing.** The page ends in a
   `<h2>` **"What you would have to hold"** (reader-facing label; internal term *cost ledger*): the complete tally of
   the load-bearing commitments the worldview requires, **each linking the page that weighs it and carrying that page's
   real assessment** (this is the one place ratings appear — at the *foot*, not smeared through the story). It is framed
   as a **conjunction**: to hold the *whole* picture as history you must accept *all* of these together, and the
   cumulative weight of the conjunction is the honest counter to the narrative's coherence (a chain of individually
   *plausible* legs can have a low joint probability — coherence makes a story feel likelier, conjunction makes it less).
   Order the ledger most-load-bearing / most-fragile first, and be honest that several of these the wiki itself rates
   weak or unsupported. A synthesis narrative that omits or softens this ledger is just apologetics with a disclaimer.
   Where a leg is one the wiki holds as a **held presupposition** (e.g. that the Flood happened and covered the whole
   earth), the ledger does not tally the presupposition itself as a cost: it says the wiki holds it (linking the
   belief-history page) and lists its open puzzles and model-level weaknesses — with their real ratings — as what the
   picture still has to carry.
3. **One worldview per page, in its own voice — rivals get their own synthesis pages, never a both-sides treatment.**
   A synthesis narrative tells *one* framework's story straight through; it does **not** stain that story with a rival's
   objections or a comparative panel (that is the scenario ledger's job, and even there the rows are neutral). The
   naturalistic/materialist reading — and any other rival framework — earns its **own** standalone synthesis page later,
   told in its own voice, so each story can be read and weighed on its own terms. Do **not** flag "the form's asymmetry"
   inside a synthesis page; the symmetry is supplied at the *family* level by the sibling pages, not inside any one of
   them. Once ≥ 2 synthesis pages exist the "The big picture" family reads as a cluster → add the `Related doctrines:`
   breadcrumb then.
4. **Legs are sourced by inline link, not a footnote apparatus.** Because every claim in the narrative is a conditional
   re-narration of a leg that is fully sourced and adversarially weighed on its *own* page, the synthesis narrative
   sources itself by **inline links to those pages** rather than a per-claim `Sources`/footnote block — a deliberate
   divergence from Hard rule 2, mirroring how the scenario ledger's cells link the full argument page instead of
   re-citing it. Every load-bearing leg must be one click from its full treatment; a leg with no page yet is a lead to
   create that page first (or the cost ledger flags it as not-yet-weighed) — the narrative may never be the *sole* home
   of a claim (no laundering by burying an unrated claim only here).

Reader-facing label **"The big picture"** / **"synthesis"**; internal term *synthesis narrative* with a kebab-case slug
per instance (`supernatural-worldview`). Arguments, argument groups, and the "Related doctrines" cluster convention all
apply unchanged. Skeleton: [`templates/synthesis-narrative.html`](templates/synthesis-narrative.html).

## Dating-skepticism & out-of-place-artifact (OOPArt) arguments
Some arguments (esp. on `primeval-evidence`) test whether an artifact is **significantly older than its official
date** — potentially reaching a pre-Flood / nephilim horizon — i.e. that the conventional dating is wrong. These are
legitimate, genuinely-advocated arguments and get honest rated pages, but they carry a **strict method** so
"strongly considered" never decays into special pleading. Rate the *interpretation* ("X is much older than dated"),
via five steps: **(1)** steelman the OOPArt/antiquity claim in its strongest form (scale, precision, technique);
**(2)** name the *actual dating method* and its specific evidence (epigraphic/inscriptional · radiocarbon · OSL/TL ·
stratigraphic · art-historical/stylistic · palaeographic · molecular-clock) — different methods have different
failure modes; **(3)** state plainly **what would have to hold true** for the older date, conceding the *real*
precedents that make it live (monument **usurpation/appropriation** — a ruler claiming a predecessor's work;
**renovation-as-construction**; reused **foundations/spolia**; circular stylistic dating); **(4)** test adversarially
whether those conditions actually hold *at this artifact*, noting where a mechanism transfers well vs. badly (e.g.
usurpation is strong against a free-standing built temple, weak against a **monolithic rock-cut excavation** with no
prior structure to appropriate); **(5)** rate on the evidence.

Non-negotiable honesty guards (these bind every such page):
- **"Strongly considered" = thorough steelman + fair examination, NOT a favorable rating regardless.** The rating
  tracks the evidence; do not pre-ordain a verdict in either direction.
- **Symmetry of skepticism.** Don't defend a date by authority/consensus alone, *and* don't unseat one on bare
  possibility. If a load-bearing assumption is genuinely live, rate up and say so; if the specific evidence defeats
  it, say that.
- **Don't invoke the supernatural to move a date.** Weigh dating on dating evidence; possibility ≠ proof (per "Don't
  rule out the supernatural a priori"). A miracle can be granted elsewhere; it does not relocate a stratum or an
  inscription.
- **Differentiate by method, don't blanket-rate.** Dating security is high where contemporary writing or converging
  methods anchor it, genuinely open where a single assumption-laden method (palaeography, molecular clocks) carries
  the weight — report which per artifact; that differentiation is the honest result.
- Keep the **manufacturing** sub-claim ("needed advanced tech to make") distinct from the **dating** sub-claim
  ("older than its date") and rate each separately. OOPArt pages are grouped under `group-oopart`; the
  reader-facing group label is "Related arguments — out-of-place artifacts."
- **Default steelman for a manufacturing / "beyond-native-capacity" claim: post-Flood *inheritance*, not a redated
  artifact.** When the maker-culture itself sits *after* the Flood, the strong form of "they couldn't have made this
  unaided" is not "the object is secretly older" (that is the *dating* sub-claim) but "the capacity is antediluvian
  know-how — the Watcher-arts of *1 Enoch* 7–8 — carried *through* the Flood into a post-Flood heir." Consider this
  reading before rating any such claim. It makes the **Septuagint** horizon *load-bearing*: only the long chronology
  leaves the culture standing after the deluge (the short one turns it into an antediluvian casualty), so here the
  Flood date is **not** moot — the opposite of the dating sub-claim, where it usually is. Concede the chronological fit
  where the LXX gives one (straddle patterns — a technique attested pre-Flood and climaxing post-Flood — count in the
  argument's favour), then rate on the **date-independent material character** of the work (tool-marks, excavated
  workshops, craft-trajectory). Worked model: `primeval-evidence/arguments/jade-manufacturing-technology.html`
  (§ "Where the Flood date is not moot").

## The biblical Flood horizon as a yardstick (Genesis 6–9 evidential pages)
When a `primeval-evidence` or `flood-date` page needs a **biblical Flood date to judge an artifact's or horizon's
fit**, steelman the *strongest* reckoning, not the most *popular* one: default to the **Septuagint long chronology**
(Flood c. 3300–3000 BC, Creation c. 5500 BC) as the working horizon, since the wiki already rates it "arguably the
stronger" reckoning (`flood-date/arguments/septuagint-long-chronology.html`), not Ussher's Masoretic 2348 BC merely
because young-earth writers favour it. But do **not** flip this into "measure against the LXX only" — that just swaps
one strawman for its mirror image. The honest standard, modelled by `primeval-evidence/arguments/ur-flood-deposit.html`
(whose verdict is "extent, not date"):
- **Test against the contested interval** — short end (Masoretic/Samaritan ~2348 BC) to long end (LXX ~3300 BC) — not
  a single number.
- **Flag any verdict that flips** with the reckoning: "'X is too early' is a verdict about a chosen yardstick, not a
  fact about the artifact." Where the verdict is date-*independent* (stratigraphy, mechanism, or wrong by orders of
  magnitude), say so and move on.
- **Don't launder a fit upward on the LXX's back — but an honest reframing may legitimately raise a rating.** The LXX
  is still *weak as a date* on its own (even c. 3200 BC the continuous Naqada/Uruk sequences run across the horizon with
  no rupture), so a fit does **not** improve *merely because* you switched to the more generous yardstick — that
  mechanical swap is the laundering to avoid. What *is* allowed: a rating that rises because the reconsidered evidence
  itself warrants it. An upward move is an acceptable outcome of a steelman pass, not a ceiling the yardstick forbids;
  the bar is honesty about *why* it moved (the evidence, not the chosen number).
- **Deep-time artifacts** (Göbekli Tepe, etc.) sit before *both* reckonings' Creation, so the horizon choice is moot
  there — the live question is dating-method security (`dating-security.html`), not which biblical number.

Two research directions extend this and are queued in `todo/`: a **calibration-spine** argument (the
dendro/varve/speleothem/ice-core anchor chain + accelerated-decay — the one *live* form of the "deep dates are
compressible" case, to be rated honestly with symmetry of skepticism) and a **mature-creation / apparent-age**
argument (does created-with-appearance-of-age neutralize the dating record? — a philosophy-of-evidence move that
*concedes* the measurements, kept distinct from dating-method skepticism).

## Doctrine clusters (cross-linking related doctrines)
A **doctrine cluster** is a named family of **two or more doctrine summaries** that share witnesses,
proof-texts, and arguments and are best read together. It is a **lightweight cross-link convention, not a
page type** — no file of its own, no `docs/` entry, no build step, and it does **not** touch any timeline.
It is realized in two places: the **concept-family `<h2>` grouping on `index.html`** (the home page lists
every doctrine under a family `<h2>` — a family with ≥ 2 members is a cluster; a single-doctrine family
is a standalone topical heading, **not** a cluster, and gets no breadcrumb. There is no "Other doctrines"
catch-all), and a **`Related doctrines:` breadcrumb** on each member summary, placed directly under the
intro paragraph (before the first `<h2>`). The breadcrumb names the family (an `<em>` label, **not** a link)
and then `see also`s its sibling members as same-directory `<sibling>.html` links — every member points at
all the others. Like all wiki metadata it is derived from visible content, not hidden frontmatter.

```html
<p><strong>Related doctrines:</strong> <em>Scripture's text &amp; canon</em> — see also
<a href="ot-canon.html">the Old Testament canon</a> · <a href="septuagint-origin.html">the Septuagint's origin</a>
· <a href="rabbinic-corruption.html">rabbinic corruption of the text</a></p>
```

Reader-facing label **"Related doctrines"**; internal term *doctrine cluster* with a kebab-case theme name
used only in these meta files. The index groups doctrines under concept-family `<h2>` headings (see above); each such heading
carries an `id="family-<slug>"` anchor (the generated TOC links to it) but **no**
`id="cluster-…"` anchor, and the summary breadcrumb's family label stays plain `<em>` text, not a link. Rules: ≥ 2 members; keep each member's
existing in-prose cross-links — the breadcrumb is the consistent nav handle, the prose is the explanation.

**Where membership lives.** Which doctrines belong to which family is recorded in exactly two visible
places: the concept-family `<h2>` groupings on `index.html` (the source of truth) and each member's
`Related doctrines:` breadcrumb. This file keeps **no** roster of clusters or families, because a
hand-kept copy drifts. To see a family, read its `<h2 id="family-…">` block on the index. When a
family grows from one doctrine to two, it becomes a cluster: add the breadcrumb to both members then.
When adding a doctrine to an existing cluster, add it to every sibling's breadcrumb.
