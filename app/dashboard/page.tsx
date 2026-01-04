"use client";

import { useAuth } from "@/app/context/AuthContext";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import ProtectedRoute from "@/components/ProtectedRoute";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Github, FileText, LayoutDashboard, Sparkles } from "lucide-react";

export default function Dashboard() {
    const { user } = useAuth();
    
    return (
        <ProtectedRoute>
            <div className="container mx-auto py-10 px-4 max-w-6xl">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold tracking-tight mb-2">Welcome back, {user?.displayName || "User"}</h1>
                    <p className="text-muted-foreground">Manage your modernization projects.</p>
                </div>

                {!user?.providerData.some(p => p.providerId === 'github.com') && (
                     <Alert className="mb-6 border-blue-200 bg-blue-50 dark:border-blue-900 dark:bg-blue-950/20 text-blue-900 dark:text-blue-200">
                        <Github className="h-4 w-4" />
                        <AlertTitle>Connect GitHub Account</AlertTitle>
                        <AlertDescription className="flex items-center justify-between">
                            <span>Link your GitHub account to analyze repositories directly.</span>
                            <Link href="/settings">
                                <Button variant="outline" size="sm" className="bg-background text-foreground border-border hover:bg-accent hover:text-accent-foreground h-7">Connect</Button>
                            </Link>
                        </AlertDescription>
                    </Alert>
                )}

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={() => window.location.href='/dashboard/repos'}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">
                                GitHub Repositories
                            </CardTitle>
                            <Github className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">Code Analysis</div>
                            <p className="text-xs text-muted-foreground">
                                Scan active repositories for agent opportunities.
                            </p>
                            <Button className="mt-4 w-full" variant="outline" size="sm">View Repos</Button>
                        </CardContent>
                    </Card>

                    <Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={() => window.location.href='/workflow/upload'}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">
                                Workflow Analysis
                            </CardTitle>
                             <FileText className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                             <div className="text-2xl font-bold">Process Docs</div>
                             <p className="text-xs text-muted-foreground">
                                Upload text docs to extract business logic.
                            </p>
                             <Button className="mt-4 w-full" variant="outline" size="sm">Analyze Workflow</Button>
                        </CardContent>
                    </Card>

                    <Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={() => window.location.href='/dashboard/reports'}>
                         <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">
                                Saved Reports
                            </CardTitle>
                             <LayoutDashboard className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                             <div className="text-2xl font-bold">History</div>
                             <p className="text-xs text-muted-foreground">
                                View past modernization playbooks.
                            </p>
                             <Button className="mt-4 w-full" variant="outline" size="sm">View All</Button>
                        </CardContent>
                    </Card>

                    <Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={() => window.location.href='/dashboard/tools'}>
                         <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">
                                Tool Library
                            </CardTitle>
                             <Sparkles className="h-4 w-4 text-purple-500" />
                        </CardHeader>
                        <CardContent>
                             <div className="text-2xl font-bold">AI Tools</div>
                             <p className="text-xs text-muted-foreground">
                                Explore 50+ curated AI tools.
                            </p>
                             <Button className="mt-4 w-full" variant="outline" size="sm">Explore Library</Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </ProtectedRoute>
    )
}
