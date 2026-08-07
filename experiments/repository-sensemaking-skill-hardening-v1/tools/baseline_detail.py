import yaml

d = yaml.safe_load(open(r"experiments\repository-sensemaking-skill-hardening-v1\baseline-scored.yaml", encoding="utf-8"))
gt = {r["repository_id"]: r for r in yaml.safe_load(open(r"experiments\repository-sensemaking-skill-hardening-v1\corpus\ground-truth.yaml", encoding="utf-8"))["repositories"]}
print("=== FOG MISMATCHES ===")
for r in d["rows"]:
    if not r.get("fog_match"):
        print(f"{r['repository_id']}: declared={r['fog_declared']} expected={r['fog_expected']}")
print("=== WEAK BOUNDARY (brief vs ground truth) ===")
for r in d["rows"]:
    want = gt[r["repository_id"]]["known_weak_boundaries"][0]["type"]
    got = r["weakness_type"]
    m = "MATCH" if want == got else "DIFF "
    print(f"{m} {r['repository_id']}: brief={got} gt={want}")
print("=== ENTRY POINT COVERAGE ===")
tot = 0
found = 0
for r in d["rows"]:
    eps = gt[r["repository_id"]]["known_entry_points"]
    tot += len(eps)
    found += len(r["entry_points_found"])
print(f"{found}/{tot} ground-truth entry points mentioned in briefs")
