#!/usr/bin/env python3
"""
Manual chunker for AI LABS's "This n8n mcp is INSANE... Let AI Create your Entire Automation"
Video ID: xf2i6Acs1mI

Content Type: Technical Tutorial / MCP Integration Guide
Channel: AI LABS
Strategy: Technical implementation tutorial with clear sections:
1. Introduction + Problem identification
2. n8n MCP architecture and advantages 
3. Platform setup and configuration
4. Live demonstration and practical examples
5. Installation guide and API setup

Note: This follows AI LABS' structured technical tutorial format with emphasis
on practical implementation and step-by-step guidance.
Chunk size: 200-350 tokens for technical content to preserve complete instructions and examples.
"""

import json
import tiktoken

def count_tokens(text):
    """Count tokens using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def create_manual_chunks():
    chunks = []
    
    # Chunk 1: Hook + Problem Statement + Solution Preview
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "The n8n Learning Problem: Too Complex, Until Now",
        "text": """n8n is a crazy powerful automation platform. It's got everything: MCPs, AI agents, and insane integrations. YouTube is exploding with tutorials about it, and it totally deserves the hype. You can do absolutely anything with it. So many tools are already baked right in. It's basically like Zapier on pure steroids. But here's the catch: there's way too much to learn. Hundreds of different pieces called nodes.

And sure, the drag and drop thing makes it easier, but honestly, building stuff in code is still way faster because you can just ask AI to write it for you. You're probably thinking, there's got to be a better way. Well, forget all that. There's now a way to just tell Claude or any AI agent exactly what you want, and it will build the entire workflow for you. You literally won't have to touch a single thing. It just does everything.""",
        "start_time": 0,
        "end_time": 60,
        "token_count": count_tokens("""n8n is a crazy powerful automation platform. It's got everything: MCPs, AI agents, and insane integrations. YouTube is exploding with tutorials about it, and it totally deserves the hype. You can do absolutely anything with it. So many tools are already baked right in. It's basically like Zapier on pure steroids. But here's the catch: there's way too much to learn. Hundreds of different pieces called nodes.

And sure, the drag and drop thing makes it easier, but honestly, building stuff in code is still way faster because you can just ask AI to write it for you. You're probably thinking, there's got to be a better way. Well, forget all that. There's now a way to just tell Claude or any AI agent exactly what you want, and it will build the entire workflow for you. You literally won't have to touch a single thing. It just does everything.""")
    }
    
    # Chunk 2: MCP Revolution + Documentation Access Advantage
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "Why n8n MCP Crushes Other AI Tools: Real Documentation Access",
        "text": """The tool that makes this possible is just an MCP. And here's why it changes everything and why you might not really need to learn anything anymore. MCPs like this are going to take over entire applications. To show you the difference, I tried the Blender MCP. It was decent, but everything it built felt incomplete, kind of like AI slop. But why? It's because it didn't really know how things worked, just vague descriptions about the tools that it had.

But the n8n MCP is completely different. This thing has access to the full documentation, real documentation. It understands 90% of the official docs and has dedicated tools that grab that documentation before doing anything. So it never guesses, it actually knows.""",
        "start_time": 60,
        "end_time": 120,
        "token_count": count_tokens("""The tool that makes this possible is just an MCP. And here's why it changes everything and why you might not really need to learn anything anymore. MCPs like this are going to take over entire applications. To show you the difference, I tried the Blender MCP. It was decent, but everything it built felt incomplete, kind of like AI slop. But why? It's because it didn't really know how things worked, just vague descriptions about the tools that it had.

But the n8n MCP is completely different. This thing has access to the full documentation, real documentation. It understands 90% of the official docs and has dedicated tools that grab that documentation before doing anything. So it never guesses, it actually knows.""")
    }
    
    # Chunk 3: Three-Tier Architecture Breakdown
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "n8n MCP Architecture: Three-Tier Tool Structure",
        "text": """Here's how it's structured. First, the core tools. These gather all the information first. They research, pull the right docs, and prep everything. Then the advanced tools. These actually build the workflow. They turn all that research into real structure. Finally, the management tools. These take your completed workflow and deploy it straight into your workspace. You don't have to touch anything at all, plus some back-end tools that keep everything running.

But those first three are the real game changers. Once you see how they work together, you'll understand why this is so powerful.""",
        "start_time": 120,
        "end_time": 160,
        "token_count": count_tokens("""Here's how it's structured. First, the core tools. These gather all the information first. They research, pull the right docs, and prep everything. Then the advanced tools. These actually build the workflow. They turn all that research into real structure. Finally, the management tools. These take your completed workflow and deploy it straight into your workspace. You don't have to touch anything at all, plus some back-end tools that keep everything running.

But those first three are the real game changers. Once you see how they work together, you'll understand why this is so powerful.""")
    }
    
    # Chunk 4: Platform Compatibility + Claude vs Cursor
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Platform Setup: Claude vs Cursor with Proper Configuration",
        "text": """Now, since this is an MCP, it works with both Claude and Cursor. So, it's really up to you, whichever one you prefer or already have set up. That said, they do recommend using it with Claude. And I think that's mainly because of its artifacts feature, which gives it way more flexibility during execution.

But here's something even more interesting. They've built in a system that makes sure the MCP follows the correct order when calling tools so it doesn't mix anything up or call the wrong thing at the wrong time. And they do this through the Claude project setup. When you create a new Claude project, you just drop these configurations in there and it gives the MCP a full rule book to follow.""",
        "start_time": 160,
        "end_time": 220,
        "token_count": count_tokens("""Now, since this is an MCP, it works with both Claude and Cursor. So, it's really up to you, whichever one you prefer or already have set up. That said, they do recommend using it with Claude. And I think that's mainly because of its artifacts feature, which gives it way more flexibility during execution.

But here's something even more interesting. They've built in a system that makes sure the MCP follows the correct order when calling tools so it doesn't mix anything up or call the wrong thing at the wrong time. And they do this through the Claude project setup. When you create a new Claude project, you just drop these configurations in there and it gives the MCP a full rule book to follow.""")
    }
    
    # Chunk 5: Configuration Benefits + Preventing AI Hallucination
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Preventing AI Hallucination: Proper Workflow Structure",
        "text": """Now, if you're not on the pro plan for Claude and you're using Cursor instead, no problem. You can just add those same rules into your Cursor rules file and it's going to work just fine. What this does is set up a clear workflow structure that the agent sticks with. It prevents the kind of hallucination or broken output you sometimes get from LLMs when they don't have proper guidance.

So with this setup in place, you're much more likely to get stable working workflows, not something half-finished or made up.""",
        "start_time": 220,
        "end_time": 260,
        "token_count": count_tokens("""Now, if you're not on the pro plan for Claude and you're using Cursor instead, no problem. You can just add those same rules into your Cursor rules file and it's going to work just fine. What this does is set up a clear workflow structure that the agent sticks with. It prevents the kind of hallucination or broken output you sometimes get from LLMs when they don't have proper guidance.

So with this setup in place, you're much more likely to get stable working workflows, not something half-finished or made up.""")
    }
    
    # Chunk 6: n8n Visual Builder + JSON Structure Explanation
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "How n8n Works: Visual Builder with JSON Foundation",
        "text": """Now the way n8n actually works is that it gives you this visual builder. You can add different nodes to build your automations, kind of like connecting blocks in a flowchart. And for those who don't know, each of these nodes represents a different task or function in your workflow. But behind the scenes, it's all just a JSON file. That file contains every detail: what nodes are used, how they're connected, the parameters, everything.

And the cool thing is, if you already have that JSON pre-built, you can just import it right into n8n and have your workflow show up instantly in the builder.""",
        "start_time": 260,
        "end_time": 310,
        "token_count": count_tokens("""Now the way n8n actually works is that it gives you this visual builder. You can add different nodes to build your automations, kind of like connecting blocks in a flowchart. And for those who don't know, each of these nodes represents a different task or function in your workflow. But behind the scenes, it's all just a JSON file. That file contains every detail: what nodes are used, how they're connected, the parameters, everything.

And the cool thing is, if you already have that JSON pre-built, you can just import it right into n8n and have your workflow show up instantly in the builder.""")
    }
    
    # Chunk 7: Why Standard LLMs Fail + MCP Advantage
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Why ChatGPT and Claude Fail at n8n: The Context Problem",
        "text": """Now, at this point, you might be thinking, wait, why not just ask ChatGPT or Claude to generate that JSON file for me? Well, here's the issue. If you try that, what you'll usually get is a broken mess. The nodes often don't connect properly or the structure doesn't make sense and it definitely won't run. That's because those models don't have the context needed to build actual working workflows.

And this is exactly where the MCP comes in and completely outperforms. As I mentioned earlier, this MCP follows a proper workflow of its own. First retrieving context, then building intelligently based on that context. It doesn't just guess or make up structure. It knows what's valid, what's compatible, and what actually works inside n8n.""",
        "start_time": 310,
        "end_time": 370,
        "token_count": count_tokens("""Now, at this point, you might be thinking, wait, why not just ask ChatGPT or Claude to generate that JSON file for me? Well, here's the issue. If you try that, what you'll usually get is a broken mess. The nodes often don't connect properly or the structure doesn't make sense and it definitely won't run. That's because those models don't have the context needed to build actual working workflows.

And this is exactly where the MCP comes in and completely outperforms. As I mentioned earlier, this MCP follows a proper workflow of its own. First retrieving context, then building intelligently based on that context. It doesn't just guess or make up structure. It knows what's valid, what's compatible, and what actually works inside n8n.""")
    }
    
    # Chunk 8: Intelligent Workflow Creation Process
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "The Smart Creation Process: Context First, Build Second",
        "text": """Here's how it works. First, it pulls up the relevant search nodes, lists available options, and figures out which ones to use. It applies internal rules and logic to guide that process. And based on all that, it starts assembling the JSON file fully formed and ready to run.

Now, this is also where Claude's artifacts feature really shines. In Claude Code, the JSON is built directly inside the chat context. And you can see it takes shape piece by piece. It's just more powerful that way. But even outside of Claude, the MCP still does all of this behind the scenes. Once it has what it needs, it begins constructing the workflow, updates it incrementally, and pushes it directly into your n8n builder where you can see it live and editable just like that.""",
        "start_time": 370,
        "end_time": 430,
        "token_count": count_tokens("""Here's how it works. First, it pulls up the relevant search nodes, lists available options, and figures out which ones to use. It applies internal rules and logic to guide that process. And based on all that, it starts assembling the JSON file fully formed and ready to run.

Now, this is also where Claude's artifacts feature really shines. In Claude Code, the JSON is built directly inside the chat context. And you can see it takes shape piece by piece. It's just more powerful that way. But even outside of Claude, the MCP still does all of this behind the scenes. Once it has what it needs, it begins constructing the workflow, updates it incrementally, and pushes it directly into your n8n builder where you can see it live and editable just like that.""")
    }
    
    # Chunk 9: Live Demo - Deep Search Agent Creation
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Live Demo: Building a Deep Search Agent with Auto-Validation",
        "text": """Let me show you how this works with a real example. I wanted to create a deep search agent, something that could pull research from multiple sources and take its time processing everything. So, I told it the flow I wanted. I asked a question and if needed, the agent follows up with clarifying questions before giving me a detailed final answer.

And it started activating its tools. It looked up templates, searched for the right nodes, and because it understands the context of each node thanks to the built-in documentation, it picked the exact ones we needed. Then, it built the workflow. And here's the cool part: it validated the workflow using a validator tool. That validator checked the logic, referenced the docs, and caught any issues before they even happened.""",
        "start_time": 430,
        "end_time": 490,
        "token_count": count_tokens("""Let me show you how this works with a real example. I wanted to create a deep search agent, something that could pull research from multiple sources and take its time processing everything. So, I told it the flow I wanted. I asked a question and if needed, the agent follows up with clarifying questions before giving me a detailed final answer.

And it started activating its tools. It looked up templates, searched for the right nodes, and because it understands the context of each node thanks to the built-in documentation, it picked the exact ones we needed. Then, it built the workflow. And here's the cool part: it validated the workflow using a validator tool. That validator checked the logic, referenced the docs, and caught any issues before they even happened.""")
    }
    
    # Chunk 10: Adaptive Node Replacement + Brave Search Implementation
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "Dynamic Adaptation: From SERP to Multiple Search Sources",
        "text": """Now, it wanted me to use the SERP API key for Google search. I had some trouble on my account setting it up. So, I told it to swap it out. And it did. It replaced SERP with DuckDuckGo search, Wikipedia search, and Reddit search. So, it created the JSON structure and uploaded it directly to my workspace. I cleaned up the layout a bit since AI created workflows usually end up messy, but that was quick.

Then I provided my OpenAI API key and tested it with a question: Is n8n better than other automation tools? And if yes, why? I hit enter and it executed successfully. It pulled in insights from different sources, including a discussion on Hacker News. Now, the sources could have been better for this specific question. So I went ahead and asked it to implement the Brave Search node using the Brave Search API. I thought this would be necessary to give it a better tool for web search.""",
        "start_time": 490,
        "end_time": 550,
        "token_count": count_tokens("""Now, it wanted me to use the SERP API key for Google search. I had some trouble on my account setting it up. So, I told it to swap it out. And it did. It replaced SERP with DuckDuckGo search, Wikipedia search, and Reddit search. So, it created the JSON structure and uploaded it directly to my workspace. I cleaned up the layout a bit since AI created workflows usually end up messy, but that was quick.

Then I provided my OpenAI API key and tested it with a question: Is n8n better than other automation tools? And if yes, why? I hit enter and it executed successfully. It pulled in insights from different sources, including a discussion on Hacker News. Now, the sources could have been better for this specific question. So I went ahead and asked it to implement the Brave Search node using the Brave Search API. I thought this would be necessary to give it a better tool for web search.""")
    }
    
    # Chunk 11: Installation Requirements + Docker Setup
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Installation Guide: Docker Requirements and Basic Setup",
        "text": """Moving on to the installation. It's actually pretty simple. There's only one requirement: you need to have Docker running on your system. That's because the tool works as a Docker container and it needs Docker to stay active in the background. If you only need the basic configuration where you just read documentation and manually build workflows, that's all you need with this. You're good to go.

But if you want the full experience where the tool manages everything for you, edits files, validates workflows, and basically takes care of everything, you'll need to set up the full integration. The only extra things you'll need for that are your API URL and API key.""",
        "start_time": 550,
        "end_time": 600,
        "token_count": count_tokens("""Moving on to the installation. It's actually pretty simple. There's only one requirement: you need to have Docker running on your system. That's because the tool works as a Docker container and it needs Docker to stay active in the background. If you only need the basic configuration where you just read documentation and manually build workflows, that's all you need with this. You're good to go.

But if you want the full experience where the tool manages everything for you, edits files, validates workflows, and basically takes care of everything, you'll need to set up the full integration. The only extra things you'll need for that are your API URL and API key.""")
    }
    
    # Chunk 12: Configuration Setup + Claude vs Cursor Instructions
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "MCP Configuration: Claude Settings vs Cursor Integration",
        "text": """Since this is essentially an MCP server setup, all you need to do is copy the configuration string for whichever tool you're using. If you're using Claude, you just go to your settings, head into the developer options, and click edit config. That'll open up the config file. You just paste your details in and you're set.

If you're using Cursor, it's slightly different. Just open settings, go to tool integrations, and hit add MCP. Then paste the config string there. That works perfectly fine if you just want to run some simple workflows in the cloud without hosting anything yourself. But if you want to run it locally on your own system, you'll need to either use Docker or the npx command.""",
        "start_time": 600,
        "end_time": 650,
        "token_count": count_tokens("""Since this is essentially an MCP server setup, all you need to do is copy the configuration string for whichever tool you're using. If you're using Claude, you just go to your settings, head into the developer options, and click edit config. That'll open up the config file. You just paste your details in and you're set.

If you're using Cursor, it's slightly different. Just open settings, go to tool integrations, and hit add MCP. Then paste the config string there. That works perfectly fine if you just want to run some simple workflows in the cloud without hosting anything yourself. But if you want to run it locally on your own system, you'll need to either use Docker or the npx command.""")
    }
    
    # Chunk 13: API Key Setup + Final Configuration Steps
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "API Key Configuration: Local vs Cloud Setup",
        "text": """As for the API key, it works the same for both local and online versions. Like I mentioned earlier, the only difference is the address part. In the online version, the blurred part in the link you see, that's your unique ID, and the rest of the link is standard. That full address is what you'll paste into the config.

To get the API key itself, just go into your settings, look for the API section, and you'll see an option to create a new key. It's the same flow for both versions. Just generate it, copy it, and paste it into your integration settings. That brings us to the end of this video. If you'd like to support the channel and help us keep making videos like this, you can do so by using the super thanks button below.""",
        "start_time": 650,
        "end_time": 700,
        "token_count": count_tokens("""As for the API key, it works the same for both local and online versions. Like I mentioned earlier, the only difference is the address part. In the online version, the blurred part in the link you see, that's your unique ID, and the rest of the link is standard. That full address is what you'll paste into the config.

To get the API key itself, just go into your settings, look for the API section, and you'll see an option to create a new key. It's the same flow for both versions. Just generate it, copy it, and paste it into your integration settings. That brings us to the end of this video. If you'd like to support the channel and help us keep making videos like this, you can do so by using the super thanks button below.""")
    }
    
    chunks.extend([chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, chunk_9, chunk_10, chunk_11, chunk_12, chunk_13])
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Calculate token statistics
    total_tokens = sum(chunk["token_count"] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    # Create the final JSON structure
    result = {
        "video_id": "xf2i6Acs1mI",
        "title": "This n8n mcp is INSANE... Let AI Create your Entire Automation",
        "channel": "AI LABS",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens) if avg_tokens else 0
        }
    }
    
    # Write to JSON file
    output_path = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_ai_labs_n8n_mcp_xf2i6Acs1mI.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} chunks with average {avg_tokens:.0f} tokens per chunk")
    print(f"Total tokens: {total_tokens}")
    print("Manual chunker completed successfully!")
    print("Note: This captures the complete n8n MCP tutorial with architecture breakdown,")
    print("live demonstration, and step-by-step installation instructions.")

if __name__ == "__main__":
    main()