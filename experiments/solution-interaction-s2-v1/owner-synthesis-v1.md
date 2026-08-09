# S2 Owner Synthesis v1 — Compact

(For the owner; substantially shorter than the investigation brief.)

## 1. Recommended next action

Execute the demo sequence your own CONTEXT.md already prescribes, in its
documented order:
1. **Prose-refinement pass on the False MC prologue demo slice**
   (`false_mc_fpa` / `false_mc_fpb`) against the Canon practical outlines —
   the documented prerequisite ("lock prose/script quality before final visual
   asset production").
2. **First fresh-persistent playthrough of the demo slice** (your action,
   ~1-2 h) — the only unchecked release item in your tracker, ever.
3. Then produce the demo asset scope via the existing ADR-005 pipeline:
   Marcus / Elena / HW bust+sprite sets and the two demo CGs.
4. Demo polish: wire the feedback form, add a release-gate that fails while
   `game/zz_local_developer.rpy` exists (it forces developer mode + console at
   init 999), rebuild + smoke test, release.

## 2. Consequential decision boundary discovered

**Polished public prologue demo (documented milestone, CONTEXT.md June 30)
vs. full-Part-1 production capacity (the actual trajectory since July 22:
ADR-004/005 expression pipeline, Vesper pilot, D16-D23 campaign wiring —
pipeline merged to main today).** Your docs and your git history pointed in
different directions; only you could resolve which is the operative priority.
You chose the demo milestone; the pipeline becomes enabling infrastructure.

## 3. Why it matters now

The rough build is functionally complete (96 backgrounds, 11 OGGs, credits,
build+smoke test done) and has **never been human-playtested**; the expression
pipeline's output is **used by zero story scenes**. Every week of continued
campaign production delays the first public feedback loop — the demo's entire
purpose — and the sprite system remains unproven in the actual product.

## 4. Strongest observed evidence

- CONTEXT.md L92-L94/L120-L125/L137-L145: demo = first public milestone;
  minimum assets = Marcus/Elena/HW + 2 CGs; prose precedes assets.
- completion-tracker L208: only open release item is the fresh-persistent
  playthrough; Tested column empty for every chapter.
- Zero `show_expr` / sprite usage in any story script; the only CG is Vesper's.
- part1_asset_tracker L19: Vesper/Harlan pilot fully complete — the pipeline
  pattern is proven enough to reuse for the demo trio.

## 5. Strongest credible alternative

Finish the Vesper C1 interactive QA, merge the ADR-005 activation, and continue
campaign asset production (Calista P0 next). Defensible because the pipeline is
still unproven inside the story — but it treats enabling infrastructure as the
milestone, which is now contrary to your stated intent.

## 6. Most important remaining uncertainty

Whether the pipeline transfers cleanly to Marcus/Elena/HW (the recurring
alpha/recrop repair-script pattern suggests friction) and how heavy the
prologue prose refinement is. Both are empirical; the playthrough and the
first scene integration will answer them cheaply.

## 7. Cheapest justified next action / probe

The prose-refinement review of `false_mc_fpa`/`false_mc_fpb` (agent-doable,
days not weeks) **plus** your 1-2 h playthrough of the demo slice. Together
they convert the two open risks (draft prose, zero playtest) into evidence
before any asset spend.

## 8. Confidence and why bounded

Medium-high, bounded. Grounded in your own documented milestone, the tracker's
only-open-item state, and the pilot's completeness; bounded because no
playtest data exists and the demo trio has not been produced yet.

## 9. Owner intent

Asked and used (one neutral clarification; you selected the demo milestone).

## 10. Prior owner intent/decisions

Preserved. The June 30 demo doctrine was reaffirmed, not challenged; the
pipeline work was repositioned as enabling infrastructure, not abandoned.

## 11. Explicit distinction

- **Repository established:** the demo milestone + sequence; functional
  completeness of the rough build; zero playtest; zero story usage of sprites;
  pilot completeness; pipeline friction signals.
- **Agent inferred:** that docs-vs-behavior divergence is a genuine fork
  needing owner intent; that prose + playtest are the cheapest critical-path
  moves (from CONTEXT.md's own sequence).
- **Owner judgment required and supplied:** which milestone is operative (demo).
