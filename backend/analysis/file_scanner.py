import os
from typing import List

class FileScanner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.supported_extensions = {'.py', '.ts', '.js', '.jsx', '.tsx', '.go', '.java'}
        self.ignore_dirs = {'node_modules', '.git', '__pycache__', 'dist', 'build', 'venv', 'env'}

    def scan(self) -> List[str]:
        files_list = []
        for root, dirs, files in os.walk(self.repo_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in self.supported_extensions:
                    full_path = os.path.join(root, file)
                    # Store relative path
                    rel_path = os.path.relpath(full_path, self.repo_path)
                    files_list.append(rel_path)
        return files_list
