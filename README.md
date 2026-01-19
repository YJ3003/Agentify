
<div align="center">
  <h1>Agentify</h1>
  <p><b>Intelligent Code Modernization & Analysis Engine</b></p>
  
  <a href="https://nextjs.org">
    <img src="https://img.shields.io/badge/Next.js_16-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  </a>
  <a href="https://react.dev">
    <img src="https://img.shields.io/badge/React_19-20232a?style=for-the-badge&logo=react&logoColor=61dafb" alt="React" />
  </a>
  <a href="https://fastapi.tiangolo.com">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  </a>

</div>

<br />

## ⚡ Overview

**Agentify** is an advanced modernization engine designed to transform legacy codebases into intelligent, agentic systems. By combining static code analysis (`AST`, `CFG`, `Dependency Graphs`) with Generative AI, Agentify generates actionable "Playbooks" to refract monolithic logic into scalable, agent-based workflows.

It's not just a linter—it's a **blueprint generator for the AI era**.

## ✨ Key Features

- **🔍 Deep Static Analysis**: Automatically scans repositories to calculate cyclomatic complexity, map dependencies, and identify tightly coupled modules.
- **🤖 AI-Powered Recommendations**: Uses LLMs (`Gemini`/`OpenAI`) to analyze code slices and suggest specific modernization strategies (e.g., "Refactor this manager class into a LangGraph node").
- **📊 Interactive Dashboard**: Visualizes system health, complexity hotspots, and modernization progress in a sleek, real-time UI.
- **🛡️ Secure & Private**: Runs locally with user-scoped data storage.

## 🛠 Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **UI Context**: React 19
- **Styling**: TailwindCSS v4 + `shadcn/ui`
- **Visualization**: Lucide Icons, Recharts

### Backend
- **Core**: FastAPI (Python)
- **Analysis**: `ast`, `networkx` (Dependency Graphs)
- **AI Engine**: Custom `LLMClient` & `SliceCollector`

## 🚀 Getting Started

### Prerequisites
- Node.js 20+
- Python 3.10+
- Pip & Npm

### Prerequisites - Detailed
Before you begin, you will need to acquire a few keys:

1.  **Google Gemini API Key**:
    *   Visit [Google AI Studio](https://aistudio.google.com/).
    *   Create a new API Key for `Gemini 2.5 Flash`.
    *   Save this for your `.env` file.

2.  **Firebase Project**:
    *   Go to [Firebase Console](https://console.firebase.google.com/).
    *   Create a project.
    *   **Auth**: Enable "GitHub" sign-in method in Authentication settings.
    *   **Service Account**: Go to *Project Settings* -> *Service Accounts*.
    *   Click **"Generate new private key"**.
    *   Rename the downloaded file to `firebase_service_account.json` and move it to the `backend/` directory.

3.  **GitHub OAuth App**:
    *   Go to GitHub -> Settings -> Developer Settings -> OAuth Apps.
    *   Create a new App.
    *   **Homepage URL**: `http://localhost:3000`
    *   **Callback URL**: `http://localhost:3000/auth/callback`
    *   Copy the `Client ID` and `Client Secret` (Client Secret is only needed if you want to verify on backend, mainly Client ID for frontend).

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/agentify.git
    cd agentify
    ```

2.  **Setup Environment Variables**
    ```bash
    cp .env.example .env
    ```
    Open `.env` and fill in the values:

    | Variable | Description | Where to find it |
    | :--- | :--- | :--- |
    | `GEMINI_API_KEY` | Google AI Key | Google AI Studio |
    | `GITHUB_CLIENT_ID` | OAuth Client ID | GitHub Developer Settings |
    | `NEXT_PUBLIC_FIREBASE_API_KEY` | Firebase Config | Firebase Console (Project Settings) |
    | `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Firebase Config | Firebase Console |
    | `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Firebase Config | Firebase Console |
    | `NEXT_PUBLIC_FIREBASE_APP_ID` | Firebase Config | Firebase Console |

3.  **Setup Backend**
    ```bash
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\\Scripts\\activate

    # Install dependencies
    pip install -r backend/requirements.txt
    
    # IMPORTANT: Ensure your service account key is in place
    # backend/firebase_service_account.json
    ```

4.  **Setup Frontend**
    ```bash
    npm install
    ```

### Running the App

Run both services concurrently:

**Terminal 1 (Backend)**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 (Frontend)**
```bash
npm run dev
```

Visit `http://localhost:3000` to start modernizing your code.