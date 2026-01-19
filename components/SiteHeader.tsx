"use client";

import Link from "next/link";
import { useAuth } from "@/app/context/AuthContext";
import { UserNav } from "@/components/UserNav";
import { usePathname } from "next/navigation";

export function SiteHeader() {
  const { user } = useAuth();
  const pathname = usePathname();

  if (!user) return null;

  if (pathname === "/") return null;

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 w-full items-center px-4 md:px-8">
        <div className="mr-4 flex">
          <Link href="/dashboard" className="mr-6 flex items-center space-x-2">
            <span className="font-bold sm:inline-block">Agentify</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
             <Link
              href="/dashboard/repos"
              className="text-foreground/60 transition-colors hover:text-foreground"
            >
              Repositories
            </Link>
            <Link
              href="/workflow/upload"
               className="text-foreground/60 transition-colors hover:text-foreground"
            >
              Workflows
            </Link>
            <Link
              href="/dashboard/reports"
               className="text-foreground/60 transition-colors hover:text-foreground"
            >
              Saved Reports
            </Link>
            <Link
              href="/dashboard/tools"
               className="text-foreground/60 transition-colors hover:text-foreground"
            >
              Tool Library
            </Link>
          </nav>
        </div>
        
        <div className="flex flex-1 items-center justify-end">
           <UserNav />
        </div>
      </div>
    </header>
  );
}