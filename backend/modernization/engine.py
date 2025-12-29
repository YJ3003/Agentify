import os
import json
import uuid
from backend.ai_engine.llm_client import LLMClient
from backend.modernization.adapters.repo_adapter import RepoAdapter
from backend.workflow_engine.text_extractor import TextExtractor
from backend.ai_engine.recommender import Recommender # To reuse slice collection logic or finding reports

class ModernizationEngine:
    def __init__(self):
        self.llm_client = LLMClient()
        self.repo_adapter = RepoAdapter()
        self.text_extractor = TextExtractor()
        # Initialize Recommender just for its helper methods if needed, or implement similar logic
        # For now, we will handle file loading manually or reuse existing helpers
        
    async def modernize_repo(self, report_id: str, uid: str) -> dict:
        """
        Orchestrates the modernization of a code repository.
        """
        # 1. Load Analysis Report
        # Try loading from user-scoped dir first, then legacy
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        
        report_path = os.path.join(user_dir, "reports", f"{report_id}.json")
        if not os.path.exists(report_path):
             # Fallback to global reports (for shared/legacy)
             report_path = os.path.join("backend", "data", "reports", f"{report_id}.json")
        
        if not os.path.exists(report_path):
             raise FileNotFoundError(f"Report {report_id} not found")
        
        with open(report_path, 'r') as f:
            report = json.load(f)

        # 2. Collect Code Slices
        repo_name = report.get("repo")
        repo_path = self._find_repo_path(repo_name)
        
        slices = []
        if repo_path:
             from backend.ai_engine.slice_collector import SliceCollector
             collector = SliceCollector()
             slices = collector.collect(report, repo_path)
        
        # 3. Adapt
        system_description = self.repo_adapter.adapt(report, slices)
        
        # 4. Modernize
        playbook = await self.llm_client.modernize(system_description)
        
        # Save Result
        self._save_result(report_id, playbook, "repo", uid)
        
        return playbook

    async def modernize_workflow(self, text: str, uid: str) -> dict:
        """
        Orchestrates modernization of a text-based workflow.
        """
        system_description = {
            "input_type": "workflow",
            "system_type": "business_process",
            "name": "Uploaded Workflow Document",
            "description": text,
            "key_flows": [], 
            "pain_points": [],
            "components": [],
            "code_slices": []
        }
        
        playbook = await self.llm_client.modernize(system_description)
        
        # Generate ID for workflow
        workflow_id = str(uuid.uuid4())
        playbook["id"] = workflow_id
        playbook["original_text_snippet"] = text[:200]
        
        self._save_result(workflow_id, playbook, "workflow", uid)
        return playbook

    def _find_repo_path(self, repo_name_slug: str) -> str:
        # Duplicated helper for finding repo path
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

    def get_workflow_report(self, report_id: str, uid: str) -> dict:
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        
        # Check user scoped new location
        path_new = os.path.join(user_dir, "modernization", "workflow", f"{report_id}.json")
        if os.path.exists(path_new):
             with open(path_new, 'r') as f:
                 return json.load(f)
        
        # Fallback to old global location
        path_old = os.path.join("backend", "data", "modernization", "workflow", f"{report_id}.json")
        if os.path.exists(path_old):
             with open(path_old, 'r') as f:
                 return json.load(f)

        # Fallback to really old location
        path_oldest = os.path.join("backend", "data", "workflows", f"{report_id}.json")
        if os.path.exists(path_oldest):
             with open(path_oldest, 'r') as f:
                 return json.load(f)
                 
        return None

    def _save_result(self, id: str, data: dict, source_type: str, uid: str):
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        
        # Save to user_data/{uid}/modernization/{source_type}/{id}.json
        base_dir = os.path.join(user_dir, "modernization", source_type)
        os.makedirs(base_dir, exist_ok=True)
        path = os.path.join(base_dir, f"{id}.json")
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def list_workflow_reports(self, uid: str) -> list:
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        workflow_dir = os.path.join(user_dir, "modernization", "workflow")
        
        reports = []
        if os.path.exists(workflow_dir):
            for filename in os.listdir(workflow_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(workflow_dir, filename), 'r') as f:
                            data = json.load(f)
                            # Extract minimal info for listing
                            reports.append({
                                "id": data.get("id", filename.replace(".json", "")),
                                "name": data.get("name", "Untitled Workflow"),
                                "summary": data.get("workflow_summary", "")[:100] + "...",
                                "created_at": data.get("created_at", "") # If we had timestamp
                            })
                    except Exception:
                        continue
        return reports
