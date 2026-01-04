import os
import json
import asyncio
from google import genai
from google.genai import types

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    async def _generate_with_retry(self, prompt: str, model: str = 'gemini-2.5-flash', retries: int = 3) -> dict:
        for attempt in range(retries):
            try:
                response = await self.client.aio.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                
                content = response.text
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "")
                
                return json.loads(content)
                
            except Exception as e:
                # Check for 429 or rate limit strings in error
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait_time = (2 ** attempt) * 2 + 5 # 7s, 9s, 13s... aggressive wait
                    print(f"Rate limited on {model}. Waiting {wait_time}s... (Attempt {attempt+1}/{retries})")
                    await asyncio.sleep(wait_time)
                else:
                    raise e
                    
        raise Exception("Max retries exceeded for AI generation")

    async def explain_opportunity(self, opportunity: dict, code_slice: str) -> dict:
        """
        Explain WHY a specific code component was flagged as an agent opportunity.
        Strictly bounded to the provided code slice.
        """
        if not self.client:
             return {"error": "AI unavailable"}

        # Construct restricted prompt
        prompt = f"""
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
        
        try:
            return await self._generate_with_retry(prompt, model='gemini-2.5-flash')
            
        except Exception as e:
            print(f"LLM Explanation Error: {e}")
            return {
                "justification": "AI explanation failed",
                "risk_assessment": "Unknown",
                "recommended_agent_pattern": "Manual Review"
            }

    async def modernize_workflow_text(self, text: str) -> dict:
        """
        Generates modernization playbook for text-based workflow descriptions.
        (Restored functionality for document uploads)
        """
        if not self.client:
            return {"error": "AI unavailable"}
            
        prompt = f"""
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
        
        try:
            return await self._generate_with_retry(prompt, model='gemini-2.5-flash')
        except Exception as e:
            print(f"Workflow Modernization Error: {e}")
            return {"error": str(e)}

    async def generate_playbook(self, repo_context: str) -> dict:
        """
        Generates a modernization playbook based on a holistic view of the repository.
        """
        if not self.client:
            return {"error": "AI unavailable"}
            
        prompt = f"""
        You are a Staff Principal Software Architect specializing in Legacy Modernization and Agentic AI.
        
        TASK:
        Analyze the provided repository context (File Tree, Dependencies, and Heuristic Signals) to deduce the actual business workflow and recommend a concrete Agentic Modernization Architecture.
        
        REPOSITORY CONTEXT:
        {repo_context[:50000]} 
        
        OBJECTIVES:
        1. **Deduce the Workflow**: What does this application actually do? (e.g. "A Triage App that uploads photos to Firebase and uses Gemini for analysis").
        2. **Filter Noise**: The heuristic scanner may have flagged UI components or utilities as "agents". IGNORE THEM unless they contain critical business logic. Focus on the CORE WORKFLOW.
        3. **Architect the Solution**: Recommend specific agents for the core parts of the workflow.
        
        OUTPUT FORMAT (JSON):
        {{
            "system_summary": "Concise (2 sentences) summary of what the system does and its architecture.",
            "pain_points": [
                "**Architectural Pain Point 1**: Explanation...",
                "**Architectural Pain Point 2**: Explanation..."
            ],
            "agent_opportunities": [
                {{
                    "location": "File :: Function",
                    "summary": "Brief explanation of what this agent would do",
                    "recommended_framework": "Orchestration Agent" | "Reasoning & Planning Agent" | "Tool Use Agent",
                    "confidence": 0.9,
                    "details": {{
                        "reasoning": "Why this is a good candidate (e.g. 'Central logic hub', 'Complex decision tree')",
                        "risk_assessment": "Potential challenges (e.g. 'State management', 'External API latency')"
                    }}
                }}
            ],
            "modernization_playbook": {{
                "agent_frameworks": [
                    {{ 
                        "tool": "LangGraph" | "CrewAI" | "PydanticAI" | "LangChain", 
                        "confidence": 0.9, 
                        "summary": "Why this tool fits this specific repo",
                        "signals": ["Stateful Workflow", "Complex Decomposition", "Type Safety"],
                        "details": {{ "why": "...", "usage": "...", "tradeoffs": "..." }}
                    }}
                ],
                "observability": [
                    {{
                        "tool": "Arize Phoenix" | "LangSmith",
                        "confidence": 0.8,
                        "summary": "Tracing recommendation",
                        "signals": ["External I/O"],
                        "details": {{ "why": "...", "usage": "...", "tradeoffs": "..." }}
                    }}
                ]
            }}
        }}
        """
        
        try:
            return await self._generate_with_retry(prompt, model='gemini-2.5-flash')
            
        except Exception as e:
            print(f"Playbook Generation Error: {e}")
            return {"error": str(e)}

    async def modernize(self, system_description: dict) -> dict:
        """
        DEPRECATED: Legacy method. 
        Retained for interface compatibility but should not be primary logic.
        """
        return {
            "modernization_playbook": {
                "agent_frameworks": [],
                "workflow_engines": []
            },
            "agent_opportunities": [] 
        }
