"use client";

import { useAuth } from "@/app/context/AuthContext";
import Link from "next/link";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Settings, LogOut } from "lucide-react";

export function UserNav() {
    const { user, signOut } = useAuth();

    if (!user) return null;

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user.photoURL || ""} alt={user.displayName || ""} />
                  <AvatarFallback>{user.displayName?.charAt(0) || "U"}</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">{user.displayName}</p>
                  <p className="text-xs leading-none text-muted-foreground">
                    {user.email}
                  </p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                  <Link href="/settings" className="cursor-pointer w-full flex items-center">
                     <Settings className="mr-2 h-4 w-4" />
                     <span>Settings</span>
                  </Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={signOut} className="cursor-pointer text-red-600 focus:text-red-600 focus:bg-red-50 dark:focus:bg-red-950/20">
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}
