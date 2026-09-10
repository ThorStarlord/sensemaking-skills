#!/usr/bin/env python3
"""Validate PM experimentation, PMF, and pricing artifact contracts."""
from __future__ import annotations
import argparse, json, math, re, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml

VALIDATOR = "validate-pm-measurement.py"
SUPPORTED = {"experiment_plan", "test_results", "pmf_report", "pricing_model"}
HANDOFF_RE = re.compile(r"^##\s+(?:\d+\.\s*)?Machine-readable handoff\s*$\s*```yaml\s*(.*?)\s*```", re.MULTILINE | re.IGNORECASE | re.DOTALL)
SECTIONS = {
 "experiment_plan": ("Hypothesis and riskiest assumption","Method and exposure","Metrics and evidence plan","Decision and kill criteria","Analysis and authority","Risks and unknowns"),
 "test_results": ("Experiment and observations","Setup integrity","Primary analysis","Guardrails and segments","Interpretation","Recommendation and limitations"),
 "pmf_report": ("Segment and evidence window","Evidence inventory","Survey and retention signals","Qualitative organic and economics signals","Assessment","Next evidence and limitations"),
 "pricing_model": ("Value and segment evidence","Pricing-model options","Competitive and willingness-to-pay evidence","Proposed packaging","Economics and assumptions","Experiment plan and risks","Recommendation and authority boundary"),
}

def err(code:str, field:str, message:str, value:Any=None)->dict[str,Any]:
 return {"error_id":code,"error_type":"contract_error","field":field,"current_value":value,"message":message,"suggested_fixes":[],"reference":"docs/product-management/artifact-contracts.md"}

def text(v:Any)->bool: return isinstance(v,str) and bool(v.strip())
def slist(v:Any, nonempty:bool=False)->bool: return isinstance(v,list) and (not nonempty or bool(v)) and all(text(x) for x in v)
def num(v:Any)->bool: return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v))
def require(d:dict[str,Any], fields:tuple[str,...], errors:list[dict[str,Any]])->None:
 for f in fields:
  if f not in d: errors.append(err("PM_MISSING_FIELD",f,f"required field {f!r} is missing"))
def observed(status:Any, refs:Any, field:str, errors:list[dict[str,Any]])->None:
 if status in {"observed","observed_current"} and not slist(refs,True): errors.append(err("PM_EVIDENCE_REQUIRED",field,"observed value requires evidence refs",refs))

def validate_plan(d,errors):
 require(d,("schema_version","status","hypothesis_ref","experiment_type","target_population","intervention","primary_metric","guardrails","sample_plan","duration_plan","decision_criteria","kill_criteria","analysis_method","execution_authority_ref","unresolved_questions"),errors)
 if d.get("status")!="designed": errors.append(err("PM_INVALID_STATUS","status","experiment plan status must be designed",d.get("status")))
 if not text(d.get("hypothesis_ref")): errors.append(err("PM_SOURCE_REQUIRED","hypothesis_ref","hypothesis_ref required"))
 if d.get("experiment_type") not in {"pretotype","usability","ab_test","other"}: errors.append(err("PM_INVALID_TYPE","experiment_type","invalid experiment type",d.get("experiment_type")))
 pm=d.get("primary_metric")
 if not isinstance(pm,dict) or not text(pm.get("name")): errors.append(err("PM_PRIMARY_METRIC_REQUIRED","primary_metric","primary metric name required",pm))
 elif pm.get("baseline_status") not in {"unknown","observed","proposed"}: errors.append(err("PM_INVALID_EVIDENCE_STATUS","primary_metric.baseline_status","invalid baseline status",pm.get("baseline_status")))
 else: observed(pm.get("baseline_status"),pm.get("evidence_refs"),"primary_metric.evidence_refs",errors)
 if any(k in d for k in ("result","winner","effect_estimate","p_value")): errors.append(err("PM_PLAN_CANNOT_CONTAIN_RESULT","artifact","experiment_plan cannot encode observed result/winner fields"))
 if not text(d.get("analysis_method")): errors.append(err("PM_ANALYSIS_METHOD_REQUIRED","analysis_method","analysis method required"))

def validate_results(d,errors):
 require(d,("schema_version","status","experiment_ref","observation_refs","primary_metric","control","treatment","method","effect_estimate","uncertainty","setup_integrity","guardrails","recommendation","limitations"),errors)
 status=d.get("status"); rec=d.get("recommendation")
 if status not in {"analyzed","insufficient_evidence"}: errors.append(err("PM_INVALID_STATUS","status","test_results status must be analyzed or insufficient_evidence",status))
 refs=d.get("observation_refs")
 if status=="analyzed":
  if not slist(refs,True): errors.append(err("PM_OBSERVATION_REQUIRED","observation_refs","analyzed results require observation evidence",refs))
  for group in ("control","treatment"):
   value=d.get(group)
   if not isinstance(value,dict) or not num(value.get("n")) or float(value["n"])<=0: errors.append(err("PM_SAMPLE_REQUIRED",f"{group}.n","analyzed results require positive sample size",value))
  if not text(d.get("method")): errors.append(err("PM_ANALYSIS_METHOD_REQUIRED","method","analysis method required"))
 elif rec!="insufficient_evidence": errors.append(err("PM_RESULT_WITHOUT_EVIDENCE","recommendation","insufficient evidence cannot produce winner/action recommendation",rec))
 if rec not in {"ship","investigate","extend","stop","do_not_ship","insufficient_evidence"}: errors.append(err("PM_INVALID_RECOMMENDATION","recommendation","invalid recommendation",rec))

def validate_pmf(d,errors):
 require(d,("schema_version","status","segment","evidence_window","survey","retention_signals","organic_signals","qualitative_signals","economics_signals","assessment","assessment_basis","limitations","next_evidence"),errors)
 status=d.get("status"); assessment=d.get("assessment")
 if status not in {"measured","partial","not_measured"}: errors.append(err("PM_INVALID_STATUS","status","invalid PMF status",status))
 survey=d.get("survey")
 if not isinstance(survey,dict): errors.append(err("PM_MAPPING_REQUIRED","survey","survey must be mapping",survey))
 else:
  n=survey.get("response_count",0); vd=survey.get("very_disappointed_count",0); share=survey.get("very_disappointed_share")
  if not isinstance(n,int) or n<0 or not isinstance(vd,int) or vd<0 or vd>n: errors.append(err("PM_INVALID_SURVEY_COUNTS","survey","invalid response counts",survey))
  elif n>0:
   expected=vd/n
   if not num(share) or not math.isclose(float(share),expected,rel_tol=1e-6,abs_tol=1e-6): errors.append(err("PM_SURVEY_SHARE_MISMATCH","survey.very_disappointed_share",f"share must equal {expected}",share))
   if not slist(survey.get("evidence_refs"),True): errors.append(err("PM_EVIDENCE_REQUIRED","survey.evidence_refs","survey counts require evidence refs",survey.get("evidence_refs")))
  elif share is not None: errors.append(err("PM_SHARE_WITHOUT_RESPONSES","survey.very_disappointed_share","share must be null with zero responses",share))
 evidence=[]
 if isinstance(survey,dict): evidence += survey.get("evidence_refs") or []
 for key in ("retention_signals","organic_signals","qualitative_signals","economics_signals"):
  if isinstance(d.get(key),list):
   for item in d[key]:
    if isinstance(item,dict): evidence += item.get("evidence_refs") or []
 if status=="measured" and not evidence: errors.append(err("PM_EVIDENCE_REQUIRED","status","measured PMF requires empirical evidence refs"))
 if status=="not_measured" and assessment!="insufficient_evidence": errors.append(err("PM_PMF_WITHOUT_MEASUREMENT","assessment","not_measured must use insufficient_evidence",assessment))

def validate_pricing(d,errors):
 require(d,("schema_version","status","segment","value_metric","model_options","recommended_model","competitor_claims","wtp_evidence","tiers","economics","experiments","external_change_authority_ref","unresolved_questions"),errors)
 if d.get("status")!="proposed": errors.append(err("PM_INVALID_STATUS","status","pricing model status must be proposed",d.get("status")))
 vm=d.get("value_metric")
 if isinstance(vm,dict): observed(vm.get("evidence_status"),vm.get("evidence_refs"),"value_metric.evidence_refs",errors)
 tiers=d.get("tiers")
 if not isinstance(tiers,list): errors.append(err("PM_LIST_REQUIRED","tiers","tiers must be list",tiers))
 else:
  ids=[]
  for i,t in enumerate(tiers):
   if not isinstance(t,dict) or not text(t.get("id")): errors.append(err("PM_ID_REQUIRED",f"tiers[{i}].id","tier id required")); continue
   ids.append(t["id"])
   if t.get("price_status") not in {"unknown","proposed","observed_current"}: errors.append(err("PM_INVALID_STATUS",f"tiers[{i}].price_status","invalid price status",t.get("price_status")))
   observed(t.get("price_status"),t.get("evidence_refs"),f"tiers[{i}].evidence_refs",errors)
  if len(ids)!=len(set(ids)): errors.append(err("PM_DUPLICATE_ID","tiers","duplicate tier ids",ids))
 econ=d.get("economics")
 if isinstance(econ,dict): observed(econ.get("evidence_status"),econ.get("evidence_refs"),"economics.evidence_refs",errors)
 for i,c in enumerate(d.get("competitor_claims") or []):
  if isinstance(c,dict): observed(c.get("evidence_status"),c.get("evidence_refs"),f"competitor_claims[{i}].evidence_refs",errors)

VALIDATORS={"experiment_plan":validate_plan,"test_results":validate_results,"pmf_report":validate_pmf,"pricing_model":validate_pricing}
def validate(path:Path):
 if not path.is_file(): return "unknown",[err("PM_ARTIFACT_NOT_FOUND","artifact",f"artifact not found: {path}")]
 content=path.read_text(encoding="utf-8"); blocks=HANDOFF_RE.findall(content)
 if len(blocks)!=1: return "unknown",[err("PM_HANDOFF_BLOCK_COUNT","machine_readable_handoff","expected exactly one handoff YAML block",len(blocks))]
 try: data=yaml.safe_load(blocks[0])
 except yaml.YAMLError as exc: return "unknown",[err("PM_INVALID_YAML","machine_readable_handoff",f"invalid YAML: {exc}")]
 if not isinstance(data,dict): return "unknown",[err("PM_INVALID_YAML_SHAPE","machine_readable_handoff","handoff must be mapping")]
 aid=data.get("artifact_id")
 if aid not in SUPPORTED: return str(aid or "unknown"),[err("PM_UNSUPPORTED_ARTIFACT","artifact_id","unsupported PM measurement artifact",aid)]
 errors=[]
 for section in SECTIONS[aid]:
  if not re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$",content,re.MULTILINE|re.IGNORECASE): errors.append(err("PM_MISSING_SECTION","sections",f"required section {section!r} is missing"))
 if data.get("schema_version") not in {"1",1}: errors.append(err("PM_INVALID_SCHEMA_VERSION","schema_version","schema_version must be 1",data.get("schema_version")))
 VALIDATORS[aid](data,errors); return aid,errors

def main(argv=None):
 p=argparse.ArgumentParser(); p.add_argument("artifact_path"); p.add_argument("--repo-root",default="."); p.add_argument("--json",action="store_true"); a=p.parse_args(argv)
 aid,errors=validate(Path(a.artifact_path)); out={"valid":not errors,"artifact_id":aid,"artifact_path":str(Path(a.artifact_path).resolve()),"validator":VALIDATOR,"errors":errors,"validation_timestamp":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
 if a.json: print(json.dumps(out,indent=2))
 elif errors:
  for e in errors: print(f"ERROR {e['error_id']}: {e['message']}")
 else: print(f"{aid} validation passed")
 return 0 if not errors else 1
if __name__=="__main__": sys.exit(main())
