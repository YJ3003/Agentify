from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.ai_engine.recommender import Recommender
from backend.auth.firebase import verify_token

router = APIRouter()

class RecommendRequest(BaseModel):
    report_id: str

@router.post("/recommend")
async def recommend(
    request: RecommendRequest,
    uid: str = Depends(verify_token)
):
    # TODO: Pass uid to Recommender for user-scoped data
    recommender = Recommender(request.report_id, uid)
    try:
        result = await recommender.generate()
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
