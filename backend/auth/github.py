import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ExchangeRequest(BaseModel):
    code: str

@router.post("/exchange")
async def exchange_code(request: ExchangeRequest):
    client_id = os.getenv("GITHUB_CLIENT_ID")
    client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI")

    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Server misconfiguration: Missing GitHub credentials")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": request.code,
                "redirect_uri": redirect_uri,
            },
        )
        
        if response.status_code != 200:
             raise HTTPException(status_code=400, detail="Failed to exchange code")

        data = response.json()
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data.get("error_description", "Unknown error"))
            
        return {"access_token": data["access_token"]}
