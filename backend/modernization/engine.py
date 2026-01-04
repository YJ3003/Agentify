import os
import json
import uuid
from backend.ai_engine.recommender import Recommender
from backend.workflow_engine.text_extractor import TextExtractor

class ModernizationEngine:
    def __init__(self):
        self.text_extractor = TextExtractor()
        
    async def modernize_repo(self, report_id: str, uid: str) -> dict:
        """
        Orchestrates the modernization using the new AI Engine Recommender.
        """
        # Delegate to the new Recommender which implements the rigor
        # We pass report_id. Recommender needs to handle user-scoped loading?
        # Current Recommender doesn't accept UID in init, let's patch it or handle pathing there.
        # But wait, Recommender assumes "backend/data/reports".
        # We need to make Recommender aware of User context OR copy report to global (bad).
        
        # Better: Update Recommender to accept UID (TODO in previous step).
        # For now, let's instantiate Recommender and let it run.
        # If Recommender is not user-aware, we might fail to find the report if it's in user_dir.
        
        # Let's fix Recommender to find the report by looking in both places
        # OR we pass the absolute path/uid to Recommender.
        
        recommender = Recommender(report_id)
        # Monkey-patch or update Recommender to look in user dir using a helper?
        # Actually I should update Recommender.py to take an optional UID or search path.
        # But to be safe and quick:
        
        # 1. Try to find the report manually
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        user_report_path = os.path.join(user_dir, "reports", f"{report_id}.json")
        
        # 2. If valid, ensure Recommender can read it.
        # I will update Recommender.py in the next step to support this.
        # For now, let's assume Recommender will be updated to take `uid`.
        
        recommender = Recommender(report_id, uid)
        return await recommender.generate()
        
    async def modernize_workflow(self, text: str, uid: str) -> dict:
        """
        Orchestrates modernization of a text-based workflow.
        Legacy flow - we can keep utilizing LLMClient directly or refactor this too.
        """
        from backend.ai_engine.llm_client import LLMClient
        client = LLMClient()
        
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
        
        # We need a non-deprecated method for workflow modernization
        # or we update LLMClient to support this specific case.
        # Let's fallback to a specific workflow prompt in LLMClient?
        # Or just use the deprecated method but un-deprecate it for WORKFLOWS only?
        
        # For now, let's inline the workflow prompt here or restore LLMClient logic for non-code inputs.
        # To avoid breaking workflows, I will restore basic LLMClient functionality for this path.
        
        # But wait, LLMClient.modernize returns empty now.
        # I MUST fix LLMClient.modernize to work for workflows OR implement `modernize_workflow`.
        
        playbook = await client.modernize_workflow_text(text)
        
        workflow_id = str(uuid.uuid4())
        playbook["id"] = workflow_id
        playbook["original_text_snippet"] = text[:200]
        
        self._save_result(workflow_id, playbook, "workflow", uid)
        return playbook

    def get_workflow_report(self, report_id: str, uid: str) -> dict:
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        
        path_new = os.path.join(user_dir, "modernization", "workflow", f"{report_id}.json")
        if os.path.exists(path_new):
             with open(path_new, 'r') as f:
                 return json.load(f)
                 
        path_old = os.path.join("backend", "data", "modernization", "workflow", f"{report_id}.json")
        if os.path.exists(path_old):
             with open(path_old, 'r') as f:
                 return json.load(f)

        return None
                  
    def get_repo_recommendation(self, report_id: str, uid: str) -> dict:
        """
        Retrieves a previously generated repo modernization recommendation.
        Returns None if not found.
        """
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
        
        path = os.path.join(user_dir, "modernization", "repo", f"{report_id}.json")
        if os.path.exists(path):
             with open(path, 'r') as f:
                 return json.load(f)
                 
        return None

    def _save_result(self, id: str, data: dict, source_type: str, uid: str):
        from backend.auth.user_manager import user_manager
        user_dir = user_manager._get_user_dir(uid)
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
                            reports.append({
                                "id": data.get("id", filename.replace(".json", "")),
                                "name": data.get("name", "Untitled Workflow"),
                                "summary": data.get("workflow_summary", "")[:100] + "...",
                                "created_at": data.get("created_at", "")
                            })
                    except Exception:
                        continue
        return reports
