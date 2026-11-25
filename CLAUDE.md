# CLAUDE.md: rules for the Doctrine Across Time ledger

This is the rule sheet every agent and maintainer loads each session. Outside contributors should also read
[`CONTRIBUTING.md`](CONTRIBUTING.md). Where the two differ, this file is the fuller statement of the same rules.

## What this site is

**Doctrine Across Time** is an ecumenical historical ledger of Christian doctrine. For each doctrine it records
who said what, when and where, **earliest extant attestation first**, with **every claim footnoted** to a source
the reader can open. Where the reading of a historical text is disputed, it gives every reading in the form its
own proponents would endorse, names those proponents, and **never judges between them**. It is written so that
Catholic, Orthodox and Protestant readers (and Oriental Orthodox, Assyrian, Jewish and critical-scholarly
readers where they have a stake) can all trust it.

**What it is not.** It does not rate arguments, decide disputes, defend or attack a doctrine, or hold any
premise. There are no ratings, verdicts, assessments, "granted premise" or "presupposition" banners, scenario
comparisons, worldview narratives or apologetic argument pages, and none may be added, even in passing prose.
Doctrinal or scriptural argument (is the doctrine true? does this verse teach it?) is out of scope except as
reported history: who argued it, when, in what words.

The site is **hand-authored static HTML** under `docs/`, served as-is: no build step, no Markdown, no
templating. You edit the `.html` files directly. The text is dedicated to the public domain under CC0 1.0
([`LICENSE`](LICENSE)); quoted sources keep their own status.

## Layout

```
docs/                                  the published site (the only folder that is deployed)
  index.html                           home page and catalog: concept families (<h2 id="family-…">), each
                                         doctrine an <h3 id="<slug>"> linking its timeline, a one-paragraph
                                         neutral description, then its interpretation pages listed by their
                                         questions. No ratings, no counts, no person-page list.
  doctrines/<slug>.html                timeline page (one footnoted block per witness)
  doctrines/<slug>/<person>.html       person page (the evidence: full quotes, context, links)
  doctrines/<slug>/arguments/<q>.html  interpretation page (one disputed question, all its readings)
  style.css, toc.js                    the one stylesheet and the one script
templates/                             skeletons for the three page types
scripts/ledger/lint.py                 the neutral-voice lint
.claude/skills/                        agent skills (footnote-check, wiki-health-check, tradition-review, next)
.github/                               CI on pull requests, issue and PR templates, the deploy workflow
CLAUDE.md  CONTRIBUTING.md  README.md  LICENSE
people.md                              dates and slugs for figures not in the source databases
corrections.md                         one line per verified factual correction (append only)
log.md  todo/  human_todo/             operator bookkeeping, git-ignored (on disk only)
```

Only `docs/` is reader-facing. Everything else is for maintainers. The `arguments/` folder name is historical;
the pages in it are interpretation pages. Keep their filenames: inbound links depend on them.

**Serving and deploy.** A push to `master` runs `.github/workflows/main.yml`, which copies `docs/` to the web
host over FTPS. Commentaries-Interface's `doctrine-render.php` serves those files on historicalchristian.faith
under `/doctrine/`, each as a standalone page. Pull requests run the checks in `.github/workflows/ci.yml`. Never
push from an agent session; commit locally and leave pushing to the owner.

## Page types

1. **Timeline page** (`docs/doctrines/<slug>.html`, [`templates/doctrine.html`](templates/doctrine.html)). A
   neutral intro naming each communion's position in its own terms; an optional `Related doctrines:` line; a
   `Timeline` of `<h3>` witness blocks, earliest first, each 2–5 footnoted sentences with the witness's name
   linked to their person page; an optional `<h2 id="disputed-readings">Disputed readings</h2>` section; and
   `Sources`.
   - **Disputed readings section.** A one-sentence neutral intro, then each interpretation page as an `<h3>` (or
     an `<h4>` under a plain themed `<h3 id="group-<theme>">`, groups first) whose link text is the page's
     question, followed by a short neutral blurb ending in a footnote that links the page. No verdict
     parentheticals.
   - A short dispute can sit inline in a timeline entry ("identified as X by A; as Y by B", both footnoted). A
     longer one gets an interpretation page, and the entry says "how this passage is to be read is disputed;
     see [the page]".
2. **Person page** (`docs/doctrines/<slug>/<person-slug>.html`,
   [`templates/person-detail.html`](templates/person-detail.html)). The head line
   `<strong>Dates:</strong> c. <year> · <a href="…">Wikipedia</a><br><strong>Summary:</strong> …`, then
   `Claims & evidence` (an `<h3>` per claim that *describes* the passage, never argues; a verbatim
   `<blockquote>`; the `— <em>source</em>, <a href="…">source</a>.` line), then an optional neutral section
   such as `Reception and debate` or `Placement on the timeline` in which every view is attributed. One page per
   (doctrine, person). The year on the `Dates:` line is the timeline sort key.
3. **Interpretation page** (`docs/doctrines/<slug>/arguments/<q>.html`,
   [`templates/interpretation.html`](templates/interpretation.html)). See the next section.

**Timeline variants.** These reuse the timeline and person page types unchanged:
- **Relationship topic:** the subject is a relationship between two people (e.g. `origenist-controversy`,
  `jerome-augustine`). Timeline entries are dated events (`<h3>Jerome settles at Bethlehem (386)</h3>`), both
  parties get a person page with life-span dates (`c. 347&ndash;420`), and the intro says the timeline is told
  through dated moments.
- **Biographical tradition timeline:** the subject is a figure (e.g. `apostle-peter`, slug `apostle-<name>`);
  the witnesses are the datable sources that report on him, earliest source first.
- **Reception history:** the subject is the church's judgement on a person (e.g. `origen-condemnation`); the
  witnesses are dated judgements and documents (synods, treatises, edicts, anathemas, modern monographs),
  reported as events.

**Doctrine clusters.** A concept family on `docs/index.html` with two or more doctrines is a cluster. Each member
timeline carries, directly under its intro and before the first `<h2>`, a line
`<p><strong>Related doctrines:</strong> <em>Family name</em> — see also <a href="sibling.html">…</a> · …</p>`
naming every other member. The family label is plain `<em>` text, not a link. The index is the only roster:
when a family grows to two members, add the line to both; when a doctrine joins, add it to every sibling.

## Interpretation pages

One page per disputed question, with **all** its readings on that page. (The ledger does not put rival readings
on separate pages.) In order:

1. **Title and `<h1>`:** the same neutral question, e.g. "Does Irenaeus's 'born again to God' (Adv. Haer.
   II.22.4) attest infant baptism?" It states no claim and builds in no premise.
2. **Meta line:** `<strong>Disputed reading</strong> · on <doctrine link> · witness(es): <person links>`, then an
   optional `<strong>Related readings:</strong>` line linking sibling pages that exist.
3. **The passage:** the disputed text verbatim in a `<blockquote>`, cited and linked.
4. **The question:** one or two neutral sentences, in terms every tradition involved would accept, saying what
   is disputed and why it matters historically. If a reading's only located holders are popular writers, say
   here that its academic literature was not located.
5. **Readings:** at least two `<h2 class="reading">` sections, ordered by the date of each reading's earliest
   named proponent. Each has, in this order:
   - a heading giving the thesis in its holders' terms, never an outcome;
   - a one-sentence plain summary, `<p><em>In brief: …</em></p>`;
   - `<p><strong>Held by:</strong> …</p>`: at most **four** principal proponents inline, each with tradition,
     work and year, footnoted; further names and qualifiers ("on the dating only", "as quoted by …") go in the
     footnote. With no named proponent in any source actually opened, the line is exactly
     `<p><strong>Held by:</strong> ⚠ unverified — no named proponent located yet.</p>`;
   - the case, stated positively as its proponents would put it, about 350 words, ending on the reading's own
     case (not on a quotation aimed at another reading, and not on a verdict-like sentence).
6. **Sources**, with ids `arg-<page-slug>-<n>`.

Readings should be of roughly equal length; the lint warns when one is more than twice another. Each tradition
with a stake should have its standard reading present, in its strongest form, with modern scholars as well as
ancient witnesses (the Orthodox as living interpreters, not only as Fathers). A tradition that holds the question
as posed is not decisive has that as its reading, sourced. A tradition sharing a reading joins its `Held by:` line
by name; a distinct reading gets its own section.

## Neutral voice (binding on every page, footnotes included)

1. **Earliest extant attestation, never "the first".** Write "the earliest extant text to state X is …".
   Absence from the surviving record is not evidence of absence. A scholar's "first" claim is reported as theirs
   ("Kelly regards this as the earliest …").
2. **Report; don't grade.** The narrator never uses the rating scale (sound, plausible, contested as a verdict,
   weak, unsupported) or verdict words: proves, refutes, debunks, clearly, wrong, mistaken, overstates, misreads,
   overreads, "the stronger/better/likelier reading", "on balance", "the evidence shows that …". No grading
   devices either: "even X", "X itself states", "of course", "plainly", "pointedly", "the decisive fact". No
   praise or blame of persons ("ablest") except as attributed quotation. These words may appear inside quotations
   and in attributed reports ("Aland judged the text indecisive").
3. **Attribute every dispute to named parties, with sources.** "A (tradition or scholar, work, year) holds P;
   B holds Q", footnoted on both sides. Never "scholars disagree", "has been read as", "historians reckon",
   "apologists" or "Rome" as an unnamed holder. "Most scholars" needs a cited survey or reference work that says
   so.
4. **Never settle a dispute.** Attribution, dating, identity, authenticity, meaning and reception disputes are
   reported with their parties: "identified as X by A; as Y by B". A disputed work sits at its conventionally
   cited date with the dispute noted. A claim that something "did not stand" or "took effect" needs a footnote or
   `⚠ unverified`.
5. **Hold no premises.** Report what sources report ("Eusebius records that …"), neither endorsing nor
   discounting it, miracles included. Never build a premise into a question, heading or sentence (e.g. "grounds it
   on tradition rather than Scripture" assumes a binary some traditions reject); where a tradition rejects a
   framing, give its framing as a reading. Never say *why* a writer held something except by attribution.
6. **No hindsight.** No witness "anticipates", "prefigures", "lays the seed of" or "stands behind" a later
   teaching, is "less developed", or is a "capstone"; nothing "would later" happen in a witness's own entry;
   traditions do not "converge" in one communion's dogma. Report later use as a dated event in its own entry
   ("Pius XII cited Germanus in 1950").
7. **No narrator rebuttals.** Don't follow a named scholar's view with "in fact …", "yet the text …",
   "nonetheless …" or "the canon itself …". If the counter-point has a holder, it goes in that holder's reading.
   Never describe a reading or its holders in their opponents' words; such phrases appear only as quotations
   inside the opponent's own reading.
8. **File scholars exactly.** Never list a scholar under a reading they reject. If they grant a point but reject
   the conclusion, say so: "(Jugie grants the documentary chain; grounds the doctrine theologically)".
9. **Tradition balance.** Use each communion's own self-designations. No "the Church" when a specific communion
   is meant; no "Rome added …" or "the Reformers restored …" framing. Include Greek, Latin, Syriac, Coptic and
   Armenian witnesses where the record has them. Where communions read a development differently, give each one's
   own account, attributed.
10. **People by dates, offices and works.** "Heretic" and "orthodox" are never the narrator's labels, and
    "saint" appears only as part of a conventional name or title ("Saint George", "St Paul's School").
    Condemnations are reported as events ("condemned by the Council of Constantinople, 553").
11. **No self-reference as authority.** Never "this wiki/site holds, rates, finds or does not discount". "This
    site" is for navigation only.
12. **Readability.** State a point once per page; don't follow a quotation with a sentence that only restates it.

## Sources and research

- **Cite only what you opened** and confirmed says the thing. Never add a name, work, page number, URL or
  quotation from memory, and never pad a page with names. A proponent you saw cited in an opened source but whose
  own work you could not open is named with that work, marked `⚠ unverified`, and footnoted to where you saw them.
- **Openly accessible sources.** Work from sources anyone can open: the source databases, public-domain
  editions, archive.org, Google Books previews, open journals, official church documents. A reading you cannot
  source that way stays `⚠ unverified` or carries the "academic literature not located" note in its question
  section; it is not filled in from memory.
- **Scholarly proponents first.** If a tradition's reading is held only by popular apologists, look for a
  scholarly holder in that tradition (academic historians and exegetes, confessional documents, faculty opinions).
  If none can be opened, keep the popular holders and add the "academic literature … was not located" note. Never
  set scholars on one side against only popular voices on the other without saying so. Prefer scholars to
  succession or martyrological compilations.
- **Quote proponents from their own work.** Keep and report any "as quoted by [opponent]".
- **Verified vs. unverified.** A claim backed by a firsthand quote you located is verified: cite the primary. A
  claim known only from a secondary report is marked `⚠ unverified` inline (person pages:
  `<h3>Claim — ⚠ unverified</h3><p>Asserted by <secondary work> that <person> held X. No primary source located
  yet.</p>`; footnotes: `… source title — ⚠ unverified.`), cites the secondary work, and gets a `todo/` lead.
- **Wikipedia** is a biography link on the `Dates:` line only, never the source for a doctrinal claim.

## Source databases

Prefer these over the web, but use the web too.
- `~/Desktop/Commentaries-Database/<Father>/<Book Ch_Vs>.toml`
  ([GitHub](https://github.com/HistoricalChristianFaith/Commentaries-Database)): `[[commentary]]` blocks with
  `quote`, `source_url`, `source_title`. Verse-oriented. A verse may sit in a **range-named** file
  (`Book 3_18-19.toml`), so glob the range too (`*/"1 Peter 3_1*.toml"`). Book spellings:
  `Commentaries-Database/book_names.json` (KJV names, no a/b sub-verses).
- `~/Desktop/Writings-Database/<Father>/<Work>.html`
  ([GitHub](https://github.com/HistoricalChristianFaith/Writings-Database)): full texts. Each father's
  `metadata.toml` has `default_year` (the timeline anchor) and `wiki` (the bio link).
- **Verse URL:** `https://historicalchristian.faith/<book>/<ch>/<vs>`, book lowercased with spaces removed
  (`john/3/5`, `2thessalonians/3/12`).
- **Work URL:** `https://historicalchristian.faith/by_father.php?file=<Father>%2F<Work>.html`, with `/` as `%2F`
  and spaces as `%2520` (`…?file=Tertullian%2FOn%2520Baptism.html` ↔ `Writings-Database/Tertullian/On
  Baptism.html`). This is the TOML `source_url`. **Read the text from the local file, never by fetching this URL**
  (the page does not serve the work body to a fetcher); the URL exists so pages can link the work.
- **A work outside the databases:** search the web for it and cite the online source like any other. Don't tell
  the reader it is "outside our corpus".
- **Source-database gaps → GitHub issue.** A missing work, a missing verse import, or an OCR or transcription
  error gets a concise issue on the relevant repo (`gh issue create -R HistoricalChristianFaith/<repo>`) with the
  gap and, if known, the correct text and source. Keep working from the web meanwhile.
- **Figures not in the databases** are dated once, by research, in [`people.md`](people.md), so every page agrees.

## HTML and footnote conventions

- **Wrapper:** copy a template. `<!doctype html>`, `<html lang="en">`, charset and viewport metas, `<title>`,
  `<link rel="stylesheet" href="…style.css">`, `<script defer src="…toc.js"></script>`. Both paths are
  **depth-relative**: `style.css` (index), `../` (timeline), `../../` (person), `../../../` (interpretation).
  Never root-absolute: the site is mounted under a subpath.
- **One stylesheet, one script.** No per-page CSS or JS. `toc.js` builds the table of contents from `h2`–`h4`
  (on the index, `h2`–`h3`) and the breadcrumb; don't author either. A new doctrine needs its
  `slug → display name` entry in `DOCTRINE_NAMES` in `docs/toc.js`.
- **Metadata is visible content and the path**, never hidden frontmatter: type and slug from the path,
  person-slug from the filename, year from the `Dates:` line, verified status from `⚠ unverified` markers.
- **Internal links are relative `.html`:** timeline → person `<slug>/<person>.html`; person → timeline
  `../<slug>.html`; interpretation → person `../<person>.html`; interpretation → timeline `../../<slug>.html`.
  Every relative link must resolve to an existing file.
- **Inline footnote ref** (the visible number runs 1..N by first appearance; the id uses the person-slug, or
  `arg-<page-slug>` on interpretation pages, so id and number may differ):
  `<sup id="fnref:<id>"><a class="footnote-ref" href="#fn:<id>">N</a></sup>`
- **Repeat citation** of one source: `fnref2:<id>`, `fnref3:<id>`, … each pointing at the one `#fn:<id>`, whose
  `<li>` carries one backref per occurrence. Never suffix ids like `-1b`.
- **Adjacent refs** are separated by `<sup>,</sup>` so they don't read as one number.
- **Sources block** at the foot, one `<li>` per note in order of first appearance:
  ```html
  <h2>Sources</h2>
  <div class="footnote">
  <hr>
  <ol>
  <li id="fn:<id>">
  <p><a href="<source URL>">source title</a>&#160;<a class="footnote-backref" href="#fnref:<id>" title="Jump back to footnote N in the text">&#8617;</a></p>
  </li>
  </ol>
  </div>
  ```
- **Footnote target priority:** the primary historicalchristian.faith verse or work URL; then the person page
  (which carries the primary links); for an unverified claim only, the secondary work.
- **Link every citation you have a URL for,** modern scholarship included, at the most specific stable target
  (an archive.org page, a Google Books page, a DOI). A bare bibliographic citation (author, title, publisher,
  year, page) is the fallback only when there is no findable online copy or no stable URL. Never present a page
  number you did not open as if it were checked.

## Hard rules

1. Timelines list witnesses **earliest year first**, order kept by hand; sort ranges by the earlier year, and use
   `c.` when uncertain.
2. **Every** claim on a timeline page ends in a footnote.
3. **Quote integrity.** Text inside `<blockquote>` or quotation marks that quotes a source is verbatim from that
   source: never paraphrased, shortened or "tidied". Change one only to fix a verified misquote, and log it in
   `corrections.md`. New quotations are copied from the source you opened and cite. Never change a citation URL
   unless it is broken and you verified the replacement.
4. `person-slug` = the lowercased full name with spaces → hyphens (mirroring the `Writings-Database` folder), and
   is the filename.
5. Adding to an existing page means **append and merge**, never overwrite.
6. **Preserve history.** Editing for neutrality removes only evaluation; every dated fact, quotation, witness,
   citation and attributed view stays. When unsure, keep the facts and drop only the judging words.
7. **No internal plumbing on reader-facing pages.** Never mention `todo/`, `log.md`, `people.md`, these rule
   files, or the source databases *as infrastructure* ("our corpus", "the database"). Cite the work and edition
   instead, and scope a negative claim as "surveyed here". Operator notes go in HTML comments.
8. **Corrections.** Fix a factual error (misquote, misattribution, wrong date, internal contradiction) only when
   you verified the fix against a source you opened, or the page contradicts itself and its own cited sources
   resolve it. Otherwise leave it, mark it `⚠ unverified` if unsourced, and report it. A reviewer's say-so is a
   lead, not verification. Append one line per fix to [`corrections.md`](corrections.md):
   `- YYYY-MM-DD <page>: <what was wrong> → <fix> (source: <source opened>)`.
9. Use the real current date (from `date`) in `log.md`, `corrections.md` and lead filenames.
10. Pages stay well-formed, with the existing wrapper and depth-relative asset links.

## Workflow

**Adding a witness or claim.**
1. Identify the doctrine and slug, the key verses, and each (person, claim) pair.
2. Date each person: `default_year` in the database's `metadata.toml`, or `people.md` (research once and add a
   row).
3. Verify each claim against the databases or an opened online source; capture the verbatim quote, URL and title.
   Not found: mark `⚠ unverified`, cite the secondary work, add a `todo/` lead.
4. Write or append the person page from the template.
5. Insert the footnoted block into the timeline at its chronological place, with matching Sources entries.
6. Touch `docs/index.html` only for a new doctrine (an `<h3 id="<slug>">` block under the right family `<h2>`; a
   new family needs its own `<h2 id="family-…">`) or a new interpretation page (an `<li>` whose link text is the
   page's question, with no verdict). Add the `DOCTRINE_NAMES` entry for a new doctrine.
7. Run the checks, append `log.md`, update `todo/`.

**Adding a disputed reading.** A dispute about how to read the historical record (a passage, a witness, a date,
an authorship or authenticity question) with named proponents on more than one side gets an interpretation page,
or a new reading on the existing page for that question. A dispute about whether a doctrine is true is out of
scope.

**Content from elsewhere.** Material brought in from another wiki, a book, a video or notes (including
evaluative research notes) is rewritten under these rules before it lands: ratings, premises, scenario
comparisons and syntheses never cross, every judgement is either attributed to a named source or dropped, and
every quote is re-checked against an opened source. The result passes the `tradition-review` skill before it is
committed. "Import X" means extract every lead from X into `todo/`, one file per lead, with the source links;
it does not mean authoring pages on the spot.

**Public pull requests.** Review against [`CONTRIBUTING.md`](CONTRIBUTING.md). CI must pass (lint with no errors,
footnote-check with no errors). Open the linked source for every new or changed quotation and confirm it is
verbatim before merging; never merge a page number presented as checked that nobody opened. Run
`tradition-review` on any change that adds or rewrites a reading, a timeline entry on a contested topic, or a
summary line. A correction that changes a fact gets its `corrections.md` line.

## Bookkeeping: todo/, human_todo/, log.md

All three are git-ignored and live on disk only. Never mention them on a published page.
- **`todo/`** is the queue of pending leads, one file per lead, named `YYYY-MM-DD-HHMM-<slug>.md`, processed in
  lexical (that is, chronological) order. It holds pending items only: when a lead is done, delete its file and
  record the outcome in `log.md`. Each file must be actionable without rereading where it came from. Lead types:
  **primary-hunt** (a secondhand claim needing a primary), **coverage** (a timeline gap: a missing tradition,
  period or major witness), **ledger gap** (a must-fix finding from a tradition review), **ledger polish** (a
  bundle of should-fix findings), **dispute** (a documented disagreement that may need an interpretation page or
  a new reading), **correction**, and **new topic**. The `next` skill works the queue. See `todo/README.md`.
- **`human_todo/`** is for sources an agent could not reach. First exhaust workarounds (other editions, web
  copies, other sources that suffice). Only then drop a request there, same filename convention, naming the exact
  document and where it is used; the owner fetches it and queues a fresh `todo/` lead.
- **`log.md`** is the append-only history: `## YYYY-MM-DD — <what was done>`, then what changed, the files
  touched, and anything declined or left open.

## Checks (run before every commit; CI runs the first two on pull requests)

```
python3 -I scripts/ledger/lint.py <files or dirs>          # neutral-voice lint; default is docs/
python3 -I .claude/skills/footnote-check/check.py <files or dirs>
```

- **Lint:** 0 errors. Errors are hard bans (rating labels, premise boxes, evaluative headings, unquoted verdict
  verbs, bold rating words, self-reference as authority, an interpretation page with fewer than two readings or a
  reading with no `Held by:` line). Warnings ("contested", "weak", "the first … to", "orthodox", unbalanced
  readings) need a judgement: leave only plain-English uses and attributed reports. Text in `<blockquote>`, `<q>`
  and HTML comments is exempt.
- **Footnote check:** 0 errors (see `.claude/skills/footnote-check/SKILL.md` for the codes). W1 (no source URL) is
  a prompt to find a link, never to invent one.
- **Links:** every relative `href` you added or touched resolves to an existing file.
- **Quotes:** every new or changed `<blockquote>` appears verbatim in the source it cites.
- **Fairness:** for contested content, the `tradition-review` skill (Catholic, Orthodox and Protestant reviewers).
  For a site-wide pass, `wiki-health-check`.

**Committing.** Stage paths explicitly (`git add -- <paths>`, deletions included); never `git add -A` or
`git commit -a`, since other sessions may be committing too. If `index.lock` exists, wait and retry. Messages are
plain and specific. Never push.
