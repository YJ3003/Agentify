import os
from fastapi import APIRouter, HTTPException, Header, Body, Depends
from pydantic import BaseModel
import httpx
import git
from typing import List, Optional
import shutil

router = APIRouter()

class RepoSelectRequest(BaseModel):
    repo_full_name: str
    access_token: str

from backend.auth.firebase import verify_token
from backend.auth.user_manager import user_manager

@router.get("/repos")
async def get_repos(uid: str = Depends(verify_token)):
    print(f"DEBUG: get_repos called for uid: {uid}")
    # Retrieve user's GitHub token
    github_token = user_manager.get_github_token(uid)
    if not github_token:
        # If no token, return empty list or specific error?
        # For now, empty list indicates no connection key
        return []
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github.v3+json"
            },
            params={"per_page": 200, "sort": "updated"}
        )

        if response.status_code != 200:
            # Token might be invalid or expired
            print(f"GitHub API Error: {response.text}")
             # If unauthorized, maybe token is bad.
            if response.status_code == 401:
                 return [] # Treat as no repos/disconnected
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch repos")

        repos = response.json()
        
        # Minimal data
        minimized_repos = []
        for repo in repos:
            minimized_repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "private": repo["private"],
                "language": repo["language"],
                "updated_at": repo["updated_at"],
                "clone_url": repo["clone_url"]
            })
            
        return minimized_repos

@router.post("/select-repo")
async def select_repo(request: RepoSelectRequest, uid: str = Depends(verify_token)):
    # Format: owner/name
    try:
        owner, name = request.repo_full_name.split("/")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repo name format")

    # Get token for cloning
    github_token = user_manager.get_github_token(uid)
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub account not connected")

    # Use a token-authenticated URL for cloning
    # https://<token>@github.com/owner/name.git
    clone_url = f"https://{github_token}@github.com/{request.repo_full_name}.git"
    
    # Store in global repos for now? OR User scoped repos?
    # CLI/Analysis tools often assume backend/repos/{owner}/{name}
    # To support multi-tenancy properly, we should scope repos too.
    # But for this fix, we stick to the existing path to avoid breaking Analyzer.
    # HOWEVER, this is a race condition risk if two users clone same repo.
    # For MVP, we accept this, but the LISTING of available repos comes from GitHub API which is scoped.
    
    target_dir = os.path.join("backend", "repos", owner, name)
    
    # Clean up if exists
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        
    try:
        git.Repo.clone_from(clone_url, target_dir)
    except git.GitCommandError as e:
        raise HTTPException(status_code=500, detail=f"Failed to clone repo: {str(e)}")
        
    return {"status": "cloned"}
