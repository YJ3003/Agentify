import ast

class ComplexityCalculator:
    def calculate(self, content: str) -> int:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return 0
            
        complexity = 1 # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler, ast.BoolOp)):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                # Functions themselves don't add to cyclomatic complexity of the module, 
                # but we can track them. For now, let's just count branching.
                pass
                
        return complexity
