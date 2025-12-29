from typing import Dict, List, Any

class RepoAdapter:
    """
    Adapts static analysis reports and code slices into a normalized system description
    suitable for the unified Modernization Engine.
    """

    def adapt(self, report: Dict[str, Any], slices: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Converts repo analysis data into a standardized system description.
        """
        slices = slices or []
        repo_name = report.get("repo", "Unknown Repo")
        summary = report.get("summary", {})
        files = report.get("files", {})
        dependencies = report.get("dependencies", {})
        agent_ops = report.get("agent_opportunities", [])

        # 1. High-level System Summary
        system_description = {
            "input_type": "repo",
            "system_type": "software_system",
            "name": repo_name,
            "languages": summary.get("languages", []),
            "stats": {
                "file_count": summary.get("files", 0),
                "total_complexity": summary.get("total_complexity", 0)
            },
            "entrypoints": self._identify_entrypoints(files),
            "key_flows": self._infer_key_flows(files),
            "pain_points": self._derive_pain_points(files, agent_ops),
            "components": [],
            "code_slices": slices
        }

        # 2. Component/File Details
        for filename, file_data in files.items():
            ast_data = file_data.get("ast", {})
            component = {
                "name": filename,
                "type": "module",
                "functions": [f["name"] for f in ast_data.get("functions", [])],
                "imports": ast_data.get("imports", []),
                "complexity": file_data.get("complexity", 0),
                "calls": ast_data.get("calls", [])
            }
            system_description["components"].append(component)

        return system_description

    def _identify_entrypoints(self, files: Dict[str, Any]) -> List[str]:
        """
        Heuristic: identifying likely entrypoints (main.py, app.py, index.js, etc.)
        """
        candidates = ["main.py", "app.py", "index.py", "wsgi.py", "manage.py", "index.js", "server.js"]
        found = []
        for f in files.keys():
            if f.lower() in candidates:
                found.append(f)
        
        # If no obvious candidates, return all files if small count, else top complexity
        if not found and files:
            # Sort by complexity
            sorted_files = sorted(files.items(), key=lambda x: x[1].get("complexity", 0), reverse=True)
            if sorted_files:
                found.append(sorted_files[0][0])
                
        return found

    def _infer_key_flows(self, files: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Infers logic flows based on function calls and imports.
        """
        flows = []
        # Simple heuristic: heavily called modules or high complexity modules represent core flows
        for filename, file_data in files.items():
            complexity = file_data.get("complexity", 0)
            if complexity > 10:
                ast = file_data.get("ast", {})
                flows.append({
                    "name": f"Complex Logic in {filename}",
                    "steps": [f"Function: {func['name']}" for func in ast.get("functions", [])[:5]],
                    "files": [filename],
                    "complexity": complexity
                })
        return flows

    def _derive_pain_points(self, files: Dict[str, Any], agent_ops: List[Dict[str, Any]]) -> List[str]:
        """
        Derives pain points from complexity and agent opportunities.
        """
        pain_points = []
        
        # From Agent Opportunities
        for op in agent_ops:
            if "reason" in op:
                pain_points.append(f"{op['file']}: {op['reason']}")

        # General Code Quality
        for filename, file_data in files.items():
            complexity = file_data.get("complexity", 0)
            if complexity > 15:
                pain_points.append(f"{filename} has very high cyclomatic complexity ({complexity}).")
            
            ast = file_data.get("ast", {})
            if len(ast.get("functions", [])) > 20:
                pain_points.append(f"{filename} is a large monolith with {len(ast.get('functions', []))} functions.")

        return list(set(pain_points)) # Deduplicate
