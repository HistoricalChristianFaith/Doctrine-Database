# Doctrine Across Time

An ecumenical historical ledger of Christian doctrine. For each doctrine, a timeline records who said what,
when and where, **earliest extant attestation first**, with **every claim footnoted** to a source you can open.
Where the reading of a historical text is disputed, a separate page sets out each reading in the form its own
proponents would endorse, names those proponents, and does not judge between them.

The ledger takes no Catholic, Orthodox or Protestant side, and it rates nothing: no verdicts, no "stronger
reading", no premises held. It is meant to be equally trustworthy to readers of every tradition.

Read it at **https://historicalchristian.faith/doctrine/**.

## What is here

```
docs/                                  the published site
  index.html                           the catalog: doctrines grouped by family
  doctrines/<slug>.html                a doctrine's timeline
  doctrines/<slug>/<person>.html       one witness's evidence: full quotes, context, links
  doctrines/<slug>/arguments/<q>.html  one disputed question, with every reading and its proponents
  style.css, toc.js                    the one stylesheet and the one script
templates/                             skeletons for the three page types
scripts/ledger/lint.py                 the neutral-voice lint
.claude/skills/                        checks and workflows for AI agents
CLAUDE.md                              the full rule sheet (for maintainers and AI agents)
CONTRIBUTING.md                        how to propose a correction, a witness or a reading
people.md                              dates and slugs for figures not in the source databases
corrections.md                         the log of factual corrections
```

The site is hand-authored static HTML: no build step, no Markdown, no generator. Edit the `.html` files directly.

The primary texts behind most citations come from two sibling projects, also served on historicalchristian.faith:
[Commentaries-Database](https://github.com/HistoricalChristianFaith/Commentaries-Database) (patristic commentary
by verse) and [Writings-Database](https://github.com/HistoricalChristianFaith/Writings-Database) (full texts of
the Fathers).

## Contributing

Corrections, missing witnesses and documented readings are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for
the neutrality rules, the source standard and how to run the checks. To report a problem without editing, open
an issue using one of the templates.

Every pull request runs two checks (`.github/workflows/ci.yml`):

```
python3 -I .claude/skills/footnote-check/check.py docs
python3 -I scripts/ledger/lint.py docs
```

Both must report 0 errors. Lint warnings are for a human to judge and don't fail the run.

## How it is served and deployed

A push to `master` runs `.github/workflows/main.yml`, which uploads the contents of `docs/` (and nothing else) to
the web host over FTPS. There the historicalchristian.faith site (its `doctrine-render.php`, part of the
Commentaries-Interface project) serves each file as a standalone page under `/doctrine/`. Internal links and asset
paths are relative, so the tree works wherever it is mounted. There is no GitHub Pages deployment.

## License

The text of this site and repository is dedicated to the public domain under
[CC0 1.0 Universal](LICENSE). You may copy, modify and republish it, even commercially, without asking.

The dedication covers the site's own prose, page structure and code. It does not cover the sources it quotes:
quotations from modern translations and modern scholarship remain under their owners' copyright and are included
as cited quotation. Ancient and other public-domain texts remain in the public domain. By contributing, you
dedicate your contribution under the same terms (see [`CONTRIBUTING.md`](CONTRIBUTING.md)).
