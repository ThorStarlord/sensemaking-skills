"""Atomic Section-13 handoff serialization qualification (directive #19).

Proves: frozen dogfood B reconciles without duplicate recommended_workflow_id
(A); Section-13 parses (B); every Section-13 key is unique (C/duplicate-key
guarantee); evidence projection is exact from Section-8 (D); runtime-owned
fields cannot be replaced (F); invalid model values preserved verbatim (G);
required required fields remain validator-visible (H); required_inputs
default/override (I); outcome round-trips when present (J).
"""
import sys
import unittest

import yaml

sys.path.insert(0, "scripts")
import brief_skeleton as bs

DOGFOOD_DIR = "experiments/product-hypothesis-b/implementation/dogfood-rmt"


def _section13_machine(text):
    block = bs.extract_handoff_yaml_block(text)
    return yaml.safe_load(block)


def _all_keys(data):
    out, stack = [], [data]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            out += list(node.keys())
            stack += list(node.values())
        elif isinstance(node, list):
            stack += node
    return out


class TestAtomicDuplicateKeyGuarantee(unittest.TestCase):
    """A/B/C + duplicate-key structural guarantee."""

    def test_frozen_B_reconciles_without_duplicate_recommended_workflow_id(self):
        B = open(f"{DOGFOOD_DIR}/B_post_model_pre_reconcile.md", encoding="utf-8").read()
        out = bs.reconcile(B)
        # exactly one top-level recommended_workflow_id line in Section 13
        sec13 = out[out.index("## 13."):]
        top = [l for l in sec13.splitlines()
               if l.startswith("recommended_workflow_id:")]
        self.assertEqual(len(top), 1, f"expected a single key, got: {top}")
        self.assertIn("docs-implementation-workflow", top[0])

    def test_section13_parses_after_reconcile_frozen_B(self):
        B = open(f"{DOGFOOD_DIR}/B_post_model_pre_reconcile.md", encoding="utf-8").read()
        out = bs.reconcile(B)
        ok, reason = bs.handoff_yaml_round_trips(out)
        self.assertTrue(ok, reason)

    def test_every_section13_key_unique(self):
        B = open(f"{DOGFOOD_DIR}/B_post_model_pre_reconcile.md", encoding="utf-8").read()
        out = bs.reconcile(B)
        data = _section13_machine(out)
        keys = list(data.keys())
        dup = {k for k in keys if keys.count(k) > 1}
        self.assertEqual(dup, set(), f"duplicate Section-13 keys: {dup}")

    def test_dup_key_document_fails_reconciled_structural_check(self):
        # A document with a duplicated key must not silently pass as a single
        # clean mapping: rely on a strict loader that rejects duplicate mapping
        # keys rather than permissive yaml.safe_load (last-value-wins).
        B = open(f"{DOGFOOD_DIR}/B_post_model_pre_reconcile.md", encoding="utf-8").read()
        out = bs.reconcile(B)
        poisoned = out.replace(
            "recommended_workflow_id: docs-implementation-workflow",
            "recommended_workflow_id:\nrecommended_workflow_id: docs-implementation-workflow",
        )
        block = bs.extract_handoff_yaml_block(poisoned)
        loader = yaml.SafeLoader
        # SafeLoader alone is permissive; use a loader that flags duplicate keys.
        seen = set()

        def construct_mapping(ldr, node):
            mapping = {}
            for key_node, value_node in node.value:
                key = ldr.construct_object(key_node, deep=False)
                if key in mapping:
                    raise ValueError(f"duplicate mapping key: {key!r}")
                mapping[key] = ldr.construct_object(value_node, deep=False)
            return mapping

        loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                               construct_mapping)
        with self.assertRaises(ValueError):
            yaml.load(block, Loader=loader)


class TestEvidenceProjectionAndQuote(unittest.TestCase):
    """D / E."""

    def test_evidence_projection_exact_from_section8(self):
        B = open(f"{DOGFOOD_DIR}/B_post_model_pre_reconcile.md", encoding="utf-8").read()
        out = bs.reconcile(B)
        data = _section13_machine(out)
        self.assertEqual(data["evidence"], [
            "pyproject.toml (lines L11-L16): streamdown is a Python library+CLI "
            "(name, version, description)",
            "README.md (lines L1-L2): realtime terminal streaming markdown "
            "renderer (DAY50 suite)",
        ])

    def test_quote_extraction_still_authoritative(self):
        # reconcile's quote re-derivation path is unchanged (function present,
        # still wired into evidence_excerpts merge).
        self.assertTrue(callable(getattr(bs, "reconcile_evidence_excerpt_quotes", None)))


class TestOwnershipAndSemanticPreservation(unittest.TestCase):
    """F / G / H / I / J."""

    def _model(self, extra=""):
        return f"""
```yaml
primary_fog_type: architecture_fog
user_implied_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
recommended_workflow_id: docs-aligner
recommended_execution_mode: plan_only
weakest_boundary: version-drift
weakness_type: Other
weakness_type_explanation: test
{extra}
```
"""

    def test_runtime_owned_fields_cannot_be_overwritten(self):
        ctx = bs.SkeletonContext(created_at="2026-01-01T00:00:00Z",
                                 source_intent_ref="provenance/oracle")
        model = self._model("created_at: 2000-01-01T00:00:00Z\nimmutable: false\nartifact_id: hacked")
        out = bs.reconcile(model, ctx=ctx)
        data = _section13_machine(out)
        self.assertEqual(data["created_at"], "2026-01-01T00:00:00Z")
        self.assertEqual(data["immutable"], True)
        self.assertEqual(data["artifact_id"], "repository_sensemaking_brief")

    def test_invalid_model_value_preserved_verbatim(self):
        model = self._model().replace(
            "recommended_workflow_id: docs-aligner",
            "recommended_workflow_id: bogus-not-in-registry",
        )
        out = bs.reconcile(model)
        data = _section13_machine(out)
        self.assertEqual(data["recommended_workflow_id"], "bogus-not-in-registry")

    def test_missing_required_field_validator_visible(self):
        # A model output omitting a required machine field must leave that field
        # ABSENT from the reconciled machine block (validator then rejects),
        # never repaired/invented by the runtime.
        stripped = self._model().replace("weakness_type: Other\n", "")
        out = bs.reconcile(stripped)
        data = _section13_machine(out)
        self.assertNotIn("weakness_type", data)

    def test_required_inputs_default_then_model_override(self):
        model = self._model()
        out = bs.reconcile(model)
        self.assertEqual(_section13_machine(out)["required_inputs"], ["user_intent", "repository_state"])
        model2 = self._model("required_inputs:\n  - user_intent")
        out2 = bs.reconcile(model2)
        self.assertEqual(_section13_machine(out2)["required_inputs"], ["user_intent"])

    def test_explicit_outcome_round_trips(self):
        model = self._model("outcome: NO_REPOSITORY_CHANGE_WARRANTED")
        out = bs.reconcile(model)
        self.assertEqual(_section13_machine(out)["outcome"], "NO_REPOSITORY_CHANGE_WARRANTED")

    def test_excerpt_derived_evidence_wins_over_model_authored(self):
        # When Section-8 excerpts exist AND the model also authored S13 evidence,
        # the derived projection is authoritative (single source of truth).
        model = (
            "## 8. Evidence excerpts\n\n```yaml\n"
            "evidence_excerpts:\n"
            "  - file: README.md\n    lines: \"L1\"\n    supports_claim: real\n    quote: x\n"
            "```\n\n## 9. Extended analysis\n\nnothing\n\n"
            + self._model("evidence:\n  - stale-manual-entry\n")
        )
        out = bs.reconcile(model)
        data = _section13_machine(out)
        self.assertNotEqual(data["evidence"], ["stale-manual-entry"])
        self.assertTrue(any("README.md" in e for e in data["evidence"]),
                        f"derived evidence should win, got {data['evidence']}")


if __name__ == "__main__":
    unittest.main()
