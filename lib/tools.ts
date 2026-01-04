export type Tool = {
    name: string;
    category: string;
    tags: string[];
    description: string;
    link: string;
    oneLiner?: string;
}

export const TOOLS: Tool[] = [
    // Developers & Coding
    {
        name: "GitHub Copilot",
        category: "Developers",
        tags: ["Paid", "Industry Standard"],
        description: "The world's most widely adopted AI pair programmer. Intelligent code completion and generation.",
        link: "https://github.com/features/copilot",
    },
    {
        name: "Cursor",
        category: "Developers",
        tags: ["Freemium", "Game Changer"],
        description: "An AI-first code editor (VS Code fork) that understands your entire codebase. Highly recommended.",
        link: "https://cursor.sh/",
    },
    {
        name: "Replit",
        category: "Developers",
        tags: ["Cloud", "Beginner Friendly"],
        description: "Instant development environment with AI powers. Build and deploy apps from your browser.",
        link: "https://replit.com/",
    },
    {
        name: "Tabnine",
        category: "Developers",
        tags: ["Privacy Focused", "Enterprise"],
        description: "AI code completion with a strong focus on privacy and enterprise security.",
        link: "https://www.tabnine.com/",
    },
    {
        name: "Amazon Q",
        category: "Developers",
        tags: ["AWS", "Enterprise"],
        description: "Generative AI assistant modernized for AWS development and IT pros.",
        link: "https://aws.amazon.com/q/",
    },
    {
        name: "Aider",
        category: "Developers",
        tags: ["Open Source", "CLI"],
        description: "AI pair programming in your terminal. Edits multiple files at once.",
        link: "https://aider.chat/",
    },
    {
        name: "Supermaven",
        category: "Developers",
        tags: ["Fast", "Huge Context"],
        description: "The fastest copilot with a 1-million token context window.",
        link: "https://supermaven.com/",
    },
    {
        name: "V0 (Vercel)",
        category: "Developers",
        tags: ["Frontend", "React", "Tailwind"],
        description: "Generate UI components from text prompts. Copy-paste ready code.",
        link: "https://v0.dev/",
    },
    {
        name: "Lovable",
        category: "Developers",
        tags: ["No Code", "Full Stack"],
        description: "Build complete full-stack web apps just by chatting.",
        link: "https://lovable.dev/",
    },
    {
        name: "Bolt.new",
        category: "Developers",
        tags: ["Browser Based", "Full Stack"],
        description: "Prompt, run, edit, and deploy full-stack web applications in the browser.",
        link: "https://bolt.new/",
    },
    {
        name: "Supabase",
        category: "Developers",
        tags: ["Database", "Open Source"],
        description: "Firebase alternative with AI vector search support built-in.",
        link: "https://supabase.com/",
    },
    {
        name: "Hugging Face",
        category: "Developers",
        tags: ["Models", "Open Source"],
        description: "The platform where the machine learning community collaborates on models, datasets, and apps.",
        link: "https://huggingface.co/",
    },
    {
        name: "LangChain",
        category: "Developers",
        tags: ["SDK", "Python/JS"],
        description: "The de-facto standard framework for developing applications powered by language models.",
        link: "https://www.langchain.com/",
    },
    {
        name: "CrewAI",
        category: "Developers",
        tags: ["Multi-Agent", "Python"],
        description: "Framework for orchestrating role-playing, autonomous AI agents.",
        link: "https://www.crewai.com/",
    },

    // Automation & Workflow
    {
        name: "n8n",
        category: "Automation",
        tags: ["Low Code", "Self-Hostable"],
        description: "Powerful workflow automation for technical people. Fair-code distribution.",
        link: "https://n8n.io/",
    },
    {
        name: "Zapier",
        category: "Automation",
        tags: ["No Code", "Easy"],
        description: "The easiest way to automate workflows. Connects 6000+ apps.",
        link: "https://zapier.com/",
    },
    {
        name: "Make",
        category: "Automation",
        tags: ["Visual", "Advanced"],
        description: "Visual platform to build and automate complex tasks and workflows.",
        link: "https://www.make.com/",
    },
    {
        name: "Retool",
        category: "Automation",
        tags: ["Low Code", "Enterprise"],
        description: "Build internal tools remarkably fast. Drag and drop UI, write SQL/JS.",
        link: "https://retool.com/",
    },
    {
        name: "Bland AI",
        category: "Automation",
        tags: ["Phone", "Sales"],
        description: "Realistic AI phone calling agents for sales and support.",
        link: "https://www.bland.ai/",
    },
    {
        name: "UiPath",
        category: "Automation",
        tags: ["Enterprise", "Legacy"],
        description: "Robotic Process Automation for large scale enterprise tasks.",
        link: "https://www.uipath.com/",
    },
    {
        name: "Relume",
        category: "Automation",
        tags: ["Figma", "Sitemap"],
        description: "AI-powered website builder and sitemap generator for designers.",
        link: "https://relume.io/",
    },

    // Productivity & Hidden Gems
    {
        name: "Napkin.ai",
        category: "Productivity",
        tags: ["Hidden Gem", "Diagrams"],
        description: "Instantly turn your text into meaningful visuals and storytelling diagrams.",
        link: "https://napkin.ai/",
    },
    {
        name: "Gamma",
        category: "Productivity",
        tags: ["No Design Skills", "Fast"],
        description: "A new medium for presenting ideas. Generate decks, docs, and webpages.",
        link: "https://gamma.app/",
    },
    {
        name: "Eraser",
        category: "Productivity",
        tags: ["Technical", "Diagram-as-Code"],
        description: "Docs and diagrams for engineering teams. Great for architecture.",
        link: "https://eraser.io/",
    },
    {
        name: "Perplexity",
        category: "Productivity",
        tags: ["Research", "Daily Driver"],
        description: "AI answer engine. Replaces traditional search for many users.",
        link: "https://www.perplexity.ai/",
    },
    {
        name: "Arc Search",
        category: "Productivity",
        tags: ["Mobile", "Summary"],
        description: "Innovative 'Browse for Me' feature summarizing web pages.",
        link: "https://arc.net/",
    },
    {
        name: "Goblin Tools",
        category: "Productivity",
        tags: ["Hidden Gem", "Simple"],
        description: "A set of simple, single-task tools (like 'Judge Tone') to help neurodivergent minds.",
        link: "https://goblin.tools/",
    },
    {
        name: "Humata",
        category: "Productivity",
        tags: ["Analysis", "Research"],
        description: "Chat with your files. Upload PDFs and ask questions.",
        link: "https://humata.ai/",
    },
    {
        name: "NotebookLM",
        category: "Productivity",
        tags: ["Google", "Audio Overview"],
        description: "Your personalized AI research assistant. Generates podcasts from your notes.",
        link: "https://notebooklm.google/",
    },
    {
        name: "Excalidraw",
        category: "Productivity",
        tags: ["Drawing", "Open Source"],
        description: "Virtual whiteboard with 'AI-to-diagram' features.",
        link: "https://excalidraw.com/",
    },
    {
        name: "Midjourney",
        category: "Productivity",
        tags: ["Art", "Best Quality"],
        description: "The highest quality AI image generator available. Discord-based.",
        link: "https://www.midjourney.com/",
    },
    {
        name: "Runway",
        category: "Productivity",
        tags: ["Video", "Creative"],
        description: "Advanced video generation (Gen-3 Alpha) for filmmakers and creators.",
        link: "https://runwayml.com/",
    },
    {
        name: "ElevenLabs",
        category: "Productivity",
        tags: ["Audio", "Realistic"],
        description: "The most realistic AI text-to-speech and voice cloning software.",
        link: "https://elevenlabs.io/",
    },
    {
        name: "Descript",
        category: "Productivity",
        tags: ["Editor", "Transcription"],
        description: "Edit video by editing text. Magic for podcasters.",
        link: "https://descript.com/",
    },
    {
        name: "Suno",
        category: "Productivity",
        tags: ["Audio", "Generation"],
        description: "Make a song about anything. AI music generation.",
        link: "https://suno.com/",
    }
]
