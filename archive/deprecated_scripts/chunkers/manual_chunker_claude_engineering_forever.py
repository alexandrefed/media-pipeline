#!/usr/bin/env python3
"""Manual chunker for IndyDevDan's 'How Claude Code CHANGED Engineering Forever' video."""

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
    """Create manual chunks for the Claude Code philosophy video."""
    
    chunks = []
    
    # Chunk 1: Opening - The Quiet Revolution
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "The Quiet Revolution: Claude Code's Emergence",
        "text": """It started quietly. No grand announcements, no hype marketing, just a simple command line interface that would change engineering forever. Claude Code emerged not as a tool, but as a partner in agentic system that understood context, state, and most importantly, engineering. It consistently reasons about code at a level previously thought impossible. And the crazy part is there was no RAG. There was no UI. Only the context, the model, and the prompt. 

The engineering community watched with a mixture of skepticism and awe. As early adopters like you and I started reporting productivity gains that defied belief, tasks that once took days were completed in hours, then minutes as we improved our agentic coding. It's clear looking back this time period marks the beginning of a new phase of engineering. 

Welcome back to the channel. In this video, I want to answer the question and I want to talk about how Claude Code changed engineering. We spend so much time planning, building, and learning. We don't take enough time to stop, reflect, digest, and think hard about the incredible things we can do with our agentic coding tools. By breaking down how Claude Code changed engineering, we can understand the state-of-the-art, which sets us up for making bets on the future and prepares us for what's coming next, so we can make the highest return on investment bets on our precious engineering time.""",
        "start_time": 0,
        "end_time": 90
    }
    
    # Chunk 2: Phase 2 - Agent Architecture Revolution
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "Phase 2: The Agent Architecture Revolution",
        "text": """How has Claude Code changed engineering? Just like deep learning worked, the agent architecture worked. Sam Altman called this out in the intelligence age post. And just like deep learning worked, the agent architecture worked. We're not just chatting with language models in chat interfaces. We're commanding compute. We're prompting agents. We're composing the language model to the next level of abstraction, the agent. It's clear that this transition marks phase 2 of the generative AI age. 

But Claude Code didn't change engineering with the agent architecture alone. It's more than that. What is Claude Code really made of? It has three essential elements that defines it. A powerful set of language models that can call any tool in the right agent loop. This is what makes Claude Code so incredible. You can't have one of these. You can't have two of these. You need all three. The architecture is everything. 

Don't let the benchmarks fool you. The performance from the Claude 4 series is not detectable by the benchmarks. We'll discuss that more in a moment. But you put powerful LLMs like the Claude 4 series with a great set of baked-in tools and the ability to connect to any MCP server. But that's not it. You need the agent architecture. You need the agent loop so that the agent can operate in the right environment and use the right information to get the job done just like you or I would. This is the architecture behind Claude Code.""",
        "start_time": 90,
        "end_time": 180
    }
    
    # Chunk 3: Engineering Primitive - Programmable Foundation
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "Claude Code as Engineering Primitive",
        "text": """So how has Claude Code changed engineering? It's not just a tool. It's not an assistant and it's more than a partner. It's a new engineering primitive, right? It's a fundamental building block of a new class of software development. A new primitive that lets you tap into agents with a single prompt. That means more compute at your fingertips at any time at scale. It's a fundamental building block. What does that mean exactly? 

Claude Code is programmable. From any terminal, you can call your powerful agentic coding tool. This is massive. As engineers, we need the Lego blocks to solve the problem for our specific use cases in our specific domains. A lot of engineering products and tools miss this. They're too opinionated. There's too much thought. 

Speaking of the terminal, Claude Code was able to change software engineering because it operates in the highest leverage point for engineers. It's not an accident that it's in the terminal. This is where us engineers have maximum control over the flow of information. We trade off that initial investment of understanding the terminal to have massive impact with minimal friction. It seems so obvious now in retrospect that this is the optimal place for an engineering agent. We have to give shoutouts to the original AI coding tools like Aider for starting right in the terminal.""",
        "start_time": 180,
        "end_time": 270
    }
    
    # Chunk 4: Real Engineering Focus
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Focus on Real Engineering Workflows",
        "text": """And of course, Claude Code and Anthropic focused on real engineering. These aren't toys. These aren't flashy demos. They change engineering by relentlessly focusing on true engineering workflows. Right? Think, plan, build with plan mode hooks to control and monitor. You can parallelize your agent. And then of course, it's programmable. This is a key feature of true engineering. Can your tool, can your work be composed? Is it interoperable? Right? You can build your own agentic systems with Claude Code. And once you start stacking these together, I've only listed a few here. Right? There are many, many more features. These all help us engineers with our boots on the ground solve real engineering problems. 

It seems so mind-blowing that no previous tool really allowed us to tap into our prompts in a reusable way until Claude Code. They did it right. They built features for real engineering. It's not just about features. It's not just about calling tools. Of course, none of this is possible without their models. And something incredible happened. Starting with the Sonnet 3.5 model. Unexplainable, untrackable emergent behavior inside of that model that again doesn't show up in benchmarks.""",
        "start_time": 270,
        "end_time": 360
    }
    
    # Chunk 5: Benchmark Ghosting and Emergent Behavior
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Benchmark Ghosting: Emergent Model Behavior",
        "text": """I have a term for this because I like to look out for this. Okay, I call these benchmark ghosting models. Their performance does not show up in a benchmark. And you know, you can see this, right? Open up artificial analysis, look for Sonnet, and just search through this. You can see this is not the quote unquote best model on almost any benchmark. You can look for Opus and you'll see the exact same thing, right? By no means is this the best model. Okay, but then why were we able to do more with it than any other model? 

This is because of emergent behavior. Something has cracked inside these models. Okay, they didn't just pass benchmarks. They made benchmarks irrelevant. Real world performance can only be approximated by benchmarks, right? They're proxies, their shells, their corollary systems, right? They don't equal true results, right? So, I'm not saying benchmarks don't matter, but models with emergent behavior that understand, and this is the important part, your context and your intent is what matters. 

And from Sonnet 3.5 to now, and I imagine whatever Anthropic is cooking next, the way they build their models encodes intent. It encodes engineering intent. This is an extremely unique property of these models. An interesting question you can ask is how can I find emergent behaviors inside of models? And so far my only answer for this is time. You need to spend time with these models. And oh boy, I know you and I, a lot of engineers were spending a lot of time with these models.""",
        "start_time": 360,
        "end_time": 450
    }
    
    # Chunk 6: Simplicity as Core Principle
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Simplicity: The Power of No Complexity",
        "text": """So how else has Claude Code changed engineering? It's brought us all back to simplicity, right? As a core principle. As soon as I heard this from Boris, it completely made sense. You can see it. You can feel it in the tool, right? Simplicity is a property and a feature. Okay? And I am worried about this for the future of Claude Code. Every successful application grows. It grows in complexity. It grows in features. It slowly becomes something that it wasn't. I hope that the Claude Code team, the Anthropic team, they stick with this property. If they don't, the tool will lose this powerful property that myself and other engineers seek pretty much in everything that we do and in every tool that we use. 

Anthropic has this beautiful principle um do the simple thing first inside of Principled AI Coding. This is the first principle we discuss and it is keep it simple stupid. Right? That's our version of it. These are all the same thing. Simple things work. And not only do they work, they work consistently. 

Also, I don't know if you've heard the news, but the creators of Claude Code, Boris and Kat, are apparently moving back over to Anthropic. They were rumored to be leaving. Now they're rumored to be coming back from Cursor. This tells me that whatever they saw at Cursor was not good. Just to call it out here, sometimes I still boot it up for the tab model, but that's a great example of an application that is no longer simple, right? It was when they started, but now it's not as simple.""",
        "start_time": 450,
        "end_time": 540
    }
    
    # Chunk 7: Just the Context Window
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "No RAG, No Complexity - Just Context",
        "text": """And that's not to say that it's not a great useful tool. But you can see the difference between Claude Code and many other tools, right? There's no complexity. It's just the context window. 

I said it long ago as everyone was piping and jumping over to RAG. You want just the context window. Don't add unnecessary complexity. Let the model do what it needs to with the right tools. Right? Let it search just like you and I search. Think about the tool you would use. Great. Now, give the model the tool you would use. Okay? At least to start. All right? So, there's no complexity. It's just a context window. No setup. Uh, this is something that's really powerful. A lot of us engineers, we overthink things. We try to compare and contrast all the time. Claude Code said no. Sonnet, Opus, no setup. All right. And then there's no friction. It's just the prompt. 

I still to this day have opened the application probably tens of thousands of times. That sounds ridiculous, but I love opening the terminal, typing Claude, and this is all you see, right? It's just this. It's an input field, and your agent loads things into its context window, and the LLM drives decision-making. That's it, right? I still love that to this day.""",
        "start_time": 540,
        "end_time": 630
    }
    
    # Chunk 8: From AI Coding to Agentic Coding
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "Beyond AI Coding: The Agentic Revolution",
        "text": """Um, you know, the Claude Code team, they've cracked it. AI coding is not enough. This is something that we have talked about on the channel. I ran into this issue very, very early on when I was using Aider. Writing code is a fraction of what engineering is. And this is why vibe coding falls apart even with powerful agents. Coding is not enough. It's not just about generating code. Engineering is about much more than that. We needed agentic coding and now we have it. We needed something that scales with the complexity of the problems we face as engineers. The agent does it and we can use it with agentic coding. 

So last thing to call out here, how has Claude Code changed engineering? It's infinitely scalable. Okay, solving two problems at once, fire up multiple parallel sub-agents. Are you working on multiple iterations, multiple problems at the same time? Open up multiple Claude Code instances, right? Do you need your own custom multi-agent system? Fire up programmable mode, right? -p run it from any terminal. Run it off device. Again, it's programmable, right? It's a new foundational unit of engineering. It's a new engineering primitive.""",
        "start_time": 630,
        "end_time": 720
    }
    
    # Chunk 9: Future Predictions - Multi-Agent Systems
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Future: Multi-Agent Swarms and ADWs",
        "text": """Okay. So, let's talk about the future. So, we know where we're at, right? We have this incredible tool that pushes us from AI coding into agentic coding. So, we have to ask the question, what's next? So, here are some predictions from the edge from everything that I can see. We talk about this on the channel. Go where the ball will be, not where it is. 

One of the trends happening right now, you're seeing this if you're paying any attention at all. Multi-agent systems, not one Claude, not two. We're talking swarms working together in order running in AI developer workflows, ADWs, commonly known as agentic workflows. Each agent specializes. You need that context window focused on one problem and then you hand off to another agent. You see this inside of Claude Code. You can fire up sub-agents. That's just the beginning of what's possible. Together they form systems more powerful than any single mind. Okay? And I'm talking about you and I. 

You know on the channel we've run some systems that are doing so much engineering work at one time that it is truly hard to follow everything that's going on. This is where observability and monitoring comes in. We talked about agent observability in our previous couple videos. We're going to see this become more and more important and we're going to continue to see multi-agent systems get used and built everywhere.""",
        "start_time": 720,
        "end_time": 810
    }
    
    # Chunk 10: Dedicated Agent Environments
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "Dedicated Agent Environments: The Next Infrastructure",
        "text": """So, dedicated agent environments to support the scale and potential of the multi-agent systems we're going to be operating in. We need dedicated agent environments. Okay. This is a big trend and an easy bet to make. This is what you want, right? As an investor of your time, money, and attention, you want big trends that are easy to bet on. And this is one of them. Okay. So, you know, I have, and others are starting to do this as well, I have a dedicated box right here. All I do in this Mac Mini, all I do in this device is run agents. They have full control over this device here. 

We're going to be talking about dedicated agent environments a lot more on the channel. You can have physical devices, cloud VMs, and there are even services that are getting spun up from nowhere. And one of these companies, I can guarantee you, is going to become the new Vercel for AI agents. This is a big idea. Um, dedicated agent environments are something that is going to happen. It's starting to happen already, right? You don't want your agent running on your device, taking over your device. This is great, but this back and forth prompting with your agent is going to be good for you building these bigger systems. Okay, a lot more to say on that on the channel. Make sure you comment and subscribe so you don't miss that and so you let the algorithm know you're interested in this.""",
        "start_time": 810,
        "end_time": 900
    }
    
    # Chunk 11: Unbelievable Automation at Scale
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Automation Scale: Months to Minutes",
        "text": """What's next? What does the future have for us? What bets can we make as engineers right now to get ahead of the curve? Unbelievable automation. This is not new, but the scale is going to be new. I don't know if you've had this experience, but I've gotten some multi-agent systems up and running that are so powerful, so complex, it's hard for me to keep up with what I can do and with what I can do with these new systems. Okay, I'm starting to see few groups of engineers running into this problem as well, right? The scale is so big. The workload, they're becoming so massive. 

What it used to take teams months will take minutes. Will close the loop and let the code write itself. Closing the loop is a principle of AI coding. You can see all the big labs going crazy over this idea right now. And frankly, any good agentic coding engineer really focuses on this idea, right? Don't just write a prompt. Write a prompt and then say validate your work with X. That creates a closed loop system. I have something that can help you understand that concept at the end of this video. But the key idea here is massive. We're going to have entire code bases refactored while you sleep. Test suites automatically generated documentation that writes itself. This is just the beginning of like the automation that's that is coming and that some engineers are starting to crack.""",
        "start_time": 900,
        "end_time": 990
    }
    
    # Chunk 12: The Widening Engineering Gap
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "The Engineering Gap: 0-1x vs 10x Engineers",
        "text": """So here's a big one. This is an important one. The engineering gap continues to widen. There's a lot of talk about the zero to 1x engineer, you know, using tools like Lovable. They are able to do more than ever. That's great. That's true. But there's a really interesting gap between the 1 to 10x engineer and the zero to 1x engineer where they just stop. There's a point where they can't build any bigger. They can't build any more value because they don't know what's going on. 

I do believe that the gap will widen and then shrink as the tools progress and as our agents become that much more powerful. But there's going to be a dark age here, right? A dark age where, you know, senior plus level engineers, mid-level plus engineers using these tools, your 10xers on your team, in your company, the difference between them and then, you know, your mid and below engineers, your noobs, your vibe coders, it's going to be mind-blowingly massive. 

And it's because when they watch an IndyDevDan video, they understand what's going on underneath, right? They know that when I gloss over, you know, certain syntax or the way I organize functions or the way I organize the codebase, the runtime of a specific method, you know, that's a great example, right? They know that you can prompt and discuss, you know, logarithmic runtime of a specific piece of code and have a discussion about optimizing it, moving it.""",
        "start_time": 990,
        "end_time": 1080
    }
    
    # Chunk 13: Learning vs Building - Choose Your Path
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "Use Tools to Learn, Not Just Build",
        "text": """There are many core engineering ideas like runtime complexity, low-level architecture, why we use certain frameworks, why you use certain tools, tool mastery, right? Even things like understanding what the terminal can do and how you can customize and modify your terminal. 

There are tons of examples of beginner engineers, they will just never learn this stuff. Some of you guys will, some of you guys are really smart and you'll use these tools to learn instead of just use the tools to build, right? There's a big difference there. A lot of vibe coders are just building. They're not learning. But anyway, I don't want to harp on this one too much. I just want to mention that there is still time to choose which side you're on. 

Use these tools to learn. You're mid senior level plus engineer. Don't become an old dog. Keep investing in learning new engineering, right? Learning the generative AI way to do things. Okay? Because it's not the same, right? This is a new skill. AI coding is a new skill. Agentic coding is a new skill, right? The way you prompt these systems continually evolves, right? The way you add context continually evolves. I don't care if you call it prompt engineering or context engineering. It's going to keep changing and evolving. All right? So, take some time, always invest in your tool. Always keep learning, right? Because the engineering gap is going to widen massively before it shrinks again.""",
        "start_time": 1080,
        "end_time": 1170
    }
    
    # Chunk 14: Agents Going Viral - Domain Opportunities
    chunk_14 = {
        "chunk_index": 14,
        "chapter_title": "Agents Going Viral: The TAM Opportunity",
        "text": """And lastly, this is really important. This is a great call out for engineers and teams looking for that next product. Agents are going viral. Okay, they're going to go viral over these next couple years. Claude Code is the agent for engineering, but there are hundreds of domains where agents don't exist yet, but where they can be created and deployed. You know what that smells like? What do we smell there? That's called opportunity. Okay, if you're a builder, if you're a creator and you're in one of these domains, right, you do want a domain advantage. If you're in one of these domains, right, or any domain, um the amount of TAM, total addressable market ready for disruption for you, for your team, for your company. This is a massive opportunity. 

Agents go viral and of course you know it's natural that the first agent right the best piece of technology would emerge for the technology builders which is you and I agents are going viral this is a big opportunity uh this is a future direction of where agents are going of where agentic coding is going so on and so forth all right the evidence is super clear this channel is one of the first to cover Claude Code before all the hype before you know everyone and their mom starts using you know Claude Code we covered it first. This is the place to be for agentic coding on the edge for really just that next phase of engineering.""",
        "start_time": 1170,
        "end_time": 1260
    }
    
    # Chunk 15: Call to Action - Master Claude Code
    chunk_15 = {
        "chunk_index": 15,
        "chapter_title": "Master Claude Code: Scale Your Compute",
        "text": """So again, I don't know how many times I can say it in one video, but comment, subscribe, like, you know what to do. Tell the algorithm you're interested. All right, we were here since the beginning and we're going to be here until the end. Okay, we're in the age of agents, okay? It's phase two. After decades of failed AI promises, the agent architecture has delivered. All right, so take action. 

Couple call outs for you, you know, as a thank you for making it to the end of the video, for sticking around. I always aim to provide value for engineers here every single week. Master Claude Code. Everyone else is copying Claude Code. All right, you saw it with the Code CLI. You saw it with the Gemini CLI. You see it with open source. It's fine. Copying is great. This is how we grow and improve, right? There are copycats everywhere. First, you copy, then you innovate. Whatever. Right now, this is the tool to master. Okay. 

Scale up your compute. More prompts, better prompts than more agents. If you can't use one Claude Code instance, getting an agent device makes no sense for you. Scaling up more agents, using sub-agents, it makes no sense for you. Okay? So, step up one step at a time. Scale your compute. More prompts, better prompts than more agents. All right? You can do a lot more with the right prompt than you think.""",
        "start_time": 1260,
        "end_time": 1350
    }
    
    # Chunk 16: Principles Over Tools - Course Pitch
    chunk_16 = {
        "chunk_index": 16,
        "chapter_title": "Focus on Principles: The Agentic Future",
        "text": """All right? And I'm looking at all of you who think your codebase is too big. Okay? No, you just haven't written the right prompts. All right? solve bigger problems. Right? 

On that same note, keep your agents running longer and then longer. Okay? These things can run for tens of minutes, half an hour, and if you set it up right, they can run for hours. Agents, okay? Solving problems, building things, doing research. It's happening right now. All right. So, that's that. 

Uh, focus on principles, not tools, not models. I know some of you that have been with the channel, you know, forgive me. Um, but it's important to keep plugging for engineers before the next big course hits. If you want to get an asymmetric advantage on your time, I definitely recommend you check out Principled AI Coding. This is my take on how to master the principles of AI coding. AI coding came first. We're now agentic coding. All the principles of AI coding directly apply to agentic coding. Okay, agentic coding is a superset of AI coding. You want to focus on principles, not tools. All right? and you want to master the big three, that's going to show up in every tool, in every agent, in every multi-agent system context model prompt.""",
        "start_time": 1350,
        "end_time": 1432
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
        "video_id": "6fCqj4xFCZI",
        "title": "How Claude Code CHANGED Engineering Forever (and what's next)",
        "channel": "IndyDevDan",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": avg_tokens
        }
    }
    
    output_file = Path("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_claude_engineering_forever_6fCqj4xFCZI.json")
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