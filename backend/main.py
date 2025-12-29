from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.auth import github as auth_github
from backend.github import repos as github_repos
from backend.analysis import routes as analysis_routes
from backend.ai_engine import routes as ai_routes
from backend.workflow_engine import routes as workflow_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_github.router, prefix="/auth/github", tags=["auth"])
app.include_router(github_repos.router, prefix="/github", tags=["github"])
app.include_router(analysis_routes.router, prefix="/analysis", tags=["analysis"])
app.include_router(ai_routes.router, prefix="/ai", tags=["ai"])
from backend.auth import github_sync
app.include_router(github_sync.router, prefix="/auth/github", tags=["auth"])
app.include_router(workflow_routes.router, prefix="/workflow", tags=["workflow"])
from backend.modernization import routes as modernization_routes
app.include_router(modernization_routes.router, tags=["modernization"])

@app.get("/")
def read_root():
    return {"message": "Agentify Backend is running"}
