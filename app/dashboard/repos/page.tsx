"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/app/context/AuthContext"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Search, Loader2 } from "lucide-react"
import { getRepos, selectRepo, runAnalysis } from "@/lib/api"
import { useRouter } from "next/navigation"
import { Skeleton } from "@/components/ui/skeleton"
import { toast } from "sonner"

interface Repo {
    name: string
    full_name: string
    private: boolean
    language: string
    updated_at: string
    clone_url: string
}

export default function ReposPage() {
  const { getToken } = useAuth()
  const [repos, setRepos] = useState<Repo[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState("")
  const [analyzing, setAnalyzing] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    const fetchRepos = async () => {
        try {
            const token = await getToken()
            if (!token) {
                // If checking auth loading, maybe wait? But simple redirect for now
                return
            }
            const data = await getRepos(token)
            setRepos(data)
        } catch (err) {
            console.error(err)
            toast.error("Failed to fetch repositories")
        } finally {
            setLoading(false)
        }
    }
    fetchRepos()
  }, [getToken, router])

  const handleAnalyze = async (repo: Repo) => {
    const token = await getToken()
    if (!token) return

    setAnalyzing(repo.full_name)
    try {
        await selectRepo(repo.full_name, token)
        toast.success(`Repository ${repo.name} cloned. Starting analysis...`)
        
        await runAnalysis(repo.full_name, token)
        toast.success("Analysis complete!")
        router.push("/dashboard/reports")
    } catch (err) {
        console.error(err)
        toast.error("Failed to clone repository")
    } finally {
        setAnalyzing(null)
    }
  }

  const filteredRepos = repos.filter(repo => 
    repo.name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-6">
        <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent w-fit">Select Repository</h1>
        </div>
        
        <div className="relative max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input 
                className="pl-9" 
                placeholder="Search repositories..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
        </div>

        <div className="border rounded-md bg-card">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Visibility</TableHead>
                        <TableHead>Language</TableHead>
                        <TableHead className="text-right">Action</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {loading ? (
                        Array.from({ length: 5 }).map((_, i) => (
                            <TableRow key={i}>
                                <TableCell><Skeleton className="h-4 w-[200px]" /></TableCell>
                                <TableCell><Skeleton className="h-4 w-[60px]" /></TableCell>
                                <TableCell><Skeleton className="h-4 w-[80px]" /></TableCell>
                                <TableCell className="text-right"><Skeleton className="h-8 w-[80px] ml-auto" /></TableCell>
                            </TableRow>
                        ))
                    ) : filteredRepos.length === 0 ? (
                        <TableRow>
                            <TableCell colSpan={4} className="text-center h-24 text-muted-foreground">
                                No repositories found.
                            </TableCell>
                        </TableRow>
                    ) : (
                        filteredRepos.map((repo) => (
                            <TableRow key={repo.full_name}>
                                <TableCell className="font-medium">{repo.name}</TableCell>
                                <TableCell>
                                    {repo.private ? (
                                        <Badge variant="secondary">Private</Badge>
                                    ) : (
                                        <Badge variant="outline">Public</Badge>
                                    )}
                                </TableCell>
                                <TableCell>{repo.language || "Unknown"}</TableCell>
                                <TableCell className="text-right">
                                    <Button 
                                        size="sm" 
                                        onClick={() => handleAnalyze(repo)}
                                        disabled={analyzing === repo.full_name}
                                    >
                                        {analyzing === repo.full_name ? (
                                            <>
                                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                                Cloning
                                            </>
                                        ) : (
                                            "Analyze"
                                        )}
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))
                    )}
                </TableBody>
            </Table>
        </div>
    </div>
  )
}
