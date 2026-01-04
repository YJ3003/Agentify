import ast
import re
from typing import Dict, Any, List

class ASTParser:
    def parse(self, file_path: str, content: str) -> Dict[str, Any]:
        if file_path.endswith('.py'):
            return self._parse_python(content)
        elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx', '.go', '.java')):
            return self._parse_regex(content, file_path)
        else:
             return self._empty_result()

    def _parse_python(self, content: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self._empty_result(error="SyntaxError")

        classes = []
        functions = []
        imports = []
        calls = []
        control_structures = {"if": 0, "for": 0, "while": 0}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({"name": node.name, "lineno": node.lineno, "end_lineno": getattr(node, "end_lineno", node.lineno)})
            elif isinstance(node, ast.FunctionDef):
                functions.append({"name": node.name, "lineno": node.lineno, "end_lineno": getattr(node, "end_lineno", node.lineno)})
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

    def _parse_regex(self, content: str, file_path: str) -> Dict[str, Any]:
        lines = content.split('\n')
        functions = []
        imports = []
        classes = []
        
        # Simple heuristics
        # JS/TS: function foo(), const foo = () =>, class Foo
        # Go: func Foo(), type Foo struct
        
        for i, line in enumerate(lines):
            lineno = i + 1
            line = line.strip()
            
            # Functions
            if re.search(r'function\s+\w+', line) or re.search(r'const\s+\w+\s*=\s*(async\s*)?\([^)]*\)\s*=>', line) or re.search(r'func\s+\w+', line):
                 # Extract name - very naive
                 name = "anonymous"
                 match = re.search(r'function\s+(\w+)', line)
                 if match: name = match.group(1)
                 else:
                     match = re.search(r'const\s+(\w+)', line)
                     if match: name = match.group(1)
                     else:
                        match = re.search(r'func\s+(\w+)', line)
                        if match: name = match.group(1)
                 
                 functions.append({
                     "name": name,
                     "lineno": lineno,
                     "end_lineno": lineno + 20 # Placeholder approximation
                 })
                 
            # Imports
            if line.startswith('import ') or line.startswith('require(') or ' from ' in line:
                 # Clean up import to get package name
                 # import { x } from 'y' -> y
                 match = re.search(r'from\s+[\'"]([^\'"]+)[\'"]', line)
                 if match: imports.append(match.group(1))
                 elif re.search(r'require\([\'"]([^\'"]+)[\'"]\)', line):
                     match = re.search(r'require\([\'"]([^\'"]+)[\'"]\)', line)
                     if match: imports.append(match.group(1))

        return {
            "classes": classes,
            "functions": functions,
            "imports": list(set(imports)),
            "calls": [],
            "control_structures": {"if": 0, "for": 0, "while": 0} # TODO
        }

    def _empty_result(self, error=None):
         return {
            "error": error,
            "classes": [],
            "functions": [],
            "imports": [],
            "calls": [],
            "control_structures": {"if": 0, "for": 0, "while": 0}
        }
