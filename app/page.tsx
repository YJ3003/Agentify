"use client";

import { Button } from "@/components/ui/button";
import { Github, Loader2 } from "lucide-react";
import Link from "next/link";
import { useAuth } from "@/app/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Home() {
  const { user, loading, signInWithGithub, signInWithEmail, signUpWithEmail } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      router.push("/dashboard");
    }
  }, [user, router]);

  const handleGithubLogin = async () => {
    setAuthError(null);
    try {
        await signInWithGithub();
    } catch (error: any) {
        console.error("Login failed", error);
        setAuthError("Failed to sign in with GitHub. Please try again.");
    }
  }

  const handleEmailSignIn = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsLoading(true);
      setAuthError(null);
      try {
          await signInWithEmail(email, password);
      } catch (error: any) {
          console.error("Email login failed", error);
          if (error.code === 'auth/invalid-credential' || error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
             setAuthError("Invalid email or password.");
          } else if (error.code === 'auth/invalid-email') {
             setAuthError("Invalid email format.");
          } else {
             setAuthError("Failed to sign in. Please try again.");
          }
      } finally {
          setIsLoading(false);
      }
  }

  const handleEmailSignUp = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsLoading(true);
      setAuthError(null);
      try {
          await signUpWithEmail(email, password);
      } catch (error: any) {
          console.error("Email signup failed", error);
          if (error.code === 'auth/email-already-in-use') {
             setAuthError("Email is already in use. Please sign in.");
          } else if (error.code === 'auth/weak-password') {
             setAuthError("Password should be at least 6 characters.");
          } else {
             setAuthError("Failed to create account. Please try again.");
          }
      } finally {
          setIsLoading(false);
      }
  }

  if (loading) return <div className="h-screen flex items-center justify-center"><Loader2 className="animate-spin w-8 h-8" /></div>;

  if (user) return <div className="h-screen flex items-center justify-center"><Loader2 className="animate-spin w-8 h-8" /></div>; // Redirecting

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background text-foreground p-4">
      <main className="flex flex-col items-center text-center max-w-lg w-full">
        <div className="mb-8">
            <span className="px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-800 text-xs font-medium text-zinc-600 dark:text-zinc-400">
                Agentify v1.0
            </span>
        </div>
        <h1 className="text-4xl font-bold tracking-tight mb-4">
          Upgrade legacy software into <span className="text-zinc-500">agentic systems.</span>
        </h1>
        <p className="text-lg text-muted-foreground mb-8">
          Analyze codebases, get AI recommendations, and modernize without rewrites.
        </p>
        
        <div className="w-full">
            <Tabs defaultValue="github" className="w-full">
                <TabsList className="grid w-full grid-cols-2 mb-4">
                    <TabsTrigger value="github">GitHub</TabsTrigger>
                    <TabsTrigger value="email">Email</TabsTrigger>
                </TabsList>
                {authError && (
                    <div className="mb-4 p-3 text-sm text-red-500 bg-red-50 dark:bg-red-950/20 rounded-md border border-red-200 dark:border-red-900">
                        {authError}
                    </div>
                )}
                <TabsContent value="github">
                    <Card>
                        <CardHeader>
                            <CardTitle>GitHub Access</CardTitle>
                            <CardDescription>
                                Connect your repositories directly.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-2">
                             <Button size="lg" className="w-full gap-2" onClick={handleGithubLogin}>
                                <Github className="w-5 h-5" />
                                Sign in with GitHub
                              </Button>
                        </CardContent>
                    </Card>
                </TabsContent>
                <TabsContent value="email">
                    <Card>
                        <CardHeader>
                            <CardTitle>Email Access</CardTitle>
                            <CardDescription>
                                Create an account or sign in.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <Tabs defaultValue="signin" className="w-full">
                                <TabsList className="grid w-full grid-cols-2 mb-4">
                                    <TabsTrigger value="signin">Sign In</TabsTrigger>
                                    <TabsTrigger value="signup">Sign Up</TabsTrigger>
                                </TabsList>
                                <TabsContent value="signin">
                                    <form onSubmit={handleEmailSignIn} className="space-y-4">
                                        <div className="space-y-2 text-left">
                                            <Label htmlFor="email">Email</Label>
                                            <Input id="email" type="email" placeholder="m@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                        </div>
                                        <div className="space-y-2 text-left">
                                            <Label htmlFor="password">Password</Label>
                                            <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                        </div>
                                        <Button type="submit" className="w-full" disabled={isLoading}>
                                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                            Sign In
                                        </Button>
                                    </form>
                                </TabsContent>
                                <TabsContent value="signup">
                                    <form onSubmit={handleEmailSignUp} className="space-y-4">
                                        <div className="space-y-2 text-left">
                                            <Label htmlFor="signup-email">Email</Label>
                                            <Input id="signup-email" type="email" placeholder="m@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                        </div>
                                        <div className="space-y-2 text-left">
                                            <Label htmlFor="signup-password">Password</Label>
                                            <Input id="signup-password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                        </div>
                                        <Button type="submit" className="w-full" disabled={isLoading}>
                                            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                            Create Account
                                        </Button>
                                    </form>
                                </TabsContent>
                            </Tabs>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
      </main>
    </div>
  );
}

