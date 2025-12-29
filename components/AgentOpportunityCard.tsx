import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ChevronDown, ChevronUp } from "lucide-react"
import { useState } from "react"
import ReactMarkdown from "react-markdown"

interface AgentOpportunityProps {
    opp: {
        location?: string
        step?: string
        summary: string
        signals?: string[]
        recommended_framework: string
        confidence?: number
        details?: {
            reasoning: string
            implementation_tips?: string
        }
        // Backward compatibility
        file?: string
        reason?: string
        candidate_frameworks?: string[]
    }
}

export function AgentOpportunityCard({ opp }: AgentOpportunityProps) {
    const [expanded, setExpanded] = useState(false)

    // Normalize data
    const title = opp.location || opp.step || opp.file || "Unknown Location"
    const framework = opp.recommended_framework || (opp.candidate_frameworks ? opp.candidate_frameworks[0] : "N/A")
    const summary = opp.summary || opp.reason || "No summary provided."
    const reasoning = opp.details?.reasoning || opp.reason || "" // Fallback if detail not strictly structured
    const signals = opp.signals || []

    return (
        <Card className="bg-background/80 hover:bg-background/100 transition-colors">
            <CardHeader className="p-4 pb-2">
                <div className="flex justify-between items-start gap-4">
                    <div className="space-y-1">
                        <CardTitle className="text-base font-semibold break-words">
                            {title}
                        </CardTitle>
                         <div className="flex flex-wrap gap-2 items-center">
                            <Badge className="bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800">
                                {framework}
                            </Badge>
                            {opp.confidence && (
                                <span className="text-xs text-muted-foreground font-medium">
                                    {(opp.confidence * 100).toFixed(0)}% Confidence
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-4 pt-2">
                <p className="text-sm text-foreground/90 mb-3">{summary}</p>
                
                {signals.length > 0 && (
                     <div className="flex flex-wrap gap-1.5 mb-3">
                        {signals.map((sig, i) => (
                             <Badge key={i} variant="outline" className="text-[10px] h-5 px-1.5">
                                {sig}
                            </Badge>
                        ))}
                     </div>
                )}

                <div className="flex justify-start">
                     <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => setExpanded(!expanded)}
                        className="h-6 px-0 text-xs text-muted-foreground hover:text-indigo-500"
                    >
                        {expanded ? "Hide Explanation" : "View Explanation"}
                        {expanded ? <ChevronUp className="ml-1 w-3 h-3" /> : <ChevronDown className="ml-1 w-3 h-3" />}
                     </Button>
                </div>

                {expanded && (
                    <div className="mt-3 pt-3 border-t border-dashed">
                        <div className="text-xs text-muted-foreground prose dark:prose-invert max-w-none">
                            <ReactMarkdown>{reasoning}</ReactMarkdown>
                        </div>
                        {opp.details?.implementation_tips && (
                             <div className="mt-2 bg-muted/50 p-2 rounded text-xs">
                                <span className="font-semibold block mb-1">Implementation Tip:</span>
                                {opp.details.implementation_tips}
                             </div>
                        )}
                    </div>
                )}
            </CardContent>
        </Card>
    )
}
