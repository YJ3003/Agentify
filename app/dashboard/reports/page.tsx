"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/app/context/AuthContext"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { getReports, getWorkflowReports, deleteReport, deleteWorkflowReport } from "@/lib/api"
import Link from "next/link"
import { FileText, FileCode, ArrowRight, Trash2 } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"

export default function ReportsPage() {
  const { getToken } = useAuth()
  const [repoReports, setRepoReports] = useState<string[]>([])
  const [workflowReports, setWorkflowReports] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
        const token = await getToken()
        if (!token) return
        
        try {
            const [repos, workflows] = await Promise.all([
                getReports(token),
                getWorkflowReports(token)
            ])
            setRepoReports(repos)
            setWorkflowReports(workflows)
        } catch (error) {
            console.error(error)
        } finally {
            setLoading(false)
        }
    }
    fetchData()
  }, [getToken])

  const handleDeleteRepo = async (e: React.MouseEvent, id: string) => {
      e.preventDefault() // Prevent navigation
      e.stopPropagation()
      
      if (!confirm("Are you sure you want to delete this report?")) return

      try {
          const token = await getToken()
          if (!token) return
          await deleteReport(id, token)
          setRepoReports(prev => prev.filter(r => r !== id))
      } catch (error) {
          console.error("Failed to delete report", error)
      }
  }

  const handleDeleteWorkflow = async (e: React.MouseEvent, id: string) => {
      e.preventDefault()
      e.stopPropagation()
      
      if (!confirm("Are you sure you want to delete this report?")) return

      try {
          const token = await getToken()
          if (!token) return
          await deleteWorkflowReport(id, token)
          setWorkflowReports(prev => prev.filter(r => r.id !== id))
      } catch (error) {
          console.error("Failed to delete report", error)
      }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent w-fit">Saved Reports</h1>
        <p className="text-muted-foreground">View and manage your past agentification analysis.</p>
      </div>
      
      <Tabs defaultValue="repos" className="w-full">
        <TabsList>
            <TabsTrigger value="repos">Repositories</TabsTrigger>
            <TabsTrigger value="workflows">Workflows</TabsTrigger>
        </TabsList>
        
        <TabsContent value="repos" className="mt-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {loading ? (
                Array.from({ length: 3 }).map((_, i) => (
                    <Skeleton key={i} className="h-32 w-full" />
                ))
                ) : repoReports.length === 0 ? (
                    <div className="col-span-full text-center py-10 border rounded-lg bg-muted/20">
                        <FileCode className="mx-auto h-10 w-10 text-muted-foreground mb-4" />
                        <h3 className="text-lg font-medium">No Repository Reports</h3>
                        <p className="text-muted-foreground mb-4">Analyze a GitHub repository to get started.</p>
                        <Link href="/dashboard/repos" className="text-primary hover:underline">Go to Repositories</Link>
                    </div>
                ) : (
                repoReports.map((report) => (
                    <Link key={report} href={`/dashboard/reports/${report}`}>
                    <Card className="hover:bg-accent transition-colors cursor-pointer h-full group relative">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-base font-medium truncate pr-2 flex-1" title={report}>
                            {report}
                        </CardTitle>
                        <div className="flex items-center gap-2 shrink-0">
                             <Button
                                variant="ghost"
                                size="icon"
                                className="h-8 w-8 text-muted-foreground hover:text-destructive hover:bg-destructive/10 opacity-0 group-hover:opacity-100 transition-opacity"
                                onClick={(e) => handleDeleteRepo(e, report)}
                            >
                                <Trash2 className="h-4 w-4" />
                            </Button>
                            <FileCode className="h-4 w-4 text-muted-foreground" />
                        </div>
                        </CardHeader>
                        <CardContent>
                        <p className="text-xs text-muted-foreground mt-2">
                            Code Analysis Report
                        </p>
                        </CardContent>
                    </Card>
                    </Link>
                ))
                )}
            </div>
        </TabsContent>
        
        <TabsContent value="workflows" className="mt-6">
             <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {loading ? (
                Array.from({ length: 3 }).map((_, i) => (
                    <Skeleton key={i} className="h-32 w-full" />
                ))
                ) : workflowReports.length === 0 ? (
                    <div className="col-span-full text-center py-10 border rounded-lg bg-muted/20">
                        <FileText className="mx-auto h-10 w-10 text-muted-foreground mb-4" />
                        <h3 className="text-lg font-medium">No Workflow Reports</h3>
                        <p className="text-muted-foreground mb-4">Upload a document to analyze a business process.</p>
                        <Link href="/workflow/upload" className="text-primary hover:underline">Analyze a Workflow</Link>
                    </div>
                ) : (
                workflowReports.map((report) => (
                    <Link key={report.id} href={`/workflow/${report.id}`}>
                    <Card className="hover:bg-accent transition-colors cursor-pointer h-full flex flex-col group relative">
                        <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
                        <CardTitle className="text-base font-medium line-clamp-2 pr-2 flex-1" title={report.name}>
                            {report.name}
                        </CardTitle>
                        <div className="flex items-center gap-2 shrink-0">
                             <Button
                                variant="ghost"
                                size="icon"
                                className="h-8 w-8 text-muted-foreground hover:text-destructive hover:bg-destructive/10 opacity-0 group-hover:opacity-100 transition-opacity"
                                onClick={(e) => handleDeleteWorkflow(e, report.id)}
                            >
                                <Trash2 className="h-4 w-4" />
                            </Button>
                            <FileText className="h-4 w-4 text-muted-foreground mt-1" />
                        </div>
                        </CardHeader>
                        <CardContent className="flex-1 flex flex-col justify-end">
                            <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                                {report.summary}
                            </p>
                             <div className="flex items-center text-xs text-primary font-medium mt-auto">
                                View Analysis <ArrowRight className="ml-1 w-3 h-3" />
                            </div>
                        </CardContent>
                    </Card>
                    </Link>
                ))
                )}
            </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
