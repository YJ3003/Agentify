import ast
from typing import Dict, Any, List

class ASTParser:
    def parse(self, file_path: str, content: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {
                "error": "SyntaxError",
                "classes": [],
                "functions": [],
                "imports": [],
                "calls": [],
                "control_structures": {"if": 0, "for": 0, "while": 0}
            }

        classes = []
        functions = []
        imports = []
        calls = []
        control_structures = {"if": 0, "for": 0, "while": 0}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({"name": node.name, "lineno": node.lineno})
            elif isinstance(node, ast.FunctionDef):
                functions.append({"name": node.name, "lineno": node.lineno})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
            elif isinstance(node, ast.If):
                control_structures["if"] += 1
            elif isinstance(node, ast.For):
                control_structures["for"] += 1
            elif isinstance(node, ast.While):
                control_structures["while"] += 1

        return {
            "classes": classes,
            "functions": functions,
            "imports": list(set(imports)),
            "calls": list(set(calls)),
            "control_structures": control_structures
        }
