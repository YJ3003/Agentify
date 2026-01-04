import os
import json
from typing import Optional
from backend.ai_engine.slice_collector import SliceCollector
from backend.ai_engine.llm_client import LLMClient

class Recommender:
    def __init__(self, report_id: str, uid: Optional[str] = None):
        self.report_id = report_id
        self.uid = uid
        self.slice_collector = SliceCollector()
        self.llm_client = LLMClient()

    async def generate(self) -> dict:
        # 1. Load Analysis Report (Static Signals + Heuristics)
        report_path = self._find_report_path()
        if not report_path or not os.path.exists(report_path):
             raise FileNotFoundError(f"Report {self.report_id} not found")
        
        with open(report_path, 'r') as f:
            report = json.load(f)
            
        repo_name = report.get("repo")
        repo_path = self._find_repo_path(repo_name)
        
        if not repo_path:
             print("Warning: Repo path not found, skipping code extraction.")
        
        # 2. Collect Code Slices
        slices = []
        if repo_path:
            slices = self.slice_collector.collect(report, repo_path)
            
        # 3. Build Repo Context for AI
        repo_context = self._build_repo_context(report, slices)
        
        # 4. Generate AI Playbook (Holistic Analysis)
        ai_result = await self.llm_client.generate_playbook(repo_context)
        
        if ai_result.get("error"):
            # Fallback to heuristics if AI fails
            print(f"AI Generation Failed: {ai_result.get('error')}")
            # ... (keep existing fallback logic logic if needed, or just return basic report)
            # For now, let's just proceed with basic data
            recommendation = {
                 "system_summary": "AI generation failed. using static analysis.",
                 "pain_points": self._format_pain_points(set()),
                 "agent_opportunities": [],
                 "modernization_playbook": self._generate_playbook([], set())
            }
        else:
            # 5. Merge AI Findings with Heuristic Data
            # The AI returns "location": "File :: Function". We need to map this back to our heuristic signals if possible
            # to get line numbers, etc.
            
            final_opportunities = []
            
            # Index heuristics for lookup
            heuristic_map = {}
            for opp in report.get("agent_opportunities", []):
                key = f"{opp.get('file_path')} :: {opp.get('function_name')}"
                heuristic_map[key] = opp
                
            for ai_opp in ai_result.get("agent_opportunities", []):
                loc = ai_opp.get("location")
                matched_heuristic = heuristic_map.get(loc)
                
                # If AI found it, it's high confidence.
                enhanced_opp = {
                    "location": loc,
                    "file": loc.split(" :: ")[0] if " :: " in loc else loc,
                    "function": loc.split(" :: ")[1] if " :: " in loc else "",
                    "signals": matched_heuristic.get("signals", []) if matched_heuristic else ["AI Identified"],
                    "summary": ai_opp.get("summary"),
                    "confidence": ai_opp.get("confidence", 0.9),
                    "recommended_framework": ai_opp.get("recommended_framework"),
                    "details": ai_opp.get("details", {}),
                    "risk_assessment": ai_opp.get("details", {}).get("risk_assessment")
                }
                final_opportunities.append(enhanced_opp)
            
            recommendation = {
                "system_summary": ai_result.get("system_summary"),
                "pain_points": ai_result.get("pain_points", []),
                "agent_opportunities": final_opportunities,
                "modernization_playbook": ai_result.get("modernization_playbook")
            }
        
        self._save_recommendation(recommendation)
        return recommendation

    def _format_pain_points(self, signals: set) -> list:
        readable_points = []
        for s in signals:
            if "external_io_dependencies" in s:
                libs = s.split(": ")[1]
                readable_points.append(f"**High External coupling**: The codebase depends heavily on `{libs}` which can be hard to mock and test.")
            if "orchestration_naming_pattern" in s:
                readable_points.append("**Implicit Orchestration**: Workflow logic is embedded in code functions matching 'process' or 'manager' patterns, making it hard to visualize.")
            if "high_complexity_context" in s:
                readable_points.append("**Cognitive Load**: High cyclomatic complexity (>20) detected in key modules, increasing maintenance risk.")
        
        if not readable_points:
            readable_points.append("No critical architectural pain points detected.")
            
        return list(set(readable_points)) # Dedupe

    def _build_repo_context(self, report: dict, slices: list) -> str:
        """
        Constructs a text representation of the repo for the LLM.
        """
        lines = []
        lines.append("=== FILE STRUCTURE ===")
        # Top 50 files by complexity
        # Sort files by complexity
        files_data = report.get("files", {})
        sorted_files = sorted(files_data.items(), key=lambda x: x[1].get("complexity", 0), reverse=True)
        
        for f, data in sorted_files[:50]:
            lines.append(f"- {f} (Complexity: {data.get('complexity')})")
            
        lines.append("\n=== DEPENDENCIES (IMPORTS) ===")
        # Group by file
        deps = report.get("dependencies", {})
        for f, imports in deps.items():
            if imports:
                lines.append(f"{f} depends on: {', '.join(imports[:5])}")
                
        lines.append("\n=== HEURISTIC CANDIDATES ===")
        # List the raw signals found by static analysis
        for opp in report.get("agent_opportunities", []):
            if opp.get("verdict") == "candidate":
                lines.append(f"Candidate: {opp.get('file_path')} :: {opp.get('function_name')}")
                lines.append(f"  Signals: {', '.join(opp.get('signals', []))}")
                
        return "\n".join(lines)

    def _find_report_path(self) -> Optional[str]:
        # 1. User Scoped
        if self.uid:
            from backend.auth.user_manager import user_manager
            user_dir = user_manager._get_user_dir(self.uid)
            path = os.path.join(user_dir, "reports", f"{self.report_id}.json")
            if os.path.exists(path):
                return path
        
        # 2. Global Scoped (Legacy/Fallback)
        path = os.path.join("backend", "data", "reports", f"{self.report_id}.json")
        if os.path.exists(path):
            return path
            
        return None

    def _generate_playbook(self, opportunities: list, signals: set) -> dict:
        """
        Generates a structured playbook compatible with the frontend.
        """
        playbook = {
            "agent_frameworks": [],
            "workflow_engines": [],
            "observability": []
        }
        
        # Rule-based playbook generation
        has_orchestration = any("Orchestration" in o.get("recommended_framework", "") for o in opportunities)
        has_complexity = any("Reasoning" in o.get("recommended_framework", "") for o in opportunities)
        has_io = any("Tool Use" in o.get("recommended_framework", "") for o in opportunities)
        
        if has_orchestration:
            playbook["agent_frameworks"].append({
                "tool": "LangGraph",
                "confidence": 0.95,
                "summary": "Best for orchestration.",
                "signals": ["State Management"],
                "details": {
                    "why": "Your code contains stateful orchestration logic (e.g. process managers) which maps perfectly to LangGraph's state machine model.",
                    "usage": "Refactor the process_transaction functions into graph nodes.",
                    "tradeoffs": "Requires learning curve for graph definition."
                }
            })
            
        if has_complexity:
             playbook["agent_frameworks"].append({
                "tool": "CrewAI",
                "confidence": 0.8,
                "summary": "Best for complex decomposition.",
                "signals": ["High Complexity"],
                "details": {
                    "why": "High complexity functions suggest a need for breaking down logic into specialized roles.",
                    "usage": "Define agents for each distinct responsibility found in the complex modules.",
                    "tradeoffs": "Higher latency."
                }
            })
            
        if has_io:
             playbook["observability"].append({
                "tool": "Arize Phoenix",
                "confidence": 0.9,
                "summary": "Tracing for AI agents.",
                "signals": ["External I/O"],
                "details": {
                    "why": "Detected external dependencies require tracing.",
                    "usage": "Instrument your LLM calls.",
                    "tradeoffs": "Adds runtime overhead."
                }
            })
            
        if not playbook["agent_frameworks"]:
             playbook["agent_frameworks"].append({
                "tool": "PydanticAI",
                "confidence": 0.7,
                "summary": "Lightweight agentic features.",
                "signals": ["Low Complexity"],
                "details": {
                    "why": "No major orchestration signals found. Use lightweight structured outputs.",
                    "usage": "Use PydanticAI for strictly typed LLM responses.",
                    "tradeoffs": "Less ecosystem tools than LangChain."
                }
             })
            
        return playbook

    def _find_repo_path(self, repo_name_slug: str) -> str:
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
        if self.uid:
            from backend.auth.user_manager import user_manager
            user_dir = user_manager._get_user_dir(self.uid)
            out_dir = os.path.join(user_dir, "modernization", "repo")
        else:
            out_dir = os.path.join("backend", "data", "ai")
            
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{self.report_id}.json")
        with open(out_path, 'w') as f:
            json.dump(data, f, indent=2)
