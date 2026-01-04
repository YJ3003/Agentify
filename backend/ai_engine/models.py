from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class AgentOpportunity(BaseModel):
    """
    Represents a specific, code-anchored opportunity for agentification.
    """
    file_path: str = Field(..., description="Relative path to the file")
    function_name: str = Field(..., description="Name of the function or class")
    start_line: int = Field(..., description="Starting line number (1-indexed)")
    end_line: int = Field(..., description="Ending line number (1-indexed)")
    
    signals: List[str] = Field(default_factory=list, description="List of heuristic signals detected")
    verdict: Literal["candidate", "rejected"] = Field(..., description="Heuristic decision")
    risk_level: Literal["low", "medium", "high"] = Field(..., description="Risk assessment")
    
    suggested_agent_type: Optional[str] = Field(None, description="Type of agent suggested (e.g. Reasoning, Orchestration)")
    integration_boundary: Optional[str] = Field(None, description="Where the agent would integrate")
    
    explanation: Optional[str] = Field(None, description="Human-readable explanation (heuristic-generated)")
    llm_justification: Optional[str] = Field(None, description="LLM-generated explanation (optional)")
