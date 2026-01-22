# Agentify Project Documentation

## 1. Executive Summary

**Agentify** is an intelligent modernization engine designed to transform legacy codebases into scalable, agentic systems. It automates the analysis of existing repositories, identifies architectural pain points (high complexity, tight coupling), and generates actionable blueprints ("Playbooks") for refactoring code into AI agents (using frameworks like LangGraph, CrewAI, PydanticAI).

The system combines **static code analysis** (AST, Control Flow Graphs) with **Generative AI** (Gemini 2.5 Flash) to provide both deterministic metrics and semantic understanding of the codebase.

---

## 2. System Architecture

The project follows a **Client-Server Architecture**:

- **Frontend**: A cohesive Next.js 16 application acting as the dashboard for users to connect repos, view analysis, and interact with the AI.
- **Backend**: A FastAPI (Python) server that handles heavy lifting: cloning repos, running static analysis, and interfacing with LLMs.
- **Database/Storage**: Uses the local filesystem for repo storage, report caching, and user data. Authentication is managed via Firebase.

### High-Level Data Flow

1.  **User Interaction**: User connects a repository via the Frontend.
2.  **Repo Acquisition**: Backend clones the repository locally.
3.  **Static Analysis**: The `Analysis Engine` scans files, parses ASTs, calculates complexity, and builds dependency graphs. It produces a `Analysis Report (JSON)`.
4.  **AI Orchestration**: The `AI Engine` reads the report and extracts "text slices" of high-interest code (e.g., complex functions).
5.  **GenAI Generation**: These slices are sent to Google Gemini (LLM) with a comprehensive system prompt.
6.  **Playbook Generation**: The LLM returns a structured "Modernization Playbook" (JSON) which suggests specific agentic refactoring strategies.
7.  **Visualization**: The Frontend renders these insights as charts, graphs, and actionable items.

---

## 3. Technology Stack

### Frontend
- **Framework**: [Next.js 16 (App Router)](https://nextjs.org/)
- **Language**: TypeScript
- **Styling**: TailwindCSS v4, `shadcn/ui` components.
- **State Management**: React Context (`app/context`).
- **Data Visualization**: Recharts (for complexity charts).
- **Icons**: Lucide React.
- **Auth**: Firebase Client SDK + NextAuth (custom implementation via `app/auth`).

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.12+
- **Static Analysis**:
    - `ast`: Python Abstract Syntax Tree parsing.
    - `networkx`: Managing dependency graphs.
- **AI Integration**:
    - `google-generativeai`: Client for Gemini models.
- **Data Persistence**: JSON-based filesystem storage (User data in `user_data/`, global data in `backend/data/`).

---

## 4. Backend Implementation Details

### Directory Structure (`backend/`)

| Directory | Purpose |
| :--- | :--- |
| `main.py` | Entry point. Configures FastAPI app, CORS, and routers. |
| `ai_engine/` | Logic for interacting with LLMs and generating recommendations. |
| `analysis/` | Core static analysis logic (AST, Complexity, Dependency Graphs). |
| `auth/` | Authentication handlers (GitHub OAuth, Firebase Token verification). |
| `modernization/` | Orchestration of the "Modernization" workflow (end-to-end flow). |
| `repos/` | Temporary storage for cloned GitHub repositories. |
| `data/` | Storage for generated reports and analysis data. |

### Key Modules

#### A. Analysis Engine (`backend/analysis`)
The `Analyzer` class (`analyzer.py`) orchestrates the static analysis pipeline:

1.  **`FileScanner`**: Recursively lists relevant source files.
2.  **`ASTParser`**: Parses code (Python-focused) to understand structure (classes, functions).
3.  **`ComplexityCalculator`**: Computes Cyclomatic Complexity for functions/files to identify difficult-to-maintain code.
4.  **`DependencyGraph`**: Maps imports to build a directed graph of module dependencies (`networkx`).
5.  **`HeuristicDetector`**: Uses rule-based logic (regex, pattern matching) to find "candidates" for agents (e.g., classes named `*Manager`, functions with high complexity).

**Output**: A comprehensive JSON report containing file metrics, dependency maps, and heuristic candidates.

#### B. AI Engine (`backend/ai_engine`)
The `Recommender` class (`recommender.py`) acts as the bridge between static data and GenAI:

1.  **Input**: Takes the Analysis Report (JSON).
2.  **Context Building (`SliceCollector`)**: detailed in `slice_collector.py`. It extracts the *actual code* of the most complex files and the candidate functions identified by heuristics. It does NOT send the whole repo to the LLM to save tokens.
3.  **Prompting (`LLMClient`)**: Sends a structured prompt to Gemini 2.5 Flash. The prompt asks the AI to act as a "Senior Architect" and recommend:
    - **Agent Frameworks**: LangGraph (for orchestration), CrewAI (for role-based agents), etc.
    - **Observability**: Tools like Arize Phoenix.
    - **Refactoring Steps**: Concrete advice on how to split the code.
4.  **Merging**: Combines the high-confidence AI insights with the raw heuristic data to form the final "Modernization Playbook".

#### C. Authentication (`backend/auth`)
Uses a hybrid approach:
- **GitHub OAuth**: Used to obtain a GitHub Access Token for cloning repos on behalf of the user.
- **Firebase**: Manages user identity. The backend verifies Firebase ID tokens passed in headers.

---

## 5. Frontend Implementation Details

### Directory Structure (`app/`)

| Path | Purpose |
| :--- | :--- |
| `app/layout.tsx` | Root layout, providers (Theme, Auth). |
| `app/page.tsx` | Landing page. |
| `app/dashboard/` | Main authenticated area. |
| `app/components/` | Shared UI components (Buttons, Cards, Charts). |
| `lib/api.ts` | Typed fetch wrappers for communicating with the backend APIs. |

### Key Workflows

1.  **Connect Repo**:
    - User authenticates with GitHub.
    - Selects a repository from the list.
    - Backend clones the repo to `backend/repos/{owner}/{name}`.
2.  **Run Analysis**:
    - User clicks "Analyze".
    - Backend `Analyzer` runs. Progress is polled or pushed (currently HTTP-based).
    - Results displayed in `app/dashboard/reports/[id]`.
3.  **Generate Playbook**:
    - User clicks "Generate Playbook".
    - Backend `Recommender` runs.
    - AI results are overlayed on the static analysis data.

---

## 6. Data Models & Storage

The system currently uses **Local User Context** storage.

- **User Data**: Stored in `user_data/{firebase_uid}/`.
    - `reports/`: JSON files containing static analysis results.
    - `modernization/repo/`: JSON files containing AI playbooks.
- **Global Data**: Fallback in `backend/data/` for non-authenticated or demo usage.

### Key JSON Schemas

**Analysis Report**:
```json
{
  "repo": "agentify",
  "summary": { "files": 50, "total_complexity": 120 },
  "files": {
    "backend/main.py": { "complexity": 5, "ast": {...} }
  },
  "dependency_graph": {...},
  "agent_opportunities": [
    { "file": "manager.py", "type": "Orchestrator", "confidence": "High" }
  ]
}
```

**Modernization Playbook**:
```json
{
  "system_summary": "Monolithic architecture...",
  "pain_points": ["High Coupling", "Implicit Orchestration"],
  "agent_frameworks": [
    { "tool": "LangGraph", "reason": "Stateful workflows detected..." }
  ]
}
```
