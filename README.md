# Doctrine-Database

A wiki tracking **how Christian doctrines developed across time**. For each doctrine, a single
timeline page shows — earliest first — what each figure believed, with **every claim footnoted**
to a primary source.

It is built and maintained by an LLM agent following the pattern in [`llm-wiki.md`](llm-wiki.md),
grounded in two sibling databases (`~/Desktop/Commentaries-Database`, `~/Desktop/Writings-Database`)
and `historicalchristian.faith`.

The wiki is a set of **hand-authored static HTML files** under [`docs/`](docs/), served as-is by
GitHub Pages — no build step, no Markdown, no Jekyll.

## Start here
- **[`project.md`](project.md)** — the full brief (concept, data formats, citation rules, authoring process).
- **[`CLAUDE.md`](CLAUDE.md)** — terse operating rules loaded each session.
- **[`docs/index.html`](docs/index.html)** — catalog of all pages (the site home page).

## Layout
```
docs/                                   the published site (GitHub Pages source = /docs)
  index.html                            catalog of all pages
  doctrines/<slug>.html                 summary timeline (1 footnoted block per person)
  doctrines/<slug>/<person>.html        detail page (full quotes + context + links)
  doctrines/<slug>/arguments/<arg>.html argument/crux page (one sub-claim → assessment; off-timeline)
templates/                              HTML page skeletons
log.md  TODO.md  people.md              meta files (not served)
```

Three page types: **doctrine** (the timeline), **person-doctrine** (a witness's detail page, placed by
date), and **argument** (a single sub-claim adduced for a reading — proof-text, parallel, or historical
thesis — weighed adversarially and given an `assessment` of the interpretation; it cuts *across* the
timeline, so it lives in the summary's "Arguments & cruxes" section rather than the chronological list).

See the worked example: the nephilim doctrine — [`docs/doctrines/nephilim.html`](docs/doctrines/nephilim.html)
(summary timeline), its detail pages under [`docs/doctrines/nephilim/`](docs/doctrines/nephilim/), and its
argument pages under [`docs/doctrines/nephilim/arguments/`](docs/doctrines/nephilim/arguments/).

## Publishing
GitHub Pages serves the `docs/` folder directly (Settings → Pages → Source = *Deploy from a branch*,
branch `master`, folder `/docs`). A `.nojekyll` file tells Pages to serve the raw HTML untouched.
