import os
import json
from typing import Dict, Any
from backend.analysis.file_scanner import FileScanner
from backend.analysis.ast_parser import ASTParser
from backend.analysis.complexity import ComplexityCalculator
from backend.analysis.dependency_graph import DependencyGraph
from backend.analysis.cfg_builder import CFGBuilder
from backend.analysis.slicer import Slicer
from backend.ai_engine.heuristics import HeuristicDetector

class Analyzer:
    def __init__(self, repo_path: str, repo_name: str):
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.scanner = FileScanner(repo_path)
        self.ast_parser = ASTParser()
        self.complexity_calc = ComplexityCalculator()
        self.dep_graph = DependencyGraph()
        self.cfg_builder = CFGBuilder()
        self.cfg_builder = CFGBuilder()
        self.slicer = Slicer()
        self.heuristic_detector = HeuristicDetector()

    def run(self) -> Dict[str, Any]:
        files = self.scanner.scan()
        files_data = {}
        
        total_complexity = 0
        
        for file_rel_path in files:
            full_path = os.path.join(self.repo_path, file_rel_path)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue # Skip non-utf8 files
                
            ast_data = self.ast_parser.parse(file_rel_path, content)
            complexity = self.complexity_calc.calculate(content)
            
            # Tools that might fail on non-python
            try:
                cfg = self.cfg_builder.build(content)
            except:
                cfg = {}
                
            try:
                slices = self.slicer.slice(content)
            except:
                slices = [] # Slicer might depend on AST
            
            total_complexity += complexity
            
            files_data[file_rel_path] = {
                "ast": ast_data,
                "complexity": complexity,
                "cfg": cfg,
                "slices": slices
            }
            
        dependencies = self.dep_graph.build(files_data)
        agent_opportunities = self._detect_agent_opportunities(files_data)
        
        # Detect languages
        detected_langs = set()
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext == '.py': detected_langs.add('python')
            elif ext in ['.js', '.jsx', '.ts', '.tsx']: detected_langs.add('typescript/javascript')
            elif ext == '.go': detected_langs.add('go')
            elif ext == '.java': detected_langs.add('java')

        report = {
            "repo": self.repo_name,
            "summary": {
                "files": len(files),
                "languages": list(detected_langs), 
                "total_complexity": total_complexity
            },
            "files": files_data,
            "dependencies": dependencies,
            "agent_opportunities": agent_opportunities
        }
        
        
        # self._save_report(report) # Responsibility moved to caller
        return report

    def _detect_agent_opportunities(self, files_data: Dict[str, Any]) -> list:
        # returns list of dicts
        opportunities = self.heuristic_detector.detect(files_data)
        return [opp.dict() for opp in opportunities]

    def _save_report(self, report: Dict[str, Any]):
        report_dir = os.path.join("backend", "data", "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"{self.repo_name}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
