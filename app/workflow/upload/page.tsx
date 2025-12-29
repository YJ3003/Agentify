"use client"

import { useState } from "react"
import { useAuth } from "@/app/context/AuthContext"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { uploadWorkflow } from "@/lib/api"
import { useRouter } from "next/navigation"
import { Loader2, Upload, FileText, ArrowRight } from "lucide-react"
import { toast } from "sonner"
import ProtectedRoute from "@/components/ProtectedRoute"

export default function WorkflowUploadPage() {
  const { getToken } = useAuth()
  const [file, setFile] = useState<File | null>(null)
  const [text, setText] = useState("")
  const [analyzing, setAnalyzing] = useState(false)
  const router = useRouter()

  const handleAnalyze = async () => {
    if (!file && !text.trim()) {
        toast.error("Please upload a file or enter text")
        return
    }

    const token = await getToken()
    if (!token) return

    setAnalyzing(true)
    try {
        const result = await uploadWorkflow(file, text, token)
        toast.success("Workflow analyzed successfully!")
        router.push(`/workflow/${result.id}`)
    } catch (error) {
        console.error(error)
        toast.error("Analysis failed. Please try again.")
    } finally {
        setAnalyzing(false)
    }
  }

  return (
    <ProtectedRoute>
    <div className="container max-w-2xl mx-auto py-20 px-4">
      <div className="space-y-6">
        <div className="space-y-2 text-center">
            <h1 className="text-3xl font-bold tracking-tighter">Analyze Your Workflow</h1>
            <p className="text-muted-foreground">Upload a document or paste your process description to get AI-powered agent recommendations.</p>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Upload Document</CardTitle>
                <CardDescription>Supported formats: PDF, DOCX, TXT, MD</CardDescription>
            </CardHeader>
            <CardContent>
                <div className="grid w-full max-w-sm items-center gap-1.5">
                    <Input 
                        type="file" 
                        accept=".pdf,.docx,.txt,.md"
                        onChange={(e) => setFile(e.target.files?.[0] || null)} 
                    />
                </div>
            </CardContent>
        </Card>

        <div className="relative">
            <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">Or paste text</span>
            </div>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Paste Description</CardTitle>
            </CardHeader>
            <CardContent>
                <Textarea 
                    placeholder="Describe your business process, e.g., 'When a new invoice arrives via email, we manually check the vendor details...'"
                    className="min-h-[150px]"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                />
            </CardContent>
        </Card>

        <Button onClick={handleAnalyze} className="w-full" size="lg" disabled={analyzing}>
            {analyzing ? (
                <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing Process...
                </>
            ) : (
                <>
                    Analyze Workflow <ArrowRight className="ml-2 h-4 w-4" />
                </>
            )}
        </Button>
      </div>
    </div>
    </ProtectedRoute>
  )
}
