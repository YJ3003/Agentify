import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.ai_engine.heuristics import HeuristicDetector
from backend.ai_engine.models import AgentOpportunity

def test_heuristic_detector():
    print("Testing HeuristicDetector...")
    detector = HeuristicDetector()
    
    # Mock Data
    file_path = "backend/services/payment_orchestrator.py"
    mock_ast = {
        "functions": [
            {"name": "process_transaction", "lineno": 10, "end_lineno": 50},
            {"name": "simple_helper", "lineno": 60, "end_lineno": 65}
        ],
        "imports": ["requests", "boto3", "json"]
    }
    
    files_data = {
        file_path: {
            "ast": mock_ast,
            "complexity": 25 # High complexity
        }
    }
    
    opportunities = detector.detect(files_data)
    
    assert len(opportunities) == 2, f"Expected 2 opportunities, got {len(opportunities)}"
    
    opp_map = {opp.function_name: opp for opp in opportunities}
    
    # Check Process Transaction (Orchestrator)
    proc = opp_map.get("process_transaction")
    assert proc is not None
    assert proc.verdict == "candidate"
    assert "orchestration_naming_pattern" in str(proc.signals)
    assert proc.suggested_agent_type == "Orchestration Agent"
    
    # Check Simple Helper (Reasoning - due to high complexity context)
    helper = opp_map.get("simple_helper")
    assert helper is not None
    assert helper.verdict == "candidate"
    assert "high_complexity_context" in str(helper.signals)
    assert helper.suggested_agent_type == "Reasoning & Planning Agent"
    
    print("✅ HeuristicDetector Test Passed!")

if __name__ == "__main__":
    test_heuristic_detector()
