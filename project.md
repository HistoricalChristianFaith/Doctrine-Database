# Doctrine Across Time — Project Brief

> **Read this first.** This is the self-contained brief for the *Doctrine Across Time* wiki.
> Any agent or person can read this single file and understand what we are building, how the
> data is structured, where the sources live, and the exact process for turning a source into
> wiki pages. For the terse day-to-day operating rules, see [`CLAUDE.md`](CLAUDE.md).

## 1. Purpose

For any Christian **doctrine** (baptism, the Trinity, the Eucharist, justification, the
canon, eschatology, …) we build a page that shows **how belief on that doctrine developed
across time**, person by person, **earliest first**. The reader should be able to scan one
page and watch a doctrine evolve through history.

Two rules are non-negotiable:

1. **Timeline-first.** People are ordered by date, earliest at the top.
2. **Every claim is cited.** No assertion about what someone believed appears without a
   footnote pointing to a source. Where we have a firsthand quote it is *verified*; where we
   only have someone else's report ("Father X believed Y") it is marked *unverified* and
   logged in the [`todo/`](todo/) queue until we find the primary source.

This is an instance of the general pattern in [`llm-wiki.md`](llm-wiki.md): the LLM owns and
maintains the wiki layer; raw sources are immutable; the wiki compounds over time.

The wiki is published as **hand-authored static HTML** under `docs/`, served as-is by GitHub
Pages. There is no Markdown source and no build step — you edit the `.html` files directly.

## 2. The three layers

| Layer | What | Where |
|-------|------|-------|
| **Raw sources** (immutable) | Primary texts + secondary works | The two sibling databases (§3) + books/web you feed in |
| **The wiki** (LLM-owned) | Doctrine pages, person-detail pages, the index, plus the log/todo bookkeeping | `docs/` (the published HTML) + `log.md`, `todo/`, `people.md` |
| **The schema** (co-evolved) | How the wiki is structured and maintained | This file + [`CLAUDE.md`](CLAUDE.md) + [`templates/`](templates/) |

## 3. Source databases (our source of truth)

Two sibling repos on disk are the primary, citable source-of-truth. Prefer them over the
open web whenever a claim can be grounded in them.

### 3a. `~/Desktop/Commentaries-Database/`  (verse-oriented)
- Layout: `Father Name/Book Chapter_Verse.toml` — e.g. `Tertullian/John 3_5.toml`.
- Each file holds one or more `[[commentary]]` blocks:
  ```toml
  [[commentary]]
  quote = '''…the father's words…'''
  source_url = 'https://historicalchristian.faith/by_father.php?file=Tertullian%2FOn%2520Baptism.html'
  source_title = "On Baptism"
  ```
- A single quote may legitimately appear under several verses. `source_title`/`source_url`
  may occasionally be missing on a block.
- Filenames use KJV book names from `Commentaries-Database/book_names.json`; verse ranges look
  like `John 3_5` or `Acts 2_38-39` (no `a`/`b` sub-verses).

### 3b. `~/Desktop/Writings-Database/`  (work-oriented)
- Layout: `Father Name/Work Title.html` — full public-domain texts — plus a per-father
  `metadata.toml`:
  ```toml
  default_year = 220
  wiki = 'https://en.wikipedia.org/wiki/Tertullian'
  ```
- **`default_year` is our timeline anchor** — roughly the figure's death/floruit year. 340 of
  ~345 fathers have one. `wiki` gives a canonical bio link.

### 3c. The two URL schemes on `historicalchristian.faith`
Both forms are valid citation targets; use whichever the source data gives you.
- **Verse page:** `https://historicalchristian.faith/<book>/<chapter>/<verse>` — book slug is
  the lowercased book name with no spaces. e.g. John 3:5 → `https://historicalchristian.faith/john/3/5`;
  2 Thess 3:12 → `https://historicalchristian.faith/2thessalonians/3/12`.
- **Work page:** `https://historicalchristian.faith/by_father.php?file=<Father>%2F<Work>.html`
  (spaces URL-encoded as `%2520`). This is exactly the `source_url` stored in the TOML files.

### 3d. On-disk ↔ URL mapping (for pulling surrounding context)
A `by_father.php` URL maps directly to a file under `Writings-Database/`. Decode `%2F`→`/` and
`%2520`→space:
```
…by_father.php?file=Tertullian%2FOn%2520Baptism.html
  ↳ ~/Desktop/Writings-Database/Tertullian/On Baptism.html
```
Use this to read the passage *around* a quote when you need more context for a person-detail
page. (The HTML is messy; strip tags before reading.)

## 4. Page model

Each doctrine has **one summary page** plus **one detail page per person**, all under `docs/`.

```
docs/doctrines/
  baptism.html            ← SUMMARY: the timeline. One short, footnoted block per person.
  baptism/
    tertullian.html       ← DETAIL: full quotes + surrounding context + all source links.
    augustine-of-hippo.html
    …
```

- **Summary page** = the headline artifact. A chronological list of people (earliest first); each
  gets a tight paragraph (2–5 sentences) stating *what they held*, every claim footnoted, with the
  person's name linked to their detail page. This is the doctrine's main reader-facing page.
- **Person-detail page** = the evidence. Full quotes (verbatim from the DBs) in `<blockquote>`,
  surrounding context, every `source_url`/`source_title`, and the reasoning for each claim. One page
  per `(doctrine, person)` pair.
- **Argument page** (`docs/doctrines/<slug>/arguments/<arg-slug>.html`) = a single *sub-claim*
  adduced in support of a main interpretation — a proof-text (e.g. 1 Peter 3:19), an
  archaeological/literary parallel (e.g. Og's bed ≅ Marduk's bed), or a historical thesis — weighed
  *adversarially* and given an `assessment` of the *interpretation* it serves. It cuts **across** the
  timeline rather than sitting at one date, so it has **no year** and is **not** in the chronological
  list; instead it appears in an "Arguments" section on the summary page and an "Arguments"
  group in the index. Use it when a claim's interest is "does this argument hold up?" rather
  than "who held this, when?" Resolving a queued *argument* lead produces one of these pages (with the assessment), as opposed to flipping a
  witness's verified status. Skeleton: [`templates/argument.html`](templates/argument.html).
- **Argument group** = a *grouping convention* over two or more argument pages that share a single proof-text,
  mechanism, or theme and are best read as a set. It is **not** a new page type, has **no year**, and
  has **no file of its own** — nothing new on disk. *"Argument group" is the internal term* (slug, anchor
  `id="group-<slug>"`, these meta files); the **reader-facing label is "Related arguments"** — the group
  heading reads `Related arguments — <theme>` and the breadcrumb label is `Related arguments:`. An argument group is
  realized purely in visible content, in three places: (1) a wrapping `<h3 id="group-<slug>">` + framing
  `<p>` placed **first** in the home summary's "Arguments" section (above the standalone `<h3>`
  arguments, matching the index), with the members demoted from `<h3>` to `<h4>`; (2) an `<h4>` group in
  the index above a trailing unheaded `<ul>` of standalone arguments; (3) a `Related arguments:` breadcrumb on
  each member page linking the home-summary anchor and the sibling members. An argument has at most one home
  group (relations to others are `see also` links, not double-grouping); a one-member-per-side
  cross-doctrine pairing stays a `see also` pattern rather than a heading group. See `CLAUDE.md`
  ("Argument groups") for the full rules.

Copy the shape of the skeletons in [`templates/`](templates/); for a full, real worked example see the
nephilim doctrine — `docs/doctrines/nephilim.html` (summary timeline), its person-detail pages under
`docs/doctrines/nephilim/`, and its argument pages under `docs/doctrines/nephilim/arguments/`.

## 5. Page structure & citation conventions

There is no YAML frontmatter. Each page is a complete HTML document (copy the templates) whose
metadata lives in the **path** and the **visible content**:

- **Document wrapper** — `<!doctype html>` … `<head>` with `<meta charset>`, viewport, and a
  `<title>`; then `<body>`. No CSS/JS (bare HTML).
- **type** ← the path; **doctrine slug** ← the path; **person-slug** ← the filename.
- **Person-detail head line** carries the date, bio link, and back-link, then a one-line summary:
  ```html
  <p><strong>Dates:</strong> c. 220 · <a href="<wiki>">Wikipedia</a> · <a href="../baptism.html">back to timeline</a><br>
  <strong>Summary:</strong> …one or two sentences…</p>
  ```
  The visible `c. <year>` is the sort key; the summary timeline order is maintained **by hand**.
- **Argument head line** carries the assessment and proponent:
  ```html
  <p><strong>Type:</strong> supporting argument (off-timeline) · <strong>Assessment:</strong> sound · …</p>
  ```

**Citations.** Footnotes use the standard markup the existing pages already use (so numbering and
back-links work). Inline reference:
```html
…held that X.<sup id="fnref:tertullian-1"><a class="footnote-ref" href="#fn:tertullian-1">1</a></sup>
```
…with a matching `<li id="fn:tertullian-1">` in the page's Sources block (a
`<div class="footnote"><hr><ol>…</ol></div>`, see [`CLAUDE.md`](CLAUDE.md) for the exact shape).
- The visible footnote number is **sequential by first appearance** on the page; the `id` uses the
  person-slug (`<person-slug>-<n>`), so the two can differ — that is expected.
- Footnote target priority: (1) the primary `historicalchristian.faith` verse/work URL; (2) the
  person-detail page (which itself carries the primary links); (3) for **unverified** claims, the
  **secondary work** that asserted it — plus an inline `⚠ unverified` marker on the claim and a file
  in the [`todo/`](todo/) queue (never name the queue on a published page).
- Quote text on detail pages is **verbatim** from the DB (do not paraphrase inside `<blockquote>`).

**Slugs & dating.**
- `person-slug` = lowercased full name, spaces→hyphens (`Augustine of Hippo` → `augustine-of-hippo`).
  This matches the `Writings-Database` folder name (sans case/spaces) and is the page's filename.
- Dates: display with a `c.` prefix when uncertain (`c. 220`); for date ranges, sort by the earlier
  year. Dates come from `Writings-Database/<Name>/metadata.toml` (`default_year`). Figures **not** in
  the DBs (Aquinas, Luther, Calvin, modern theologians) are researched **once** and recorded in
  [`people.md`](people.md) so dating stays consistent.

## 6. Verification policy

| State | Meaning | What to do |
|-------|---------|-----------|
| **Verified** | A firsthand quote was located in the Commentaries/Writings DBs (or a directly-quoted primary text). | Cite the primary `historicalchristian.faith` URL. |
| **Unverified** | We only have a secondary work claiming the person believed it; no primary quote found yet. | Mark the claim `⚠ unverified`, cite the secondary work, add a file to [`todo/`](todo/). |

The goal over time is to convert unverified → verified by tracking down primaries. The `todo/` queue is
the backlog for that.

## 7. Operations

Adapted from [`llm-wiki.md`](llm-wiki.md). Inputs come in three flavors, all handled by the same
authoring process: **(a)** a secondary book/work asserting beliefs, **(b)** "mine the DBs for what
the fathers said on X", **(c)** an ad-hoc topic prompt.

### Authoring — turning a source into pages
1. **Identify** the doctrine(s) and extract every `(person, claim)` assertion from the source.
   Pick/confirm the doctrine `slug`. Note the doctrine's **key verses** (used for DB lookups).
2. **Date** each person: DB father → `Writings-Database/<Name>/metadata.toml` `default_year`;
   non-DB figure → research once and add to [`people.md`](people.md).
3. **Verify** each claim against the local DBs:
   - Search `Commentaries-Database/<Name>/` for the doctrine's key verses, and/or grep the
     father's `Writings-Database` HTML for relevant passages.
   - **Found** → capture the verbatim quote + `source_url` + `source_title`; build the link.
   - **Not found** → mark unverified, cite the secondary work, add a [`todo/`](todo/) file.
4. **Write the person-detail page** `docs/doctrines/<slug>/<person-slug>.html` — full quote(s),
   surrounding context, all links (copy [`templates/person-detail.html`](templates/person-detail.html)).
   If it exists, **append/merge** rather than overwrite.
5. **Update the doctrine summary page** `docs/doctrines/<slug>.html` — insert/merge the person's
   paragraph at the correct **chronological** position with footnote(s), and add the matching `<li>`
   to its Sources block. Re-order by hand if needed.
6. **Bookkeep** — add a line to `docs/index.html`; append a line to [`log.md`](log.md)
   (`## [YYYY-MM-DD] ingest | <source title>`); update [`todo/`](todo/).

**When a (person, claim) is really an *argument*** — a sub-claim whose interest is "does this argument hold
up?" rather than "who held it, when?" — don't force it onto the timeline. Instead write an **argument
page** (`docs/doctrines/<slug>/arguments/<arg-slug>.html`, skeleton
[`templates/argument.html`](templates/argument.html)): state the claim and its proponent-lineage,
marshal the strongest case, weigh it adversarially, and render an `assessment` of the interpretation.
Then surface it in the summary's "Arguments" section + the index's "Arguments" group
(not the timeline), and flag any part the proponent overstates on their own detail page. Resolving a
queued argument lead produces one of these (with an assessment), not a flipped verified status.

**When a new argument shares a proof-text, mechanism, or theme with existing arguments**, file it into that
**argument group** rather than leaving it standalone: group it with its siblings under the
`<h3 id="group-<slug>">` heading on the summary and the `<h4>` group in the index (both labelled
`Related arguments — <theme>`), and add the `Related arguments:` breadcrumb (linking the home-summary anchor +
siblings) to it and to the siblings. If the shared theme has only just reached **two** members, promote
it from standalone arguments to an argument group (coin a slug + reader-facing display name, wrap both members,
re-sequence footnotes by first appearance). One home
group per argument; cross-group relations are `see also` links, not double-grouping.

### Query — answering a question against the wiki
Read `docs/index.html` → open the relevant doctrine page(s) → synthesize a cited answer. Good
answers worth keeping get **filed back** as a new page and indexed.

### Lint — periodic health check
Look for: claims on summary pages **missing footnotes**; broken footnote `<sup>`/`<li>` id pairs;
contradictions between pages; people in detail pages **missing from the summary timeline** (or out of
date order); orphan detail pages with no inbound link; relative links that 404; unverified items
lingering in `todo/`; doctrines that should exist but don't. For **argument pages**: each has an
assessment; is linked from both the summary's and the index's "Arguments" section (not the
timeline); any proponent overstatement is reflected as a flag on that proponent's detail page; and it
carries **no year/date** on the timeline. For **argument groups**: every grouped argument group has ≥ 2 members on
its home summary, and each member appears under exactly **one** `<h3 id="group-…">` group (no
double-grouping); each grouped member carries a `Related arguments:` breadcrumb whose anchor
(`../../<doctrine>.html#group-<slug>`) resolves to an existing `<h3 id="group-<slug>">` and whose
sibling links all resolve; summary and index **agree on membership** (same args grouped the same way);
footnote `<sup>`↔`<li>` integrity holds after any re-sequencing; and no standalone argument is silently
dropped from a summary or the index.

## 8. Glossary of conventions (quick reference)
- **doctrine slug** — short, lowercased, hyphenated (`lords-supper`, `infant-baptism`); the path stem.
- **person-slug** — lowercased full name, spaces→hyphens; mirrors the `Writings-Database` folder; the
  page's filename.
- **footnote id** — `fn:<person-slug>-<n>` / `fnref:<person-slug>-<n>`; visible number sequential.
- **dates** — `c.` prefix in prose when uncertain; earliest-first ordering on every summary page,
  maintained by hand.
- **book names** — KJV spellings from `Commentaries-Database/book_names.json`.
- **quotes** — verbatim on detail pages; never paraphrase inside `<blockquote>`.
- **date stamp** — use the real current date for `log.md` entries.

## 9. Status / publishing
The wiki is served as static HTML from `docs/` via GitHub Pages (Settings → Pages → Source =
*Deploy from a branch*, branch `master`, folder `/docs`; a `.nojekyll` file keeps the HTML raw). The
first worked doctrine — the nephilim / "sons of God" timeline — is complete, and several more doctrines
have since been built out (see `index.html` for the live set). Future work (out of scope for now): a
search/CLI tool over the wiki, and optional styling.
This project began as Markdown rendered to HTML; it is now authored directly in HTML and the Markdown
source has been retired (see `log.md`).
