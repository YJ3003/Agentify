"use client"

import { useState, useMemo } from "react"
import Link from "next/link"
import { motion } from "framer-motion"
import { Tool, TOOLS } from "@/lib/tools"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Search, ExternalLink, Sparkles, SlidersHorizontal, ArrowLeft } from "lucide-react"

export default function ToolsLibraryPage() {
    const [searchQuery, setSearchQuery] = useState("")
    const [selectedCategory, setSelectedCategory] = useState("All")
    const [selectedTags, setSelectedTags] = useState<string[]>([])

    // Extract unique categories and tags
    const categories = ["All", ...Array.from(new Set(TOOLS.map(t => t.category)))]
    const allTags = Array.from(new Set(TOOLS.flatMap(t => t.tags)))

    const filteredTools = useMemo(() => {
        return TOOLS.filter(tool => {
            const matchesSearch = tool.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                                  tool.description.toLowerCase().includes(searchQuery.toLowerCase())
            const matchesCategory = selectedCategory === "All" || tool.category === selectedCategory
            const matchesTags = selectedTags.length === 0 || selectedTags.every(tag => tool.tags.includes(tag))
            
            return matchesSearch && matchesCategory && matchesTags
        })
    }, [searchQuery, selectedCategory, selectedTags])

    const toggleTag = (tag: string) => {
        setSelectedTags(prev => 
            prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
        )
    }

    return (
        <div className="container mx-auto py-10 px-4 max-w-7xl space-y-8">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="space-y-2">
                    <h1 className="text-4xl font-bold tracking-tighter bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                        AI Tool Library
                    </h1>
                    <p className="text-muted-foreground text-lg">
                        Discover {TOOLS.length}+ curated tools for agentification, automation, and productivity.
                    </p>
                </div>
            </div>

            {/* Controls Section */}
            <div className="space-y-6 bg-zinc-900/50 p-6 rounded-xl border border-zinc-800 backdrop-blur-sm">
                <div className="flex flex-col md:flex-row gap-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <Input 
                            placeholder="Search tools (e.g., 'coding', 'diagrams', 'free')..." 
                            className="pl-10 h-10 bg-zinc-950/50 border-zinc-800"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <Tabs value={selectedCategory} onValueChange={setSelectedCategory} className="w-full md:w-auto">
                        <TabsList className="bg-zinc-950/50 border border-zinc-800">
                            {categories.map(cat => (
                                <TabsTrigger key={cat} value={cat} className="data-[state=active]:bg-zinc-800">
                                    {cat}
                                </TabsTrigger>
                            ))}
                        </TabsList>
                    </Tabs>
                </div>

                {/* Tag Filters */}
                <div className="flex flex-wrap gap-2 items-center">
                    <SlidersHorizontal className="h-4 w-4 text-muted-foreground mr-2" />
                    <span className="text-sm text-muted-foreground mr-2">Filters:</span>
                    {allTags.slice(0, 12).map(tag => (
                        <Badge 
                            key={tag} 
                            variant={selectedTags.includes(tag) ? "default" : "outline"}
                            className="cursor-pointer hover:bg-zinc-800 transition-colors"
                            onClick={() => toggleTag(tag)}
                        >
                            {tag}
                        </Badge>
                    ))}
                    {selectedTags.length > 0 && (
                        <Button variant="ghost" size="sm" onClick={() => setSelectedTags([])} className="h-6 px-2 text-xs">
                            Clear
                        </Button>
                    )}
                </div>
            </div>

            {/* Results Grid - Masonry style with CSS columns */}
            <div className="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6">
                {filteredTools.length > 0 ? (
                    filteredTools.map((tool) => (
                        <motion.div 
                            key={tool.name} 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3 }}
                            className="break-inside-avoid"
                        >
                            <Card className="h-full border-zinc-800 bg-zinc-900/30 hover:bg-zinc-900/60 hover:border-zinc-700 transition-all duration-300 group">
                                <CardHeader className="pb-3">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <Badge variant="secondary" className="mb-2 text-xs bg-zinc-800 text-zinc-400 hover:bg-zinc-700">
                                                {tool.category}
                                            </Badge>
                                            <CardTitle className="text-xl flex items-center gap-2">
                                                {tool.name}
                                            </CardTitle>
                                        </div>
                                        <Link href={tool.link} target="_blank">
                                            <Button size="icon" variant="ghost" className="h-8 w-8 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                                                <ExternalLink className="h-4 w-4" />
                                            </Button>
                                        </Link>
                                    </div>
                                    <CardDescription className="line-clamp-2 mt-1">
                                        {tool.description}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="flex flex-wrap gap-2 mt-2">
                                        {tool.tags.map(tag => (
                                            <Badge key={tag} variant="outline" className="text-[10px] px-2 py-0 h-5 border-zinc-700 text-zinc-400">
                                                {tag}
                                            </Badge>
                                        ))}
                                    </div>
                                </CardContent>
                                <CardFooter className="pt-0">
                                    <Link href={tool.link} target="_blank" className="w-full">
                                        <Button className="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700" size="sm">
                                            Visit Website <ExternalLink className="ml-2 h-3 w-3" />
                                        </Button>
                                    </Link>
                                </CardFooter>
                            </Card>
                        </motion.div>
                    ))
                ) : (
                    <div className="col-span-full py-20 text-center text-muted-foreground">
                        <Sparkles className="h-10 w-10 mx-auto mb-4 opacity-50" />
                        <p className="text-lg">No tools found matching your criteria.</p>
                        <Button variant="link" onClick={() => {setSearchQuery(""); setSelectedTags([]); setSelectedCategory("All")}}>
                            Reset Filters
                        </Button>
                    </div>
                )}
            </div>
        </div>
    )
}
