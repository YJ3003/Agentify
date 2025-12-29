export const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function exchangeCode(code: string) {
  const res = await fetch(`${API_URL}/auth/github/exchange`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code }),
  });
  
  if (!res.ok) {
    throw new Error("Failed to exchange code");
  }
  
  return res.json();
}

// ... (API_URL)

export async function getRepos(token: string) {
    const res = await fetch(`${API_URL}/github/repos`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        throw new Error("Failed to fetch repos");
    }

    return res.json();
}

export async function selectRepo(repoFullName: string, token: string) {
    const res = await fetch(`${API_URL}/github/select-repo`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ repo_full_name: repoFullName, access_token: token }), // Note: access_token for github might be different from firebase token
    });

    if (!res.ok) {
        throw new Error("Failed to select repo");
    }

    return res.json();
}

export async function runAnalysis(repoFullName: string, token: string) {
    const res = await fetch(`${API_URL}/analysis/run`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ repo_name: repoFullName }),
    });

    if (!res.ok) {
        throw new Error("Failed to run analysis");
    }

    return res.json();
}

export async function getReports(token: string) {
    const res = await fetch(`${API_URL}/analysis/list`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (!res.ok) {
        throw new Error("Failed to fetch reports");
    }
    return res.json();
}

export async function getReport(id: string, token: string) {
    const res = await fetch(`${API_URL}/analysis/${id}`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (!res.ok) {
        throw new Error("Failed to fetch report");
    }
    return res.json();
}

export async function generateRecommendations(reportId: string, token: string) {
    const res = await fetch(`${API_URL}/ai/recommend`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ report_id: reportId }),
    });

    if (!res.ok) {
        throw new Error("Failed to generate recommendations");
    }
    return res.json();
}

export async function modernizeRepo(reportId: string, token: string) {
    const res = await fetch(`${API_URL}/modernize/repo`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
             "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ report_id: reportId }),
    });

    if (!res.ok) {
        throw new Error("Failed to generate modernization playbook");
    }
    return res.json();
}

export async function uploadWorkflow(file: File | null, text: string | null, token: string) {
    const formData = new FormData();
    if (file) formData.append("file", file);
    if (text) formData.append("text", text);

    const res = await fetch(`${API_URL}/workflow/analyze`, {
        method: "POST",
        headers: {
             "Authorization": `Bearer ${token}`
        },
        body: formData,
    });

    if (!res.ok) {
        throw new Error("Failed to analyze workflow");
    }
    return res.json();
}

export async function getWorkflowAnalysis(id: string, token: string) {
    const res = await fetch(`${API_URL}/workflow/${id}`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (!res.ok) {
        throw new Error("Failed to fetch workflow analysis");
    }
    return res.json();
}

export async function syncGithubToken(githubAccessToken: string, token: string) {
    const res = await fetch(`${API_URL}/auth/github/sync`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ github_access_token: githubAccessToken }),
    });

    if (!res.ok) {
        throw new Error("Failed to sync GitHub token");
    }
    return res.json();
}

export async function getWorkflowReports(token: string) {
    const res = await fetch(`${API_URL}/modernize/workflows`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        throw new Error("Failed to fetch workflow reports");
    }
    return res.json();
}
