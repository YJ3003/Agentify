from typing import Dict, List, Any

class DependencyGraph:
    def __init__(self):
        self.graph = {}

    def build(self, files_data: Dict[str, Any]) -> Dict[str, List[str]]:
        # files_data is { "file_path": { "imports": [...] } }
        for file, data in files_data.items():
            imports = data.get("ast", {}).get("imports", [])
            self.graph[file] = imports
        return self.graph
