"use client"

import { useEffect, useState, use } from "react"
import { useAuth } from "@/app/context/AuthContext"
import { getWorkflowAnalysis } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { CheckCircle2, AlertTriangle, Lightbulb, ArrowLeft } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

import ReactMarkdown from "react-markdown"
import { ModernizationPlaybook } from "@/components/ModernizationPlaybook"
import { AgentOpportunityCard } from "@/components/AgentOpportunityCard"
import ProtectedRoute from "@/components/ProtectedRoute"

export default function WorkflowResultPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params)
  const { getToken } = useAuth()
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAnalysis = async () => {
        const token = await getToken()
        if (!token) return
        
        getWorkflowAnalysis(resolvedParams.id, token)
          .then(setAnalysis)
          .catch(console.error)
          .finally(() => setLoading(false))
    }
    fetchAnalysis()
  }, [resolvedParams.id, getToken])

  if (loading) return <div className="container mx-auto py-10 px-4 space-y-4"><Skeleton className="h-12 w-full" /><Skeleton className="h-64 w-full" /></div>
  if (!analysis) return <div className="container mx-auto py-10 px-4">Analysis not found</div>

  return (
    <ProtectedRoute>
    <div className="container mx-auto py-10 px-4 max-w-4xl space-y-8">
      <Link href="/dashboard">
        <Button variant="ghost" className="mb-4 pl-0">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Dashboard
        </Button>
      </Link>
      
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tighter">Workflow Analysis</h1>
        <p className="text-muted-foreground">AI-driven insights for agentifying your process.</p>
      </div>

      <Card>
        <CardHeader>
            <CardTitle>Executive Summary</CardTitle>
        </CardHeader>
        <CardContent>
            <div className="prose dark:prose-invert max-w-none text-sm">
                <ReactMarkdown>{analysis.workflow_summary}</ReactMarkdown>
            </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="border-red-200 dark:border-red-900 bg-red-50 dark:bg-red-950/20">
            <CardHeader className="pb-2">
                <CardTitle className="flex items-center text-red-600 dark:text-red-400">
                    <AlertTriangle className="mr-2 h-5 w-5" /> Pain Points
                </CardTitle>
            </CardHeader>
            <CardContent>
                <ul className="list-disc list-inside space-y-1">
                    {analysis.pain_points.map((point: string, i: number) => (
                        <li key={i} className="text-sm">
                             <span className="inline-block align-top">
                                <ReactMarkdown components={{p: ({node, ...props}) => <span {...props} />}}>{point}</ReactMarkdown>
                             </span>
                        </li>
                    ))}
                </ul>
            </CardContent>
        </Card>

        <Card className="border-green-200 dark:border-green-900 bg-green-50 dark:bg-green-950/20">
            <CardHeader className="pb-2">
                <CardTitle className="flex items-center text-green-600 dark:text-green-400">
                    <Lightbulb className="mr-2 h-5 w-5" /> Opportunities
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="text-3xl font-bold mb-2">{analysis.agent_opportunities.length}</div>
                <p className="text-sm text-muted-foreground h-full">Areas identified for potential agentification.</p>
            </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Agent Opportunities</h2>
        {analysis.agent_opportunities.map((opp: any, i: number) => (
             <AgentOpportunityCard key={i} opp={opp} />
        ))}
      </div>

      <Card className="bg-zinc-950 text-zinc-50 border-zinc-800">
          <CardHeader>
              <CardTitle className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-400" />
                  Suggested Architecture
              </CardTitle>
          </CardHeader>
          <CardContent>
              <div className="prose prose-invert max-w-none text-sm">
                  <ReactMarkdown>{analysis.suggested_architecture}</ReactMarkdown>
              </div>
          </CardContent>
      </Card>

      <ModernizationPlaybook playbook={analysis.modernization_playbook} />
      
      <div className="text-xs text-muted-foreground border-t pt-4">
          <p className="font-semibold mb-1">Source Snippet:</p>
          <div className="font-mono bg-muted p-2 rounded whitespace-pre-wrap break-words max-h-40 overflow-y-auto">
            {analysis.original_text_snippet}
          </div>
      </div>
    </div>
    </ProtectedRoute>
  )
}
