"""Repository qualification tests for PM experimentation, PMF, and pricing."""
from __future__ import annotations
import importlib.util, json, subprocess, sys
from pathlib import Path
import pytest, yaml
from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import ArtifactAdmissionService, CampaignService
from sensemaking_skills.campaigns.capabilities import load_capability_registry

REPO_ROOT=Path(__file__).resolve().parents[2]
IDS=("experiment_plan","test_results","pmf_report","pricing_model")
SECTIONS={
"experiment_plan":("Hypothesis and riskiest assumption","Method and exposure","Metrics and evidence plan","Decision and kill criteria","Analysis and authority","Risks and unknowns"),
"test_results":("Experiment and observations","Setup integrity","Primary analysis","Guardrails and segments","Interpretation","Recommendation and limitations"),
"pmf_report":("Segment and evidence window","Evidence inventory","Survey and retention signals","Qualitative organic and economics signals","Assessment","Next evidence and limitations"),
"pricing_model":("Value and segment evidence","Pricing-model options","Competitive and willingness-to-pay evidence","Proposed packaging","Economics and assumptions","Experiment plan and risks","Recommendation and authority boundary"),}

def payload(aid):
 if aid=="experiment_plan": return {"artifact_id":aid,"schema_version":"1","status":"designed","hypothesis_ref":"H-1","experiment_type":"ab_test","target_population":"eligible users","intervention":"new flow","primary_metric":{"name":"completion","baseline":None,"baseline_status":"unknown","evidence_refs":[]},"guardrails":[],"sample_plan":{"size":None,"status":"unknown","method":"power analysis before run"},"duration_plan":{"value":None,"status":"unknown"},"decision_criteria":{"go":"predeclared lift","no_go":"harm","investigate":"integrity concern"},"kill_criteria":[],"analysis_method":"two-proportion comparison","execution_authority_ref":None,"unresolved_questions":[]}
 if aid=="test_results": return {"artifact_id":aid,"schema_version":"1","status":"analyzed","experiment_ref":"EXP-1","observation_refs":["data-1"],"primary_metric":"conversion","control":{"n":100,"value":0.2},"treatment":{"n":100,"value":0.25},"method":"two-proportion z-test","effect_estimate":0.05,"uncertainty":{"kind":"confidence_interval","lower":-0.06,"upper":0.16,"p_value":0.4},"setup_integrity":{"status":"pass","concerns":[]},"guardrails":[],"recommendation":"extend","limitations":[]}
 if aid=="pmf_report": return {"artifact_id":aid,"schema_version":"1","status":"partial","segment":"teams","evidence_window":"2026-Q3","survey":{"response_count":10,"very_disappointed_count":4,"very_disappointed_share":0.4,"evidence_refs":["survey-1"]},"retention_signals":[],"organic_signals":[],"qualitative_signals":[],"economics_signals":[],"assessment":"insufficient_evidence","assessment_basis":["small survey"],"limitations":["limited sample"],"next_evidence":["collect more responses"]}
 return {"artifact_id":aid,"schema_version":"1","status":"proposed","segment":"teams","value_metric":{"name":"seat","evidence_status":"hypothesis","evidence_refs":[]},"model_options":["per-seat","tiered"],"recommended_model":"tiered per-seat","competitor_claims":[],"wtp_evidence":[],"tiers":[{"id":"TIER-1","name":"Pro","price":None,"price_status":"unknown","evidence_refs":[]}],"economics":{"evidence_status":"unknown","evidence_refs":[],"values":{}},"experiments":[],"external_change_authority_ref":None,"unresolved_questions":[]}

def write(tmp_path,aid,data=None):
 parts=[f"# {aid}",""]
 for s in SECTIONS[aid]: parts += [f"## {s}","Fixture.",""]
 parts += ["## Machine-readable handoff","```yaml",yaml.safe_dump(data or payload(aid),sort_keys=False).rstrip(),"```",""]
 p=tmp_path/f"{aid}.md"; p.write_text("\n".join(parts),encoding="utf-8"); return p

def route(path):
 cp=subprocess.run([sys.executable,str(REPO_ROOT/"scripts"/"validate-and-report.py"),str(path),"--repo-root",str(REPO_ROOT)],cwd=REPO_ROOT,capture_output=True,text=True,check=False)
 return cp.returncode,json.loads(cp.stdout)

def router():
 p=REPO_ROOT/"scripts"/"validate-and-report.py"; spec=importlib.util.spec_from_file_location("pm_measurement_router",p); m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m

def test_router_maps_all_measurement_artifacts():
 for aid in IDS: assert router().select_validator(aid)=="scripts/validate-pm-measurement.py"

@pytest.mark.parametrize("aid",IDS)
def test_valid_measurement_artifacts_pass(tmp_path,aid):
 code,out=route(write(tmp_path,aid)); assert code==0,out; assert out["validator"]=="validate-pm-measurement.py"

def test_experiment_plan_cannot_encode_result(tmp_path):
 d=payload("experiment_plan"); d["winner"]="treatment"; code,out=route(write(tmp_path,"experiment_plan",d)); assert code==1; assert any(e["error_id"]=="PM_PLAN_CANNOT_CONTAIN_RESULT" for e in out["errors"])

def test_results_without_observations_cannot_claim_ship(tmp_path):
 d=payload("test_results"); d.update(status="insufficient_evidence",observation_refs=[],recommendation="ship"); code,out=route(write(tmp_path,"test_results",d)); assert code==1; assert any(e["error_id"]=="PM_RESULT_WITHOUT_EVIDENCE" for e in out["errors"])

def test_pmf_not_measured_cannot_claim_strong(tmp_path):
 d=payload("pmf_report"); d.update(status="not_measured",assessment="strong"); d["survey"]={"response_count":0,"very_disappointed_count":0,"very_disappointed_share":None,"evidence_refs":[]}; code,out=route(write(tmp_path,"pmf_report",d)); assert code==1; assert any(e["error_id"]=="PM_PMF_WITHOUT_MEASUREMENT" for e in out["errors"])

def test_pricing_observed_current_price_requires_evidence(tmp_path):
 d=payload("pricing_model"); d["tiers"][0].update(price=49,price_status="observed_current",evidence_refs=[]); code,out=route(write(tmp_path,"pricing_model",d)); assert code==1; assert any(e["error_id"]=="PM_EVIDENCE_REQUIRED" for e in out["errors"])

def test_campaign_admission_binds_measurement_validator(tmp_path):
 ws=tmp_path/"campaign"; CampaignService(ws).initialize(CampaignState(campaign_id="CMP-PM-W4",mission="qualify",status="active",current_state="initialized")); result=ArtifactAdmissionService(ws).admit(write(tmp_path,"experiment_plan"),framework_root=REPO_ROOT); assert result.admission.validator=="validate-pm-measurement.py"

def test_campaign_catalog_exposes_wave4_without_external_authority():
 reg=load_capability_registry(); expected={"experiment-design":("experimentation","experiment_plan"),"ab-test-analysis":("experimentation","test_results"),"measure-pmf":("product_measurement","pmf_report"),"pricing":("commercial_strategy","pricing_model")}
 for cid,(resp,out) in expected.items():
  item=reg.get(cid); assert item is not None; assert item.capability.accepted_responsibility_types==(resp,); assert item.capability.output_artifact==out; assert item.mutates_repository is False; assert item.returns_control is True
