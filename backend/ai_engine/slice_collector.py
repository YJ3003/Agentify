import os

class SliceCollector:
    def collect(self, report: dict, repo_path: str) -> list:
        slices = []
        opportunities = report.get("agent_opportunities", [])
        
        # Cache file content to avoid repeated reads
        file_cache = {}

        for opp in opportunities:
            file_rel_path = opp.get("file_path") or opp.get("file") # Fallback for old keys if any
            if not file_rel_path:
                continue
                
            full_path = os.path.join(repo_path, file_rel_path)
            
            if file_rel_path not in file_cache:
                if not os.path.exists(full_path):
                     continue
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        file_cache[file_rel_path] = f.readlines()
                except UnicodeDecodeError:
                    continue
            
            lines = file_cache.get(file_rel_path)
            if not lines:
                continue
                
            start_line = opp.get("start_line", 1) - 1 # 0-indexed
            end_line = opp.get("end_line", start_line + 50)
            
            # Ensure bounds
            start_line = max(0, start_line)
            end_line = min(len(lines), end_line)
            
            code_snippet = "".join(lines[start_line:end_line])
            
            slices.append({
                "file": file_rel_path,
                "function": opp.get("function_name"),
                "start_line": start_line + 1,
                "end_line": end_line,
                "code": code_snippet,
                "reason": opp.get("explanation"),
                "signals": opp.get("signals", [])
            })
        
        return slices
