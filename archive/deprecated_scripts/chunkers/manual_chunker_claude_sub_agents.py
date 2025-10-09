"""
Manual Chunker for Claude Code Sub Agents BUILD THEMSELVES
Creates high-quality semantic chunks for the Claude Code sub-agents tutorial.
"""

import json
from datetime import datetime
from typing import List, Dict
import tiktoken

# Video metadata
VIDEO_ID = "7B2HJr0Y68g"
VIDEO_TITLE = "My Claude Code Sub Agents BUILD THEMSELVES"
VIDEO_CHANNEL = "IndyDevDan"
VIDEO_DURATION = 1838  # seconds
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def create_manual_chunks() -> List[Dict]:
    """Create manually curated chunks for the Claude Code sub-agents video."""
    
    chunks = []
    
    # Chunk 1: Introduction and Vision
    chunks.append({
        "text": """Claude Code Sub Agents BUILD THEMSELVES by IndyDevDan

Imagine starting your day, opening the terminal, firing up Claude Code, then kicking off a single prompt that does hours of work in minutes. This is possible with Claude Code sub agents - specialized workflows where each agent does one thing extraordinarily well.

The meta agent demonstrated can build other agents. Code is a commodity, but fine-tuned prompts yield extreme value. This video covers two big mistakes engineers make with sub agents and how to build effective ones.

Sub agents don't work like most think. The flow: You prompt → Primary agent → Sub agents work autonomously → Report to primary agent → Primary agent reports to you. This critical flow means sub agents respond to your primary agent, not directly to you. This changes how you write sub agent prompts.""",
        "start_time": 0,
        "end_time": 180,
        "topics": ["Claude Code", "sub agents", "meta agent", "workflow automation", "prompt engineering"],
        "importance": "high",
        "context": "Introduction and key concept explanation"
    })
    
    # Chunk 2: Sub Agent System Prompts and First Mistake
    chunks.append({
        "text": """The first big mistake engineers make: not understanding that sub agent prompts are SYSTEM prompts, not user prompts. When writing in the agents directory, you're defining the system prompt that configures the sub agent's behavior.

Example hello world agent structure:
- Agent name: Unique ID
- Description: Tells primary agent when to call this sub agent
- Tools: Specific tools available
- System prompt with purpose and report sections

The report/response format is crucial - explicitly instruct the sub agent how to communicate back to the primary agent. For example: "Claude, respond to the user with this message..."

This is different from slash commands (like /p prime) which are user prompts going directly to the primary agent's context window. Understanding this distinction is critical for sub agent success.""",
        "start_time": 180,
        "end_time": 360,
        "topics": ["system prompts", "user prompts", "agent configuration", "common mistakes"],
        "importance": "high",
        "context": "First major mistake explanation"
    })
    
    # Chunk 3: Information Flow and the Big Three
    chunks.append({
        "text": """You don't prompt sub agents directly - you write prompts for your primary agent to prompt sub agents. Claude Code sub agents are tools of delegation for your primary agent.

The Big Three concept becomes even more important with multi-agent systems:
1. Context - flows between agents
2. Model - used by each agent
3. Prompt - chain of prompts between agents

This isn't going away - it's becoming MORE important as we scale to multi-agent systems. Understanding information flow is crucial.

The true flow: Sub agents respond to primary agent, not to you. With powerful multi-agent orchestration, you can chain calls and responses. We started with prompt chaining years ago, now we're prompt chaining with bigger compositional units.""",
        "start_time": 360,
        "end_time": 540,
        "topics": ["information flow", "Big Three", "multi-agent systems", "delegation", "prompt chaining"],
        "importance": "high",
        "context": "Core architectural concepts"
    })
    
    # Chunk 4: Meta Agent Problem-Solution-Tech Approach
    chunks.append({
        "text": """A big issue in GenAI: engineers using technology to solve non-existent problems. Real engineers work: Problem → Solution → Tech (not the reverse).

Example problem: "When doing agentic coding at scale, I lose track of what agents have done"
Solution: "Add text-to-speech to agents so they notify when done and what they've done"
Technology: Claude Code sub agents with meta agent to build TTS agent

The meta agent approach allows building specialized agents rapidly. First, understand available tools using 'all tools' command to list everything in TypeScript function signature format. For this example, need 11 Labs text-to-speech and play audio tools.

Validate the workflow by testing tools manually in primary agent context before encoding into a sub agent.""",
        "start_time": 540,
        "end_time": 780,
        "topics": ["problem-solution-tech", "meta agent", "11 Labs", "text-to-speech", "tool discovery"],
        "importance": "high",
        "context": "Practical implementation approach"
    })
    
    # Chunk 5: Meta Agent in Action
    chunks.append({
        "text": """The meta agent creates new sub agents from descriptions. It has a system prompt detailing agent creation, works in isolated context, and pulls live Claude Code documentation for accuracy.

Key meta agent features:
- Triggered by "build a new sub agent" language
- Generates complete agent configuration files
- Creates proper format with all required fields
- Double-checks work with reasoning model

After generation, customize the agent description - this is THE MOST IMPORTANT part as it tells the primary agent when to call this sub agent. Add trigger phrases like "if they say TTS, TTS summary, use this agent."

Remember to instruct in the description how the primary agent should prompt this sub agent, since sub agents have no conversation context.""",
        "start_time": 780,
        "end_time": 960,
        "topics": ["meta agent", "agent generation", "description importance", "customization"],
        "importance": "high",
        "context": "Meta agent demonstration"
    })
    
    # Chunk 6: Sub Agent Benefits
    chunks.append({
        "text": """Key benefits of Claude Code sub agents:

1. Context Preservation - Each sub agent operates in its own context, preventing main conversation pollution. Fresh agent instances for every task with isolated context windows.

2. Save Context Window - Important until we get 2.5M+ token windows (not coming soon).

3. Specialized Agent Expertise - Fine-tune instructions and tools. Lock down specific tools each agent can access.

4. Reusability - Store in repository to build agents for your codebase.

5. Hidden Benefits:
   - Focused agents perform better (like focused engineers)
   - Simple multi-agent orchestration
   - Combine with custom commands and hooks for powerful systems

Example: Enhance 'prime' command with 'prime TTS' to chain text-to-speech summary agent after completion.""",
        "start_time": 960,
        "end_time": 1200,
        "topics": ["benefits", "context preservation", "specialization", "reusability", "orchestration"],
        "importance": "high",
        "context": "Advantages of sub agent architecture"
    })
    
    # Chunk 7: Sub Agent Challenges
    chunks.append({
        "text": """Issues with sub agents:

1. No Context History - Sub agents only know what primary agent tells them. Like firing up Claude in one-shot mode. Both a problem and benefit (context preservation flip side).

2. Hard to Debug - Can't see actual workflows, prompts, or full tool parameters. Only get tool calls, making debugging challenging.

3. Decision Overload - As agent count scales, primary agent may struggle choosing which to call. Clear descriptions critical.

4. Dependency Coupling - Agents depending on other agents' output creates fragility. One change can break entire chains in non-deterministic systems.

5. Can't Call Sub Agents in Sub Agents - Currently not supported (might be added as 'dangerous' mode later).

Solution: Keep agents separate in isolated workflows, don't overload sub agent chains, be extremely clear about when to call each agent.""",
        "start_time": 1200,
        "end_time": 1440,
        "topics": ["challenges", "debugging", "dependency management", "limitations", "best practices"],
        "importance": "high",
        "context": "Common problems and solutions"
    })
    
    # Chunk 8: Scaling with Multi-Agent Systems
    chunks.append({
        "text": """This is a powerful feature with more to explore combining agents and custom slash commands (reusable prompts). Perspective matters when scaling multi-agent systems.

The flow of the Big Three (Context, Model, Prompt) matters more as you scale agent count. It's a core principle of AI coding that differentiates what you can do with agent coding.

Key takeaways:
- Agents are the most important technology right now
- Leading agent is Claude Code
- Don't offload all cognitive work to agents - deeply understand your tools
- Focus on the signal, cancel out the noise
- As it gets easier to build, we can scale compute further
- If you scale your compute, you scale your success

The meta agent and all examples will be available in the Claude Code hooks mastery codebase.""",
        "start_time": 1440,
        "end_time": 1838,
        "topics": ["scaling", "multi-agent systems", "principles", "compute scaling", "best practices"],
        "importance": "high",
        "context": "Future directions and conclusions"
    })
    
    return chunks


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def main():
    """Generate the manual chunks and save to file."""
    chunks = create_manual_chunks()
    
    # Add metadata to each chunk
    for i, chunk in enumerate(chunks):
        chunk['chunk_id'] = f"{VIDEO_ID}_chunk_{i+1}"
        chunk['video_id'] = VIDEO_ID
        chunk['video_title'] = VIDEO_TITLE
        chunk['channel'] = VIDEO_CHANNEL
        chunk['video_url'] = VIDEO_URL
        chunk['processed_date'] = datetime.now().isoformat()
        chunk['token_count'] = count_tokens(chunk['text'])
        chunk['processing_method'] = 'manual_semantic'
    
    # Calculate statistics
    total_tokens = sum(chunk['token_count'] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    print(f"Created {len(chunks)} manual chunks")
    print(f"Total tokens: {total_tokens}")
    print(f"Average tokens per chunk: {avg_tokens:.0f}")
    print(f"Token range: {min(c['token_count'] for c in chunks)} - {max(c['token_count'] for c in chunks)}")
    
    # Save chunks
    output_file = f"manual_chunks_{VIDEO_ID}.json"
    output_data = {
        'video_metadata': {
            'video_id': VIDEO_ID,
            'title': VIDEO_TITLE,
            'channel': VIDEO_CHANNEL,
            'duration': VIDEO_DURATION,
            'url': VIDEO_URL,
            'processing_date': datetime.now().isoformat()
        },
        'chunks': chunks,
        'statistics': {
            'total_chunks': len(chunks),
            'total_tokens': total_tokens,
            'average_tokens': avg_tokens,
            'processing_method': 'manual_semantic'
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved manual chunks to: {output_file}")


if __name__ == "__main__":
    main()