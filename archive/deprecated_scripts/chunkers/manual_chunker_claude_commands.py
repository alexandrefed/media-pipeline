#!/usr/bin/env python3
"""
Manual chunking script for "5 AMAZING Claude Code Commands You MUST Know About"
Video URL: https://www.youtube.com/watch?v=eM_Tg8_BGx4
Channel: All About AI
Duration: 942 seconds (15:42)

Content Structure:
1. /init command - Creating CLAUDE.md files
2. Custom commands - Creating reusable documentation commands
3. Using images in Claude Code
4. -p flag for one-shot mode
5. Extended thinking with "think deeply about"

Chunking Strategy:
- Each major command gets 1-2 chunks
- Introduction and conclusion get separate chunks
- Average chunk size: ~150-200 tokens for command tutorials
"""

import json
from datetime import datetime

def create_manual_chunks():
    """Create high-quality manual chunks for the Claude Code Commands video"""
    
    chunks = []
    
    # Chunk 1: Introduction
    chunks.append({
        "text": """Okay, so today I wanted to kind of go over five different commands probably maybe you haven't used yet in Claude Code that I think is pretty interesting. It could be if you like this. So I'm already a big fan of Claude Code. I use it yeah kind of all the time if I have something I want to do. So yeah, I'm just going to go through some different commands I use to help me save some time sometimes and it could be easier if you wanted to dive deeper into Claude Code to know about this.""",
        "start_time": 0,
        "end_time": 25,
        "topics": ["claude code", "commands", "productivity"],
        "importance": "high",
        "context": "Introduction to 5 useful Claude Code commands"
    })
    
    # Chunk 2: /init Command Introduction
    chunks.append({
        "text": """So the first one we're going to start with is just /init. So this is going to create a CLAUDE.md file. You might have heard about this. So I'm just going to show you kind of a simple example of how we can use this CLAUDE.md file today. And yeah, just going to do something simple and I'm going to show you kind of how this works and how we can use this for our advantage.""",
        "start_time": 26,
        "end_time": 50,
        "topics": ["init command", "CLAUDE.md", "project setup"],
        "importance": "high",
        "context": "Introduction to /init command for creating CLAUDE.md"
    })
    
    # Chunk 3: CLAUDE.md Rules Setup
    chunks.append({
        "text": """So this is the CLAUDE.md file I want to use today. You can see here I kind of prepare this but you can do this manually, right? So do you want to create CLAUDE.md? Yes, I do. And then I'm going to edit it manually. So this is going to be placed here in my folder. Now you can see this in Cursor. So we can go into this. So this is basically rules you can set for your project. So this file provides guidance to Claude Code, right?""",
        "start_time": 51,
        "end_time": 90,
        "topics": ["CLAUDE.md", "project rules", "guidance"],
        "importance": "high",
        "context": "Setting up CLAUDE.md file for project-specific rules"
    })
    
    # Chunk 4: CLAUDE.md Example Rules
    chunks.append({
        "text": """So an example of this could be let's update our CLAUDE.md. So number one, we must always write secure best practice Python code. Two, always write tests for each function we create and execute the tests. Iterate the function based on the test results. Delete test scripts if the test passes. And number four is always commit after each new function is added to our codebase. So this is what we are going to update our CLAUDE.md file with. And hopefully now Claude Code will always follow these simple rules when we actually do some changes to our codebase.""",
        "start_time": 91,
        "end_time": 140,
        "topics": ["CLAUDE.md", "best practices", "automation", "testing"],
        "importance": "high",
        "context": "Example rules for CLAUDE.md: secure code, testing, commits"
    })
    
    # Chunk 5: CLAUDE.md in Action
    chunks.append({
        "text": """So let's do write an email input validator function in cc.py. So we're not going to instruct this to test this now. Write test for it. But this because this should be in our markdown file CLAUDE.md, right? So let's see what happens now if we create a cc.py with an email input validator. Hopefully now it will look in this and create the tests we need. So you can see cc. Okay. So yeah. Perfect. We created the cc.py. So now I want to see if we create a test for this. Yes. test_cc.py. So this is going to import this probably. Yes. Okay. And hopefully we will execute this test. Yes. Okay. So those were okay. Now I want to see if we delete this test remove. Yeah. Okay. So you can see how this follows our CLAUDE.md and this is very helpful sometimes.""",
        "start_time": 141,
        "end_time": 240,
        "topics": ["CLAUDE.md", "testing", "automation", "workflow"],
        "importance": "high",
        "context": "Demonstration of CLAUDE.md rules being automatically followed"
    })
    
    # Chunk 6: Custom Commands Introduction
    chunks.append({
        "text": """So, let's move on to our second command. I sometimes like to use. Another thing we can do is actually create this custom commands. This could be project or global. So, we can create a global one here. So, just to create this file in this Claude commands folder. So, let's just do that. I prepared some of these. So, one I use sometimes is a file called claude-docs.md. So this is kind of a command file that kind of points to where I have stored my Claude documentation. So I kind of can update this. This is some information about yeah how to use the Claude AI API. So this is the file I refer to in Claude Code to kind of look up documentation so I can show you how this works.""",
        "start_time": 241,
        "end_time": 320,
        "topics": ["custom commands", "documentation", "claude-docs"],
        "importance": "high",
        "context": "Creating custom commands for documentation lookup"
    })
    
    # Chunk 7: Custom Commands Usage
    chunks.append({
        "text": """So if you do slash you can see we have these different user commands here. So let's do use let's say we can do user and we can do let's do claude-docs right and I can do a question behind here. Give me a code example of Claude AI API. So this will now look in the file I have pointed to here, right? Hopefully. Yeah, you can see it's going to look in my claude-docs file. So this is kind of pre-arranged. So now it kind of has all the documentation from this MD file here and we should pick up that how to create a call chat or like a client message create call to Claude or Anthropic is this. Right? So now we can bring this into context and it's a very easy way to yeah use documentation you already have stored locally if you wanted to do that.""",
        "start_time": 321,
        "end_time": 400,
        "topics": ["custom commands", "documentation", "API", "context"],
        "importance": "high",
        "context": "Using custom commands to access documentation"
    })
    
    # Chunk 8: Using Images in Claude Code
    chunks.append({
        "text": """But there's also something that is almost as fast if not faster if you're already on the page. So what we can do if you didn't know, we can use images in Claude Code. So let's say yeah, I just wanted to do a quick call to let's say OpenAI. I just need some simple. Yeah, we can do a Python here, right? So I can just screenshot this, right? For some reason I tried to copy this but I couldn't make it work. But we can just save this right into our images. So we can just drag the image in here and explain this and let's see what happens. So you can see this is clearly working.""",
        "start_time": 401,
        "end_time": 480,
        "topics": ["images", "screenshots", "visual input"],
        "importance": "high",
        "context": "Using images/screenshots in Claude Code"
    })
    
    # Chunk 9: -p Flag for One-Shot Mode
    chunks.append({
        "text": """Another simple thing you can do is you don't have to run everything in like an interactive mode here. So we can do one-shot mode by using the -p command and a query for quick commands. So you can see an example here. We can actually do claude -p what does this function do and this would just answer this single command and exit. But we can pipe content into this. So this is like specific context. So you can do cat maybe log.txt and kind of analyze this error. So this will only focus on this one particular file combined with the query.""",
        "start_time": 481,
        "end_time": 560,
        "topics": ["-p flag", "one-shot mode", "piping", "context"],
        "importance": "high",
        "context": "Using -p flag for one-shot commands with specific context"
    })
    
    # Chunk 10: -p Flag Examples
    chunks.append({
        "text": """So I can show you kind of quickly how that works. So if I grab the path to my OpenAI documentation here and if I go back to let's say yeah we can just go back here and what I can do is do cat right do this we can do this and we can do claude -p and then we can do our query what model are we using here. So now we specifically just going to look in this file here, right? You can see we're going to read this file. So this is just if you want to do like one simple command. So it read all of this. And you can see we are looking at the GPT-4.1 model in this case. And we just exit. We don't continue here.""",
        "start_time": 561,
        "end_time": 640,
        "topics": ["-p flag", "file context", "one-shot queries"],
        "importance": "medium",
        "context": "Practical example of using -p flag with cat command"
    })
    
    # Chunk 11: Output Format with -p
    chunks.append({
        "text": """Another thing we can do is just do claude -p and do let's say create a list of my currency rates dataset. So this could be 10 and we do --output-format and we set our format. This could be JSON. So this if we run this now this is probably just going to look up to create this dataset here and the output format we specified you can see here is going to be JSON currency.json and we have 10 different currencies. Yes. I want to create that and this is something you can always do just do this output format command here to get yeah kind of the format you want.""",
        "start_time": 641,
        "end_time": 720,
        "topics": ["output format", "-p flag", "JSON", "data generation"],
        "importance": "medium",
        "context": "Using --output-format flag with -p command"
    })
    
    # Chunk 12: Extended Thinking Introduction
    chunks.append({
        "text": """The final thing I wanted to look at is extended thinking. So this is me it's not specified in Claude Code but they recommend that you can use the kind of the prompt think about or think harder about. So you kind of just have to specify this and you can ask kind of Claude think deeply about. I think we're going to try think deeply about so let's try to do that and see what kind of changes if we use that command in Claude Code. So let's try think deeply about a step-by-step plan to calculate arbitrage trading from our currency rates.json dataset.""",
        "start_time": 721,
        "end_time": 800,
        "topics": ["extended thinking", "think deeply", "planning"],
        "importance": "high",
        "context": "Introduction to extended thinking with 'think deeply about'"
    })
    
    # Chunk 13: Extended Thinking Results
    chunks.append({
        "text": """So let's see what happens now if we do this think deeply command we probably won't see the thinking tokens but maybe we use more time but let's see now. Okay so I'll create a plan and thinking so this is what I wanted to see. So if you didn't know about this this is something you can try out. So just use kind of the think deeply about and we will get this thinking tokens here. So yeah I've tested this out and kind of doing like an initial plan. This could be good for this but let's let this run out. You can see we're going to implement the Bellman-Ford algorithm to detect negative cycles, calculate potential profit, calculate functions.""",
        "start_time": 801,
        "end_time": 880,
        "topics": ["extended thinking", "thinking tokens", "algorithms"],
        "importance": "high",
        "context": "Extended thinking generates detailed plans and algorithms"
    })
    
    # Chunk 14: Conclusion
    chunks.append({
        "text": """And basically, that's what I wanted to cover today. I just wanted to go over Claude Code and do maybe some things that could gave you some inspiration how you can use this. Like I said, I don't use all this all the time, but I really like to use the CLAUDE.md if I'm going to I'm know I'm going to work in a project. So, it can kind of follow my rules. So, I don't kind of save some input tokens on that. And, -p just to save some tokens on kind of looking into one specific file, you know, about is also something I like. Images is always good. So yeah, hope you learned something, gave you some ideas, some inspiration, and I'll see you in the next one!""",
        "start_time": 881,
        "end_time": 942,
        "topics": ["summary", "claude code", "productivity tips"],
        "importance": "medium",
        "context": "Summary of the 5 Claude Code commands covered"
    })
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Add metadata to each chunk
    video_metadata = {
        "video_id": "eM_Tg8_BGx4",
        "video_title": "5 AMAZING Claude Code Commands You MUST Know About",
        "video_channel": "All About AI",
        "video_url": "https://www.youtube.com/watch?v=eM_Tg8_BGx4",
        "video_duration": 942,
        "processing_date": datetime.now().isoformat(),
        "processing_method": "manual_claude_commands",
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
        "video_id": "eM_Tg8_BGx4",
        "video_title": "5 AMAZING Claude Code Commands You MUST Know About", 
        "video_url": "https://www.youtube.com/watch?v=eM_Tg8_BGx4",
        "processing_date": datetime.now().isoformat(),
        "processing_method": "manual_claude_commands",
        "chunk_count": len(chunks),
        "chunks": chunks
    }
    
    with open('manual_chunks_claude_commands.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} manual chunks for Claude Code Commands video")
    print(f"Total tokens: ~{total_tokens}")
    print(f"Average tokens per chunk: ~{total_tokens // len(chunks)}")
    print(f"Saved to: manual_chunks_claude_commands.json")

if __name__ == "__main__":
    main()