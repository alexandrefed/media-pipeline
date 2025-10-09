"""
Manual Chunker for n8n AI Agent Army Video
Creates high-quality semantic chunks for the n8n agent automation tutorial.
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple
import tiktoken

# Video metadata
VIDEO_ID = "u2NluvotA80"
VIDEO_TITLE = "How to INSTANTLY Build An AI Agent Army in n8n with Claude"
VIDEO_CHANNEL = "Mark Kashef"
VIDEO_DURATION = 1448  # seconds
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def create_manual_chunks() -> List[Dict]:
    """Create manually curated chunks for the n8n AI agent army video."""
    
    chunks = []
    
    # Chunk 1: Introduction and System Overview
    chunks.append({
        "text": """How to INSTANTLY Build An AI Agent Army in n8n with Claude by Mark Kashef

Imagine building an entire army of agents from just one prompt. This video demonstrates how to use Claude 4 Opus to instantly generate complete n8n workflow sets. You'll learn to spin up master orchestrating agents, create specialized subworkflows that report to that agent, and add tools dynamically to sub-agents without writing any code.

The entire process takes only minutes from start to finish, making sophisticated agent systems accessible even to automation beginners. Two methods will be covered: both requiring only one prompt each. The first method uses a Claude project with specialized files, while the second involves sending a direct chat message.

Before diving into prompt mechanics, the video first proves the system works by examining actual results. The demonstration shows sending a comprehensive prompt with JSON files to create a master agent called "Retrofit Master Assistant" along with multiple subworkflows. This leverages Claude 4 Opus's extended thinking and web search capabilities to analyze files and understand AI agent module creation, tool connections, and workflow relationships.""",
        "start_time": 0,
        "end_time": 220,
        "topics": ["n8n", "Claude 4 Opus", "AI agents", "automation", "workflow generation", "extended thinking", "web search"],
        "importance": "high",
        "context": "Video introduction, value proposition, and system overview"
    })
    
    # Chunk 2: Two Approaches Overview
    chunks.append({
        "text": """Two methods for assembling your agent army will be covered: both requiring only one prompt each. The first method uses a Claude project with specialized files, while the second involves sending a direct chat message.

Before diving into prompt mechanics, let's first prove the system works by examining the actual results it produces.""",
        "start_time": 85,
        "end_time": 125,
        "topics": ["methodology", "Claude projects", "prompt engineering"],
        "importance": "medium",
        "context": "Setup and approach explanation"
    })
    
    # Chunk 3: System Demonstration - Master Agent
    chunks.append({
        "text": """The demonstration shows sending a comprehensive prompt with JSON files to create a master agent called "Retrofit Master Assistant" along with multiple subworkflows. This leverages Claude 4 Opus's extended thinking and web search capabilities to analyze files and understand AI agent module creation, tool connections, and workflow relationships.

The process takes 5-10 minutes for Opus to generate multiple agent sets. Users can request samples of three agents, and Claude creates not just drafts but complete JSON implementations ready for n8n import.""",
        "start_time": 125,
        "end_time": 220,
        "topics": ["Claude 4 Opus", "JSON generation", "master agent", "extended thinking", "web search"],
        "importance": "high",
        "context": "Core system functionality demonstration"
    })
    
    # Chunk 4: Workflow Import and Structure
    chunks.append({
        "text": """The generated JSON files can be directly imported into n8n, creating functional agents with pre-configured prompts and tool integrations. Each agent comes with detailed instructions on operation and sub-tool usage, creating nested agent architectures where agents manage other agents.

The system generates multiple specialized subworkflows that the master agent coordinates, each with specific tools and functionalities tailored to business requirements.""",
        "start_time": 220,
        "end_time": 290,
        "topics": ["n8n import", "agent architecture", "workflow structure", "tool integration"],
        "importance": "high",
        "context": "Implementation and structure explanation"
    })
    
    # Chunk 5: Agent Intelligence and Tool Selection
    chunks.append({
        "text": """Generated agents demonstrate sophisticated decision-making, automatically selecting appropriate language models (ChatGPT, OpenAI, or Anthropic) based on specific tasks. Each agent receives distinct tools and functionalities while maintaining coordination with the central orchestrating agent.

This creates a dynamic system where agents can adapt their tooling and model selection to optimize for their assigned responsibilities.""",
        "start_time": 290,
        "end_time": 350,
        "topics": ["agent intelligence", "model selection", "tool assignment", "task optimization"],
        "importance": "high",
        "context": "Agent capability and intelligence features"
    })
    
    # Chunk 6: Claude 4 Capabilities - The Trifecta
    chunks.append({
        "text": """Claude 4's power comes from combining three key features: the base intelligence of Claude 4 Sonnet and Opus, extended thinking for reflection over time, and web search for real-time information gathering. This trifecta creates the perfect conditions for generating sophisticated n8n workflows.

Previously, creating n8n workflows with Claude required supplemental cheat sheets and node examples. Now, web search and extended thinking enable Claude to understand workflow structures and tool relationships natively.""",
        "start_time": 350,
        "end_time": 425,
        "topics": ["Claude 4", "extended thinking", "web search", "workflow generation"],
        "importance": "high",
        "context": "Technical foundation and capabilities"
    })
    
    # Chunk 7: AI Agent Module and LangChain Foundation
    chunks.append({
        "text": """The AI agent module in n8n is built on LangChain, a framework that revolutionized the n8n community. This module creates central agents that process prompts, communicate with tools, utilize language models, and maintain internal memory.

Since n8n uses JSON (JavaScript Object Notation) for workflow visualization, language models like Claude 4 Opus can manipulate and generate these JSONs to create complete workflows and import them directly into n8n.""",
        "start_time": 425,
        "end_time": 495,
        "topics": ["AI agent module", "LangChain", "JSON", "workflow architecture"],
        "importance": "high",
        "context": "Technical architecture explanation"
    })
    
    # Chunk 8: Tool Limitations and Agent Constraints
    chunks.append({
        "text": """AI agents have specific tool limitations compared to standard n8n workflows. Agents cannot use trigger-based tools (like watching for new Google Sheet rows) but require action-based tools that perform specific functions when called.

For Google Sheets integration, agents can add rows, retrieve data, or search content - all functional operations rather than trigger-based monitoring. Understanding these constraints is crucial for successful agent workflow design.""",
        "start_time": 495,
        "end_time": 570,
        "topics": ["tool limitations", "triggers vs actions", "Google Sheets", "workflow constraints"],
        "importance": "high",
        "context": "Critical technical limitations"
    })
    
    # Chunk 9: The Core Challenge - Tool Creation
    chunks.append({
        "text": """The key to this entire process lies in creating tools reliably in the exact format the AI agent node expects. Without proper tool configuration, even sophisticated prompts will fail to generate working workflows.

The goal is creating JSON sets with one orchestrating agent and multiple sub-agents with attached tools, avoiding deep nesting that could create overly complex agent hierarchies.""",
        "start_time": 570,
        "end_time": 630,
        "topics": ["tool creation", "JSON structure", "agent hierarchy", "workflow design"],
        "importance": "high",
        "context": "Critical success factor identification"
    })
    
    # Chunk 10: Master Prompt Structure and Goals
    chunks.append({
        "text": """The master prompt positions Claude as an expert n8n workflow architect with the mission to generate comprehensive, functional, and importable AI agent systems. The prompt emphasizes emulating structural patterns, node types, and connection methods from provided examples.

Paramount goals include ensuring 100% valid JSON generation - meaning corruption-free, importable workflows without property value errors that would prevent n8n visualization and import.""",
        "start_time": 630,
        "end_time": 700,
        "topics": ["prompt engineering", "JSON validation", "workflow architecture", "error prevention"],
        "importance": "high",
        "context": "Prompt design principles"
    })
    
    # Chunk 11: Two-Stage Process and Agent Brainstorming
    chunks.append({
        "text": """The prompt implements a two-stage process. Stage one requires analyzing business descriptions to conceptualize 6-8 potential specialized AI agents, providing baseline ideas for development.

Each conceptual agent needs a one-sentence description and specification of n8n nodes or verifiable public APIs discovered through web search. The prompt explicitly prohibits unverified or hallucinated tools/APIs to ensure functional implementations.""",
        "start_time": 700,
        "end_time": 775,
        "topics": ["two-stage process", "agent brainstorming", "API verification", "web search"],
        "importance": "medium",
        "context": "Prompt methodology breakdown"
    })
    
    # Chunk 12: Hallucination Prevention and Credit Management
    chunks.append({
        "text": """Hallucinated tools/APIs represent a significant risk where Claude might create fictional APIs for specific companies rather than using real, functional endpoints. The prompt specifically guards against this by requiring web search verification.

Starting with three agents rather than all 6-8 serves two purposes: credit conservation (preventing full Claude Pro plan consumption) and time management (5-10 minutes vs 30+ minutes), allowing quick validation before full commitment.""",
        "start_time": 775,
        "end_time": 845,
        "topics": ["hallucination prevention", "credit management", "validation strategy", "API verification"],
        "importance": "medium",
        "context": "Risk mitigation and practical considerations"
    })
    
    # Chunk 13: Tool Requirements and Error Handling
    chunks.append({
        "text": """Specialized agents must utilize 2-3 tools with an absolute maximum of 5 if genuinely distinct, critical, and verifiable. All tools must be real and functional, not fabricated.

Additionally, each agent requires correctly connected response and try-again nodes wired to the AI agent's success and error outputs, ensuring proper error handling and retry capabilities for temporary failures.""",
        "start_time": 845,
        "end_time": 905,
        "topics": ["tool requirements", "error handling", "retry logic", "workflow reliability"],
        "importance": "high",
        "context": "Technical requirements and reliability"
    })
    
    # Chunk 14: Prompt Engineering and Business Context
    chunks.append({
        "text": """Business descriptions are strategically placed at the prompt's end because language models typically pay strongest attention to the beginning and end sections. This ensures business operations and mechanisms receive proper focus during generation.

Users can adapt the entire system by simply changing the business description at the bottom while keeping the sophisticated prompt structure intact.""",
        "start_time": 905,
        "end_time": 965,
        "topics": ["prompt engineering", "attention patterns", "business context", "adaptability"],
        "importance": "medium",
        "context": "Advanced prompt optimization techniques"
    })
    
    # Chunk 15: Claude Projects and Enhanced Capabilities
    chunks.append({
        "text": """The system becomes significantly more powerful when combined with Claude projects and tool specifications. This creates a sophisticated version that goes beyond basic prompt functionality.

The enhanced approach will be demonstrated through three hypothetical businesses: Flexiflow Studios (TikTok agency), Unicorn Milkshake (dessert place), and Chaos Coffee (coffee shops), each using different tool combinations like ClickUp, Airtable, Slack, Google, Zoom, Monday.com, and Asana.""",
        "start_time": 965,
        "end_time": 1030,
        "topics": ["Claude projects", "business examples", "tool combinations", "enhanced capabilities"],
        "importance": "medium",
        "context": "Advanced implementation preview"
    })
    
    # Chunk 16: The Golden Nugget - agents_tools.json
    chunks.append({
        "text": """The breakthrough insight involves creating an agents_tools.json file - a "cheat code" that solves the tool limitation problem. While Asana offers 22+ options in standard n8n, the AI agent module can only access a subset of these functions.

By creating one massive agent with all desired tools attached and exporting it as JSON, this file becomes a knowledge base that teaches Claude exactly how to connect various services (Slack, Asana, Monday, Zoho) to AI agents. This eliminates the need for constant web search or manual tool configuration.""",
        "start_time": 1030,
        "end_time": 1135,
        "topics": ["agents_tools.json", "tool limitations", "knowledge base", "cheat code", "tool attachment"],
        "importance": "high",
        "context": "Key breakthrough and solution"
    })
    
    # Chunk 17: Practical Business Examples
    chunks.append({
        "text": """Three business examples demonstrate the system's versatility:

Flexiflow Studios (TikTok agency): Generated client request handler, project setup, and team coordination agents using Zoom, ClickUp, Slack, Google Sheets, and Airtable.

Pet Pal Concierge (pet care service): Created emergency care coordinator, provider management, booking/scheduling, and photo update agents using Airtable, Slack, Zoom, and Asana.

Chaos Coffee Co. (15 coffee shops): Produced inventory discovery, recipe innovation, quality control, and financial analytics agents with Google Sheets, Airtable, and ClickUp integration.""",
        "start_time": 1135,
        "end_time": 1235,
        "topics": ["business examples", "agent specialization", "tool integration", "practical applications"],
        "importance": "medium",
        "context": "Real-world application demonstrations"
    })
    
    # Chunk 18: Results and Value Proposition
    chunks.append({
        "text": """Each generated workflow produces logically structured agents with sophisticated starter prompts ready for immediate use. While not perfect out-of-the-box, the system provides a strong foundation getting users from 0 to 80% completion rapidly.

The approach excels at brainstorming possibilities and establishing architectural foundations, significantly accelerating development time even when fine-tuning is required for specific use cases.""",
        "start_time": 1235,
        "end_time": 1295,
        "topics": ["workflow results", "value proposition", "rapid prototyping", "development acceleration"],
        "importance": "medium",
        "context": "Expected outcomes and benefits"
    })
    
    # Chunk 19: Community Resources and Access
    chunks.append({
        "text": """Two resource tiers are available: basic prompt and sample agent network through the first description link, and premium supercharged prompt with cheat sheet guide through the exclusive community access.

The community provides additional "mad scientist experiments" and exclusive content unavailable on YouTube, designed for early AI adopters seeking advanced automation capabilities.""",
        "start_time": 1295,
        "end_time": 1355,
        "topics": ["community resources", "access tiers", "exclusive content", "advanced automation"],
        "importance": "low",
        "context": "Resource availability and community access"
    })
    
    # Chunk 20: Conclusion and Call to Action
    chunks.append({
        "text": """The system enables rapid creation of AI agent network drafts, transforming complex automation development into an accessible, prompt-driven process. Users can quickly move from concept to functional agent armies without deep technical expertise.

This represents a significant shift in automation development, making sophisticated agent architectures available to a broader audience through intelligent prompt engineering and Claude 4's advanced capabilities.""",
        "start_time": 1355,
        "end_time": 1448,
        "topics": ["conclusion", "democratization", "accessibility", "agent development"],
        "importance": "medium",
        "context": "Final summary and impact statement"
    })
    
    return chunks


def add_metadata_to_chunks(chunks: List[Dict]) -> List[Dict]:
    """Add video metadata and embeddings info to chunks."""
    
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    for i, chunk in enumerate(chunks):
        # Add token count
        chunk['token_count'] = len(enc.encode(chunk['text']))
        
        # Add video metadata
        chunk['video_id'] = VIDEO_ID
        chunk['video_title'] = VIDEO_TITLE
        chunk['video_channel'] = VIDEO_CHANNEL
        chunk['video_url'] = VIDEO_URL
        chunk['video_duration'] = VIDEO_DURATION
        
        # Add chunk metadata
        chunk['chunk_index'] = i
        chunk['total_chunks'] = len(chunks)
        chunk['processing_date'] = datetime.now().isoformat()
        chunk['processing_method'] = 'manual_n8n_agents'
        
        # Quality indicators
        chunk['has_timestamps'] = True
        chunk['has_topics'] = True
        chunk['manually_reviewed'] = True
        
    return chunks


def validate_chunks(chunks: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate chunks for completeness and quality."""
    
    issues = []
    
    # Check coverage
    total_duration = chunks[-1]['end_time']
    if abs(total_duration - VIDEO_DURATION) > 10:
        issues.append(f"Duration mismatch: chunks cover {total_duration}s, video is {VIDEO_DURATION}s")
    
    # Check for gaps
    for i in range(1, len(chunks)):
        gap = chunks[i]['start_time'] - chunks[i-1]['end_time']
        if gap > 10:
            issues.append(f"Gap between chunk {i-1} and {i}: {gap}s")
    
    # Check chunk sizes
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    for i, chunk in enumerate(chunks):
        tokens = len(enc.encode(chunk['text']))
        if tokens < 100:
            issues.append(f"Chunk {i} too small: {tokens} tokens")
        if tokens > 800:
            issues.append(f"Chunk {i} too large: {tokens} tokens")
    
    return len(issues) == 0, issues


def save_chunks(chunks: List[Dict], filename: str = None):
    """Save chunks to JSON file."""
    
    if filename is None:
        filename = f"manual_chunks_n8n_agents_{VIDEO_ID}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'video_id': VIDEO_ID,
            'video_title': VIDEO_TITLE,
            'video_url': VIDEO_URL,
            'processing_date': datetime.now().isoformat(),
            'processing_method': 'manual_n8n_agents',
            'chunk_count': len(chunks),
            'chunks': chunks
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(chunks)} chunks to {filename}")


def print_summary(chunks: List[Dict]):
    """Print summary statistics."""
    
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    total_tokens = sum(len(enc.encode(c['text'])) for c in chunks)
    avg_tokens = total_tokens // len(chunks)
    
    print("\n📊 Chunk Summary:")
    print(f"Total chunks: {len(chunks)}")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Average tokens per chunk: {avg_tokens}")
    print(f"Coverage: {chunks[0]['start_time']}s - {chunks[-1]['end_time']}s")
    
    # Topic distribution
    all_topics = []
    for chunk in chunks:
        all_topics.extend(chunk.get('topics', []))
    
    topic_counts = {}
    for topic in all_topics:
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    print("\n🏷️ Topic Distribution:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {topic}: {count} chunks")


def main():
    """Create and save manual chunks."""
    
    print(f"🎬 Creating manual chunks for: {VIDEO_TITLE}")
    print(f"📺 Channel: {VIDEO_CHANNEL}")
    print(f"⏱️ Duration: {VIDEO_DURATION}s")
    print("="*70)
    
    # Create chunks
    chunks = create_manual_chunks()
    chunks = add_metadata_to_chunks(chunks)
    
    # Validate
    valid, issues = validate_chunks(chunks)
    if not valid:
        print("\n⚠️ Validation issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ All validation checks passed!")
    
    # Save chunks
    save_chunks(chunks)
    
    # Print summary
    print_summary(chunks)
    
    print("\n✨ Manual chunking complete!")
    print(f"\nNext steps:")
    print("1. Review the generated chunks")
    print("2. Run: uv run python import_chunks.py manual_chunks_n8n_agents_u2NluvotA80.json")
    print("3. Update knowledge base with learnings from this video")


if __name__ == "__main__":
    main()