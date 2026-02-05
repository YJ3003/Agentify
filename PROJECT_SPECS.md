# Agentify Project Specifications

## 1. Executive Summary

**Agentify** is an intelligent modernization engine designed to transform legacy codebases into scalable, agentic systems. It automates the analysis of existing repositories, identifies architectural pain points (high complexity, tight coupling), and generates actionable blueprints ("Playbooks") for refactoring code into AI agents.

The system leverages **static code analysis** (AST, Control Flow Graphs) for deterministic metrics and **Generative AI** (Google Gemini 2.5 Flash) for semantic understanding and architectural recommendations.

---

## 2. System Architecture

The project follows a decoupled **Client-Server Architecture**:

### A. Frontend (Client)
- **Role**: User Interface, Dashboard, & Orchestrator.
- **Tech**: Next.js 16 (React 19), TailwindCSS v4, shadcn/ui.
- **Responsibilities**:
    - Managing user session state (Firebase Auth).
    - Visualizing analysis reports (Charts, Graphs).
    - interacting with the Backend API.

### B. Backend (Server)
- **Role**: Heavy Compute, File Processing, & AI Gateway.
- **Tech**: FastAPI (Python 3.12+).
- **Responsibilities**:
    - Cloning and managing git repositories.
    - Running CPU-intensive static analysis (AST parsing).
    - maintaining the interface with Google Gemini.
    - **Persistence**: Managing local file storage for user sessions.

### C. Data Persistence Strategy
**Critical Note**: Agentify uses a **Local-First / File-Based** persistence model.
- **User Data**: Stored locally in `user_data/{firebase_uid}/`.
    - Includes: Saved Reports, Modernization Playbooks, GitHub Tokens.
- **Global Data**: Stored in `backend/data/` (for fallbacks/templates).
- **Firestore**: **NOT USED** for application data. It is only utilized implicitly by Firebase Authentication for managing user identities.

---

## 3. Detailed Data Flow

### 3.1 Authentication & Token Sync
1.  **Login**: User signs in via GitHub on the Frontend (using Firebase SDK).
2.  **Token Retrieval**: Firebase returns an ID Token (for identity) and a GitHub Access Token (for repo access).
3.  **Sync**: Frontend calls `POST /auth/github/sync` with these tokens.
4.  **Backend Storage**: Backend validates the ID Token and saves the GitHub Access Token to `user_data/{uid}/github_token.txt`.
    *   *Why?* To allow the backend to run `git clone` operations asynchronously without requiring the frontend to pass the token every time.

### 3.2 Repository Analysis Pipeline
1.  **Connect**: Frontend requests `GET /github/repos`. Backend reads the local `github_token.txt` and fetches the list from GitHub API.
2.  **Select**: User selects a repo. Backend clones it to `backend/repos/{owner}/{name}`.
3.  **Analyze**:
    - `Analysis Engine` scans files.
    - Parses AST to calculate Complexity & Dependency Graphs.
    - Output: `Analysis Report` (JSON) saved to `user_data/{uid}/reports/{repo_id}.json`.

### 3.3 Modernization Engine (AI)
1.  **Ingest**: Reads the `Analysis Report`.
2.  **Slice**: Extracts "Code Slices" (actual source code) from high-complexity modules.
3.  **Prompt**: Sends context + slices to Google Gemini (`google-genai` SDK).
4.  **Generate**: LLM returns a structured "Playbook" recommending specific Agent Frameworks (LangGraph, CrewAI).
5.  **Save**: Playbook saved to `user_data/{uid}/modernization/repo/{repo_id}.json`.

---

## 4. Technology Stack

### Frontend
- **Framework**: [Next.js 16](https://nextjs.org/) (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS v4
- **State**: React Context (`UseAuth`)
- **Icons**: Lucide React

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.12+
- **AI SDK**: `google-genai` (Official Google Gemini SDK)
- **Analysis Tools**:
    - `ast` (Standard Library)
    - `networkx` (Graph Theory)
    - `gitpython` (Git operations)

---

## 5. Backend Module Breakdown (`backend/`)

| Module | Sub-components | Responsibility |
| :--- | :--- | :--- |
| `ai_engine` | `recommender.py`, `llm_client.py` | Handles Prompt Engineering and Gemini API calls. |
| `analysis` | `analyzer.py`, `complexity.py` | Static Analysis core. Calculates metrics data. |
| `auth` | `firebase.py`, `github_sync.py` | Verifies Firebase tokens; manages local token files. |
| `modernization`| `engine.py` | High-level orchestrator linking Analysis and AI phases. |
| `workflow_engine`| `routes.py`, `text_extractor.py` | Handles non-code inputs (PDF/Text) for business process modernization. |

---

## 6. Directory Structure

```text
/
├── app/                  # Next.js Frontend
│   ├── context/          # Global State (Auth)
│   ├── dashboard/        # Main App Pages
│   └── components/       # Shadcn UI Components
├── backend/              # FastAPI Backend
│   ├── main.py           # Entry Point
│   ├── repos/            # Cloned Repositories (Temp Storage)
│   └── ...modules
├── user_data/            # [CRITICAL] Local Persistence Layer
│   └── {uid}/            # Per-user isolated storage
│       ├── reports/      # Static Analysis Results
│       └── modernization/# AI Generated Playbooks
└── lib/                  # Shared Types & API Wrappers
```

---

## 7. Future Roadmap

- **Graph Database**: Move dependency graphs from JSON to Neo4j for deeper query capabilities.
- **Multi-Agent Simulation**: Allow users to "run" the proposed agentic workflow in a sandbox.
- **IDE Extension**: Port the analysis engine to a VS Code Extension.
