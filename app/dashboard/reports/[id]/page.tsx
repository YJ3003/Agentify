"use client"

import { useEffect, useState, use } from "react"
import { useAuth } from "@/app/context/AuthContext"
import { getReport, modernizeRepo, getModernizationRecommendation } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { ModernizationPlaybook } from "@/components/ModernizationPlaybook"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Terminal, Lightbulb, Sparkles, Loader2, AlertTriangle, CheckCircle2, Info } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

import ReactMarkdown from "react-markdown"
import { AgentOpportunityCard } from "@/components/AgentOpportunityCard"

export default function ReportDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params)
  const { getToken } = useAuth()
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [recommendation, setRecommendation] = useState<any>(null)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    const fetchReport = async () => {
        const token = await getToken()
        if (!token) return
        
        try {
            // Fetch report and try to fetch saved recommendation in parallel
            const reportPromise = getReport(resolvedParams.id, token);
            const recommendationPromise = getModernizationRecommendation(resolvedParams.id, token);

            const [reportData, recommendationData] = await Promise.all([
                reportPromise,
                recommendationPromise
            ]);

            setReport(reportData);
            if (recommendationData) {
                setRecommendation(recommendationData);
            }
        } catch (error) {
            console.error("Failed to load report data", error);
        } finally {
            setLoading(false);
        }
    }
    fetchReport()
  }, [resolvedParams.id, getToken])

  const handleGenerateAI = async () => {
      const token = await getToken()
      if (!token) return

      setGenerating(true)
      modernizeRepo(resolvedParams.id, token)
        .then(setRecommendation)
        .catch(console.error)
        .finally(() => setGenerating(false))
  }

  if (loading) return <div className="space-y-4"><Skeleton className="h-12 w-full" /><Skeleton className="h-64 w-full" /></div>
  if (!report) return <div>Report not found</div>

  return (
    <TooltipProvider>
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent w-fit">{report.repo}</h1>
        <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-muted-foreground mr-1">Total Complexity:</span>
            <Badge variant="outline" className="text-base px-3 py-1">{report.summary.total_complexity}</Badge>
            <Tooltip>
                <TooltipTrigger>
                    <Info className="w-4 h-4 text-muted-foreground hover:text-foreground transition-colors" />
                </TooltipTrigger>
                <TooltipContent>
                    <p className="max-w-xs">Aggregate cyclomatic complexity score. Higher values indicate more complex codebases that may be harder to maintain.</p>
                </TooltipContent>
            </Tooltip>
        </div>
      </div>
      
      <div className="flex justify-end">
         <Button onClick={handleGenerateAI} disabled={generating || recommendation} className="gap-2">
            {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            {recommendation ? "Workflow Agentified" : "Agentify Workflow"}
         </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
            <CardHeader className="pb-2"><CardTitle className="text-sm font-medium">Files Analyzed</CardTitle></CardHeader>
            <CardContent><div className="text-2xl font-bold">{report.summary.files}</div></CardContent>
        </Card>
        <Card>
            <CardHeader className="pb-2"><CardTitle className="text-sm font-medium">Languages</CardTitle></CardHeader>
            <CardContent>
                <div className="flex gap-2">
                    {report.summary.languages.map((l: string) => <Badge key={l}>{l}</Badge>)}
                </div>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center justify-between">
                    Agent Candidates
                    <Tooltip>
                        <TooltipTrigger><Info className="w-3 h-3 text-muted-foreground/50 hover:text-foreground" /></TooltipTrigger>
                        <TooltipContent><p className="max-w-[200px]">Candidates for refactoring into AI Agents based on code signals.</p></TooltipContent>
                    </Tooltip>
                </CardTitle>
            </CardHeader>
            <CardContent><div className="text-2xl font-bold">{report.agent_opportunities.length}</div></CardContent>
        </Card>
      </div>

      {recommendation ? (
        <Card className="border-indigo-500/20 bg-indigo-500/5 dark:bg-indigo-500/10">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-indigo-500" />
                    AI Agentification Playbook
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                {recommendation.error ? (
                    <div className="text-red-500">Error: {recommendation.error}</div>
                ) : (
                    <>
                         <div className="grid gap-6 md:grid-cols-2">
                             {/* Pain Points first - The Why */}
                            <Card className="border-red-200 dark:border-red-900 bg-red-50 dark:bg-red-950/20">
                                <CardHeader className="pb-2">
                                    <CardTitle className="flex items-center text-red-600 dark:text-red-400 text-sm">
                                        <AlertTriangle className="mr-2 h-4 w-4" /> Architectural Pain Points
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <ul className="list-disc list-inside space-y-2">
                                        {recommendation.pain_points?.map((point: string, i: number) => (
                                            <li key={i} className="text-sm leading-relaxed">
                                                <span className="inline-block align-top">
                                                    <ReactMarkdown components={{
                                                        p: ({node, ...props}) => <span {...props} />,
                                                        strong: ({node, ...props}) => <span className="font-semibold text-red-700 dark:text-red-300" {...props} />
                                                    }}>{point}</ReactMarkdown>
                                                </span>
                                            </li>
                                        ))}
                                    </ul>
                                </CardContent>
                            </Card>

                            <Card className="border-green-200 dark:border-green-900 bg-green-50 dark:bg-green-950/20">
                                <CardHeader className="pb-2">
                                    <CardTitle className="flex items-center text-green-600 dark:text-green-400 text-sm">
                                        <Lightbulb className="mr-2 h-4 w-4" /> The Solution
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="prose prose-sm dark:prose-invert max-w-none">
                                        <ReactMarkdown>{recommendation.system_summary}</ReactMarkdown>
                                    </div>
                                    <div className="mt-4 pt-4 border-t border-green-200 dark:border-green-800">
                                        <p className="text-xs font-semibold text-green-700 dark:text-green-300 uppercase tracking-wide mb-2">Recommended Stack</p>
                                        <div className="flex flex-wrap gap-2">
                                            {recommendation.modernization_playbook?.agent_frameworks?.map((fw: any) => (
                                                <Badge key={fw.tool} className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">
                                                    {fw.tool}
                                                </Badge>
                                            ))}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                        
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="font-semibold text-lg flex items-center gap-2">
                                    <Terminal className="w-5 h-5" /> Agentification Candidates
                                </h3>
                                <Badge variant="secondary">{recommendation.agent_opportunities?.length} Identified</Badge>
                            </div>
                            <div className="grid gap-4">
                                {recommendation.agent_opportunities?.map((opp: any, i: number) => (
                                    <AgentOpportunityCard key={i} opp={opp} />
                                ))}
                            </div>
                        </div>

                        {/* Modernization Playbook / How-To */}
                        <div className="mt-8 pt-6 border-t border-indigo-500/20">
                             <h3 className="font-semibold text-lg mb-4">Implementation Strategy</h3>
                             <ModernizationPlaybook playbook={recommendation.modernization_playbook} />
                        </div>
                        
                    </>
                )}
            </CardContent>
        </Card>
      ) : (
          /* Initial State - Show Raw List if Playbook not generated yet */
          report.agent_opportunities.length > 0 && (
            <div className="space-y-4 opacity-60 hover:opacity-100 transition-opacity">
                <div className="flex items-center justify-between">
                     <h2 className="text-xl font-semibold flex items-center gap-2"><Lightbulb className="w-5 h-5" /> Potential Candidates</h2>
                     <span className="text-xs text-muted-foreground">Agentify Workflow to see full details</span>
                </div>
               
                {report.agent_opportunities.map((opp: any, i: number) => (
                    <Alert key={i}>
                        <Terminal className="h-4 w-4" />
                        <AlertTitle>{opp.file || opp.file_path} :: {opp.function_name}</AlertTitle>
                        <AlertDescription>
                            <p className="line-clamp-1">{opp.explanation}</p>
                        </AlertDescription>
                    </Alert>
                ))}
            </div>
          )
      )}

      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Detailed Analysis</h2>
        <Accordion type="single" collapsible className="w-full">
            {Object.entries(report.files).map(([file, data]: [string, any]) => (
                <AccordionItem key={file} value={file}>
                    <AccordionTrigger className="font-mono text-sm">
                        {file} 
                        <span className="ml-auto mr-4 text-xs text-muted-foreground flex items-center gap-1">
                             Complexity: {data.complexity}
                             {data.complexity > 10 && (
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <span><AlertTriangle className="w-3 h-3 text-amber-500" /></span>
                                    </TooltipTrigger>
                                    <TooltipContent><p>High complexity. Consider refactoring.</p></TooltipContent>
                                </Tooltip>
                             )}
                        </span>
                    </AccordionTrigger>
                    <AccordionContent>
                        <div className="grid gap-4 md:grid-cols-2">
                            {data.ast.error ? (
                                <div className="col-span-2 text-red-500 text-sm">
                                    Parse Error: {data.ast.error}
                                </div>
                            ) : (
                                <>
                                    <div className="space-y-2">
                                        <h4 className="font-semibold text-xs uppercase text-muted-foreground">Functions</h4>
                                        <ul className="list-disc list-inside text-sm">
                                            {data.ast.functions?.map((f: any) => (
                                                <li key={f.name}>{f.name} (Line {f.lineno})</li>
                                            ))}
                                            {(!data.ast.functions || data.ast.functions.length === 0) && <li className="text-muted-foreground italic">None</li>}
                                        </ul>
                                    </div>
                                    <div className="space-y-2">
                                        <h4 className="font-semibold text-xs uppercase text-muted-foreground">Imports</h4>
                                        <div className="flex flex-wrap gap-1">
                                            {data.ast.imports?.map((imp: string) => (
                                                <Badge key={imp} variant="outline" className="text-xs">{imp}</Badge>
                                            ))}
                                            {(!data.ast.imports || data.ast.imports.length === 0) && <span className="text-muted-foreground italic text-sm">None</span>}
                                        </div>
                                    </div>
                                </>
                            )}
                        </div>
                    </AccordionContent>
                </AccordionItem>
            ))}
        </Accordion>
      </div>
    </div>
    </TooltipProvider>
  )
}
