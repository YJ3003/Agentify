"use client";

import { useAuth } from "@/app/context/AuthContext";
import ProtectedRoute from "@/components/ProtectedRoute";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Github } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function SettingsPage() {
    const { user } = useAuth();

    // Check if user has github provider linked
    const isGithubLinked = user?.providerData.some(p => p.providerId === 'github.com');
    const { linkWithGithub } = useAuth();
    
    const handleConnect = async () => {
        try {
            await linkWithGithub();
            toast.success("GitHub account linked successfully!");
        } catch (error: any) {
            console.error("Failed to link account", error);
            if (error.code === 'auth/credential-already-in-use') {
                toast.error("This GitHub account is already linked to another user. Please log in with GitHub directly, or unlink it from the other account.", {
                    duration: 5000
                });
            } else {
                toast.error("Failed to link GitHub account. Please try again.");
            }
        }
    };

    return (
        <ProtectedRoute>
            <div className="container mx-auto py-10 px-4 max-w-4xl">
                <h1 className="text-3xl font-bold tracking-tight mb-8">Settings</h1>
                
                <div className="grid gap-8">
                    <Card>
                        <CardHeader>
                            <CardTitle>Connected Accounts</CardTitle>
                            <CardDescription>Manage your linked identity providers.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex items-center justify-between p-4 border rounded-lg">
                                <div className="flex items-center gap-4">
                                    <div className="bg-zinc-100 dark:bg-zinc-800 p-2 rounded-full">
                                        <Github className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <p className="font-medium">GitHub</p>
                                        <p className="text-sm text-muted-foreground">
                                            {isGithubLinked ? "Connected" : "Not connected"}
                                        </p>
                                    </div>
                                </div>
                                <div>
                                    {isGithubLinked ? (
                                        <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">Connected</Badge>
                                    ) : (
                                        <Button variant="outline" size="sm" onClick={handleConnect}>Connect</Button>
                                    )}
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                    
                    <Card>
                        <CardHeader>
                            <CardTitle>Profile Information</CardTitle>
                            <CardDescription>Your basic account details from Firebase.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                             <div className="grid gap-2">
                                <div className="text-sm font-medium">Email</div>
                                <div className="p-2 bg-muted rounded text-sm">{user?.email}</div>
                             </div>
                             <div className="grid gap-2">
                                <div className="text-sm font-medium">User ID</div>
                                <div className="p-2 bg-muted rounded font-mono text-xs">{user?.uid}</div>
                             </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </ProtectedRoute>
    )
}
