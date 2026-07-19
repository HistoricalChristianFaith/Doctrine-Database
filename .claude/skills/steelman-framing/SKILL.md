---
name: steelman-framing
description: Give one wiki argument page a fair-shake steelman pass — reconstruct the strongest version of the interpretation it serves, re-rate honestly to track that steelman (not the proponent's stumble), correct overreaches, and propagate the reframing coherently across the wiki. Use when the user invokes /steelman-framing <page>, or asks to steelman / re-examine / "give a fairer shake to" an argument page.
---

Run a **steelman-framing pass** on a single argument page named by the caller. The goal is the one in
`CLAUDE.md` under **Assessments → "Steelman before you weigh"** and **"State the finding, don't rebut a
label"**: judge the *interpretation* on its **best available case**, not the proponent's particular
(possibly clumsy) wording of it, and never shut down a genuinely plausible reading just because the
proponent overstated it or rested it on a weak prop.

This is the generalization of the worked example in `log.md` where the "excised descent-prophecy"
argument was given a deeper dive — its plausible kernel steelmanned, its overreaches corrected, and its
assessment reframed to track the strongest version of the reading rather than the narrow proof-text
claim it was originally titled for.

## Parameter

`$ARGUMENTS` (or what the user passes) names the **target page** — usually an **argument page**. Accept
either a slug (`excised-descent-prophecy`), a doctrine-qualified slug
(`intermediate-state/arguments/excised-descent-prophecy`), or a full path under `docs/`. Resolve it to
the file `docs/doctrines/<doctrine>/arguments/<arg>.html`. If the resolution is ambiguous (a bare slug
that exists under two doctrines), or the page named isn't an argument page, **ask which page** before
proceeding. This skill is built for argument pages (the things that carry an `assessment`); a
person-detail or summary page isn't its proper object.

## 1. Map the page and its neighbourhood

Before touching anything, read enough to know what the page actually claims and what depends on it:

1. **The target argument page** — its `<title>`/`<h1>`, the `Assessment:` line, the body sections, the
   proof-texts and witnesses, and the current rating.
2. **The proponent(s)' detail page(s)** linked from it — to see how the claim is framed there and
   whether any overreach is (or isn't) already flagged.
3. **The home summary** (`docs/doctrines/<doctrine>.html`) — the `<h4>`/`<h3>` heading + blurb +
   footnote that surface this argument, and its **Related-arguments group** siblings.
4. **The index** entry (`docs/index.html`) — the `<li> … — <strong>rating</strong>` line.
5. **Every cross-reference to this page elsewhere** — grep for the slug across `docs/`:
   ```
   grep -rn "<arg-slug>" docs/
   ```
   Other doctrines often cite an argument (with its title + rating) inside their own footnotes/prose.
   These are the coherence hazards in step 5.

## 2. Reconstruct the steelman (research, don't armchair it)

Find the **strongest version of the interpretation the argument serves** — which may be stronger than
the proponent's stated case. Do genuine research, per `CLAUDE.md` **Source databases** (prefer the
Commentaries/Writings DBs, but **use the web too** — most references are found online):

- Is there a **better proof-text, a sounder mechanism, or a fitter witness** for the *same* reading than
  the one the proponent leaned on? Steelman *that*.
- What is the **genuinely decisive** consideration on each side? (In the worked example: the LXX
  pre-dating the alleged motive was the real crux, sharper than the three objections first marshalled;
  and Aquila + the Qumran Isa 53:11 loss were the real support, which the page had omitted.) Hunt for the
  strongest argument on *both* sides, not just more of the ones already there.
- Keep **two questions separate and answer both**: (a) is the *proponent's stated* argument sound? and
  (b) is the *interpretation* sound **on its best available case**? A reading can stand even where the
  proponent's prop for it fails.
- Honour the other `CLAUDE.md` assessment rules: **don't rule out the supernatural a priori** (weigh a
  miracle claim on attestation/dating/coherence, not on naturalism), and distinguish **plausible**
  (coherent, not ruled out) from **probable** (more likely than not).

Cite every source you actually consulted, with URLs where you have them (rule 10). File a
`gh issue` if research surfaces a fixable gap in the upstream source repos.

## 3. Decide the honest reframing

- **Re-rate to track the steelman**, not the proponent's stumble. The rating ∈ {`sound`, `plausible`,
  `contested`, `weak`, `unsupported`} (definitions in `CLAUDE.md`). It may go **up** (the interpretation
  is stronger than the page credited), **down**, or **stay** — be honest, not generous. If the page was
  titled/scoped to the proponent's *narrow* claim but the *interpretation* it serves is broader, **retitle
  the page for the interpretation** and rate that (e.g. `… authentic Scripture cut by the Jews` →
  `… a genuine early witness to the descent`).
- **State the finding; do not rebut a label** — *especially* not a rating *we* assigned. Never write
  "often called weak, but actually …". Just say what the evidence shows. (The summary/index/breadcrumb
  copy should read as if it had always said the new thing.)
- **Scope the rating precisely** when the steelmanned reading and the narrow proponent-claim diverge:
  rate the page for the strong reading, but keep the weak sub-claim visibly *flagged as the part that
  fails* (the two-question structure on `descent-to-the-dead.html` / the reworked
  `excised-descent-prophecy.html` is the model).
- If the rating is a **genuine judgment call** (e.g. `plausible` vs `contested`), pick the one you can
  best defend, make the change, and **flag the alternative** to the user in your report — don't block.

## 4. Rewrite the target page and flag the proponent

- Rework the argument page: `<title>` + `<h1>` (if reframing), the `Assessment:` line, a real
  steelman section ("What can be said for it" / strongest case), corrected/sharpened objections, and an
  `Assessment` that answers both questions of step 2. Keep quotes **verbatim** in `<blockquote>` (rule
  3); keep footnote markup exact (rule 2 + the footnote conventions); add footnotes for new sources.
- **Flag the proponent's misstep on their detail page — always, whatever the new rating** (`CLAUDE.md`:
  "Flag the proponent's misstep on their page (always)"). Frame it as a *less-probable reading* or
  *conjecture beyond the evidence*, not "wrong/false" (unless it is genuinely a factual error).

## 5. Propagate coherently (the part that's easy to half-do)

A rating/title change must be carried to **every** surface, and must not silently contradict the rest of
the wiki:

- **Home summary** — the argument's `<h4>`/`<h3>` heading (`(assessment: <rating>)`), its blurb, and its
  Sources footnote (`(assessment: <rating>)`). Rewrite the blurb to lead with the reframed reading.
- **Index** — the `<li> … — <strong>rating</strong>` line (title text + rating).
- **Related-arguments breadcrumbs / group headings** — if the link text used the old title anywhere.
- **Cross-doctrine cross-references** (from step 1's grep) — update the title link-text and the
  `(assessment: …)` label. **Crucially:** check the new rating against the assessments of *sibling and
  related arguments* (same group, and any other doctrine that cites this page). If another page rates a
  *neighbouring* claim differently, make sure the labels don't read as a contradiction — **scope** the
  cross-ref label to the exact proposition that page uses it for (e.g. "plausible as a descent-witness;
  the specific excision is not established"), rather than blindly swapping the rating word. The worked
  example reconciled this page's `plausible` with `rabbinic-corruption`'s `weak` deliberate-corruption /
  `weak` aquila-revision / vindicated reverse-charge by scoping every cross-ref label.
- For a **new doctrine** only, the `DOCTRINE_NAMES` map in `toc.js` — not relevant to a re-rating.

## 6. Verify and bookkeep

- Run the footnote healthcheck on **every** page you touched and fix to clean:
  ```
  python3 .claude/skills/footnote-check/check.py <each touched file>
  ```
  (Re-sequence footnotes if you reordered anything; fix any duplicate `fnref` ids — use the
  `fnref2:`/`fnref3:` repeat-citation namespace, not a duplicated id.)
- **`log.md`** — append a dated entry (real current date, rule 7) recording: the page, the
  rating/title change and *why* (the steelman + the decisive evidence), the overreaches corrected, the
  coherence reconciliation, and every file touched.
- **Commit.** Review the diff first (`git diff --stat` then eyeball each hunk) to confirm it contains
  **only** this steelman pass and swept up nothing stray — the working tree may hold unrelated edits at
  session start. If it's clean, `git add` exactly the pages you touched (the argument page + every
  propagation surface: summary, index, cross-referencing pages) and commit with a message of the form
  `<doctrine>/<arg-slug>: steelman … (<old-rating> → <new-rating>)`, a body summarising the steelman,
  the corrections, and the coherence reconciliation, ending with the standard
  `Co-Authored-By: Claude …` trailer. **Do not push** — leave that to the user. (`log.md` and `todo/`
  are git-ignored, so they won't appear in the commit; that's expected.) If the diff is *not* isolable
  from unrelated pre-existing changes, don't force it — commit nothing and flag it in your report
  instead.
- **Report** to the user: the before/after rating, the core of the steelman, what was corrected, any
  cross-doctrine coherence issue you resolved, the commit made (hash + that it's unpushed), and any
  rating that was a judgment call (with the alternative).

Respect all `CLAUDE.md` hard rules throughout (no internal plumbing on reader-facing pages, verbatim
quotes, depth-relative links, append-don't-overwrite, footnote on every summary claim).
