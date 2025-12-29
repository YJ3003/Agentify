from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.analysis.analyzer import Analyzer
from typing import List, Dict, Any
from backend.auth.firebase import verify_token
import os
import json

router = APIRouter()

class AnalysisRequest(BaseModel):
    repo_name: str # owner/name

@router.post("/run")
async def run_analysis(
    request: AnalysisRequest,
    uid: str = Depends(verify_token)
):
    try:
        owner, name = request.repo_name.split("/")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repo name format")
        
    # We need to find the repo. It might be in user-scoped dir if we updated that, 
    # but for now repos might still be global or we need to check user's repo dir.
    # Assuming repos are cloned to backend/repos/{owner}/{name} globally for now?
    # If users see "repositories", they are seeing what git clone produced.
    # We should probably update repo cloning to be user-scoped too, but step by step.
    
    repo_path = os.path.join("backend", "repos", owner, name)
    
    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail="Repository not found. Please clone it first.")
        
    analyzer = Analyzer(repo_path, f"{owner}-{name}")
    try:
        report = analyzer.run()
        
        # Save to user scoped directory
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        reports_dir = os.path.join(user_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        report_path = os.path.join(reports_dir, f"{owner}-{name}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
    return {"status": "ok", "report": report}

@router.get("/list")
async def list_reports(uid: str = Depends(verify_token)):
    from backend.auth.user_manager import user_manager
    user_dir = user_manager._get_user_dir(uid)
    report_dir = os.path.join(user_dir, "reports")
    
    if not os.path.exists(report_dir):
        return []
        
    reports = []
    for file in os.listdir(report_dir):
        if file.endswith(".json"):
            reports.append(file.replace(".json", ""))
    return reports

@router.get("/{report_id}")
async def get_report(report_id: str, uid: str = Depends(verify_token)):
    from backend.auth.user_manager import user_manager
    user_dir = user_manager._get_user_dir(uid)
    report_path = os.path.join(user_dir, "reports", f"{report_id}.json")
    
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")
        
    with open(report_path, 'r') as f:
        return json.load(f)
