#!/usr/bin/env python3
"""
Manual chunking script for "Agentic Claude Code: 3 Codebase Folders for TOP 1% AI Coding"
Video URL: https://www.youtube.com/watch?v=hGg3nWp7afg
Channel: IndyDevDan
Duration: 1471 seconds (24:31)

Content Structure:
1. Introduction - Context is King
2. AI docs folder - Persistent knowledge base
3. Specs folder - Plans and specifications
4. .claude folder - Reusable prompts
5. Live demo - Pocket Pick feature implementation

Chunking Strategy:
- Each major folder gets 2-3 chunks
- Demo section gets 3-4 chunks
- Average chunk size: ~200-250 tokens for technical content
"""

import json
from datetime import datetime

def create_manual_chunks():
    """Create high-quality manual chunks for the 3 Folders video"""
    
    chunks = []
    
    # Chunk 1: Introduction and Context is King
    chunks.append({
        "text": """What's up engineers? IndyDevDan here. Imagine opening your codebase and having your AI coding tool instantly understand your codebase better and faster than you can read the readme. There are three simple folders that can unlock that superpower for you in every project you touch. We're going to break them down into their atoms so you can use them to increase your compute advantage. The AI coding tool you use does not change this one critical fact of engineering in the generative AI age. Doesn't matter if you're a Cursor fan, Windsurf, Aider, Codex, or even Claude Code. You already know what this idea is. Context is everything. Context is king. If your agent can't see critical information, it simply cannot build what you need. That's what these three essential directories solve comprehensively and systematically.""",
        "start_time": 0,
        "end_time": 60,
        "topics": ["context", "AI coding tools", "codebase organization"],
        "importance": "high",
        "context": "Introduction to 3 essential folders for AI coding"
    })
    
    # Chunk 2: AI docs Introduction
    chunks.append({
        "text": """Let's start with the foundation: AI docs. Think of this as your AI coding tool's persistent memory, a knowledge repository your AI tools can instantly access. Inside of the Claude Code's programmable codebase - a big idea we discussed in last week's video - you can see we have an AI docs directory. Inside of this directory, we have two markdown files: Claude Code best practices and OpenAI's agent SDK. I can now boot up any agent and have them quickly read these files. They can then turn around to get work done quickly.""",
        "start_time": 61,
        "end_time": 120,
        "topics": ["AI docs", "persistent memory", "documentation"],
        "importance": "high",
        "context": "Introduction to AI docs folder"
    })
    
    # Chunk 3: AI docs Contents
    chunks.append({
        "text": """So what goes inside of AI docs? Here you have third-party API documentation, integration details, you have custom patterns and conventions, any implementation notes, anything specific to your codebase, it all goes in AI docs. I mostly use this for third-party documentation so that I can quickly ramp up my codebases over and over and over. The AI docs directory is persistent.""",
        "start_time": 121,
        "end_time": 180,
        "topics": ["AI docs", "documentation", "third-party APIs"],
        "importance": "high",
        "context": "What to put in AI docs folder"
    })
    
    # Chunk 4: Specs Directory Introduction
    chunks.append({
        "text": """So, we of course have the specs directory. What goes in the specs directory? Specs is short for specification, which also just means plan. You might know these as PRDs, product documents, whatever you want to call them. These are the new units of getting massive amounts of work done with your AI coding tools. And now with your agentic coding tools, we can now use multiple tools inside of single prompts with powerful agentic coding tools like Claude Code, Cursor, Aider, so on and so forth.""",
        "start_time": 181,
        "end_time": 240,
        "topics": ["specs", "specifications", "PRDs", "planning"],
        "importance": "high",
        "context": "Introduction to specs folder"
    })
    
    # Chunk 5: Specs Directory Importance
    chunks.append({
        "text": """The specs directory is the most important folder in your entire codebase. This is where we write great plans. This is where we scale up our compute and do more work than ever in single massive swings. This 1,000 token prompt expanded into an entire codebase. This is due to the fact that we are agentic coding, right? We can write self-validating loops inside of our prompt. Remember, agentic coding is a superset of AI coding, a massive superset. And great tools like Claude Code allow us to take all of our plans from all of our repositories from the specs directory and blow them out into full-on codebases and features.""",
        "start_time": 241,
        "end_time": 320,
        "topics": ["specs", "agentic coding", "planning", "self-validation"],
        "importance": "high",
        "context": "Why specs directory is most important"
    })
    
    # Chunk 6: Planning Philosophy
    chunks.append({
        "text": """This is why you should always have a specs directory that details the plan for all the work that you're going to hand off to your powerful agentic coding tools. If you're still iteratively prompting back and forth and back and forth and back and forth, I can guarantee you, you are wasting time and you're not scaling your compute as much as you could be. Sit down, take your time, think, plan, and then build. The key idea here is very simple. Every principled AI coding member knows this and everyone that's been following this channel knows this as well. The plan is the prompt and great planning is great prompting.""",
        "start_time": 321,
        "end_time": 400,
        "topics": ["planning", "prompting", "efficiency", "specs"],
        "importance": "high",
        "context": "Philosophy of planning over iterative prompting"
    })
    
    # Chunk 7: .claude Directory Introduction
    chunks.append({
        "text": """So every codebase I build now has the AI docs directory, the specs directory for plans and .claude. Now .claude is a new emerging directory. To be super clear, this is specific to Claude Code, but what you write in these directories is not specific to Claude Code. If we go to the just prompt codebase, open up .claude and go into the commands directory, you can see we have several different commands. So what are these and how are they useful for scaling our engineering work? These are nothing but prompts. If we open up Claude Code here in the just prompt codebase and we type slash, you can see the names of all these commands right at the top here. These are reusable runnable prompts that we can use across sessions.""",
        "start_time": 401,
        "end_time": 480,
        "topics": [".claude", "commands", "reusable prompts"],
        "importance": "high",
        "context": "Introduction to .claude directory"
    })
    
    # Chunk 8: Context Priming
    chunks.append({
        "text": """The most important reusable prompt that I recommend you set up inside of all your codebases is the context priming prompt. This is where you prompt Claude Code, Codex, Cursor, whatever tool you're using. This is not Claude Code specific, right? The names of these directories can really be anything. So if you were to prime our just prompt server here, we'll do the basic context prime. It's going to run through these commands, right? Using tool calls, it's going to read the readme, then run git ls-files to understand the context of this project. So, I recommend you set this up in every codebase so that you can quickly operate on the files and the ideas that matter.""",
        "start_time": 481,
        "end_time": 560,
        "topics": ["context priming", ".claude", "setup"],
        "importance": "high",
        "context": "Context priming as most important reusable prompt"
    })
    
    # Chunk 9: Context Windows and Resets
    chunks.append({
        "text": """What is the big idea of what we're doing here? We're making it easy to set up new instances of our agentic tooling over time. And by over time, I mean on the day-to-day basis, but also on a session to session basis. If you've used Claude Code or Codex or any one of your AI coding tools, they will run out of context. You can see the current context windows of the state-of-the-art models. A lot of these are limited to 200K or 1 million tokens. When using your AI coding tools, you'll eventually run out of context and then you'll have to reset. So this is what the context prime does and this is what the .claude commands directory gives you specifically for Claude Code, but you can deploy this across any AI coding tool.""",
        "start_time": 561,
        "end_time": 640,
        "topics": ["context windows", "resets", "context priming"],
        "importance": "high",
        "context": "Why context priming matters for long sessions"
    })
    
    # Chunk 10: Advanced Prompts
    chunks.append({
        "text": """These directories are not limited to context priming. We built out an ultra diff review where we created a diff and then we had multiple language models review the diff and offer feedback. This is something we're going to be talking about a lot on the channel. The capabilities of your prompts are now unlimited thanks to agentic coding tools. You can run any tool. You can run custom MCP servers like we have here. You can do a tremendous amount by having reusable prompts inside your codebase.""",
        "start_time": 641,
        "end_time": 700,
        "topics": ["advanced prompts", "diff review", "MCP servers"],
        "importance": "medium",
        "context": "Advanced uses of reusable prompts"
    })
    
    # Chunk 11: Three Directories Summary
    chunks.append({
        "text": """So these are the three essential directories I have in every single one of my codebases. Now AI docs is the persistent knowledge base for your AI coding tools. Specs is where you define your plans. It's where you define all the work you want done so that you can hand it off to your AI coding tool and to your agentic coding tools. And then we have the .claude. Again, you can name these whatever you want. This is where you place your reusable prompts that you want at the ready inside of your agentic coding tool. Reusable prompts are an essential pattern even outside of coding. You want to be able to use compute over and over in different shapes and forms.""",
        "start_time": 701,
        "end_time": 780,
        "topics": ["summary", "three folders", "AI docs", "specs", ".claude"],
        "importance": "high",
        "context": "Summary of the three essential directories"
    })
    
    # Chunk 12: Pocket Pick Demo Introduction
    chunks.append({
        "text": """What does this look like in action? Let's go ahead and build out a simple, concise, brand new feature inside of Pocket Pick. There's a tweak that I've been wanting to make. Let me go ahead and open this up for you and just briefly explain. Pocket Pick. As engineers, we reuse ideas, patterns, and code snippets all the time, but keeping track of these can be hard. Pocket Pick is the solution to that problem. This simplistic MCP server creates and stores all of your personal knowledge-based items, right? any code snippets, files, documentation that you want to reuse inside of a simple SQLite database.""",
        "start_time": 781,
        "end_time": 840,
        "topics": ["Pocket Pick", "demo", "MCP server", "knowledge base"],
        "importance": "high",
        "context": "Introduction to Pocket Pick demo"
    })
    
    # Chunk 13: Feature Planning
    chunks.append({
        "text": """The key change we want to make today is updating the add command. If we look at the data types here to add new items to the pocket pick database, we have text, tags, and database path. Right now, the ID is automatically generated. I want to improve the searching capabilities so that we can pass in IDs when we're creating pocket items with pocket add and pocket add file. This just makes it super easy to run pocket get and pocket get file by ID. How are we going to do that? We're going to use these three essential directories.""",
        "start_time": 841,
        "end_time": 900,
        "topics": ["feature planning", "Pocket Pick", "IDs"],
        "importance": "high",
        "context": "Planning the ID feature for Pocket Pick"
    })
    
    # Chunk 14: Plan Drafting Technique
    chunks.append({
        "text": """How do we do real work? We don't iteratively prompt. That's the old 2024 way of doing things. We create concise, agentic plans. We're going to take this a step further with an emerging technique I like to call plan drafting. The big difference here is that both myself and my AI coding tool are going to be part of drafting this plan. So instead of writing the plan myself, creating the file myself, doing any of that work, I'm going to have Claude Code create the first draft of this plan. What I'm doing here is having Claude Code draft the first draft of this plan. I've briefly looked at this codebase. I roughly remember the architecture and how it works. But our agentic coding tools can quite literally read hundreds of times faster than we can.""",
        "start_time": 901,
        "end_time": 1000,
        "topics": ["plan drafting", "agentic planning", "collaboration"],
        "importance": "high",
        "context": "Plan drafting technique introduction"
    })
    
    # Chunk 15: Plan Review and Execution
    chunks.append({
        "text": """So now we're reviewing, right? We're moving more and more every single day into a code reviewer, into a plan reviewer. We're becoming curators of information, right? Curators of code ideas, and then we're handing them off to our AI coding tools. And you know the great part about this is that we're not iteratively updating our codebase, putting it into bad temporary states. We're operating solely in this file. I'm going to go ahead and say implement this file. Okay, that's it. Claude Code has this new feature. It's got a to-do list system. This is a new emerging pattern inside of agentic coding tools where you effectively create a plan first and then you work through the plan.""",
        "start_time": 1001,
        "end_time": 1100,
        "topics": ["plan review", "curation", "implementation"],
        "importance": "high",
        "context": "Reviewing and executing the plan"
    })
    
    # Chunk 16: Self-Validation and Testing
    chunks.append({
        "text": """The most important thing here, we have self-validation on. So I can pretty much be guaranteed. I can be assured that everything here works, right? All the tests passed. Our agentic coding tool is testing itself. Just to highlight it again, this is the big difference between agentic coding and AI coding. I'm not just writing prompts that generate code. Okay? I'm writing prompts that do engineering work. That's building. That's planning. That's testing. Okay? It's the whole development life cycle. This is the power. This is the capability you can unlock.""",
        "start_time": 1101,
        "end_time": 1200,
        "topics": ["self-validation", "testing", "agentic coding"],
        "importance": "high",
        "context": "Self-validation as key differentiator"
    })
    
    # Chunk 17: Demo Results
    chunks.append({
        "text": """So, it's pretty incredible how quickly we were able to build that out here. Look at all the files that were just changed. And remember what was done. All these changes, right? Very precise, very surgical. And it's all because of these essential files, right? These essential directories that let us scale what we can do inside of this codebase and every codebase. I hope it's becoming clear as we spend more time together, as you watch the channel. It's really about the patterns. It's about the principles. It's about how you approach this new age of engineering.""",
        "start_time": 1201,
        "end_time": 1300,
        "topics": ["demo results", "patterns", "principles"],
        "importance": "medium",
        "context": "Results of the Pocket Pick implementation"
    })
    
    # Chunk 18: Final Summary
    chunks.append({
        "text": """AI docs is your persistent knowledge base for your AI tooling. Specs is where you plan your work. It's where you hand off more and more work to your compute to your agentic coding tool. Remember, great planning is great prompting. And then we have .claude. This is where we build reusable prompts we use across time in our codebase. The most important prompt here to set up is the context prime prompt. Set up your agents so that they have the essential information to work concisely. Don't waste tokens giving them access to your entire codebase. Be precise. Be focused. Having too much context is just as bad as not having enough. Having too much context can confuse your agent. Having too little won't let them get the job done. Put these together and you can scale your engineering work further beyond.""",
        "start_time": 1301,
        "end_time": 1471,
        "topics": ["summary", "best practices", "AI docs", "specs", ".claude"],
        "importance": "high",
        "context": "Final summary and best practices"
    })
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Add metadata to each chunk
    video_metadata = {
        "video_id": "hGg3nWp7afg",
        "video_title": "Agentic Claude Code: 3 Codebase Folders for TOP 1% AI Coding",
        "video_channel": "IndyDevDan",
        "video_url": "https://www.youtube.com/watch?v=hGg3nWp7afg",
        "video_duration": 1471,
        "processing_date": datetime.now().isoformat(),
        "processing_method": "manual_3_folders",
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
        "video_id": "hGg3nWp7afg",
        "video_title": "Agentic Claude Code: 3 Codebase Folders for TOP 1% AI Coding", 
        "video_url": "https://www.youtube.com/watch?v=hGg3nWp7afg",
        "processing_date": datetime.now().isoformat(),
        "processing_method": "manual_3_folders",
        "chunk_count": len(chunks),
        "chunks": chunks
    }
    
    with open('manual_chunks_3_folders.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} manual chunks for 3 Folders video")
    print(f"Total tokens: ~{total_tokens}")
    print(f"Average tokens per chunk: ~{total_tokens // len(chunks)}")
    print(f"Saved to: manual_chunks_3_folders.json")

if __name__ == "__main__":
    main()