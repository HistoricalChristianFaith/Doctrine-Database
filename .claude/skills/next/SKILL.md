---
name: next
description: Work the next pending lead in the ledger's todo/ queue (earliest timestamp filename first) under the ledger's neutral-voice rules, then delete the lead and log the outcome. Handles primary-hunt, coverage, ledger-gap and ledger-polish (tradition-review findings), dispute, correction and new-topic leads, plus older leads written for the earlier evaluative format. Use when the user invokes /next or asks to work the next lead in the queue.
---

Work exactly **one** lead from `todo/`, under the rules in `CLAUDE.md`. Read `CLAUDE.md` first if it is not
already loaded this session.

## 1. Pick the lead

```
ls todo/*.md 2>/dev/null | grep -v '/README.md$' | sort | head -1
```

If nothing comes back, the queue is empty: say so and stop. Only this file is in play. New leads may appear
while you work; leave them alone.

## 2. Orient

- Read the lead in full, then the pages it names **as they now stand**. Pages change after leads are written:
  the problem may already be fixed, partly fixed, or moved. Check before editing.
- Ignore any pointer in a lead to internal run reports or other private files; the lead's own text is meant to be
  self-contained. If it is not enough to act on, look the pages and sources up yourself.
- A lead's suggested fix is a suggestion, not an instruction. Verify everything against sources you open.

## 3. Act, by lead type

- **Ledger gap** (`…-ledger-gap-<n>.md`, a must-fix finding from a Catholic, Orthodox or Protestant review).
  Confirm the problem on the current page. If it stands, fix it: add the missing reading or holder, re-attribute
  the claim, remove the verdict or rebuttal device, correct the fact. Use only sources you opened, copy new
  quotations verbatim, and apply the **balance guard**: if you add one tradition's argument against another's
  position, that tradition's own ground on the point must be on the page too, or leave the argument out. Log a
  verified factual fix in `corrections.md`. If the problem is already gone, say so in the log. If the fix needs a
  source you cannot reach, follow §5.
- **Ledger polish** (`…-ledger-gap-should.md`, a numbered bundle of should-fix findings). Work every item the same
  way. Record each item as fixed, already fixed, or declined (with the reason) in the log entry; the file is then
  deleted as one lead.
- **Coverage** (`…-coverage.md`, a timeline gap). Research the candidate witnesses from every side the lead names,
  and others you find, opening each source. Add each witness you can verify as a person page plus a footnoted
  timeline block at its date, earliest first, under the neutral-voice rules. A witness you cannot verify from an
  opened source stays off the page (or, if a secondary source you opened reports them, goes in as `⚠ unverified`
  with that source cited). Add witnesses from every side the gap concerns, not only the one that is missing, if
  the record calls for it. If only some candidates could be done, write one new lead for the rest.
- **Primary-hunt.** Find the primary in the source databases or an open online edition. Found: quote it verbatim,
  cite and link it, and remove the `⚠ unverified` marker. Not found after real effort: leave the marker, and say
  in the log where you looked.
- **Dispute** (a documented disagreement about how to read the record). If named proponents on more than one side
  can be cited from opened sources, add a reading to the existing interpretation page for that question, or create
  one from `templates/interpretation.html` and surface it in the timeline's Disputed readings section and on the
  index. A short dispute may instead go inline in the timeline entry, attributed on both sides.
- **Correction.** Verify against the source; fix; log it in `corrections.md`.
- **New topic.** A spine lead for a new doctrine timeline: build the timeline and person pages from the
  templates, earliest extant attestation first, with balanced witnesses; add the doctrine to `docs/index.html`
  under the right family and its `DOCTRINE_NAMES` entry in `docs/toc.js`. Supporting leads for the same topic
  that say "do not action until …" are re-queued (renamed with a later timestamp) if what they depend on does not
  yet exist.
- **Older leads written for the earlier evaluative format.** Some leads predate the ledger and ask for an
  "argument page", an assessment or rating, a "harvest" scan, a granted premise or held presupposition, or a
  scenario. Translate them; never carry the evaluation over:
  - an argument about **how to read a historical text, witness, date or authorship**, with named holders on more
    than one side → treat it as a dispute lead;
  - an argument about **whether a doctrine is true**, or an apologetic, scientific or speculative claim → out of
    scope: delete the lead and log it as out of scope for the ledger;
  - a witness or source to add → treat it as a coverage or primary-hunt lead, written neutrally;
  - a **harvest** lead → survey the named area for witnesses and disputes the pages mention but don't yet carry,
    and write one new lead per item (coverage, primary-hunt or dispute), each self-contained;
  - a lead aimed at a topic the ledger does not carry (check `docs/doctrines/`) → a new-topic lead only if the
    subject is a belief or practice whose history can be told as a timeline of witnesses; otherwise out of scope.
  Any wording in the lead that rates, assumes a premise, or tells you which reading is right is ignored.

Whatever the type: no ratings, verdicts, hindsight or narrator rebuttals; every dispute attributed; at most four
inline `Held by:` names with a one-sentence summary per reading; quotes verbatim from an opened source; scholars
before popular writers, with the "academic literature … was not located" note where none could be opened. Never
mention `todo/` or other bookkeeping on a published page.

## 4. Check

```
python3 -I scripts/ledger/lint.py <files you touched>
python3 -I .claude/skills/footnote-check/check.py <files you touched>
```

Lint 0 errors (judge each warning), footnote-check 0 errors, every relative link you added resolves, every new
quotation is verbatim from its cited source. If you added or rewrote a reading, or edited a contested topic's
timeline, run the `tradition-review` skill on the touched files and apply its must findings before finishing.

## 5. Blocked on a source

Exhaust workarounds first (other editions, archive.org, Google Books, other sources that suffice). If none works,
drop a request in `human_todo/` (same filename convention) naming the exact document, what it is needed for, and
the page it would support. Do what you can without it; the lead still ends as below, with the log noting the
human request.

## 6. Finish

1. **Log.** Append to `log.md`: `## YYYY-MM-DD — <slug>: <what was done>` (real date from `date`), then a few
   lines: the lead's filename, what changed, the files touched, sources opened, anything declined or left open,
   and any new leads or `human_todo/` requests written.
2. **Commit** the page changes (and `corrections.md`, `people.md`, if touched), naming paths explicitly:
   `git add -- <paths>` then `git commit -m "…" -- <paths>`. Never `git add -A` or `git commit -a`; if
   `index.lock` exists, wait and retry. Use a plain, specific message. Do not push. If nothing on a tracked file
   changed (an out-of-scope or already-fixed lead), there is nothing to commit.
3. **Delete the lead file** (`rm todo/<file>.md`). `todo/` and `log.md` are git-ignored, so the deletion and the
   log entry won't show in `git status`; do both explicitly.
