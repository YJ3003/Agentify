import os
import json
import asyncio
from google import genai
from google.genai import types
from backend.ai_engine import prompts

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
                
                # Robustly extract JSON if wrapped in markdown code blocks
                import re
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
                else:
                    # Cleanup strictly if startswith (legacy fallback) but avoid naive replace checks
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    content = content.strip()

                return json.loads(content)
                
            except json.JSONDecodeError as e:
                print(f"JSON Parsing Failed on attempt {attempt+1}. Error: {e}")
                print(f"Raw Content Snippet: {content[:500]}...") # Print first 500 chars for debug
                if attempt == retries - 1:
                    raise e
                    
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

        # Construct restricted prompt using the new prompts module
        prompt = prompts.get_explain_opportunity_prompt(opportunity, code_slice)
        
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
            
        prompt = prompts.get_modernize_workflow_prompt(text)
        
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
            
        prompt = prompts.get_playbook_generation_prompt(repo_context, tool_library_str)
        
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
