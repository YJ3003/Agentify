import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import ReactMarkdown from "react-markdown"
import { ChevronDown, ChevronUp } from "lucide-react"
import { useState } from "react"
import { Button } from "./ui/button"

interface PlaybookItem {
  tool: string
  confidence?: number
  summary: string
  signals?: string[]
  details: {
    why: string
    usage?: string
    tradeoffs?: string
    example?: string
  }
}

interface ModernizationPlaybookProps {
  playbook: {
    [key: string]: PlaybookItem[] | undefined
  }
}

const CATEGORY_TITLES: Record<string, string> = {
  agent_frameworks: "1. Agent Frameworks",
  workflow_engines: "2. Automation / Workflow Engines",
  integration_platforms: "3. Enterprise Integration Platforms",
  rag_retrieval: "4. Knowledge + RAG + Retrieval Systems",
  grounding_tools: "5. Web / Real-Time Grounding Tools",
  dev_tools: "6. Developer Tooling / Code Intelligence",
  observability: "7. Observability & Runtime",
  runtime_inference: "8. Runtime / Deployment & Inference",
  visualization_tools: "9. Workflow Visualization Tools",
}

function PlaybookCard({ item }: { item: PlaybookItem }) {
    const [expanded, setExpanded] = useState(false)

    return (
        <div className="border rounded-lg bg-background/50 hover:bg-background/80 transition-colors">
            <div className="p-4 cursor-pointer" onClick={() => setExpanded(!expanded)}>
                <div className="flex items-start justify-between gap-4">
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                             <h4 className="font-bold text-indigo-600 dark:text-indigo-400">{item.tool}</h4>
                             {item.confidence && (
                                 <Badge variant="outline" className="text-[10px] h-5 px-1.5 border-indigo-200 text-indigo-700 dark:border-indigo-800 dark:text-indigo-300">
                                     {(item.confidence * 100).toFixed(0)}% Match
                                 </Badge>
                             )}
                        </div>
                        <p className="text-sm font-medium leading-snug">{item.summary}</p>
                    </div>
                </div>
                
                {item.signals && item.signals.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mt-3">
                        {item.signals.map((sig, i) => (
                            <Badge key={i} variant="secondary" className="text-[10px] h-5 px-1.5 bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400">
                                {sig}
                            </Badge>
                        ))}
                    </div>
                )}
                
                <div className="flex justify-end mt-2">
                     <Button variant="ghost" size="sm" className="h-6 text-xs text-muted-foreground hover:text-foreground p-0">
                        {expanded ? "Hide Details" : "View Reasoning"}
                        {expanded ? <ChevronUp className="ml-1 w-3 h-3" /> : <ChevronDown className="ml-1 w-3 h-3" />}
                     </Button>
                </div>
            </div>

            {expanded && (
                <div className="px-4 pb-4 pt-0 border-t border-dashed border-indigo-500/10 mt-2">
                     <div className="grid gap-4 pt-4 text-xs md:text-sm">
                         <div>
                            <span className="font-semibold text-xs uppercase text-muted-foreground block mb-1">Why this tool?</span>
                            <div className="text-muted-foreground prose dark:prose-invert max-w-none">
                                <ReactMarkdown>{item.details.why}</ReactMarkdown>
                            </div>
                         </div>
                         {item.details.usage && (
                            <div>
                                <span className="font-semibold text-xs uppercase text-muted-foreground block mb-1">Implementation</span>
                                <div className="text-muted-foreground">{item.details.usage}</div>
                            </div>
                         )}
                         {item.details.tradeoffs && (
                             <div>
                                <span className="font-semibold text-xs uppercase text-muted-foreground block mb-1">Tradeoffs</span>
                                <div className="text-muted-foreground italic">{item.details.tradeoffs}</div>
                             </div>
                         )}
                     </div>
                </div>
            )}
        </div>
    )
}

export function ModernizationPlaybook({ playbook }: ModernizationPlaybookProps) {
  if (!playbook || Object.keys(playbook).length === 0) return null

  return (
    <Card className="border-indigo-500/20 bg-indigo-500/5 dark:bg-indigo-500/10 mt-8">
      <CardHeader>
        <CardTitle className="text-xl flex items-center gap-2">
            Agentification Playbook
        </CardTitle>
        <p className="text-sm text-muted-foreground">Comprehensive recommendations grounded in latest tools and standards.</p>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {Object.entries(CATEGORY_TITLES).map(([key, title]) => {
             const items = playbook[key as keyof typeof playbook];
             if (!items || items.length === 0) return null;

             return (
                <AccordionItem key={key} value={key}>
                  <AccordionTrigger className="font-semibold text-left">{title}</AccordionTrigger>
                  <AccordionContent>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 pt-2">
                        {items.map((item, i) => (
                             <PlaybookCard key={i} item={item} />
                        ))}
                    </div>
                  </AccordionContent>
                </AccordionItem>
             )
          })}
        </Accordion>
      </CardContent>
    </Card>
  )
}
