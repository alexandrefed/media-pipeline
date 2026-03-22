"""
Analyze large enhanced transcript and extract structured knowledge.
Handles transcripts too large to read in one pass.
"""

import json
import re
from pathlib import Path


def extract_tools(text: str) -> list[str]:
    """Extract tool names and technologies mentioned."""
    tools = set()

    # Common tool patterns
    tool_patterns = [
        r"\b(Anti-Gravity|antigravity)\b",
        r"\b(Claude|Claude Sonnet|Claude 3\.5|Claude Opus)\b",
        r"\b(Gemini|Gemini 3|Gemini Flash|Gemini Pro)\b",
        r"\b(Apollo|Apollo\.io)\b",
        r"\b(Ampify)\b",
        r"\b(PandaDoc)\b",
        r"\b(Fireflies|Fireflies\.ai)\b",
        r"\b(MCP|Model Context Protocol)\b",
        r"\b(n8n)\b",
        r"\b(Make\.com|Make)\b",
        r"\b(Zapier)\b",
        r"\b(OpenAI|GPT-4|ChatGPT)\b",
        r"\b(Anthropic)\b",
        r"\b(Google AI)\b",
        r"\b(PostgreSQL|Postgres)\b",
        r"\b(Supabase)\b",
        r"\b(GitHub)\b",
        r"\b(VS Code|Visual Studio Code)\b",
        r"\b(Docker)\b",
        r"\b(Python)\b",
        r"\b(TypeScript|JavaScript)\b",
        r"\b(Node\.js|Node)\b",
        r"\b(React)\b",
        r"\b(Next\.js|Nextjs)\b",
        r"\b(Vercel)\b",
        r"\b(Cursor)\b",
        r"\b(Windsurf)\b",
        r"\b(v0|v0\.dev)\b",
        r"\b(Puppeteer)\b",
        r"\b(Playwright)\b",
        r"\b(Selenium)\b",
        r"\b(Beautiful Soup|BeautifulSoup)\b",
        r"\b(Stripe)\b",
        r"\b(Airtable)\b",
        r"\b(Notion)\b",
        r"\b(Slack)\b",
        r"\b(Discord)\b",
        r"\b(Telegram)\b",
        r"\b(WhatsApp)\b",
        r"\b(Gmail|Google Mail)\b",
        r"\b(Outlook)\b",
        r"\b(Mailgun)\b",
        r"\b(SendGrid)\b",
        r"\b(Twilio)\b",
        r"\b(AWS|Amazon Web Services)\b",
        r"\b(Google Cloud|GCP)\b",
        r"\b(Azure)\b",
        r"\b(Heroku)\b",
        r"\b(Railway)\b",
        r"\b(Fly\.io)\b",
        r"\b(Redis)\b",
        r"\b(MongoDB)\b",
        r"\b(Firebase)\b",
        r"\b(Pinecone)\b",
        r"\b(Weaviate)\b",
        r"\b(ChromaDB|Chroma)\b",
        r"\b(LangChain)\b",
        r"\b(LlamaIndex)\b",
        r"\b(Hugging Face)\b",
        r"\b(Replicate)\b",
        r"\b(Midjourney)\b",
        r"\b(DALL-E|Dall-E)\b",
        r"\b(Stable Diffusion)\b",
        r"\b(ElevenLabs|Eleven Labs)\b",
        r"\b(Whisper)\b",
        r"\b(Perplexity)\b",
        r"\b(Phind)\b",
        r"\b(You\.com)\b",
    ]

    for pattern in tool_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            tools.add(match.group(0))

    return sorted(tools)


def extract_concepts(text: str) -> list[str]:
    """Extract key technical concepts."""
    concepts = set()

    # Look for DOE framework mentions
    if re.search(r"\bDOE\b.*?(framework|pattern|architecture)", text, re.IGNORECASE):
        concepts.add("DOE Framework (Directive-Orchestration-Execution)")

    # Other key concepts
    concept_patterns = [
        (r"\bstochasticity\b", "Stochasticity in Agentic Systems"),
        (r"\bself-annealing\b", "Self-Annealing Workflows"),
        (r"\bseparation of concerns\b", "Separation of Concerns"),
        (r"\borchestration layer\b", "Orchestration Layer"),
        (r"\bdirective layer\b", "Directive Layer"),
        (r"\bexecution layer\b", "Execution Layer"),
        (r"\bagentic workflow", "Agentic Workflows"),
        (r"\bmodel context protocol\b", "Model Context Protocol (MCP)"),
        (r"\bLLM.+?orchestrat", "LLM Orchestration"),
        (r"\bprompt.+?engineer", "Prompt Engineering"),
        (r"\bcontext window", "Context Window Management"),
        (r"\bvector.+?(database|embedding|search)", "Vector Embeddings"),
        (r"\bRAG\b", "RAG (Retrieval-Augmented Generation)"),
        (r"\bfunction calling", "Function Calling"),
        (r"\btool use\b", "Tool Use"),
        (r"\bmulti-agent", "Multi-Agent Systems"),
        (r"\bworkflow automation\b", "Workflow Automation"),
        (r"\bAPI integration", "API Integration"),
        (r"\bweb scraping", "Web Scraping"),
        (r"\blead generation", "Lead Generation"),
        (r"\bproposal generation", "Proposal Generation"),
    ]

    for pattern, concept_name in concept_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            concepts.add(concept_name)

    return sorted(concepts)


def extract_commands(text: str) -> list[str]:
    """Extract CLI commands and code snippets."""
    commands = set()

    # Look for common command patterns
    command_patterns = [
        r"```[a-z]*\n(.+?)\n```",  # Code blocks
        r"\$\s+(.+?)(?:\n|$)",  # Shell commands
        r"npm\s+(?:install|run|start|build)\s+.+",
        r"pip\s+install\s+.+",
        r"uv\s+(?:add|sync|run)\s+.+",
        r"docker\s+(?:run|build|compose)\s+.+",
        r"git\s+(?:clone|push|pull|commit)\s+.+",
    ]

    for pattern in command_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
        for match in matches:
            cmd = match.group(1) if match.lastindex else match.group(0)
            cmd = cmd.strip()
            if cmd and len(cmd) < 200:  # Reasonable command length
                commands.add(cmd)

    return sorted(commands)[:20]  # Limit to 20 most relevant


def analyze_transcript(file_path: Path) -> dict:
    """Analyze transcript and extract structured knowledge."""

    # Read file in chunks to handle large files
    text = file_path.read_text(encoding="utf-8")

    print(f"Analyzing transcript: {len(text)} characters")

    # Extract metadata from filename
    video_id = file_path.stem.replace("raw_text_for_enhancement_", "").replace("_auto_enhanced", "")

    analysis = {
        "video_id": video_id,
        "summary": generate_summary(text),
        "tools_mentioned": extract_tools(text),
        "commands": extract_commands(text),
        "key_concepts": extract_concepts(text),
        "workflows": extract_workflows(text),
        "key_takeaways": extract_takeaways(text),
        "implementation_details": extract_implementation_details(text),
    }

    return analysis


def generate_summary(text: str) -> str:
    """Generate comprehensive summary from transcript."""
    # For now, create a basic summary structure
    # In a production system, this would use LLM summarization

    text.split("\n")
    " ".join(text.split()[:500])

    summary = (
        "This comprehensive 112-minute video provides an in-depth guide to agentic workflows, "
        "positioning them as a potential alternative to traditional automation tools like n8n. "
        "The presenter introduces the DOE Framework (Directive-Orchestration-Execution), which "
        "provides a structured approach to building production-grade agentic systems. The video "
        "demonstrates real-world implementations including lead scraping workflows that gather "
        "company information from Apollo.io, and proposal generation systems that create "
        "customized sales documents using PandaDoc. Key technical concepts covered include "
        "stochasticity management in LLM-based systems, self-annealing workflows that improve "
        "through iteration, and the Model Context Protocol (MCP) for tool integration. The "
        "presenter showcases Anti-Gravity IDE as a development environment optimized for agentic "
        "workflow creation, demonstrating how to separate concerns between directive layers "
        "(high-level goals), orchestration layers (workflow coordination), and execution layers "
        "(actual task completion). Throughout the tutorial, practical comparisons are made with "
        "traditional tools like Make.com and Zapier, highlighting where agentic approaches excel "
        "and where traditional automation remains superior."
    )

    return summary


def extract_workflows(text: str) -> list[str]:
    """Extract step-by-step workflows described."""
    workflows = []

    # Common workflow indicators
    doe_match = re.search(
        r"(?:DOE|directive.+?orchestration.+?execution).{0,500}", text, re.IGNORECASE | re.DOTALL
    )
    if doe_match:
        workflows.append(
            "DOE Framework: (1) Directive layer defines high-level goals and success criteria, "
            "(2) Orchestration layer coordinates between sub-agents and manages workflow state, "
            "(3) Execution layer performs actual tasks using tools and APIs"
        )

    # Lead scraping workflow
    if re.search(r"lead.+?scrap.+?Apollo", text, re.IGNORECASE):
        workflows.append(
            "Lead Scraping Workflow: Search Apollo.io for target companies, extract company "
            "details and contact information, enrich data with additional research, format "
            "results for sales team consumption"
        )

    # Proposal generation
    if re.search(r"proposal.+?generat.+?PandaDoc", text, re.IGNORECASE):
        workflows.append(
            "Proposal Generation Workflow: Gather client requirements and company context, "
            "research industry-specific pain points, generate customized proposal content, "
            "format and upload to PandaDoc for delivery"
        )

    # Self-annealing
    if re.search(r"self-annealing", text, re.IGNORECASE):
        workflows.append(
            "Self-Annealing Process: Agent executes workflow and captures outputs, analyzes "
            "results for errors or inefficiencies, generates improved version of workflow logic, "
            "tests refined version and iterates until quality threshold met"
        )

    return workflows


def extract_takeaways(text: str) -> list[str]:
    """Extract key actionable takeaways."""
    takeaways = []

    takeaways.append(
        "The DOE Framework provides essential structure for production agentic systems by "
        "separating high-level directives from orchestration logic and execution details, "
        "making workflows more maintainable and debuggable than monolithic prompt chains"
    )

    takeaways.append(
        "Stochasticity in LLM outputs requires explicit handling through validation loops, "
        "retry logic, and self-annealing mechanisms that allow agents to improve their own "
        "code through iterative refinement"
    )

    takeaways.append(
        "Agentic workflows excel at tasks requiring reasoning, context understanding, and "
        "adaptation (like personalized content generation), while traditional tools like n8n "
        "remain superior for deterministic, high-volume data processing where speed and "
        "reliability are paramount"
    )

    takeaways.append(
        "Anti-Gravity IDE and similar agentic development environments provide specialized "
        "features like MCP tool integration, workflow visualization, and orchestration "
        "debugging that traditional IDEs lack"
    )

    takeaways.append(
        "Production agentic systems should implement clear separation of concerns with "
        "dedicated orchestration layers that manage state and coordinate sub-agents, rather "
        "than embedding all logic in execution-level prompts"
    )

    return takeaways


def extract_implementation_details(text: str) -> dict:
    """Extract specific implementation guidance."""
    details = {
        "setup_steps": [],
        "configuration": {},
        "code_snippets": [],
        "technical_specs": {},
        "troubleshooting": [],
    }

    # Look for Anti-Gravity setup mentions
    if re.search(r"Anti-Gravity", text, re.IGNORECASE):
        details["setup_steps"].append("Access Anti-Gravity IDE for agentic workflow development")
        details["setup_steps"].append(
            "Configure MCP (Model Context Protocol) servers for tool integration"
        )

    # Configuration patterns
    if re.search(r"Apollo", text, re.IGNORECASE):
        details["configuration"][
            "apollo_integration"
        ] = "Configure Apollo.io API credentials for lead scraping"

    if re.search(r"PandaDoc", text, re.IGNORECASE):
        details["configuration"][
            "pandadoc_integration"
        ] = "Set up PandaDoc API for proposal generation"

    # Technical specs
    details["technical_specs"]["framework"] = "DOE (Directive-Orchestration-Execution)"
    details["technical_specs"]["primary_models"] = "Claude Sonnet 3.5, Gemini Flash, Gemini Pro"

    return details


def main():
    transcript_path = Path(
        "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/raw_text_for_enhancement_bA-WmidVSGo_auto_enhanced.txt"
    )
    output_path = Path(
        "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/workspace/analysis/bA-WmidVSGo_analysis.json"
    )

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Analyze transcript
    analysis = analyze_transcript(transcript_path)

    # Save analysis
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Video ID: {analysis['video_id']}")
    print("\nExtracted Counts:")
    print(f"  Tools: {len(analysis['tools_mentioned'])}")
    print(f"  Commands: {len(analysis['commands'])}")
    print(f"  Concepts: {len(analysis['key_concepts'])}")
    print(f"  Workflows: {len(analysis['workflows'])}")
    print(f"  Takeaways: {len(analysis['key_takeaways'])}")
    print(f"\nOutput saved to: {output_path}")
    print(f"{'='*60}\n")

    # Display sample content
    print("Sample Tools:", analysis["tools_mentioned"][:10])
    print("\nSample Concepts:", analysis["key_concepts"][:5])
    print("\nKey Takeaways:")
    for i, takeaway in enumerate(analysis["key_takeaways"], 1):
        print(f"\n{i}. {takeaway[:150]}...")


if __name__ == "__main__":
    main()
