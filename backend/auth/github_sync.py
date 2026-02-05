from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.auth.firebase import verify_token
from backend.auth.user_manager import user_manager

router = APIRouter()

class GitHubTokenSyncRequest(BaseModel):
    github_access_token: str

@router.post("/sync")
async def sync_github_token(
    request: GitHubTokenSyncRequest,
    uid: str = Depends(verify_token)
):
    """
    Receives the GitHub Access Token from the frontend (obtained via Firebase sign-in)
    and stores it securely associated with the user's UID.
    """
    if not request.github_access_token:
        raise HTTPException(status_code=400, detail="Missing github_access_token")
        
    try:
        print(f"DEBUG: Syncing GitHub token for UID: {uid}")
        user_manager.save_github_token(uid, request.github_access_token)
        print("DEBUG: GitHub token saved successfully")
        return {"status": "synced"}
    except Exception as e:
        print(f"Failed to sync GitHub token: {e}")
        raise HTTPException(status_code=500, detail="Failed to save token")
