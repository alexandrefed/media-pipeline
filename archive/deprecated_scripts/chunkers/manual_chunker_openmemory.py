#!/usr/bin/env python3
"""
Manual chunking script for "All My AI Apps Are Connected to One MIND — With Open Memory"
Video URL: https://www.youtube.com/watch?v=Y2XI2nk44WE
Channel: AI LABS
Duration: 635 seconds (10:35)

Content Structure:
1. Problem statement - No shared context between AI tools
2. Introduction to OpenMemory MCP
3. Installation and setup guide
4. Configuration for Claude and Cursor
5. Demo - Time tracking app with shared memory
6. Limitations and issues discovered

Chunking Strategy:
- Setup instructions get detailed chunks
- Demo sections get narrative chunks
- Average chunk size: ~150-200 tokens for tutorial content
"""

import json
from datetime import datetime

def create_manual_chunks():
    """Create high-quality manual chunks for the OpenMemory MCP video"""
    
    chunks = []
    
    # Chunk 1: Problem Statement
    chunks.append({
        "text": """Many of you brainstorm inside Claude Desktop because it is pretty good. It writes clearly and gives you a solid plan. What I usually do is take that plan and go back and forth between different tools. But then this problem comes up. They do not have any shared context. For example, if you are working on a single project and make a change in one place, then go to another tool and ask something that depends on that change. It just does not know. There is no awareness of what happened elsewhere. No shared memory. But what if I told you that all these clients, especially MCP clients, could have one shared memory block? That is what I am going to show you today.""",
        "start_time": 0,
        "end_time": 45,
        "topics": ["shared context", "AI tools", "memory", "MCP"],
        "importance": "high",
        "context": "Problem: No shared context between AI tools"
    })
    
    # Chunk 2: OpenMemory Introduction
    chunks.append({
        "text": """You've probably heard about Mem0, which was a memory layer for AI agents, and it turned out to be really impressive. It was featured on many channels, and a lot of people praised how powerful it made their agents. Now, they've released a pretty cool tool called OpenMemory. It basically gives you a single memory, which you can think of as a memory chip that works across all your MCP clients. It connects all your memory clients together into one continuous memory space. Right now you can use it locally and it's also designed for cloud use which means you will not need to install anything. Your memories will be stored on the cloud if you choose although both options are fully supported.""",
        "start_time": 46,
        "end_time": 90,
        "topics": ["OpenMemory", "Mem0", "shared memory", "MCP"],
        "importance": "high",
        "context": "Introduction to OpenMemory MCP"
    })
    
    # Chunk 3: Installation Setup
    chunks.append({
        "text": """So this is the OpenMemory GitHub folder and you can see that OpenMemory is actually inside mem because mem is the main repository. In order to get OpenMemory we're going to have to clone the entire mem repository. What you're going to do is go back to the Mem0 repository, get the link, copy it, then open your terminal and type git clone followed by the GitHub repository link. Once that's done, you'll go inside that repository and inside the mem folder, you're going to find the OpenMemory folder. You'll then navigate into that and all further commands will happen from there.""",
        "start_time": 91,
        "end_time": 140,
        "topics": ["installation", "GitHub", "setup", "OpenMemory"],
        "importance": "high",
        "context": "Cloning and navigating to OpenMemory"
    })
    
    # Chunk 4: Docker Setup
    chunks.append({
        "text": """If you scroll down, you'll see that to quick start, you need to run these commands which are basically make files that set up the dependencies. You'll need to run the UI and the MCP server. First things first, Docker needs to be up and running on your system because it downloads and sets up Docker containers along with the dependencies. To do this, just run the make build command which installs those containers. After that, run make up which starts the containers. Keep in mind that you only need to run make build once to build the containers. Later, when you want to use it again, just run make up.""",
        "start_time": 141,
        "end_time": 200,
        "topics": ["Docker", "setup", "make commands", "containers"],
        "importance": "high",
        "context": "Docker setup and make commands"
    })
    
    # Chunk 5: OpenAI API Key Configuration
    chunks.append({
        "text": """One more thing I forgot to mention. You need to open this directory in Cursor. Once you open it, it'll look something like this. And the file structure will appear like this. Inside the file structure, go to the API folder. In there, you'll find a .env.example file. You need to paste your OpenAI API key into this file. Copy it. Rename it to .env by removing the word example from the file name and then paste your actual API key into it. Once that's done, you'll be able to use the make up command. They've listed this step as a prerequisite because it's required for LLM interactions which is why they ask for the OpenAI API key.""",
        "start_time": 201,
        "end_time": 260,
        "topics": ["API key", "OpenAI", "configuration", "env file"],
        "importance": "high",
        "context": "Setting up OpenAI API key"
    })
    
    # Chunk 6: MCP Client Configuration
    chunks.append({
        "text": """Okay, you can see that now that the app is open again, we need to install the MCP for different tools. We have the MCP link which you have to manually configure in the settings. The MCP configuration lets you accept it manually or what I really like is the set of pre-built commands they provide. For example, if I write a command, you'll see the one they've given. When you run it, it automatically adds the MCP to the Claude client for you. The same applies to Cursor. I'll just set it for Claude or whatever you want to use and it handles it for you.""",
        "start_time": 261,
        "end_time": 310,
        "topics": ["MCP configuration", "Claude", "Cursor", "setup"],
        "importance": "high",
        "context": "Configuring MCP for different tools"
    })
    
    # Chunk 7: Features Overview
    chunks.append({
        "text": """Let's look at what the OpenMemory MCP has to offer. On the website, they've listed a lot of features and we can see them right here. For example, you can personalize your interactions with your preferences saved in memory. Then there are supported clients besides the ones shown. Others can be added too. You also get full memory control including the ability to define retention and even pause memories if you want. As I told you, if you want to use it with the cloud platform, you should go ahead and sign up for the waitlist.""",
        "start_time": 311,
        "end_time": 360,
        "topics": ["features", "memory control", "personalization", "cloud"],
        "importance": "medium",
        "context": "OpenMemory features overview"
    })
    
    # Chunk 8: Time Tracking App Demo Start
    chunks.append({
        "text": """This is an example of how you can actually use the MCP server. What I did was open Claude Desktop and asked it to brainstorm an idea for a time tracking app. First, it gave me its own plan. Then, I added my follow-up points, things I thought should be implemented. After it integrated my changes into the original plan, I asked it to add the plan to memory as time track plan. I didn't know exactly how that worked at first, but it turns out you can't add full plans directly to memory. What actually happens is, it takes the whole text as input. And remember, we input the OpenAI key earlier. That's used to break the input down into smaller tasks automatically.""",
        "start_time": 361,
        "end_time": 420,
        "topics": ["demo", "time tracking app", "Claude Desktop", "memory"],
        "importance": "high",
        "context": "Demo: Creating time tracking app with shared memory"
    })
    
    # Chunk 9: Memory Chunking and Grouping
    chunks.append({
        "text": """For example, I opened this plan here. And although other tasks had also been added, I think about 10 tasks were extracted from this single plan. You can see it's broken into different plans and categories. Now, you might be thinking all these plans are scattered. But don't worry, I'll explain later how they've actually grouped the prompts. I didn't notice it at first either, but eventually I saw that they were being grouped together. I actually figured out the method they used and I'll explain that part soon.""",
        "start_time": 421,
        "end_time": 470,
        "topics": ["memory chunking", "task extraction", "grouping"],
        "importance": "medium",
        "context": "How OpenMemory chunks and groups information"
    })
    
    # Chunk 10: Cross-Tool Memory Access
    chunks.append({
        "text": """Moving on to Cursor. I gave it a prompt saying I want to build a time track app and asked if it could pull the details from memory. It then used the MCP tools to list and search the memory. This part is really useful. It searches relevant information. So when it queried about the time track app, it retrieved memories related to that. From there, it pulled details about Next.js, React, TypeScript, and the rest of the stack we'd be using. It started building. After it finished, I asked it to save its progress to memory and it did.""",
        "start_time": 471,
        "end_time": 520,
        "topics": ["Cursor", "memory retrieval", "cross-tool", "tech stack"],
        "importance": "high",
        "context": "Accessing shared memory from Cursor"
    })
    
    # Chunk 11: Memory Retrieval Mechanism
    chunks.append({
        "text": """Now what I want to show you is how it actually retrieves the memories. Before that you can also see the source app for each memory like some were created by Cursor others by Claude. If we open up memory you can see the access log. You can change the status or even edit the memory itself. But the main thing I want to show is this. This memory is linked to all the other memories created in the same session. So if the MCP client requests one memory labeled time, it also fetches related memories. That's how they're grouped. I figured this out while checking the search calls.""",
        "start_time": 521,
        "end_time": 570,
        "topics": ["memory retrieval", "grouping", "session linking"],
        "importance": "high",
        "context": "How memory retrieval and grouping works"
    })
    
    # Chunk 12: Limitations and Issues
    chunks.append({
        "text": """Now, this is a problem that could really hurt when you're building multiple projects with this memory layer. For example, even if you're not using the same tech stack, let's say you build a to-do app, then later want to build another one or any project with the same name, there's no clear way to separate those memories. At some point, one memory will cross into another and that can break your whole project. That's one thing I feel should be added to this system. But overall, it's a really strong start, and I really love the direction it's going in. It works great if you're doing single projects or projects with very different names.""",
        "start_time": 571,
        "end_time": 635,
        "topics": ["limitations", "project separation", "memory conflicts"],
        "importance": "high",
        "context": "Limitations: Memory conflicts between similar projects"
    })
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Add metadata to each chunk
    video_metadata = {
        "video_id": "Y2XI2nk44WE",
        "video_title": "All My AI Apps Are Connected to One MIND — With Open Memory",
        "video_channel": "AI LABS",
        "video_url": "https://www.youtube.com/watch?v=Y2XI2nk44WE",
        "video_duration": 635,
        "processing_date": datetime.now().isoformat(),
        "processing_method": "manual_openmemory",
        "has_timestamps": True,
        "has_topics": True,
        "manually_reviewed": True
    }
    
    # Calculate token counts and add metadata to each chunk
    total_tokens = 0
    for i, chunk in enumerate(chunks):
        # Rough estimate: 1 token per 4 characters
        chunk['token_count'] = len(chunk['text']) // 4
        total_tokens += chunk['token_count']
        
        # Add metadata to each chunk
        chunk.update(video_metadata)
        chunk['chunk_index'] = i
        chunk['total_chunks'] = len(chunks)
    
    # Create output data in expected format
    output_data = {
        "video_id": "Y2XI2nk44WE",
        "video_title": "All My AI Apps Are Connected to One MIND — With Open Memory", 
        "video_url": "https://www.youtube.com/watch?v=Y2XI2nk44WE",
        "processing_date": datetime.now().isoformat(),
        "processing_method": "manual_openmemory",
        "chunk_count": len(chunks),
        "chunks": chunks
    }
    
    with open('manual_chunks_openmemory.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} manual chunks for OpenMemory video")
    print(f"Total tokens: ~{total_tokens}")
    print(f"Average tokens per chunk: ~{total_tokens // len(chunks)}")
    print(f"Saved to: manual_chunks_openmemory.json")

if __name__ == "__main__":
    main()