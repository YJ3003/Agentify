from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.modernization.engine import ModernizationEngine
from backend.auth.firebase import verify_token

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

@router.get("/modernize/workflows")
async def list_workflows(uid: str = Depends(verify_token)):
    try:
        return engine.list_workflow_reports(uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
