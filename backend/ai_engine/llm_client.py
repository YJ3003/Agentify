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

    def _load_tool_library(self) -> str:
        """
        Dynamically reads the project's own tool library from lib/tools.ts.
        Parses TypeScript content and filters for relevant tools (Developers & Automation)
        to avoid flooding the context with irrelevant consumer apps.
        """
        try:
            # Resolve path to lib/tools.ts relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            tools_path = os.path.join(base_dir, "lib", "tools.ts")
            
            if not os.path.exists(tools_path):
                return "No local tool library found."

            with open(tools_path, 'r') as f:
                content = f.read()

            # Simple regex parser to extract relevant fields from the TS object structure
            # Looking for patterns like: name: "X", category: "Y", description: "Z"
            import re
            tools = []
            
            # Find all object blocks inside the TOOLS array
            matches = re.finditer(r'{\s*name:\s*"(.*?)",\s*category:\s*"(.*?)",.*?description:\s*"(.*?)",', content, re.DOTALL)
            
            # Categories considered relevant for "Agentic Workflow Modernization"
            RELEVANT_CATEGORIES = {"Developers", "Automation"}
            
            for m in matches:
                name = m.group(1)
                category = m.group(2)
                desc = m.group(3)
                
                if category in RELEVANT_CATEGORIES:
                    tools.append(f"- {name} ({category}): {desc}")
                
            if not tools:
                return "Tool library detected but no relevant tools found."
                
            return "=== RELEVANT PROJECT TOOLS (Developers & Automation) ===\n" + "\n".join(tools[:50]) # Limit to top 50 relevant ones
            
        except Exception as e:
            print(f"Error loading tool library: {e}")
            return "Error loading tool library."

    async def generate_playbook(self, repo_context: str) -> dict:
        """
        Generates a modernization playbook based on a holistic view of the repository.
        """
        if not self.client:
            return {"error": "AI unavailable"}

        # Load the dynamic tool library
        tool_library_str = self._load_tool_library()
            
        prompt = f"""
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
        3. **Flexible Architecture**: Recommend the *right* architecture for the problem using tools from the Project Tool Library where appropriate.
        
        OUTPUT FORMAT (JSON):
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
                    "confidence": 0.8-1.0,
                    "details": {{
                        "reasoning": "Why this workflow step needs an agent.",
                        "risk_assessment": "Implementation challenges."
                    }}
                }}
            ],
            "modernization_playbook": {{
                "agent_frameworks": [
                    {{ 
                        "tool": "Tool Name from Library (or best fit)", 
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
