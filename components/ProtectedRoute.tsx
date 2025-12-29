"use client";

import { useAuth } from "@/app/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Skeleton } from "@/components/ui/skeleton";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
        <div className="flex items-center justify-center h-screen w-full">
            <Skeleton className="h-12 w-12 rounded-full" />
        </div>
    )
  }

  if (!user) {
    return null; 
  }

  return <>{children}</>;
}
