# Contributing to Doctrine Across Time

Thank you for helping. This ledger records who said what about Christian doctrine, and when, so that readers of
every tradition can check the record for themselves. Contributions from anyone are welcome, whatever their
tradition, as long as they follow the rules below. [`CLAUDE.md`](CLAUDE.md) is the full rule sheet; this file is
the short version.

## What is welcome, and what is not

**Welcome:**
- correcting a quotation, a date, a citation, an attribution or a broken link;
- adding a missing witness to a timeline, with a primary source;
- adding a reading to a disputed question, or proposing a new disputed question, when named scholars or
  traditions actually hold the reading and you can cite them;
- replacing a `⚠ unverified` claim with the primary source that confirms it (or showing it is wrong);
- linking a citation to an open online copy.

**Not accepted:**
- arguments for or against a doctrine, ratings, or conclusions about which reading is right;
- apologetics or polemics from any side;
- content that only an unnamed "some scholars" hold;
- quotations or page numbers you have not checked yourself.

## The neutrality rules in brief

1. **Earliest extant attestation, not "the first".** Say "the earliest surviving text to state X is …". Absence
   from the surviving record is not evidence of absence.
2. **Report, don't grade.** No verdict words in the site's own voice: proves, refutes, debunks, clearly, wrong,
   overstates, misreads, "the stronger reading", "on balance", and no rating words (sound, plausible, weak,
   unsupported, or contested as a verdict). They are fine inside quotations and in attributed reports ("Aland
   judged the text indecisive").
3. **Name both sides.** "A (tradition or scholar, work, year) holds P; B holds Q", with a footnote for each. Never
   "scholars disagree" or "most scholars" without names or a cited survey.
4. **State every reading at its strongest, as its holders would,** and decide none. Readings go in order of
   their earliest named proponent, and no reading is written as a rebuttal of another.
5. **Hold no premises.** Report what a source reports ("Eusebius records that …"), neither endorsing nor
   discounting it.
6. **No hindsight.** A witness doesn't "anticipate" or "lay the seed of" a later teaching; later uses are
   reported as dated events of their own.
7. **No narrator rebuttals.** Don't follow a scholar's view with "in fact …" or "yet …". If the counter-point has
   a holder, it belongs in that holder's reading.
8. **Balance.** Use each communion's own names for itself and its teaching. No "Rome added …" or "the Reformers
   restored …" framing, and no "the Church" when one communion is meant. "Heretic" and "orthodox" are never the
   site's own labels.
9. **Scholars first.** Prefer academic historians, exegetes and confessional documents to popular apologists. If
   a reading's only holders you can find are popular writers, say that its academic literature was not located.
10. **Keep it readable.** On a disputed-question page each reading opens with a one-sentence summary, its
    `Held by:` line names at most four people inline (others go in the footnote), and its case runs to about 350
    words.

## The source standard

- **Primary first.** Cite the text itself, quoted **verbatim** and linked. Never paraphrase inside a
  `<blockquote>`, and never shorten a quotation.
- **Link what you cite.** Prefer open, stable copies: historicalchristian.faith verse and work pages,
  public-domain editions, archive.org, Google Books, open journals, official church documents. A bare
  bibliographic citation is acceptable only when no online copy exists.
- **Only what you opened.** Cite only sources you actually read and confirmed say the thing. If you know a claim
  only from a secondary source, mark it `⚠ unverified` and cite that secondary source.
- **Wikipedia** is used only as a biography link, never as the source for a claim about what someone taught.

## How to cite

Inline reference (the visible number runs 1, 2, 3 … in order of first appearance; the id uses the person's slug,
or `arg-<page-slug>` on a disputed-question page):

```html
…held that X.<sup id="fnref:tertullian-1"><a class="footnote-ref" href="#fn:tertullian-1">1</a></sup>
```

Matching entry in the page's `Sources` block:

```html
<li id="fn:tertullian-1">
<p><a href="https://historicalchristian.faith/by_father.php?file=Tertullian%2FOn%2520Baptism.html">Tertullian, <em>On Baptism</em> 18</a>&#160;<a class="footnote-backref" href="#fnref:tertullian-1" title="Jump back to footnote 1 in the text">&#8617;</a></p>
</li>
```

- Citing the same source again: use `fnref2:tertullian-1`, then `fnref3:…`, all pointing at `#fn:tertullian-1`,
  and add one backref per use to its `<li>`.
- Two references side by side are separated by `<sup>,</sup>`.
- **Verse pages:** `https://historicalchristian.faith/<book>/<chapter>/<verse>`, book lowercased with no spaces
  (`john/3/5`, `2thessalonians/3/12`).
- **Works of the Fathers:** `https://historicalchristian.faith/by_father.php?file=<Father>%2F<Work>.html`, with
  `/` written `%2F` and spaces written `%2520`.

## Quick paths

- **Fix a quotation or citation.** Edit the HTML and say in the pull request which source you checked it
  against (with the link).
- **Fix a date.** Cite your source. For a figure not in the source databases, update [`people.md`](people.md)
  too.
- **Add a witness.** Copy [`templates/person-detail.html`](templates/person-detail.html) to
  `docs/doctrines/<slug>/<person-slug>.html`, then add a footnoted block to the timeline at its date, earliest
  first.
- **Add a reading or a disputed question.** Follow
  [`templates/interpretation.html`](templates/interpretation.html). Each reading needs named, footnoted holders.
- **Report a problem without editing.** Open an issue: *Correction*, *New witness* or *New reading*.

If you find a missing work or a transcription error in the source texts themselves, open an issue on
[Writings-Database](https://github.com/HistoricalChristianFaith/Writings-Database) or
[Commentaries-Database](https://github.com/HistoricalChristianFaith/Commentaries-Database).

## Running the checks

Both checks need only Python 3, with no packages. Run them on the files you changed (or on `docs`):

```
python3 -I .claude/skills/footnote-check/check.py docs/doctrines/<slug>.html docs/doctrines/<slug>
python3 -I scripts/ledger/lint.py docs/doctrines/<slug>.html docs/doctrines/<slug>
```

- **footnote-check** must report 0 errors. It catches refs without sources, sources without refs, broken
  numbering and backrefs.
- **lint** must report 0 errors. Its warnings flag words such as "contested" or "orthodox" that are often fine
  in plain English; check each one, and leave it only if it is a plain-English use or an attributed report.

The same checks run automatically on every pull request.

## Using an AI agent

You are welcome to work with an AI agent. Point it at [`CLAUDE.md`](CLAUDE.md) and require it to:
- open every source it cites, and quote verbatim from the text it opened;
- never invent a URL, page number, name or quotation;
- mark anything it could not confirm `⚠ unverified`;
- run both checks;
- list in the pull request the sources it actually opened.

You are responsible for what you submit, whoever drafted it.

## Pull request checklist

- [ ] footnote-check and lint report 0 errors
- [ ] every new or changed quotation matches the linked source, word for word
- [ ] no rating or verdict words in the site's own voice
- [ ] every dispute is attributed to named parties, with footnotes
- [ ] timelines stay in date order, earliest first
- [ ] no mention of internal files or bookkeeping on published pages
- [ ] the pull request lists the sources you opened

## Review

A maintainer checks each new or changed quotation against its source before merging. Changes that add or
rewrite a reading, or touch a contested topic, are also read from Catholic, Orthodox and Protestant points of
view, to make sure each tradition would find the page fair. A verified factual correction gets a line in
[`corrections.md`](corrections.md). Your credit is kept in the git history.

## License of contributions

The ledger is dedicated to the public domain under [CC0 1.0 Universal](LICENSE). By submitting a contribution you
confirm that you have the right to do so, and you dedicate your contribution to the public domain under the same
CC0 1.0 terms. The dedication covers your own writing; quotations you include from other works keep their own
status and must be short, cited quotations.
