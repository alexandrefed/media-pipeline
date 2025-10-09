#!/usr/bin/env python3
"""Manual chunking for IndyDevDan's Programmable Agentic Coding video."""

import json
from pathlib import Path
import tiktoken

def count_tokens(text: str) -> int:
    """Count tokens in text."""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def create_manual_chunks():
    """Create manual chunks for the programmable agentic coding video."""
    
    chunks = []
    
    # Chunk 0: Introduction and the Next Level Feature
    chunks.append({
        "chunk_index": 0,
        "start_time": 0,
        "end_time": 60,
        "chapter_title": "The Next Level Feature: Programmable Agentic Coding",
        "text": "There's a next level feature inside of Claude Code that once you truly see it's impossible to unsee. Once you see this feature, you'll understand that AI coding is not enough. This feature lets you build in ways engineers using Cursor, Windsurf and other easy mode vibe coding tools simply cannot. Now, don't worry. If you're using one of these tools, you can still tap in to this capability. Every single thing we do now is about scaling our impact by scaling our compute usage. If you understand this one idea, you are setting yourself up to win in the generative AI age. I've been shipping software for over a decade. And every couple of years, there's a tool with a feature that transforms what you can do. This is one of them. In this video, I'm going to share this feature with you. We'll then break down the key difference between AI coding and agentic coding so you can truly understand the impact that you can have with agentic coding. Then we'll look at three concrete ways you can take advantage of this capability for your engineering work. Let's talk about programmable agentic coding for next."
    })
    
    # Chunk 1: Claude Code is Programmable
    chunks.append({
        "chunk_index": 1,
        "start_time": 60,
        "end_time": 120,
        "chapter_title": "Claude Code is Programmable: The Single Line Revolution",
        "text": "What's better than an agentic coding tool? An agentic coding tool that you can embed inside your tools, work, and projects. Claude Code is programmable. What does that mean? Here's exactly what that looks like in a single line of code. claude -p, whatever your prompt is, and then you specify your allowed tools. Why is this so important? If you're a Principal AI Coding member, you know that you can do this with Aider. You've seen this already. Here's the exact same version inside of Aider. We use aider-message. We pass in the prompt and then we specify the exact file we want changed. Big whoop. Who cares? Not so fast. The difference between these two examples is monumental."
    })
    
    # Chunk 2: AI Coding vs Agentic Coding
    chunks.append({
        "chunk_index": 2,
        "start_time": 120,
        "end_time": 180,
        "chapter_title": "Understanding the Difference: AI Coding vs Agentic Coding",
        "text": "So, what's the difference? To understand why this is so different, we must understand the difference between AI coding and agentic coding. These are two different animals. What's the difference? With AI coding, you're effectively using a single tool call where the tool is a function where you pass in the big three context, model, and prompt. And the side effect is your code being written by your AI coding tool. We're all very familiar with this idea. We're all very familiar with this concept. Agentic coding takes that a step further. Agentic coding has of course that AI coding tool, but you also have access to any tool you can think of. But not all tools are created equally. There are some that are exponentially more important."
    })
    
    # Chunk 3: Claude Code's 11 Essential Tools
    chunks.append({
        "chunk_index": 3,
        "start_time": 180,
        "end_time": 270,
        "chapter_title": "Claude Code's 11 Essential Tools vs Traditional AI Coding",
        "text": "We can see this by looking at the default tools inside of Claude Code. Here's a list, the current list of every single essential baked in tool that ships with Claude Code. You can see we have 11 tools versus traditional AI coding tool just has the one. With tool 8 and 9, edit and write, we already cover everything an AI coding tool can do with Claude Code. Once we cover edit and write, you can look at agentic coding as a superset of AI coding, a much larger superset. All right. So with the edit and the write tool, we can write code with AI. Now that's just the beginning. With Glob, Grep, LS and Read, our agentic coding tool can now act as we would inside of the codebase looking for important information to help us write the change. Now, as we know, there are costs associated with using these tools. Claude 3.7 Sonnet is priced at $3 per million input and $15 per million output tokens. All the searching you do stacks up. This is the biggest problem with Claude Code right now. This is the price we pay for state-of-the-art agentic coding."
    })
    
    # Chunk 4: The Game-Breaking Bash Tool
    chunks.append({
        "chunk_index": 4,
        "start_time": 270,
        "end_time": 360,
        "chapter_title": "The Game-Breaking Bash Tool and Task Parallelization",
        "text": "And then we have the game-breaking bash tool. This is where agentic coding really takes off. With just the bash tool, your AI coding tool can now act like you would inside the terminal. It can call any bash command that you could. This tool and frankly many of these tools scale directly with the intelligence of the model. With just these tools, we have a brand new tool to wield and get tons of engineering work done. But the cracked Claude Code team at Anthropic has gone even further. They added Task which lets you run tools in parallel to save time and task. Now, this is where we get into incredible agentic behavior where the agent itself can launch a sub agent to perform a slew of tasks. This is an extremely powerful capability and the state of AI coding. We talk about this a little bit as a key property of agents. Powerful agents of the future will be self-organizing and self-replicating. This tool paints a picture of what that will look like."
    })
    
    # Chunk 5: MCP Servers and Infinite Programmability
    chunks.append({
        "chunk_index": 5,
        "start_time": 360,
        "end_time": 450,
        "chapter_title": "MCP Servers: Building Any Tool You Can Imagine",
        "text": "So this is just the baked-in feature set from Claude Code. As you know, Claude Code lets you tap in to MCP servers. This means that you can not only use existing tools, but you can build out any tool set you can imagine. MCP servers allow you to create tools for everything. And this is why effective tool calling with a smart model is so critically important. It lets you scale your compute and step outside the simple bounds of AI coding. This is the big difference between AI coding and agentic coding. Agentic coding puts together three essential ideas: a model capable of calling the right tools, arbitrary tool calling from baked-in tools to tools you create via MCP servers, and then finally the right agent architecture that lets the agent be more autonomous and get work done on its own. To be super super clear, Claude Code is an AI agent. When you put this all together and you're able to program this, you get a tool that is infinitely programmable. Claude Code is infinitely programmable. What does that mean? What does that allow us to do?"
    })
    
    # Chunk 6: Simple UV Script Example
    chunks.append({
        "chunk_index": 6,
        "start_time": 450,
        "end_time": 540,
        "chapter_title": "10-Line Python Script: Engineering Beyond Code Writing",
        "text": "Here's a simple UV single file script with 10 lines of Python where we can see this in action. We're not just writing code anymore. AI coding is not enough. Engineering is a lot more than just writing code. We need to be able to call arbitrary tools in many, many, many different workflows to get real engineering work done. Let's look at this simple to-do. Here's a prompt: Git checkout a new branch. Create todo.ts. Then commit your changes. We have at least three tool calls happening here that we're handing off to Claude Code. You can see the list of allowed tools we're passing in. Edit, bash, create, and then we're kicking off the subprocess. We're going to run this in a moment. I'm going to show you exactly what this looks like with the three essential examples that you can use to get ramped up with this incredible capability."
    })
    
    # Chunk 7: Building Reusable Workflows
    chunks.append({
        "chunk_index": 7,
        "start_time": 540,
        "end_time": 630,
        "chapter_title": "Infinitely Programmable: Building Reusable Workflows",
        "text": "Claude Code is infinitely programmable. This means we can build reusable workflows. Principal AI Coding members know exactly what this is. You're already aware of this capability. Inside of Principal AI Coding, we use Aider to really showcase what this looks like. Claude Code takes this to the next level with arbitrary tool calling in natural language. Speaking of, we can call any tool and many tools in natural language in any sequence that our work requires. This is part of why Claude Code is so incredible. The Claude Code team has built out the tool that you need to get real engineering work done. Huge shout out to Anthropic. They are actually building with this stuff. They know what's going on unlike the insanely weirdly rushed responsive Codex release from OpenAI. Check out the previous video to see my thoughts on that."
    })
    
    # Chunk 8: Automation and Scaling Impact
    chunks.append({
        "chunk_index": 8,
        "start_time": 630,
        "end_time": 720,
        "chapter_title": "Automating Engineering and DevOps Work at Scale",
        "text": "Moving on, we can embed this inside scripts. Okay, so it means we can automate engineering work and DevOps work. This is big. Your infra work can now be automated in natural language with any tool you want. Now, we can push this even further. Okay, these these next two ideas are big and we're going to spend a lot of time on the channel digging deeper and scaling up what you can do with compute. Make sure you're subscribed so you don't miss these big ideas. This is just the tip of the iceberg. We can stack up multiple Claude Code instances for insane impact. Here we're running a single prompt, but we can set up a reviewer Claude Code instance to review this code. We can set up another one to do the next series of work. We can set up all types of automation. Okay, this is just a simple example. I want to get the gears turning in your mind. I want your engineering brain to turn on and start understanding how you can scale your impact with Claude Code as a programmable agentic coding tool."
    })
    
    # Chunk 9: Building Claude Code Into Your Agents
    chunks.append({
        "chunk_index": 9,
        "start_time": 720,
        "end_time": 810,
        "chapter_title": "The Future: Building Claude Code Into Your AI Agents",
        "text": "The last big idea here is truly the future of engineering. This is the next next phase. You can build Claude Code into your agents. Okay, we're going to take a little pause here just to let this idea air out and really take hold. You can scale your compute with Claude Code inside of your AI agents. This is a next level idea we're going to be talking about on the channel in the future. So again, make sure you're part of the journey. You don't want to miss what's next. We can take this and improve it right here. This is a static script. It's going to do one thing. is going to do it well, but it isn't as useful. Okay, we can easily build up a workflow with this one idea. Okay, so we can take that exact same workflow and add just one dynamic variable. We can parse the CLI args and place it as the second step in this three-step workflow. Git checkout a new branch, do whatever the prompt is, then commit your changes. All we're doing here is internalizing the capability of using Claude Code in agentic coding tool as a programmable tool. You can build this into your scripts, into your workflows, into anywhere you can write code. Then you can commit this file. You can commit whatever workflow you build and iterate on it across every single one of your code bases."
    })
    
    # Chunk 10: Simple Hello.js Example
    chunks.append({
        "chunk_index": 10,
        "start_time": 810,
        "end_time": 900,
        "chapter_title": "Hands-On Example: Creating Hello.js Script",
        "text": "Let's execute some real examples. Everything we do here on the channel is hands-on. I always aim to hand you as much value as I can every single Monday. Let's first look at the essential files of this codebase. If we run ls-programmable, you can see we have, you know, seven files here showcasing how Aider is programmable and how Claude Code is programmable with increasingly more agentic examples to help you understand what you can really do with this technology. Here's a simple example. Make hello.js a script that prints out hello. Okay, super straightforward. Nothing complicated going on here. So, we can go ahead and run this. I'm going to use my file reference hotkey. I highly recommend you set something like this up so you can quickly reference files for your AI tools. I've mapped this to command shift R. And then I'll just kick this off like this. So, to be clear here, let me actually first do this. If we look for hello, you can see there is no hello file. So, hello.js. Nothing there. And now we can go ahead and kick this off. So, we'll run this file successfully created. If we do ls | grep hello, you can now see that file cat hello. You can see exactly what we wanted there. We can run whatever your favorite version of JS is to kick this off. There's bun, node and of course deno."
    })
    
    # Chunk 11: Todo CLI App in New Branch
    chunks.append({
        "chunk_index": 11,
        "start_time": 900,
        "end_time": 990,
        "chapter_title": "Building a Todo CLI App with Branch Management",
        "text": "Let's push this further. Shell scripts are kind of nasty. Not all of us like to use these. Trust me, I'm one of those people. I prefer using Python or JS for my scripting. This is a single file Python script. We can kick this off and get this file generated in a brand new branch. Let's go ahead and kick this off. Same flow. And this is going to be really cool. And you know, while this is running, just to be super clear, you know, ls | grep cc_todo. This does not exist. You can see here our branch changed. We're now in todo-cli-app. And so after this completes, we're going to have a stage commit. And then we're going to switch back to the main branch. Claude Code is going to switch this back to main after it completes its work. You can see here at least four distinct tool calls with one or more of our allowed tools enabling this functionality, right? Okay. So, there it is. We're back on our main branch and Claude Code is printing its output here. We can look at the changes and you can see here we have that new branch zero dependencies. Add list update toggle. Fantastic."
    })
    
    # Chunk 12: Verifying the Todo App
    chunks.append({
        "chunk_index": 12,
        "start_time": 990,
        "end_time": 1080,
        "chapter_title": "Verifying the Todo App and Living Software Vision",
        "text": "So, we can check this out, right? If we open up our directory and we git checkout this branch, you can see that cc_todo now exists. We can open this up and we can see our file exactly as we asked, right? Create this file, a zero library CLI to-do app. We can click into this and you can see we have a clean TypeScript application. Looks like we can kick this off in node. I'll use bun since it usually works out of the box, no problem. And there you can see we have our nice simple to-do list application built out for us with our agentic coding tool. We're not going to go through the code. It's a to-do app. No one cares. But what we can do is clear and type git log. And you can see a clean commit here from our agentic coding tool. Add CLI to-do app. This is that next step. And then it switched back to main. Okay. So git checkout main. Now we're back in main. Now that code is gone. This work happened with a script with our agentic coding tool. On the channel, we're on a mission to build living software. I hope you can see how this is directly in line with that goal. We need these arbitrary tool calling capabilities inside of small to large workflows in order to build out full-on agents full on agentic software that operates on its own while we sleep."
    })
    
    # Chunk 13: Claude Code with MCP Servers
    chunks.append({
        "chunk_index": 13,
        "start_time": 1080,
        "end_time": 1170,
        "chapter_title": "Claude Code with MCP Servers: The Notion Integration",
        "text": "Let's move on to another large example to see how we can use Claude Code as a programmable AI coding tool. So, this one is really, really cool. This is going to blow your mind a little bit. We can use Claude Code with arbitrary MCP servers. So, inside of this codebase, I have an MCP setup. If you click this, you're going to see an MCP setup for Notion. Notion is your second brain. It's an application you can use to store to take notes and do a lot of knowledge work. All the setup you need is in here and the readme will explain exactly how to get it set up. You can see I have mcp.json gitignored because my Notion API key is in that file. But now that we have this and now that we know that we can use Claude Code as a programmable tool, we can do something incredible. If you want to understand an agent or an MCP server, first look at its tool set. I like to call this the tool belt. We can see we have the essential built-in Claude Code standard tools and we have a huge list of Notion API tools. If we collapse everything here, you can see all you need to see. We have a nice prompt here that we're going to look at in a second. And then we have our programmable Claude Code line. We're going to use the output format flag to stream the output as this program runs."
    })
    
    # Chunk 14: Notion as Planning Document
    chunks.append({
        "chunk_index": 14,
        "start_time": 1170,
        "end_time": 1260,
        "chapter_title": "Great Planning is Great Prompting: Notion as Spec",
        "text": "I built out a complete workflow here that reads a Notion page, analyzes the instructions, and executes on the task one by one. Let's kick this off and I'll explain exactly what's happening as we progress. So, Claude Code has started to work for us. So, what is it doing here? Like I mentioned, it's going to read this file and then it's going to start calling tools to actually write this code. You can see this directory just got created, notion-todos. And now Claude Code is reading this file and it's going to execute every one of these tasks top to bottom. And now we're tapping into another key principle of AI coding and of agentic coding. Great planning is great prompting. We've detailed everything we want out here in this Notion page. And now we can use our Notion page as a document, as a spec, right, as a plan to get work done. So you can see here Claude Code just created this add method. We can click into this and you can see, you know, some of that code here. Update just got created there. As Claude Code moves through these features, it's going to make a tool call back into Notion."
    })
    
    # Chunk 15: Agentic vs AI Coding Difference
    chunks.append({
        "chunk_index": 15,
        "start_time": 1260,
        "end_time": 1350,
        "chapter_title": "The Key Difference: Arbitrary Tool Calling",
        "text": "Claude Code had to use a Notion read tool to get all this information inside of its context window. We have every Notion API tool that we need to interact with Notion. So here we're using Notion as our, you know, planning document that we can use to get work done. So whatever you can write in here, whatever you can communicate with a great prompt, which we'll look at in just a second, Claude Code can pull off, right? We're quite literally reading from Notion. Then Claude Code is going to review these tasks and check them off one by one. There we go. So this is really cool, right? Our top level todos got checked off. You can see that exist. Our add just got checked off. And then update, delete and list are going to follow, right? Because all this functionality exists. Our agentic coding tool is running Notion tools, right? It has the Notion tool belt attached to it. So it can perform arbitrary work inside of our Notion page as well as in our codebase. This is the key difference between AI coding and agentic coding. Agentic coding is not limited to AI coding. It can call any tool. It can act as if you or I were calling the tool. We're clicking the buttons. We're hitting the API calls ourselves."
    })
    
    # Chunk 16: Reusable Workflows with Notion
    chunks.append({
        "chunk_index": 16,
        "start_time": 1350,
        "end_time": 1440,
        "chapter_title": "Building Reusable Assets: 200-Line Prompt Magic",
        "text": "Right? You can see a nice output there that cost us, you know, 50 cents to run. Not too bad considering. I literally just set this up, right? I just wrote the plan. Now, this can be rerun over and over and over and we can run anything we can put in a Notion page. Anything we can communicate to our agentic coding tool. Okay, so I really hope you can see the value in this. Let me just briefly show you the prompt that I use to write this. You can see here I'm writing a clean markdown prompt. You can also use an XML-ish prompt if you like. But all we're doing here is clearly stating how Claude Code should behave here in a loop. Right? And then we have a process flow. All right. Step one, find the Notion page, get the page content. Remember, we've passed in the page that we want it to run. Okay? So this can run on any page you can set up. Then it processes each to-do. And then it wraps up with a summary. We have some additional important notes. And then we list a couple key tools that are going to be helpful for our agent. And and that's it, right? 200 lines. We have a reusable asset that we can use to deploy Claude Code over and over and over to get real engineering work done."
    })
    
    # Chunk 17: The Future of Agentic Coding
    chunks.append({
        "chunk_index": 17,
        "start_time": 1440,
        "end_time": 1530,
        "chapter_title": "Claude Code Leadership and Next Generation Agentic Coding",
        "text": "Okay, so this is just one simple example and I hope you can see where this is all going. There are only a few AI coding tools that have this agentic capability. This is why I stress the importance of Aider and now Claude Code. Okay, the fact that this is a programmable tool puts it in its own category. So if you're an Aider user and you know I completely understand using Aider, it's a great tool. You can script with Aider. As mentioned, there is potential for Aider adding MCP support. This could really open it up to become an agentic coding tool instead of just an AI coding tool. I've been keeping a sharp eye on this PR, but I haven't seen Paul, the creator of Aider, jump on this. So, I'm a little pessimistic that this is going to get out and really transform Aider to become an agentic coding tool. But I'm also personally on the fence. I think Aider is a beautiful, fantastic tool because it is simply an AI coding tool. It does one thing and it does it well. The Claude Code team is one of the few teams really shipping value into the agentic coding space. If you ask me, they are the leaders here and it's very, very clear. I recommend you pay the price it costs to use this tool. It's just too valuable to miss and it truly is paving the way for next generation agentic coding."
    })
    
    # Chunk 18: Principal AI Coding Course Announcement
    chunks.append({
        "chunk_index": 18,
        "start_time": 1530,
        "end_time": 1575,
        "chapter_title": "Next Phase: Principal AI Coding Course Evolution",
        "text": "So, what's the big announcement? I'm super excited to announce that the next course, the next phase that I'm going to be building on top of Principal AI Coding is officially in the works. I'm starting to build up the essential ideas for what's going to pave the way for the next essential set of lessons that's going to help you accelerate what you can do with AI coding and now with agentic coding. I'm massively prioritizing all existing Principal AI Coding members as I'm building out this next generation course. So, if you're not a Principal AI Coding member already, definitely jump in and start getting ahead. Start setting up the foundations you need to survive with AI coding and what's coming next. We detail this transition from AI coding to agentic coding and the state of AI coding. I'll also link this in the description for you. The big three ideas here is engineering with exponentials, AI coding is transitory. I hope after you see this video, you can kind of understand why. And then part three, agentic coding is the endgame. Look out for a late Q2, early Q3 launch of the next course where we accelerate what we can do with next generation agentic coding tools like Claude Code. Remember, we're moving away from AI coding into agentic coding. AI coding is not enough. It's just the beginning. It's the tip of the iceberg. As you now know, it's a single tool. Where we're headed, we're going to be calling tens and hundreds of tools to ship real engineering value in record time. You know where to find me every single Monday. Stay focused and stay curious."
    })
    
    # Calculate token counts and prepare output
    total_tokens = 0
    for chunk in chunks:
        token_count = count_tokens(chunk["text"])
        chunk["token_count"] = token_count
        total_tokens += token_count
    
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    output = {
        "video_id": "2TIXl2rlA6Q",
        "title": "AI Coding is NOT ENOUGH: Claude Code's NEXT LEVEL Agentic Coding FEATURE",
        "channel": "IndyDevDan",
        "duration": 1575,
        "total_chunks": len(chunks),
        "avg_tokens_per_chunk": round(avg_tokens),
        "chunks": chunks
    }
    
    # Save to file
    output_file = Path("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_programmable_agentic_2TIXl2rlA6Q.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {len(chunks)} manual chunks")
    print(f"📊 Average tokens per chunk: {round(avg_tokens)}")
    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    create_manual_chunks()