from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from backend.modernization.engine import ModernizationEngine
from backend.auth.firebase import verify_token

router = APIRouter()
# We can eventually deprecate WorkflowAnalyzer if ModernizationEngine covers all features
modernization_engine = ModernizationEngine()

@router.post("/analyze")
async def analyze_workflow_document(
    file: UploadFile = File(None),
    text_input: str = Form(None),
    uid: str = Depends(verify_token)
):
    try:
        # Extract text first (using helper from Engine or manually)
        text = ""
        if file:
            text = await modernization_engine.text_extractor.extract(file)
        elif text_input:
            text = text_input
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        analysis = await modernization_engine.modernize_workflow(text, uid)
        return analysis
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
async def get_workflow_analysis(
    id: str,
    uid: str = Depends(verify_token)
):
    result = modernization_engine.get_workflow_report(id, uid)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result
