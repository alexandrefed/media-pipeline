#!/usr/bin/env python3
"""Manual chunker for IndyDevDan's Voice to Claude Code video."""

import json
from pathlib import Path
import tiktoken
import sys
sys.path.insert(0, '/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/src')

def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def create_manual_chunks():
    """Create manual chunks for the Voice to Claude Code video."""
    
    chunks = []
    
    # Chunk 1: Introduction and Voice-to-Code Demo Hook
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "Voice-to-Code Introduction and Live Demo",
        "text": """Claude, are you ready to build? Ready to help. What do you want to build? All right, so let's start simple. Claude, go ahead and create a simple Hello World starter coding examples for the six most popular programming languages. Let's go ahead and create them inside of a Hello world examples are in the starter coding folder for Python, JavaScript, Java, C++, Go, and Ruby. Fantastic. Okay, Claude, go ahead take those examples and showcase how to make an HTTP request, make a um go ahead and pass in the URL as a CLI parameter and updated six programming examples to make HTTP requests using URL parameters with added detailed comments. Nice. Okay, as you guys can see here, we have real time speech to text running and it's getting fed into our agentic coding tool. And you know, this is really cool, right? Real time speech to text coming in. I love to see this in real time. Inside of the Claude Code is programmable codebase. I've got everything dialed into a single file within, you know, 700 lines of code. We have our ears, we have our brain, and we have the voice of our personal AI assistant.""",
        "start_time": 0,
        "end_time": 120
    }
    
    # Chunk 2: Personal AI Assistant Architecture Overview
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "Personal AI Assistant System Architecture",
        "text": """Now, we're going to break this down, but let me go ahead and cancel this large request. This is really cool. We have a personal AI assistant that we can talk to to make changes for us. We're going to talk about how Claude Code completely changes the game for personal AI assistants in this video. Let's go ahead and continue making useful changes. So, inside of the script, we have an issue. You can see we have the default list of Claude Code tools. And if I search for this, um, I'm not actually using this yet. This is a real problem that I just kind of left in here to showcase in this video. And what I want to do here is have our personal AI assistant fueled by Claude Code go ahead and make this change for us. Fire this up again with that same ID. A cool feature is that we can reference previous conversations. I'll show that off in a second. Let's just go ahead and kick this off.""",
        "start_time": 120,
        "end_time": 200
    }
    
    # Chunk 3: Trigger Words and Voice Recognition System
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "Voice Activation with Trigger Words",
        "text": """And now you can see our personal AI assistant listening to us, right? This is an always on assistant. You can see there it's autocorrecting things as it proceeds. And I'm going to go ahead and pause here. And you'll notice nothing will happen. Okay. So, nothing happened there because the trigger word wasn't detected. My trigger words here are one of these four. And as soon as I say them, the assistant will actually act. Right. So let's go ahead and make this change. Sonnet, go ahead and update our allowed tools CLI parameters. Update these to use our constant at the top of the file. We have a constant called default Claude Code tools. Go ahead and use this instead of basically duplicating those items. We should get this picked up here. There we go. So Sonnet is one of my trigger words. So it's going to go ahead and actually run this command.""",
        "start_time": 200,
        "end_time": 280
    }
    
    # Chunk 4: Live Code Execution and Performance Analysis
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Voice Command Execution and Performance",
        "text": """So you can see Claude Code got kicked off. We should use the spread operator here so that we can reuse that constant that we had at the top of the file. Right? So we had our default Claude Code tools. We want to see this get used here on the left. As we'll talk about in a second, you know, the system is not perfect. You know, the first Claude Code is expensive. And then the second problem is that we have uh updated the process message method to use the default Claude tools constant from lines 85 to 93 for CLI parameters avoiding duplicate tool lists. Fantastic. And so you know the second issue here is that it does take some time. You can see there audio itself playing took 9 seconds. That's fine. But running our agent coding tool did take a decent amount of time. So you can see that change got rolled in there. That looks fantastic.""",
        "start_time": 280,
        "end_time": 360
    }
    
    # Chunk 5: Anthropic Web Search Tool Integration
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Anthropic Web Search Tool Demo",
        "text": """So, Anthropic just released the uh web search tool, and I want to play with this a little bit. So, I already have this documentation inside of our AI docs, one of the three essential folders. Highly recommend you set up this directory inside your codebase. Our assistant has access to this. So, let's go ahead and create a brand new plan that'll combine this and our uv single file script so that we can get a concrete demo of how the web search tool looks. So, I'm just going to use my assistant to build out this plan and then implement it for us. So, I'm here. Sonnet, read a couple files in our AI docs directory. I want you to read the uv single file script and I also want you to read the uh Anthropic web search tool documentation. So, put these together into a single spec inside of our specs directory. This is going to detail how we can build out a minimal version of the new Anthropic web search as a uv single file script. I just want you to create the plan for us here. Write a brand new plan in the specs directory.""",
        "start_time": 360,
        "end_time": 480
    }
    
    # Chunk 6: Natural Language Planning and Great Planning is Great Prompting
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Natural Language Planning and Spec Creation",
        "text": """Okay. So, as you can see there, I think one of the problems with natural language is that, you know, it just takes some time to like really communicate everything you want. I've created a detailed spec for a self-contained Python script that takes search queries from the command line, uses Anthropic's web search with authentication, formats results with citations, and supports options like domain filtering and location context. The spec covers script structure, dependencies, CLI, authentication, usage examples, output format, error handling, and future improvements. Okay, so this looks good overall. It looks like we are actually missing our uh code examples. So, Sonnet, update that file. Uh we are missing a concrete code example. Make sure you pull, you know, real code examples from Anthropic web search tool markdown file from our AI docs and make sure that that's added in there. We need concrete examples because we're going to use this as the kind of framework for actually writing this code. So, we have the update coming in here. And so, you know, this is just continuing down that trend of great planning is great prompting. This is the key principle in lesson five and I've mentioned it on the channel a million times now. I'm going to keep mentioning it because you know successful engineering really being successful at anything um it's not always about new different ideas. It's really about doing the same correct thing over and over and over.""",
        "start_time": 480,
        "end_time": 600
    }
    
    # Chunk 7: Context Reusability and Claude Resume Feature
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Context Reusability and Conversation Tracking",
        "text": """So the great part about this, you know, this is a really important part of whatever system you're building out if you're, you know, integrating with LLMs and agentic systems. You really want context reusability. This is something that uh I hope the Claude Code team spends some more time building out. They just recently launched this feature where you can do claude continue and this will pick up on your previous session. They also just added claude resume. So if we click Claude resume you can see different sessions pop up and so this is a really great way to hop back in specific sessions. But in the system I've built out a simple conversation tracker which you can see here in the output directory. If we click cc you can see all I'm doing is tracking you know basic conversation history right? So there's that intro. Claude Code, are you ready to build? So on and so forth. This is a great way to reload the conversation. Obviously, we're using Claude Code here as a programmable tool. That means we need to do a little bit more managing of context.""",
        "start_time": 600,
        "end_time": 720
    }
    
    # Chunk 8: Live Implementation Demo and Claude Code Intelligence
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "Live Script Implementation with Voice Commands",
        "text": """Go ahead and fire this off and let's get this feature implemented. Claude, go ahead and read the Anthropic web search uv script spec and let's go ahead and implement this into a brand new uv single file script. All right. So, this should be good enough. The big unlock here is that Claude Code is smart enough. It's intelligent enough. It has enough searching capabilities, right? It's agentic enough to take this request and it has the abilities to look through whatever it needs to inside this codebase, right? The specs and the AI docs in particular. This should be enough for Claude Code to get started, right? it knows to read this spec and of course it can see that specs directory if it does any file searching and then we say let's go ahead and implement this into a new uv single file script. So let's see what Claude Code comes up with here. Let's yeah there we go. Nice. That looks great. Um let's uh see what we got here. I've created a self-contained Python script for the Anthropic web search uv with command line support, error handling, API key checks, citation formatting, and colored output. It includes time zone support, usage tracking, domain filtering, and robust API error handling. There's also a readme with install steps, usage examples, output details, and pricing notes. The script runs via python anthropic_search.py "your search query". Awesome.""",
        "start_time": 720,
        "end_time": 840
    }
    
    # Chunk 9: Script Testing and Voice Assistant Cleanup
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Script Testing and Automated Cleanup",
        "text": """Okay. So, you know, really what I want to do here is showcase the uh capabilities of a personal AI assistant. So, I don't want to harp too much on this script. Um, but you know, since it's here, let's go ahead and run this. So, let's open up the readme that was created. And there's our search query. So, uh, we probably need to run chmod +x on this. Probably give permissions here. chmod +x anthropic_search.py file. And then let's go ahead and run a search. anthropic Claude Code and let's see what we get here. So, I'll be impressed if this uh works in one shot. I feel like that happens more and more. You know, the more you kind of learn to write concise prompts, you know, natural language, written language, the easier it gets to actually clean this code up. So, um looks like there was an issue. Okay, interesting. So, we got one search and response. I'll search these capabilities for you. So, that worked. This is here. I'm actually going to go ahead and commit this into this codebase. While we're talking about this, I'm going to fire this up. And I don't want this additional readme here. So, um, I'm just going to have our assistant clean this up. I want to merge this. So, uh, Sonnet, can you go ahead and take the anthropic search readme and merge it into our base level readme? I don't want that duplicate readme. Please go ahead, clean that up, and then delete the anthropic search readme when you finish.""",
        "start_time": 840,
        "end_time": 960
    }
    
    # Chunk 10: Compute Equals Success Philosophy
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "Compute Equals Success - Core Philosophy",
        "text": """Why is this important? Why is having a incredible 700 line personal AI assistant valuable? Right? Why is this valuable? It's valuable because of one simple idea. You know it. We talk about on the channel all the time. So, the key idea here is compute equals success. Okay, the more you scale your compute, the more success you will have as an engineer in the generative AI age. If you understand this one idea, you are going to win. You're setting yourselves up to win. So, how were we able to tap into more compute here with our personal AI assistant plugged into Claude Code? Claude Code is a programmable agentic coding tool. And not only is it just programmable, it's infinitely programmable. So, you can do stuff like this, right? Um, you can write entire workflows, right? Here's a super simple one we've looked at, right? You have a prompt that uh creates a new branch, creates a to-do, todo.ts, ts minimal C CLI application and then it commits okay so there are tools embedded in this prompt right and and that's the big idea if you get that you'll get a lot of things there are tool calls embedded in this prompt and it unlocks all types of craziness right reusable ADWs principal AI coding members know how powerful that can be.""",
        "start_time": 960,
        "end_time": 1080
    }
    
    # Chunk 11: Claude Code vs Industry Tools Comparison
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Claude Code vs Cursor, Windsurf, and Codex",
        "text": """There is some confusion in the industry right now. Some engineers are wondering what is Claude Code for? How is it different? You know, is Cursor better? Is better? A couple thoughts there. First, don't think in ors, think in ands. Use these tools together. Use different combinations. Don't limit yourself with the or mindset. That will set you back. Point number two here is there is no other tool right now that is an agentic programmable tool. Okay, we've gone into detail on this in a couple previous videos. You know, we know that AI coding is a small subset of agentic coding, but the the the true impact of this we're going to be unpacking on the channel. Make sure you're subscribed. Make sure you're part of the journey because this is going to get really interesting, right? You you can't do this with Windsurf. You can't do this with Cursor. You can't do this with Cline. Codex is the only tool uh close to accomplishing this. It has full auto mode and then you can write a prompt and then your assistant will do work for you. Okay, so this is close but Codex is is you know to be fully honest it's nothing special. It's basically a clone of Claude Code. The only thing they have going for them is the fact that they enable open models.""",
        "start_time": 1080,
        "end_time": 1200
    }
    
    # Chunk 12: 50K Subscriber Thank You and Channel Mission
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "50K Subscriber Milestone and Channel Values",
        "text": """You can see here um you know what but before we get to this before we dive into this uh. I just really want to. I want to stop and uh. I always forget to do this. I want to stop and say uh just a huge thank you. Uh we're about to hit 50k subs and we were never supposed to get this big. I imagine we would flatline around 10 or 20k subs and we would just go sideways for basically ever, right? Like I imagine that this was it. Okay, but here we are almost at 50K subs. It's been a really long drive. Every week I show up four, you know, mid and senior plus engineers working in the field with their boots on the ground every single day, right? It's about building real valuable software. Engineers are skeptical by nature. It's like a huge percentage of the audience that watches the channel, they're not subscribed. And that's fine. That's fine. Whenever you're ready, I'm here. I'll be here every single week. I don't know if you can tell yet. If you can't, this is not a scam. This is not a grift. The one product that I do sell on the channel, Principled AI Coding, has been immensely valuable to every engineer that's taken it. The reviews have been insane and it's setting up for what we're going to do next.""",
        "start_time": 1200,
        "end_time": 1320
    }
    
    # Chunk 13: Three Priorities Framework
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "Three Priorities: Living Software, Engineering Potential, Value Creation",
        "text": """One last thing I'll say here is I have three priorities and no matter how big we get, I want you to know that you know what these priorities are because it differentiates what we do here on the IndyDevDan channel. Okay, so one build living software, two unlock your engineering potential and three make a living by creating value. Okay, the order is everything, right? Um, I want you to know my priorities and I want to just really hint on why it's so important to have priorities yourself. I'm not here to make a living, right? That's not my first priority. That's my third priority. I'm not here to just unlock your engineering potential. Okay? My top priority is to build living software that works while I sleep. Okay? And by having this mission, right? By having that as my key cornerstone mission, I'm able to provide you with unique value that you can't find anywhere else. Because of my mission, because of my priorities, this isn't changing. It's not going to change. And I'm going to be here every single week, 50K, 60K, no matter how high or how low we go. We're going to have big videos. We're going to have crappy videos that don't do well. But in every single video, I'm going to be aiming to give you concrete value to help your engineering every single week, every single day.""",
        "start_time": 1320,
        "end_time": 1440
    }
    
    # Chunk 14: Claude Code Cost Analysis
    chunk_14 = {
        "chunk_index": 14,
        "chapter_title": "Claude Code Cost Analysis and ROI Discussion",
        "text": """So, um I just want to talk about costs. Okay. Uh we're getting deep fried here. This is my cost chart for Claude Code. I just took a quick image of this today. Um and you can see here in just 10 days I'm at $100. Okay. And I even have some off days on here, right, where I'm using other technology. So, I can guarantee you uh I'm not using enough compute. You're not using enough compute. We can get these numbers way higher. And we're going to. And you know, to be clear, it's not about spending more money. It's about spending more money and getting more value out. If you can spend $100 and get $200 worth of engineering work done, you should put in as much money as you can, right? You have a value generator, right? That's what a lot of these powerful tools are. You put 20 bucks in and 40 bucks worth of value comes out right now. Now, the trick obviously is when we're comparing our compute advantage across all these tools, the real question is, can you put a 100 bucks in and get 300 bucks out using a different tool? Okay. And then then and that's what the compute advantage equation is really all about.""",
        "start_time": 1440,
        "end_time": 1560
    }
    
    # Chunk 15: Claude Max Plan and Industry Recognition
    chunk_15 = {
        "chunk_index": 15,
        "chapter_title": "Claude Max Plan Analysis and Industry Recognition",
        "text": """So, I love Claude Code. I'm going to continue using it. I'm definitely not saying don't use this. You know, they just launched their Max plan. And I've been scratching my head on this one a little bit, as you may have as well. I can't really tell if this is actually going to save money or not. As you can see, I'm like a prime candidate for something like this. I'm already at 100. The big problem with a lot of AI labs right now that are providing compute is that there are still limits. Okay? Like it doesn't matter how much you're paying. Um you can see there's still limits. I don't know if this will actually be helpful. I'm going to wait to hear a little bit more before jumping in on this membership. So, something to mention here is, you know, we were one of the first channels to really start talking about Claude Code. But you can see here inside of Hacker News, we might need to go to the second page now. You can see uh you know, Claude Code is getting a lot more attention. 246 comments on Hacker News for this post. Exactly. To me, this is a really great sign. Uh the industry is catching up to how important this tool is.""",
        "start_time": 1560,
        "end_time": 1680
    }
    
    # Chunk 16: Three Component Architecture - Ears, Brain, Voice
    chunk_16 = {
        "chunk_index": 16,
        "chapter_title": "Personal AI Assistant Architecture: Ears, Brain, Voice",
        "text": """I think you know big takeaway here. Uh Claude Code isn't going anywhere. This is the best leading agentic coding tool. Um as you saw here we were able to build out a very very powerful voice to Claude Code personal AI assistant in just 700 lines of code. So what are the components of this? Personal AI assistants at their core are simple. You have the ears, you have the brain and you have the voice. So the ears of our application is something called the real time speech to text. So this is a great library. You saw we were using it here and this gets our input from speech into text so that we can run it into our brain. And so for our brain we are of course using Claude Code. This is what actually does all the work. This is what does the heavy lifting. This is what does the responding and this is how we get work done in natural language using our voice. Okay. Lastly, we have our voice. Right? So, our voice is fueled by OpenAI. And you can see here it's a simple request. You pass in your text. It gives you an output file. You play the output file. The only kind of important note here is that we're using compressed speech. Sometimes Claude Code will return a bunch of details. So, we're using GPT-4.1 Mini to just compress whatever was returned.""",
        "start_time": 1680,
        "end_time": 1800
    }
    
    # Add chunks to list with token counts
    for chunk in [chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, 
                  chunk_9, chunk_10, chunk_11, chunk_12, chunk_13, chunk_14, chunk_15, chunk_16]:
        chunk['token_count'] = count_tokens(chunk['text'])
        chunks.append(chunk)
    
    # Calculate statistics
    total_tokens = sum(chunk['token_count'] for chunk in chunks)
    avg_tokens = total_tokens // len(chunks)
    
    print(f"Created {len(chunks)} manual chunks")
    print(f"Total tokens: {total_tokens}")
    print(f"Average tokens per chunk: {avg_tokens}")
    print(f"Min tokens: {min(chunk['token_count'] for chunk in chunks)}")
    print(f"Max tokens: {max(chunk['token_count'] for chunk in chunks)}")
    
    # Save to JSON
    output_data = {
        "video_id": "LvkZuY7rJOM",
        "title": "Voice to Claude Code: SPEAK to SHIP Agentic Coding AI Assistant",
        "channel": "IndyDevDan",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": avg_tokens
        }
    }
    
    output_file = Path("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_voice_claude_LvkZuY7rJOM.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved manual chunks to: {output_file}")
    
    # Print chunks for review
    print("\n" + "="*80)
    for chunk in chunks:
        print(f"\nChunk {chunk['chunk_index']}: {chunk['chapter_title']}")
        print(f"Tokens: {chunk['token_count']}")
        print(f"Time: {chunk['start_time']}s - {chunk['end_time']}s")
        print(f"Preview: {chunk['text'][:150]}...")

if __name__ == "__main__":
    create_manual_chunks()