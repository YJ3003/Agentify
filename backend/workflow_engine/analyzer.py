import os
import json
import uuid
from fastapi import UploadFile
from backend.workflow_engine.text_extractor import TextExtractor
from backend.ai_engine.llm_client import LLMClient

class WorkflowAnalyzer:
    def __init__(self):
        self.extractor = TextExtractor()
        self.llm_client = LLMClient()
        self.storage_dir = os.path.join("backend", "data", "workflows")
        os.makedirs(self.storage_dir, exist_ok=True)

    async def analyze(self, file: UploadFile = None, text_input: str = None) -> dict:
        text = ""
        if file:
            text = await self.extractor.extract(file)
        elif text_input:
            text = text_input
        else:
            raise ValueError("No input provided")
            
        analysis = await self.llm_client.analyze_workflow(text)
        
        # Save analysis with ID
        report_id = str(uuid.uuid4())
        analysis["id"] = report_id
        analysis["original_text_snippet"] = text[:200] + "..." if len(text) > 200 else text
        
        self._save_report(report_id, analysis)
        
        return analysis

    def _save_report(self, report_id: str, data: dict):
        path = os.path.join(self.storage_dir, f"{report_id}.json")
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def get_report(self, report_id: str) -> dict:
        path = os.path.join(self.storage_dir, f"{report_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return json.load(f)
