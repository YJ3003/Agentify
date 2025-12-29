"use client"

import { useEffect, Suspense } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { exchangeCode } from "@/lib/api"

function CallbackContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const code = searchParams.get("code")

  useEffect(() => {
    if (code) {
      exchangeCode(code)
        .then((data) => {
          localStorage.setItem("github_access_token", data.access_token)
          router.push("/dashboard/repos")
        })
        .catch((err) => {
          console.error(err)
          router.push("/")
        })
    }
  }, [code, router])

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Authenticating...</p>
    </div>
  )
}

export default function CallbackPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <CallbackContent />
    </Suspense>
  )
}
