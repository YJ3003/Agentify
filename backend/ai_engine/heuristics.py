from typing import Dict, Any, List
from backend.ai_engine.models import AgentOpportunity

class HeuristicDetector:
    """
    Deterministic engine for identifying agent opportunities based on static analysis signals.
    """
    
    def detect(self, files_data: Dict[str, Any]) -> List[AgentOpportunity]:
        opportunities = []
        
        for file_path, data in files_data.items():
            ast_data = data.get("ast", {})
            complexity = data.get("complexity", 0)
            
            # Analyze functions
            for func in ast_data.get("functions", []):
                opp = self._analyze_function(file_path, func, complexity, ast_data)
                if opp:
                    opportunities.append(opp)
                    
        return opportunities

    def _analyze_function(self, file_path: str, func: Dict[str, Any], file_complexity: int, file_ast: Dict[str, Any]) -> AgentOpportunity:
        signals = []
        name = func.get("name")
        start_line = func.get("lineno")
        end_line = func.get("end_lineno", start_line + 10) # Fallback if not provided
        
        # 1. Complexity Signal
        # We don't have function-level complexity in this MVP, using file-level proxy or simple heuristics
        # Ideally we'd calculate cyclomatic complexity per function. 
        # For now, let's use a placeholder if file complexity is VERY high, it likely trickles down.
        if file_complexity > 20: 
             signals.append("high_complexity_context")
             
        # 2. Context Filtering (path based)
        is_frontend = file_path.endswith(('.tsx', '.jsx', '.ts', '.js'))
        is_component = 'components' in file_path or 'views' in file_path or 'pages' in file_path
        
        # Skip UI event handlers and hooks in frontend components
        if is_frontend:
            low_value_prefixes = ['render', 'toggle', 'set', 'use', 'on', 'get', 'handle']
            # Allow 'handle' only if it's 'handleSubmit' or complex
            if any(name.startswith(p) for p in low_value_prefixes):
                # Exception: complex submit handlers might be agents
                if not (name.startswith('handle') and 'submit' in name.lower()):
                     return None # Skip pure UI handlers
            
            # Skip pure UI components (starting with Uppercase) unless they are in specific directories
            # actually we extracted definitions. If it's a function named "Home", it's a React component.
            if name[0].isupper() and is_component:
                 return None # Skip React components
                 
        # 3. External I/O Signals from imports
        imports = file_ast.get("imports", [])
        # Broader I/O detection including common patterns
        io_patterns = ["requests", "httpx", "aiohttp", "boto3", "sql", "mongo", "redis", "firebase", "api", "client", "ai", "openai", "anthropic", "google"]
        
        # Strict mode for frontend: only count "AI" or "API" as relevant I/O, ignore generic utils
        if is_frontend:
             # For frontend, "api" is too generic if it's just local.
             # We want specific external services or 'api' IF it's in a non-component file (like lib/api.ts)
             if is_component:
                 io_patterns = ["openai", "anthropic", "langchain", "firebase", "google"] # Strict for components
             
        detected_io = [imp for imp in imports if any(pat in imp.lower() for pat in io_patterns)]
        
        if detected_io:
             signals.append(f"external_io_dependencies: {', '.join(detected_io)}")
             
        # 4. Error Handling (Try/Except) - Not in current AST output, assuming generic
        # 5. Magic Strings / Heuristic Naming
        # Expanded keywords for typical agent tasks
        agent_keywords = ["process", "manager", "workflow", "run", "execute", "summarize", "generate", "analyze", "chat", "bot", "service", "job", "task"]
        # Removed 'handle' to avoid noise
        
        if any(x in name.lower() for x in agent_keywords):
            signals.append("orchestration_naming_pattern")
            
        # Decision Logic
        verdict = "rejected"
        risk = "low"
        agent_type = None
        
        # Rules for qualification
        if "orchestration_naming_pattern" in signals and detected_io:
            verdict = "candidate"
            risk = "medium"
            agent_type = "Orchestration Agent"
        elif "high_complexity_context" in signals and detected_io:
             verdict = "candidate"
             risk = "high"
             agent_type = "Reasoning & Planning Agent"
        elif detected_io and file_complexity > 5: # Relaxed rule: I/O + moderate complexity
             verdict = "candidate"
             risk = "low"
             agent_type = "Tool Use Agent"
             
        if verdict == "candidate":
            # Generate user-friendly explanation
            readable_explanation = ""
            if agent_type == "Orchestration Agent":
                readable_explanation = f"This function ('{name}') appears to coordinate multiple tasks or services."
                if detected_io:
                    readable_explanation += f" It interacts with external services like {', '.join(detected_io[:3])}."
            elif agent_type == "Reasoning & Planning Agent":
                readable_explanation = "This code handles complex logic and decision making."
                if detected_io:
                    readable_explanation += f" It integrates with {', '.join(detected_io[:3])} to perform its tasks."
            elif agent_type == "Tool Use Agent":
                 readable_explanation = f"This function interacts with external tools or APIs ({', '.join(detected_io[:3])})."
            
            # fallback
            if not readable_explanation:
                readable_explanation = f"Identified as a candidate for {agent_type} based on code patterns."

            return AgentOpportunity(
                file_path=file_path,
                function_name=name,
                start_line=start_line,
                end_line=end_line,
                signals=signals,
                verdict=verdict,
                risk_level=risk,
                suggested_agent_type=agent_type,
                integration_boundary="Internal Logic Replacement",
                explanation=readable_explanation
            )
            
        return None
