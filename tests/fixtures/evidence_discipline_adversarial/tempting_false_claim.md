# Tempting false weakest-boundary conclusion (adversarial fixture)

A model relying only on the docstring of `run_all_diagnostics` in
`module_under_test.py` (and not reading the full body of `_analyze_structure`,
nor searching for other `DiagnosticLayer.THEME` / `DiagnosticLayer.MODULATION`
usages) would be tempted to write:

> **Weakest boundary (Ghost Features):** `run_all_diagnostics()` only runs
> STRUCTURE-layer checks per its docstring ("Currently runs: STRUCTURE
> only"). THEME and MODULATION are declared in `DiagnosticLayer` but have no
> active diagnostic rules and are never generated.

This conclusion is FALSE. `_analyze_structure()` -- called unconditionally
by `run_all_diagnostics()` -- emits both `DiagnosticLayer.THEME` and
`DiagnosticLayer.MODULATION` findings. A contradiction search (grep for
`DiagnosticLayer.THEME` / `DiagnosticLayer.MODULATION` across the fixture,
or reading `_analyze_structure`'s full body instead of stopping at the
caller's docstring) finds this immediately.
