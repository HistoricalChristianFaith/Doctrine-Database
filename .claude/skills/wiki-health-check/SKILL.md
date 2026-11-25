---
name: wiki-health-check
description: Do a consistency pass over the whole ledger (or one doctrine) — run the neutral-voice lint and the footnote check, then look for cross-page inconsistencies (conflicting dates, quotes or attributions, timeline order, broken or non-reciprocal links, index-vs-timeline drift, orphaned pages, plumbing leaks) and for coverage gaps worth queuing as todo/ leads. Use when the user invokes /wiki-health-check, or asks for a ledger audit, consistency pass or "anything worth researching" sweep.
---

A survey-and-report pass over the ledger. It **finds inconsistencies** and **queues research leads**. It does not
author pages, it does not judge any reading, and it does not commit unless the user asks. Everything below is a
check against the rules in `CLAUDE.md`; read that file first.

`$ARGUMENTS` sets the scope: empty for all of `docs/`, or a doctrine slug for `docs/doctrines/<slug>.html` plus
`docs/doctrines/<slug>/`. For a whole-site pass, fan out with subagents (one per concept family or per check) and
keep their conclusions, not their file dumps.

## 1. Run the mechanical checks

```
python3 -I scripts/ledger/lint.py <scope>
python3 -I .claude/skills/footnote-check/check.py <scope> --errors-only
```

- **Lint errors** are always findings. **Lint warnings** need a judgement: a plain-English "contested" or an
  attributed "Aland judged it weak" is fine; a narrator's verdict is not. Report only the warnings you judge to be
  real problems, with the line.
- **Footnote errors** are findings; leave the repairs to `/footnote-check` unless they are trivial.
- **Broken relative links.** Check that every relative `href` in scope resolves:

  ```
  python3 -I - <<'EOF'
  import os, re, sys
  bad = 0
  for d, _, fs in os.walk("docs"):
      for f in fs:
          if not f.endswith(".html"): continue
          p = os.path.join(d, f)
          doc = re.sub(r"<!--.*?-->", "", open(p, encoding="utf-8").read(), flags=re.S)
          for h in re.findall(r'href="([^"#:]+)(?:#[^"]*)?"', doc):
              if not os.path.exists(os.path.normpath(os.path.join(d, h))):
                  bad += 1; print(f"{p}: {h}")
  print(bad, "broken")
  EOF
  ```

## 2. Consistency checks (things that are wrong and should be reconciled)

- **Dates and order.** A person's `Dates: c. <year>` against their slot on the timeline (earliest first), against
  `people.md` or `default_year` in the database's `metadata.toml`, and against the same person's page under
  another doctrine.
- **Quotes and attributions.** The same passage quoted differently in two places, or attributed to different
  works, editions or authors. Check against the cited source before saying which is right.
- **Readings across pages.** A scholar or tradition filed under one reading on an interpretation page and
  described as holding the opposite on a person page or timeline entry; a timeline blurb that summarizes an
  interpretation page with only some of its readings, or in one side's terms; a `Held by:` name with no footnote.
- **Index ↔ timeline drift.** Every doctrine on the index has a timeline, and every timeline is on the index under
  its family; every interpretation page listed in a timeline's Disputed readings section is listed on the index
  and vice versa, with the same question as link text; no index entry carries a rating, verdict or count.
- **Clusters and breadcrumbs.** `Related doctrines:` lines are reciprocal and match the family on the index;
  `Related readings:` links resolve; every doctrine has its `DOCTRINE_NAMES` entry in `docs/toc.js`.
- **Orphans.** A person or interpretation page linked from no timeline; a timeline not reachable from the index.
- **Plumbing leaks.** A published page that mentions `todo/`, `log.md`, `people.md`, the rule files, or the
  source databases as infrastructure; a timeline claim with no footnote.
- **Leftovers of the evaluative format.** Any rating, assessment line, premise or presupposition banner,
  "What holds" or "What is overstated" heading, scenario table, or "on balance" conclusion (the lint catches most
  of these; also look for paraphrases it misses, such as "the likelier reading" or "this cannot bear the weight").

For each finding give the pages, quote the conflicting text, and propose the minimal fix. **Mechanical,
unambiguous fixes** (a broken relative link, a missing `DOCTRINE_NAMES` entry, a non-reciprocal breadcrumb, a
timeline entry out of date order) you may apply directly, following the hard rules, then rerun both checks on the
files you touched. **Substantive questions** (which of two dates is right, whether a quote is accurate, how a
reading should be put) become `todo/` leads, not silent edits. Never resolve a dispute between readings.

## 3. Coverage checks (things worth researching)

- **Tradition balance on a timeline.** Witnesses that skew to one tradition's genealogy (for example, no Catholic
  or Orthodox witness after a given century, or no Syriac, Coptic or Armenian witness where the record has them).
- **Missing standard readings.** An interpretation page on which a tradition with a stake has no reading, or only
  ancient witnesses and no modern scholar, or only popular holders without the "academic literature not located"
  note.
- **Shared witnesses.** A writer on one timeline who wrote on a neighbouring doctrine but is absent there.
- **`⚠ unverified` claims** whose primary looks locatable (a primary-hunt lead).
- **Long silences** on a timeline that the record does not explain.

## 4. File the leads

One `todo/` file per lead, named `YYYY-MM-DD-HHMM-<slug>.md` with the real time from `date` (stagger the minutes so
they sort). Check `ls todo` first so you don't duplicate a pending lead. Each file says what is missing and why,
which pages raised it, the lead type (primary-hunt, coverage, correction, dispute), and candidate witnesses or
sources from every side, each marked opened or unverified. Point at sources; don't dictate the edit.

## 5. Report

A tight summary: the check results (lint errors, footnote errors, broken links); inconsistencies grouped by
severity, each marked fixed (mechanical) or filed (substantive), with every file you edited; the leads filed, one
line each; and any judgement calls for the user. If you edited pages, append a `log.md` entry. Don't commit unless
asked.
