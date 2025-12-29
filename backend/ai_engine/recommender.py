import os
import json
from backend.ai_engine.slice_collector import SliceCollector
from backend.ai_engine.llm_client import LLMClient

class Recommender:
    def __init__(self, report_id: str, uid: str):
        self.report_id = report_id
        self.uid = uid
        self.slice_collector = SliceCollector()
        self.llm_client = LLMClient()

    async def generate(self) -> dict:
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(self.uid)
        
        # Load analysis report from user-scoped dir
        report_path = os.path.join(user_dir, "reports", f"{self.report_id}.json")
        if not os.path.exists(report_path):
             # Fallback to legacy location for backward compatibility
             legacy_path = os.path.join("backend", "data", "reports", f"{self.report_id}.json")
             if os.path.exists(legacy_path):
                 report_path = legacy_path
             else:
                 raise FileNotFoundError(f"Report {self.report_id} not found")
        
        with open(report_path, 'r') as f:
            report = json.load(f)
            
        repo_name = report.get("repo")
        repo_path = self._find_repo_path(repo_name)
        if not repo_path:
             raise FileNotFoundError("Source code not found for slicing")

        slices = self.slice_collector.collect(report, repo_path)
        recommendation = await self.llm_client.analyze_slices(slices)
        
        # Save recommendation
        self._save_recommendation(recommendation)
        
        return recommendation

    def _find_repo_path(self, repo_name_slug: str) -> str:
        # Expecting repo_name_slug like "owner-name"
        # We need to find "backend/repos/owner/name"
        repos_root = os.path.join("backend", "repos")
        if not os.path.exists(repos_root):
            return ""
            
        for owner in os.listdir(repos_root):
            owner_dir = os.path.join(repos_root, owner)
            if os.path.isdir(owner_dir):
                for name in os.listdir(owner_dir):
                    if f"{owner}-{name}" == repo_name_slug:
                         return os.path.join(owner_dir, name)
        return ""

    def _save_recommendation(self, data: dict):
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(self.uid)
        
        out_dir = os.path.join(user_dir, "ai")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{self.report_id}.json")
        with open(out_path, 'w') as f:
            json.dump(data, f, indent=2)
