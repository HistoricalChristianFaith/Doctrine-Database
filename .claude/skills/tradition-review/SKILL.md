---
name: tradition-review
description: Review ledger pages from three standpoints in turn (a Catholic, an Orthodox and a Protestant church historian), each judging whether their tradition would find the pages fair and complete, and return pass/fail verdicts plus must/should findings; optionally apply the fixes and re-review. Use when the user invokes /tradition-review, asks for a tradition or fairness review, or before committing new or rewritten readings, contested timeline entries, or content brought in from elsewhere.
---

The ledger must be trusted equally by Catholic, Orthodox and Protestant readers. This skill checks that, page by
page, from each side. It is **read-only** until the fix stage, and it never commits.

`$ARGUMENTS` sets the scope: a doctrine slug (the timeline, every interpretation page under it, and its most
contested person pages), a list of files, or "changed" (the files in `git diff --name-only HEAD -- docs` plus any
untracked pages under `docs/`). Add `fix` to apply the findings afterwards (stage 3).

## 0. Prepare

- Read `CLAUDE.md`, especially "Interpretation pages", "Neutral voice" and "Sources and research". That is the
  standard the reviewers apply.
- Read the pages in scope. For a doctrine: `docs/doctrines/<slug>.html`, every page in
  `docs/doctrines/<slug>/arguments/`, and at least five of the person pages most likely to be contested (all of
  them if fewer). Where the pages were recently changed, read `git diff HEAD -- <paths>` too, and compare with
  the earlier text (`git show HEAD:<path>`) where it helps.
- Check `ls todo | grep <slug>` so reviewers don't re-raise a coverage gap that already has a lead.
- Modify nothing and run no git command that changes state during stages 1 and 2.

## 1. Three reviewer passes

Run three passes, one per tradition, each as a well-informed church historian of that tradition. Use three
subagents in parallel if the scope is large (give each the scope, `CLAUDE.md`, and the instructions below), or do
them in turn yourself. Each reviewer gives:

- **A verdict**, pass or fail, with a one-sentence reason. **Pass** means a well-informed scholar of that
  tradition would find the pages fair and, where the tradition has a stake, would recognize its readings as put
  strongly and accurately. A tradition with no stake in the topic passes if nothing misrepresents it.
- **Findings**, at most 12 per review overall, most important first.

Each reviewer checks explicitly:
- **Completeness.** Where its tradition has a stake, is that tradition's standard reading present, in its
  strongest form, with named proponents **including modern scholars**, not only ancient witnesses? (The Orthodox
  must appear as living interpreters, not only as Fathers.) A missing standard reading is a **must**.
- **Fair statement.** Is its reading stated positively, in its holders' own terms, rather than as a foil? Are its
  holders described in their opponents' words? Is any of its scholars filed under a reading they reject?
- **Neutral voice.** Residual verdicts or grading devices; narrator rebuttals ("in fact", "yet", "nonetheless"
  after a named view); hindsight or teleology; premises built into a question or heading; unattributed contested
  claims ("has been read as", "historians reckon"); "the Church" for one communion; "Rome added" or "the Reformers
  restored" framing; "heretic" or "orthodox" as the narrator's label.
- **Accuracy.** Factual errors (dates, offices, attributions, what a council or document actually said) and quote
  integrity (is each quotation verbatim from the cited source?).
- **Readability.** A reading without its one-sentence summary, more than four names inline on a `Held by:` line, a
  case far beyond about 350 words, a point restated on the same page.

**Sourcing limits.** Reviewers work from openly accessible sources. Where a page says a reading's academic
literature was not located, or marks a holder `⚠ unverified`, that is allowed; flag it only if an openly
accessible scholarly source exists, and name only sources actually opened (WebSearch and WebFetch may be used to
check).

**Severity.** **must** = a reader of some tradition would reasonably distrust the page, or a factual error.
**should** = polish.

## 2. Report the review

Return a single JSON object, then a short plain summary:

```json
{
  "catholic":   {"pass": true,  "reason": "one sentence"},
  "orthodox":   {"pass": false, "reason": "one sentence"},
  "protestant": {"pass": true,  "reason": "one sentence"},
  "findings": [
    {
      "file": "path relative to docs/doctrines/",
      "quote": "the offending text, at most 25 words",
      "problem": "one sentence",
      "fix": "a concrete fix, naming any source to add and where it is",
      "tradition": "catholic | orthodox | protestant | all",
      "severity": "must | should"
    }
  ]
}
```

The review **passes** when all three verdicts pass and no finding is a must.

## 3. Fix (only when asked: `fix`, or the user says so)

Apply the findings under the rules in `CLAUDE.md`:
- **Treat findings as suggestions.** Decline any that would tilt the page another way, or that you cannot verify
  from a source you opened, and give the reason.
- **Balance guard.** A fix must not open a new imbalance. If you add one tradition's argument against another's
  position, the other tradition's own ground on that point must be on the page too (from a source you opened), or
  leave the argument out. Add no polemic beyond what a finding asks.
- **Research rules hold.** Cite only what you opened; never add a name, work, page number, URL or quotation from
  memory; copy new quotations verbatim; log verified factual fixes in `corrections.md`.
- Rerun the checks: `python3 -I scripts/ledger/lint.py <files>`, `python3 -I
  .claude/skills/footnote-check/check.py <files>`, relative links, quote integrity.

Then **re-review** (stages 1–2) the pages as they now stand, giving the reviewers the previous review and the fix
report. A reviewer does not re-raise a finding that was declined with a reason unless it judges the decline wrong,
and then says why. Stop when the review passes, or after **two** fix rounds.

**What is left over.** Each must finding still open after the last round becomes one `todo/` lead,
`YYYY-MM-DD-HHMM-<slug>-ledger-gap-<n>.md` (real time from `date`), carrying the doctrine, the file, the quoted
text, the problem, the suggested fix, which tradition raised it, and the neutral-voice reminder the `next` skill
needs to work it cold. Leftover should findings go together in one `…-ledger-gap-should.md` lead.

## 4. Report back

The verdicts (and how they changed across rounds), the findings fixed and declined (each decline with its
reason), proponents or sources added (with what was opened), check results, and any leads written. Don't commit;
if pages were edited, append a `log.md` entry.
