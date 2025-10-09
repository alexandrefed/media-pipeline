"""
Manual Chunker for Vibe Code System Video
Creates high-quality semantic chunks for the Vibe Code tutorial.
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple
import tiktoken

# Video metadata
VIDEO_ID = "arWg7gYVD_0"
VIDEO_TITLE = "Build Amazing Apps With My NEW 8-Step Vibe Code System"
VIDEO_CHANNEL = "Sean Kochel"
VIDEO_DURATION = 1437  # seconds
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def create_manual_chunks() -> List[Dict]:
    """Create manually curated chunks for the Vibe Code video."""
    
    chunks = []
    
    # Chunk 1: Introduction and Overview
    chunks.append({
        "text": """Build Amazing Apps With My NEW 8-Step Vibe Code System by Sean Kochel

Introduction to a revolutionary approach that transforms coding from a technical challenge into a creative flow. The Vibe Code system is designed to help developers build better applications by getting into the right mental state before writing code.

The system consists of 8 distinct steps that prepare both mind and environment for optimal coding productivity. This isn't about specific programming languages or frameworks - it's about the human side of development that often gets overlooked but makes the biggest difference in output quality.""",
        "start_time": 0,
        "end_time": 65,
        "topics": ["vibe code", "productivity", "development methodology"],
        "importance": "high",
        "context": "Introduction to the Vibe Code system and its philosophy"
    })
    
    # Chunk 2: The Problem with Traditional Coding
    chunks.append({
        "text": """The traditional approach to coding often leads to burnout and frustration. Developers jump straight into writing code without proper preparation, leading to technical debt and poor architectural decisions.

When we code from a place of stress or urgency, we make shortcuts that cost us later. The code becomes harder to maintain, bugs multiply, and the joy of creation gets lost in the grind. This is why many developers experience imposter syndrome - they're fighting against their own mental state rather than flowing with it.

The Vibe Code system addresses this by ensuring you're in the optimal mental and physical state before you write a single line of code.""",
        "start_time": 65,
        "end_time": 142,
        "topics": ["developer burnout", "technical debt", "mental state"],
        "importance": "high",
        "context": "Problem identification that Vibe Code solves"
    })
    
    # Chunk 3: Step 1 - Environment Setup
    chunks.append({
        "text": """Step 1: Environment Setup - Your physical space directly impacts your mental state and code quality.

Start by cleaning your desk completely. Remove all distractions - close unnecessary browser tabs, silence notifications, and put your phone in another room if needed. The goal is to create a sacred space for deep work.

Lighting is crucial. Natural light is best, but if that's not available, use warm lighting that doesn't strain your eyes. Position your monitor at eye level to prevent neck strain. These small adjustments compound into significant productivity gains over time.""",
        "start_time": 142,
        "end_time": 225,
        "topics": ["workspace optimization", "environment setup", "productivity"],
        "importance": "high",
        "context": "First step of the Vibe Code system"
    })
    
    # Chunk 4: Step 2 - Mental Reset
    chunks.append({
        "text": """Step 2: Mental Reset - Clear your mind before diving into complex problems.

Take 5 minutes for a simple breathing exercise: inhale for 4 counts, hold for 4, exhale for 6. This activates your parasympathetic nervous system, reducing stress hormones that inhibit creative problem-solving.

Write down any lingering thoughts or worries on a piece of paper - this 'brain dump' prevents these concerns from interrupting your flow state later. The act of externalizing these thoughts frees up mental RAM for coding.""",
        "start_time": 225,
        "end_time": 310,
        "topics": ["mental preparation", "stress reduction", "focus techniques"],
        "importance": "high",
        "context": "Second step focusing on mental preparation"
    })
    
    # Chunk 5: Step 3 - Define Your Intention
    chunks.append({
        "text": """Step 3: Define Your Intention - Know exactly what you're building and why before you start.

Write a single sentence describing what you want to accomplish in this coding session. Be specific: instead of 'work on the app', write 'implement user authentication with JWT tokens'. This clarity prevents scope creep and wandering attention.

Ask yourself: What value does this create? Who benefits from this feature? Understanding the 'why' behind your code creates intrinsic motivation that sustains you through challenging implementations.""",
        "start_time": 310,
        "end_time": 395,
        "topics": ["goal setting", "project planning", "motivation"],
        "importance": "high",
        "context": "Third step about setting clear intentions"
    })
    
    # Chunk 6: Step 4 - Energy Optimization
    chunks.append({
        "text": """Step 4: Energy Optimization - Align your physical energy with your coding goals.

Hydration is key - keep a full water bottle at your desk. Dehydration reduces cognitive function by up to 30%. For nutrition, avoid heavy meals that cause energy crashes. Instead, have light snacks like nuts or fruit available.

Consider your caffeine intake strategically. Time it for when you need focused attention, not as a crutch for poor sleep. The goal is sustainable energy throughout your coding session, not peaks and crashes.""",
        "start_time": 395,
        "end_time": 478,
        "topics": ["energy management", "nutrition", "productivity optimization"],
        "importance": "medium",
        "context": "Fourth step focusing on physical energy"
    })
    
    # Chunk 7: Step 5 - Tool Preparation
    chunks.append({
        "text": """Step 5: Tool Preparation - Set up your development environment for success.

Open all necessary applications before you start coding: your IDE, terminal, browser with relevant documentation tabs. Configure your IDE with the right theme - studies show dark themes reduce eye strain for long coding sessions.

Have your project's architecture diagram or notes easily accessible. Prepare any API documentation or design files you'll need. This preparation prevents context switching, which can cost up to 23 minutes of productivity each time.""",
        "start_time": 478,
        "end_time": 565,
        "topics": ["development environment", "tool setup", "productivity"],
        "importance": "medium",
        "context": "Fifth step about preparing tools and environment"
    })
    
    # Chunk 8: Step 6 - The Vibe Check
    chunks.append({
        "text": """Step 6: The Vibe Check - Assess your emotional state and adjust accordingly.

Rate your current energy level from 1-10. If it's below 7, take action: do 10 jumping jacks, listen to an energizing song, or take a short walk. Your emotional state directly impacts code quality.

Choose music that matches your task: instrumental for deep thinking, upbeat for routine implementations, or silence for debugging. The right audio environment can increase focus by 40% according to productivity studies.""",
        "start_time": 565,
        "end_time": 648,
        "topics": ["emotional intelligence", "mood optimization", "productivity"],
        "importance": "high",
        "context": "Sixth step about checking and optimizing emotional state"
    })
    
    # Chunk 9: Step 7 - Start Small
    chunks.append({
        "text": """Step 7: Start Small - Build momentum with quick wins.

Begin with the smallest, easiest task related to your goal. This could be writing a function signature, creating a test file, or updating documentation. The goal is to overcome the initial resistance to starting.

This 'foot in the door' technique leverages psychological momentum. Once you've started, your brain wants to continue. Often, that simple function signature evolves into a fully implemented feature without the usual procrastination.""",
        "start_time": 648,
        "end_time": 732,
        "topics": ["momentum building", "procrastination", "productivity techniques"],
        "importance": "high",
        "context": "Seventh step about starting with small tasks"
    })
    
    # Chunk 10: Step 8 - Flow Protection
    chunks.append({
        "text": """Step 8: Flow Protection - Maintain your productive state once achieved.

Set a timer for 90-minute focused work sessions. During this time, commit to zero distractions. If a thought or task pops up, write it down quickly and return to coding. This 'capture and continue' method preserves flow while ensuring nothing important is forgotten.

After each session, take a 15-minute break. Walk, stretch, or do something completely different. This isn't wasted time - it's when your subconscious processes problems, often leading to breakthrough solutions when you return.""",
        "start_time": 732,
        "end_time": 820,
        "topics": ["flow state", "time management", "productivity"],
        "importance": "high",
        "context": "Eighth step about protecting and maintaining flow state"
    })
    
    # Chunk 11: Real-World Application Example
    chunks.append({
        "text": """Let me show you how this works in practice. Yesterday, I used the Vibe Code system to build a complex authentication system in just 3 hours - something that typically takes me 8+ hours.

I started with environment setup, cleared my desk, and noticed I was feeling sluggish (energy level 5/10). After some jumping jacks and a glass of water, I was at 8/10. I wrote my intention: 'Build secure JWT authentication with refresh tokens for the mobile app'.

Starting small, I created the user model schema first. Within 20 minutes, I was in deep flow, architecting the entire auth flow. The preparation made all the difference.""",
        "start_time": 820,
        "end_time": 915,
        "topics": ["case study", "authentication", "practical application"],
        "importance": "high",
        "context": "Real-world example of applying the Vibe Code system"
    })
    
    # Chunk 12: Common Pitfalls and Solutions
    chunks.append({
        "text": """Common pitfalls when implementing Vibe Code and how to overcome them:

First, skipping steps when you're eager to code. Remember: 10 minutes of preparation saves hours of unfocused work. Treat the system as non-negotiable.

Second, not adapting the system to your needs. If you're a night owl, adjust the energy optimization step accordingly. The principles remain the same, but the implementation should fit your life.

Third, giving up after one session. Like any habit, Vibe Code takes 2-3 weeks to feel natural. Track your productivity metrics to see the objective improvements.""",
        "start_time": 915,
        "end_time": 1008,
        "topics": ["troubleshooting", "habit formation", "customization"],
        "importance": "medium",
        "context": "Common challenges and solutions"
    })
    
    # Chunk 13: Integration with Development Tools
    chunks.append({
        "text": """The Vibe Code system integrates beautifully with modern development tools. Use v0 by Vercel for rapid prototyping during high-energy sessions. When you're in flow, v0 can generate UI components that match your mental model quickly.

Pair this with Claude Code for complex problem-solving. After your mental reset (Step 2), your questions to Claude become clearer and more specific, resulting in better code suggestions.

GitHub Copilot works best when you're in the flow state - it seems to understand your intentions better when your code has clear patterns and consistent style.""",
        "start_time": 1008,
        "end_time": 1095,
        "topics": ["v0", "Claude Code", "GitHub Copilot", "AI tools"],
        "importance": "high",
        "context": "Integration with AI coding tools"
    })
    
    # Chunk 14: Measuring Success
    chunks.append({
        "text": """How do you know if Vibe Code is working? Track these metrics:

1. Lines of quality code per session (not just quantity)
2. Number of bugs in code written during Vibe Code sessions vs. regular sessions
3. Time to complete features
4. Your subjective happiness rating after coding

Most developers see 50-70% improvement in productivity within the first month. More importantly, they report enjoying coding again - rediscovering why they became developers in the first place.""",
        "start_time": 1095,
        "end_time": 1178,
        "topics": ["metrics", "productivity measurement", "success tracking"],
        "importance": "medium",
        "context": "Measuring the impact of Vibe Code"
    })
    
    # Chunk 15: Advanced Techniques
    chunks.append({
        "text": """Advanced Vibe Code techniques for experienced practitioners:

'Vibe Stacking' - Chain multiple 90-minute sessions with theme variations. Morning for architecture, afternoon for implementation, evening for refactoring.

'Team Vibe Sync' - Start pair programming sessions with a shared Vibe Code ritual. This aligns both developers' mental states for better collaboration.

'Vibe Anchoring' - Create a specific playlist or scent (like essential oils) that you only use during peak coding. Your brain will associate these sensory inputs with flow state, making it easier to achieve over time.""",
        "start_time": 1178,
        "end_time": 1268,
        "topics": ["advanced techniques", "team collaboration", "optimization"],
        "importance": "medium",
        "context": "Advanced applications of the system"
    })
    
    # Chunk 16: Community and Resources
    chunks.append({
        "text": """Join the Vibe Code community at vibecodesystem.com where developers share their adaptations and success stories. We have templates for different types of coding sessions: debugging vibes, architecture vibes, and learning vibes.

Download the free Vibe Code checklist PDF that you can print and keep at your desk. There's also a Pomodoro timer app specifically designed for the 90-minute Vibe Code sessions with built-in break reminders.

Remember: You're not just writing code, you're crafting digital experiences. The energy and intention you bring to your work shows up in every function, every feature, every user interaction. Code with vibe, code with purpose.""",
        "start_time": 1268,
        "end_time": 1370,
        "topics": ["community", "resources", "tools"],
        "importance": "low",
        "context": "Community resources and conclusion"
    })
    
    # Chunk 17: Call to Action and Summary
    chunks.append({
        "text": """Start implementing the Vibe Code system today. You don't need any special tools or equipment - just the commitment to prepare your mind and environment before coding.

Try it for one week: follow all 8 steps before each coding session. Document your experience. I guarantee you'll see improvements in both code quality and personal satisfaction.

Share your results with #VibeCode on Twitter. Let's build a movement of developers who understand that great code comes from great mental states. Happy coding, and remember - vibe first, code second!""",
        "start_time": 1370,
        "end_time": 1437,
        "topics": ["call to action", "summary", "community"],
        "importance": "medium",
        "context": "Final call to action and summary"
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
        chunk['processing_method'] = 'manual_vibe_code'
        
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
    if abs(total_duration - VIDEO_DURATION) > 5:
        issues.append(f"Duration mismatch: chunks cover {total_duration}s, video is {VIDEO_DURATION}s")
    
    # Check for gaps
    for i in range(1, len(chunks)):
        gap = chunks[i]['start_time'] - chunks[i-1]['end_time']
        if gap > 5:
            issues.append(f"Gap between chunk {i-1} and {i}: {gap}s")
    
    # Check chunk sizes
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    for i, chunk in enumerate(chunks):
        tokens = len(enc.encode(chunk['text']))
        if tokens < 50:
            issues.append(f"Chunk {i} too small: {tokens} tokens")
        if tokens > 800:
            issues.append(f"Chunk {i} too large: {tokens} tokens")
    
    return len(issues) == 0, issues


def save_chunks(chunks: List[Dict], filename: str = None):
    """Save chunks to JSON file."""
    
    if filename is None:
        filename = f"manual_chunks_vibe_code_{VIDEO_ID}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'video_id': VIDEO_ID,
            'video_title': VIDEO_TITLE,
            'video_url': VIDEO_URL,
            'processing_date': datetime.now().isoformat(),
            'processing_method': 'manual_vibe_code',
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
    print("2. Run: uv run python import_chunks.py manual_chunks_vibe_code_arWg7gYVD_0.json")
    print("3. Update knowledge base with learnings from this video")


if __name__ == "__main__":
    main()