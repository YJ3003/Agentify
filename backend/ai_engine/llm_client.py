import os
import json
from google import genai
from google.genai import types

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    async def modernize(self, system_description: dict) -> dict:
        """
        Unified modernization analysis for both Codebase and Workflow inputs.
        Expects a normalized system_description dictionary.
        """
        if not self.client:
            return {
                "error": "Missing GEMINI_API_KEY",
                "framework": "N/A",
                "reason": "AI analysis unavailable.",
                "modernization_playbook": {}
            }

        prompt = f"""
        You are an expert Principal Software Architect specializing in legacy modernization and AI agentification.
        Your goal is to provide a comprehensive modernization playbook for the supplied system description.

        SYSTEM CONTEXT:
        Input Type: {system_description.get("input_type", "unknown")}
        System Name: {system_description.get("name", "Unnamed System")}
        Description: {system_description.get("description", "No description provided.")}
        
        FULL SYSTEM DATA:
        {json.dumps(system_description, indent=2)}

        INSTRUCTIONS:
        1. Analyze the provided system data.
        2. Treat both Codebase and Workflow inputs as equivalent.
        3. Use Google Search to ground recommendations.
        4. Do NOT default to specific frameworks (like CrewAI/LangGraph) unless justified.
        5. Provide concrete recommendations across ALL 9 categories.
        
        CRITICAL OUTPUT RULES:
        - "summary" fields MUST be < 120 characters. No prose.
        - "signals" are short tags (e.g. "High Impact", "Easy Integration").
        - "details" contains the verbose explanation.
        - "confidence" is a float 0.0-1.0.

        CATEGORIES:
        1. Agent Frameworks
        2. Automation / Workflow Engines
        3. Enterprise Integration Platforms
        4. Knowledge + RAG + Retrieval Systems
        5. Web / Real-Time Grounding Tools
        6. Developer Tooling / Code Intelligence
        7. Observability & Runtime
        8. Runtime / Deployment & Inference Engines
        9. Workflow Visualization Tools

        OUTPUT FORMAT (JSON ONLY):
        {{
            "system_summary": "High-level summary (< 2 sentences)...",
            "pain_points": ["Critical issue 1 (< 10 words)", "Critical issue 2"],
            "agent_opportunities": [
                {{
                    "location": "File or Step Name",
                    "summary": "Why this needs AI (< 120 chars)",
                    "signals": ["High Complexity", "Orchestration"],
                    "recommended_framework": "Framework Name",
                    "confidence": 0.9,
                    "details": {{
                        "reasoning": "Detailed explanation...",
                        "implementation_tips": "How to implement..."
                    }}
                }}
            ],
            "suggested_architecture": "Description of the proposed agentic architecture...",
            "modernization_playbook": {{
                "agent_frameworks": [ 
                    {{
                        "tool": "Name", 
                        "confidence": 0.9,
                        "summary": "Why this tool (< 120 chars)",
                        "signals": ["Python-native", "Graph-based"],
                        "details": {{
                            "why": "Detailed justification...",
                            "usage": "Specific usage pattern...",
                            "tradeoffs": "Pros/cons..."
                        }}
                    }} 
                ],
                "workflow_engines": [], 
                "integration_platforms": [],
                "rag_retrieval": [],
                "grounding_tools": [],
                "dev_tools": [],
                "observability": [],
                "runtime_inference": [],
                "visualization_tools": []
            }}
        }}
        """

        try:
            # Enable Google Search grounding
            tools = [types.Tool(google_search=types.GoogleSearch())]
            
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=tools
                )
            )
            
            print("----- GROUNDING METADATA (MODERNIZE) -----")
            if response.candidates and response.candidates[0].grounding_metadata:
                 print(response.candidates[0].grounding_metadata)
            else:
                 print("No grounding metadata found.")
            print("------------------------------------------")
            
            content = response.text
             # Clean up potential markdown formatting
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "")
            elif content.startswith("```"):
                content = content.replace("```", "")
                
            result = json.loads(content)
            # Normalize summary key for compatibility
            if "system_summary" in result:
                result["workflow_summary"] = result["system_summary"]
            return result
        except Exception as e:
            print(f"LLM Error: {e}")
            return {
                "error": str(e),
                "system_summary": "Analysis Generation Failed",
                "pain_points": ["The AI model failed to generate a valid structured response."],
                "agent_opportunities": [],
                "suggested_architecture": "We encountered an error while processing the AI response. This usually happens when the model generates invalid JSON. Please try analyzing the document again.",
                "modernization_playbook": {}
            }
