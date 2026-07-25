# Evidence Rules for Repo Sensemaking

To maintain diagnostic rigor, all claims in a **Repository Sensemaking Brief** must be backed by evidence:

1. **File Citation**: Mention the specific file and line numbers where a signal or weakness is found. Line numbers are **required**, not optional — `scripts/validate-brief.py` rejects any `evidence_excerpts[].lines` value that does not match `^L?\d+(?:-L?\d+)?$`.
   - **Accepted forms**: a bare line number (`12`), a prefixed line number
     (`L12`), a bare range (`12-18`), or a prefixed range (`L12-L18`).
   - **Rejected forms**: any descriptive substitute, e.g. `"Entire file"`,
     `"Entire skill file"`, `"Routing section"`, `"Routing accuracy section"`,
     `"See above"`, `"See README"`. These are not line numbers and will fail
     validation with `INVALID_LINE_FORMAT`.
   - **If the relevant evidence is genuinely file-wide** (no single line or
     small range captures it): do not write a descriptive placeholder into
     `lines`. Instead, cite the single most relevant concrete line or range
     that best represents the claim (e.g. the file's opening declaration, the
     specific function signature, or the first line of the relevant block),
     and use the accompanying prose (Section 7's logic trace, or the
     `supports_claim` field) to explain that the pattern holds across the
     file. The validator's grammar does not currently support a "whole file"
     value — do not invent one.
2. **Structural Proof**: Cite the directory tree or file organization as proof of shape or missing pieces.
3. **Contrastive Evidence**: Compare what the README says vs. what the `ls` or `view_file` output shows.
4. **Logic Trace**: Follow the execution path of a workflow or skill to identify where boundaries are unenforced.
5. **No Vibe-based Diagnosis**: Avoid saying something "feels" off. State exactly which boundary is unproven or ambiguous.
