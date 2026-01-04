from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.modernization.engine import ModernizationEngine
from backend.auth.firebase import verify_token
import os

router = APIRouter()
engine = ModernizationEngine()

class RepoModernizeRequest(BaseModel):
    report_id: str

@router.post("/modernize/repo")
async def modernize_repo(
    request: RepoModernizeRequest,
    uid: str = Depends(verify_token)
):
    try:
        result = await engine.modernize_repo(request.report_id, uid)
        if not result:
             raise HTTPException(status_code=404, detail="Analysis failed or report not found")
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/modernize/repo/{report_id}")
async def get_repo_recommendation(
    report_id: str,
    uid: str = Depends(verify_token)
):
    try:
        result = engine.get_repo_recommendation(report_id, uid)
        if not result:
             raise HTTPException(status_code=404, detail="Modernization report not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/modernize/workflows")
async def list_workflows(uid: str = Depends(verify_token)):
    try:
        return engine.list_workflow_reports(uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/modernize/workflow/{workflow_id}")
async def delete_workflow(workflow_id: str, uid: str = Depends(verify_token)):
    try:
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        
        # Delete workflow report
        path = os.path.join(user_dir, "modernization", "workflow", f"{workflow_id}.json")
        if os.path.exists(path):
            os.remove(path)
            return {"status": "deleted", "id": workflow_id}
        else:
            raise HTTPException(status_code=404, detail="Workflow report not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
