def get_explain_opportunity_prompt(opportunity: dict, code_slice: str) -> str:
    return f"""
        You are a Staff Software Engineer analyzing a specific component for refactoring into an AI Agent.
        
        CONTEXT:
        File: {opportunity.get('file')}
        Function: {opportunity.get('function')}
        Detected Signals: {', '.join(opportunity.get('signals', []))}
        
        CODE SNIPPET:
        ```python
        {code_slice}
        ```
        
        TASK:
        Explain why this specific component is a good candidate for agentification based ONLY on the code and signals provided.
        Do NOT hallucinate other files. Do NOT suggest generic workflows.
        
        OUTPUT FORMAT (JSON):
        {{
            "justification": "Concise technical explanation (< 200 chars)",
            "risk_assessment": "Specific risks in this code (e.g. database locks, external api latency)",
            "recommended_agent_pattern": "Reasoning Loop / Orchestrator / Tool User"
        }}
        """

def get_modernize_workflow_prompt(text: str) -> str:
    return f"""
        Analyze this business process workflow and suggest AI agent modernization.
        
        WORKFLOW TEXT:
        {text[:2000]}
        
        OUTPUT FORMAT (JSON):
        {{
            "workflow_summary": "Summary of the process",
            "modernization_playbook": {{
                "agent_frameworks": [
                    {{ "tool": "Framework Name", "summary": "Why this framework", "details": {{ "why": "...", "usage": "..." }} }}
                ],
                "workflow_engines": []
            }},
            "pain_points": ["List of inefficiencies"],
            "agent_opportunities": [
                {{
                    "location": "Step in process",
                    "summary": "Agent application here",
                    "recommended_framework": "Orchestrator"
                }}
            ]
        }}
        """

def get_playbook_generation_prompt(repo_context: str, tool_library_str: str) -> str:
    return f"""
        You are a Staff Principal Software Architect specializing in AI Agent Workflows and Legacy Modernization.
        
        TASK:
        Analyze the provided repository context to identify **where and how the workflow can be changed to make use of AI and AI Agents**.
        
        Your goal is NOT just to "sprinkle AI" on existing code, but to reimagine the business process as an Agentic Workflow.
        Think about:
        - Which human decisions can be offloaded to Reasoning Agents?
        - Which manual orchestrations can be handled by State Machines or Agents?
        - Where can data intake be automated by Tool Uses?
        
        REPOSITORY CONTEXT:
        {repo_context[:50000]} 
        
        {tool_library_str}
        
        
        OBJECTIVES:
        1. **Workflow Discovery**: Deduce the underlying business goal. What is the user trying to achieve?
        2. **Agentic Transformation**: Identify concrete opportunities to replace imperative logic with Agentic reasoning or orchestration.
        3. **Flexible Architecture**: Recommend the *right* architecture for the problem.
           - Start with the provided Project Tool Library.
           - **CRITICAL**: You have access to Google Search. If the provided library is insufficient or out of date, SEARCH for the best modern tools matching the user's technology stack.
        
        OUTPUT FORMAT (JSON):
        Your output must be a SINGLE valid JSON object.
        - Do NOT include markdown formatting (like ```json).
        - Do NOT include any text before or after the JSON.
        - If you used Search, incorporate the findings into the `details` fields of the JSON, do NOT output raw search results or citations.
        
        {{
            "system_summary": "Concise summary of the system's purpose and your proposed agentic transformation.",
            "pain_points": [
                "**Workflow Bottleneck**: Explanation of a manual or rigid process...",
                "**Hidden Complexity**: Explanation of logic that is better suited for an LLM..."
            ],
            "agent_opportunities": [
                {{
                    "location": "File :: Function (or Logical Area)",
                    "summary": "High-level description of the agent's role",
                    "recommended_framework": "Generic pattern name (e.g. 'Orchestrator', 'Researcher', 'Planner')",
                    "confidence": 0.8,
                    "details": {{
                        "reasoning": "Why this workflow step needs an agent.",
                        "risk_assessment": "Implementation challenges."
                    }}
                }}
            ],
            "modernization_playbook": {{
                "agent_frameworks": [
                    {{ 
                        "tool": "Tool Name (from Library or Search)", 
                        "confidence": 0.9, 
                        "summary": "How this tool enables the new workflow",
                        "signals": ["Signal 1", "Signal 2"],
                        "details": {{ "why": "Technical justification...", "usage": "Implementation strategy...", "tradeoffs": "..." }}
                    }}
                ],
                "observability": [
                    {{
                        "tool": "Tool Name",
                        "confidence": 0.8,
                        "summary": "Why this is needed",
                        "signals": ["Signal"],
                        "details": {{ "why": "...", "usage": "...", "tradeoffs": "..." }}
                    }}
                ]
            }}
        }}
        """
