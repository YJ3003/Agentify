import ast

class ComplexityCalculator:
    def calculate(self, content: str) -> int:
        try:
            tree = ast.parse(content)
            complexity = 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler, ast.BoolOp)):
                    complexity += 1
            return complexity
        except SyntaxError:
            # Fallback for non-Python: Count branching keywords
            # Very rough approximation
            c = 1
            c += content.count("if ")
            c += content.count("for ")
            c += content.count("while ")
            c += content.count("case ")
            c += content.count("catch ")
            return c
