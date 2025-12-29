import os

class SliceCollector:
    def collect(self, report: dict, repo_path: str) -> list:
        slices = []
        files = report.get("files", {})

        for file_rel_path, data in files.items():
            full_path = os.path.join(repo_path, file_rel_path)
            if not os.path.exists(full_path):
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                continue

            complexity = data.get("complexity", 0)
            functions = data.get("ast", {}).get("functions", [])
            
            # Heuristic: Extract functions from files with high complexity or many functions
            if complexity > 5 or len(functions) > 0:
                 for func in functions:
                    start_line = func["lineno"] - 1 # 0-indexed
                    # Naively estimate end line (until next function or end of file)
                    # For a real implementation, we would use AST end_lineno if available (Python 3.8+)
                    # Here we just take a chunk of lines
                    
                    category = "function"
                    reason = "Function found in analysis"
                    
                    if complexity > 10:
                        reason = f"High complexity ({complexity}) function"
                    
                    # Grab content (placeholder logic for extraction)
                    # We grab 20 lines or until end of file
                    end_line = min(start_line + 50, len(lines)) 
                    code_snippet = "".join(lines[start_line:end_line])
                    
                    slices.append({
                        "file": file_rel_path,
                        "function": func["name"],
                        "start_line": func["lineno"],
                        "end_line": end_line,
                        "code": code_snippet,
                        "reason": reason
                    })
        
        # Limit slices to avoid token limits in MVP
        return slices[:10]
