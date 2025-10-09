#!/usr/bin/env python3
"""Manual chunker for IndyDevDan's Codex vs Claude Code video."""

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
    """Create manual chunks for the Codex vs Claude Code video."""
    
    chunks = []
    
    # Chunk 1: Introduction and AI Coding Spectrum
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "AI Coding Spectrum: Codex vs Claude Code",
        "text": """Engineers, it's time to buckle up. OpenAI's brand new Codex and Anthropic's Claude Code sit at opposite ends of the AI coding spectrum. On the one hand, we have the new OpenAI Codex, an all-in-one developer agent running on OpenAI compute that completes tasks for you in parallel in the background. On the other end, we have Claude Code, the most performant programmable agentic coding tool. Claude Code represents a new engineering primitive. This is a massive two for one video. We're first going to take a look at Codex to see how it looks, feels, and performs. While tasks are running in the background, I have five key insights you don't want to miss right from the Claude Code team. They put out this great interview with the latent space podcast that we must discuss. We need to talk about why terminal AI coding always wins. Then we'll look at why composability matters. We'll talk about Aider versus Claude. We'll discuss why simplicity always builds the best products. And then we'll talk about how you can scale your engineering output with parallelism and background tasks. As you'll see in this video, with brand new tools like Codex, you can run many background tasks putting more compute to work for you throughout the day. Remember, if you scale your compute, you scale your success.""",
        "start_time": 0,
        "end_time": 90
    }
    
    # Chunk 2: Codex First Look and Interface
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "Codex Interface and Parallel Tasks Demo",
        "text": """Let's put Codex to work. You can see a nice clean familiar interface. It looks just like ChatGPT. I do like the product consistency. I have to say when I first saw this tool, I thought, "Wow, now they've copied Claude Code with the Codex CLI and now they've copied Devon with the Codex ChatGPT interface." Anyway, more on that later. Let's kick off some tasks. So, you can see here I have the Claude Code is programmable codebase connected on the main branch. I have no active tasks. Let's fix that. I'm going to kick off multiple tasks in parallel. Let's make the tool do what it does best. Teach me about this codebase. How is it organized? Why does it exist? One task kicked off there. Find a bug in this codebase and write a fix for it. Let's kick that off. And then let's kick off something more interesting. I'm going to say create a new engineering plan that aligns with the codebase purpose. Create a new markdown file. Don't change any code, just plan. Let's kick this off. We are setting up three instances of our codebase. We have three junior engineers, you know, three interns now working on this codebase for us and we are just sitting here. Okay, so this is a big selling point of Codex of all these powerful agentic coding tools like Devon, like Replit, right? We're just prompting and now we have full ecosystems, right? We have full codebase environments being operated on by an agentic coding tool.""",
        "start_time": 90,
        "end_time": 180
    }
    
    # Chunk 3: Codex Task Execution and Review
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "Codex Task Results and Workflow",
        "text": """So find and fix a bug. You know, a very small thing here. I actually don't think this is needed or necessary, but nevertheless, they have a fix here just to show off this workflow. We would hit push create new PR. Now we can view this pull request. So if we click this, we can see this is still work in progress. So now on GitHub, we can see that pull request. This looks great. I can go to conversation and just merge this in. And if we keep track of this change here, we open up cursor. And if we run git pull, we're going to see this change come in right here. And it looks great. That was agentically done. Eight lines of code ran outside of my developer environment. Pretty cool stuff there, right? If we hop back into the Codex interface, you can see that this is now merged. We can now hit archive task. So that's it, right? This is Codex, right? That's the basic workflow. You write a prompt, the task gets executed. You then review the code. Then you merge the code into your codebase. For these explanation tasks, basically it's just informational. So whenever we want to, we can just archive that.""",
        "start_time": 180,
        "end_time": 240
    }
    
    # Chunk 4: Claude Code Definition and Terminal Advantage
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "What is Claude Code? Terminal vs Web Apps",
        "text": """Let's go ahead and turn our attention to this fantastic interview with the Claude Code creators. Well, thank you for making the time. We're here to talk about Claude Code. Most people probably have heard of it. We think like you know quite a few people have tried it, but let's get a Chris upfront definition like what is Claude Code? Yeah, so Claude Code is Claude in the terminal. You know Claude has a bunch of different interfaces. There's desktop, there's web, and yeah, Claude Code. It runs big shout out to Boris and Cat. Claude Code is an incredible product because it runs in the terminal. It has access to a bunch of stuff that you just don't get if you're running on the web or on desktop or whatever. So, it can run bash commands. It can see all of the files in the current directory and it does all that agentically. Okay, so already we have to stop and talk about what that really means. Okay, the fact that Claude Code runs in the terminal is a critical detail to understand. Okay, the terminal is the highest leverage point for engineering work. On the left, we have control. On the right, we have ease of use. This is the plane in which all AI coding and all agentic coding tools sit on. On the left, where we have maximum control are all of our terminal applications. The terminal is where the greatest highest leverage engineering work can happen. Why? Because you have the most control. You can do everything from the terminal. But it doesn't come for free, right? Control costs time. Control costs effort. It costs experience.""",
        "start_time": 240,
        "end_time": 360
    }
    
    # Chunk 5: AI Coding Spectrum - Control vs Ease of Use
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "The AI Coding Spectrum: Terminal to Web Apps",
        "text": """Now, as we move up, we get to desktop apps. Okay. This is the happy medium. You get a lot of control, but you also get web app-like features, right? This is where our Cursors, our VS Code, and our Windsurf sit. So, this is a great place to be. And then at the top, we have our web apps. Web apps are fantastic. They're the easiest to use. Both vibe coders and senior plus level engineers spending a lot of time with web apps. This is because they are the easiest to use. The bang for your buck is the highest here at the cost of control. These easy-to-use tools are highly opinionated. They tell you what you need to do. They tell you how you need to do it and you must for the most part do it their way. So this is the trade-off we make. We have the brand new Codex. This is a web application. It's easy to use but we give up a lot of control. As engineers, you want to be able to have maximum control. And the brand new programmable agentic coding tool, Claude Code, gives us maximum control over what we're building. Right? We can build out these brand new ADWs, also known as agentic workflows that were quite literally impossible to build before this tool came into existence. This is the spectrum. It's really important to know when to trade off control for ease of use. I'm not saying any one of these is better than the other. It's really about managing trade-offs and using the best tool for the job.""",
        "start_time": 360,
        "end_time": 450
    }
    
    # Chunk 6: Claude Code as a Primitive and Simplicity Principle
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Claude Code Architecture and Do Simple Thing First",
        "text": """But yeah, it's just sort of this crazy research project and obviously it's kind of bare bones and simple. Um, but yeah, it's like a agent in your terminal. Right. Right. So this stuff starts. Yeah. So it's really important to call this out real quick. It's a crazy research project. Barebones agent in the terminal. I've talked about this a couple times on the channel, but the fact that this is an agent makes it a different type of tool. Okay, so how do you make a great agent? You have a powerful LLM that can call any tool that has the right agent architecture. This is a differentiated tool. This is a different type of application structure. Claude Code is a brand new form factor that has not existed before. It's one of the first successful multi-purpose agents. What's the process within Anthropic to like graduate one of these projects? Generally at Anthropic, we have this product principle of do the simple thing first. And I think that the way we build product is really based on that principle. So you kind of staff things as little as you can and keep things as scrappy as you can because the constraints are actually pretty helpful. For this case, we wanted to see some signs of product market fit before we scaled it. Yeah. So this is a big idea. Pack members know the KISS principle. Keep it simple stupid is the same idea. This is how you build the best tools and ship before anyone else. Simplicity is one of the most important properties in engineering work because it lets you generate proof of value.""",
        "start_time": 450,
        "end_time": 570
    }
    
    # Chunk 7: Product Management and Engineering Culture
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Claude Code Team Culture and Leadership",
        "text": """So I'm kind of curious for for Cat like how do you view PMing something like this the velocity is something I've never seen coming out of the topic. I think I PM with a pretty light touch um I think Boris and the team are like extremely strong product thinkers. So very little actually is tops down. I feel like I'm mainly there to like clear the path if anything gets in the way and just make sure that we're all good to go from like a legal marketing etc perspective. Yeah. Yeah. So I just want to shout this out. I think this is excellent PMing and really just great leadership, right? Um, at a previous position, I was a lead platform engineer using AI to predict uh information in the accounting document space. Okay, that's the TLDR. And it was one of my favorite places to work because the CTO would do exactly what Cat has mentioned here. Clear the road, make sure that we had every resource, every tool, every answer that we needed. This made it easy for the entire engineering org to focus all their time, energy, and attention on one job. And not only that, it let us spend our time in long unbroken chains of focus. That's everything in engineering. There's so much noise in the space. There's always something to miss. But that long chain of focus is what is going to differentiate your work from the engineer sitting next to you. And a lot of this is driven by great engineering culture and great leaders like Cat and Boris where they're just focused on keeping things simple and they're focused on clearing the road for the team.""",
        "start_time": 570,
        "end_time": 690
    }
    
    # Chunk 8: Aider's Influence and Claude Code's Position
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "From Aider to Claude Code Evolution",
        "text": """I'm sure you're familiar with Aider which is another thing that people in our discord loved and then when Claude Code came out the same people love Claude Code. Um any thoughts on like you know inspiration that you took from it things you did differently kind of like maybe design principle in which you went a different way. Um so Aider inspired this internal tool that we used to have at Anthropic called Clyde and that's the predecessor to Claude Code. So yeah it was uh Aider inspired Clyde which inspired Claude Code. Yeah. So, this is so cool and it makes a ton of sense. Aider is a massively important tool, not just because it's the best open source AI coding tool, but because it's paved the way for nearly every tool since its release, and that includes the new breed of agentic coding tools. Like Claude Code is uh obviously it's it's a little different than some of these other tools in that it's a lot more raw. Like I said, there isn't this kind of big beautiful UI on top of it. It's raw access to the model. It's as raw as it gets. So if you want to use a power tool that lets you access the model directly and use Claude for automating, you know, big workloads, you know, for example, if you like a thousand lint violations and you want to start a thousand instances of Claude and have it fix each one and make then make a PR then Claude Code is a pretty good tool. Got it. It's it's a tool for power workloads for power users. Yeah. Um and I think that's kind of where it fits.""",
        "start_time": 690,
        "end_time": 810
    }
    
    # Chunk 9: ROI vs Cost Discussion
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Claude Code Cost and ROI Discussion",
        "text": """The cost thing is interesting. Do people pay internally or do you get free? If you work at Anthropic, you can just run this thing as much as you want every day. Um, it's for it's for free internally. Nice, man. Imagine that. How much do you think of that being your responsibility to try and make it more efficient versus that's not really what we're trying to do with the tool? We really see Claude Code as like the tool that gives you the smartest abilities out of the model. We do care about cost in so far as it's very correlated with latency and we want to make sure that this tool is extremely snappy to use and extremely thorough in its work. We want to be very intentional about all the tokens that it produces. I think we can do more to like communicate the cost with users. Um, currently we're seeing costs around like $6 per day per active user. The way I think about it is it's a ROI question. It's not a cost question. And so if you think about, you know, an average engineer salary, like engineers are very expensive. And if you can make an engineer 50 70% more productive, that's worth a lot. Yeah. Yeah. Yeah. Yeah. So this is this is huge. I'm so glad they mentioned this. Um this is where a lot of engineers make a critical mistake. Your time is your most valuable resource. Let me say it one more time. Your time is your most valuable resource. Understanding what it's worth will pay you so much. You want to understand what your engineering time is worth and then pay to get more work done in less time.""",
        "start_time": 810,
        "end_time": 930
    }
    
    # Chunk 10: AI-Generated Code Percentage and Code Review
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "80% AI-Generated Code and Future Workflows",
        "text": """Paul from Aider always says how much of it was coded by Aider, you know. So then the question is how much of it was coded by Claude Code? I wonder if you have a number like 50 pretty high. Probably near 80. Yeah, very high. Yeah. Yeah, 80% I think is a that's a great number. If you're still typing code manually, uh I think that's an absolute disaster. You need to you need to move into at least iteratively planning with AI coding tools. Focus on the ends of the process, right? The planning and the reviewing. Lots of reviewing. A lot of human code review though. Yeah, lot of lot of human code review. I think yeah yeah yeah that's that's that's perfect right lots of human code review for Claude Code internally in the GitHub repo we have this GitHub action that runs and the GitHub action invokes Claude Code with a local uh slash command and the slash command is lint so it just runs a linter using Claude and it's a bunch of things that are pretty tricky to do with a traditional linter that's based on static analysis. Boris has just literally spelled out the future of engineering in in its like really kind of first version, right? Linting documentation, writing tests. These are just the the the low-hanging fruit of the type of workflows you can build out, right? You can with Claude Code, right? Again, with a programmable low-level terminal based tool like Claude Code, you can now build out these powerful workflows, right? You can embed your coding agent and put it anywhere in your stack. In pack, we call these ADWs. They're more commonly just known as agentic workflows, but in the future, they'll just be called scripts.""",
        "start_time": 930,
        "end_time": 1080
    }
    
    # Chunk 11: Claude Code as a Primitive
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Claude Code as Engineering Primitive",
        "text": """The way we're thinking about it is Claude Code is, like I said before, it's a primitive. So, if you want to use it to build a code review tool, you can do this. If you want to, you know, build like a security scanning vulnerability scanning tool, you can do that. If you want to build a semantic linter, you can do that. And hopefully with Claude Code, it makes it so if you want to do this, it's just a few lines of code. Yeah. So, this is incredible. And and again, that really hits on this the key idea, right? Claude Code is a primitive. It gives you full control. You can build whatever you want. And as engineers, it's important to gravitate toward, you know, an array of tools so that you can reach for the right tool for the job. And the general move for engineers is just to use the tool they're most familiar with or the most popular tool or tools that are just easy to use. But you always want to have that granular tool in the age that you're in. We are in the generative AI age. The most granular, performant, programmable tool for us right now is Claude Code. At the same time, you do want to have, you know, your powerful Codex, your Devon, your, you know, Replit v0, whatever. You want to have that in the bag as well. But it's really important to distinguish that, right? That's that's the tool for the agentic era. For the, you know, AI coding era, you know, Aider was that low-level uh tool. But I just want to give you a you know concrete framework of how you can think about how you can maximize your compute at the right level with all these tools available to you.""",
        "start_time": 1080,
        "end_time": 1200
    }
    
    # Chunk 12: Engineers Still Essential
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "AI Enhances Engineers, Doesn't Replace",
        "text": """Claude Code is a primitive. Even if we use Claude Code to write a lot of our code, it's still up to the individual who merges it to be responsible for like this being well-maintained, well documented code that has like reasonable abstractions. And so I I think that's something that will continue to happen where Claude Code isn't its own engineer that's like committing code by itself. It's still very much up to the ICs to be responsible for the code. Yeah. Yeah. This this is really important. I've never believed that narrative that AI is replacing engineers. Um even when you get to powerful agent coding tools like Codex uh Devon lovable what whatever the tool is it never replaces the engineer because someone is still reviewing that final output that final you know block of code just as you saw here right as you write your task you need to review them you need to see that there it's doing what you want the the big advantage now is that we can automate a lot of this process right we can hand off a lot of this to compute but you still need to validate. You still need to plan and review. You still need to apply your taste and judgment to what's going on and what's the best way to have taste and judgment. You've built tools yourself. You analyze the inputs and outputs yourself. Right? It doesn't matter how great or how agentic whatever the tooling gives us. You still need to at some point enter a review process. Right? AI is not replacing engineers. Engineers using AI are going to replace the non-AI engineer.""",
        "start_time": 1200,
        "end_time": 1320
    }
    
    # Chunk 13: Prototyping vs Spec-First Approach
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "Rapid Prototyping with Multiple Versions",
        "text": """As it gets easier to build stuff, it changes the way that I write software where like like Cat saying like before I would write a big design doc and I would think about a problem for a long time before I would build it sometimes for some set of problems. And now I'll just ask Claude Code to prototype like three versions of it and I'll try the feature and see which one I like better. And then that informs me much better and much faster than a doc would have. Very interesting. So this is something that I have been playing with a little bit more. I think that there's a line between, you know, which one you choose with these powerful agent coding tools. Do you go the rapid prototype route where you create multiple versions or do you, you know, go into design doc world. AI plan draft, right? Build with your AI, plan with your AI, but you first, you know, spec everything out. I think you want to be doing a little bit of both depending on the situation. Um, I think the doc PRD or spec first approach is still optimal right now. So I'm going to be comparing and contrasting the multi-version rapid prototype approach versus the spec first approach. I'll definitely share my findings on the channel.""",
        "start_time": 1320,
        "end_time": 1410
    }
    
    # Chunk 14: Parallelism in Claude Code
    chunk_14 = {
        "chunk_index": 14,
        "chapter_title": "Parallel Execution and Context Windows",
        "text": """So for example, something I'll do sometimes is if I have a planning question or a research type question, I'll ask Claude to investigate a few paths in parallel. And you can do this today if you just ask it. So say you know I want to refactor X to do Y. Can you research three separate ideas for how to do it? Do it in parallel. Use three agents to do it. Yeah. So, so, so this hints on a really powerful idea, right? I mean, you can quite literally see this inside of Codex, right? We use this idea in Codex, right? It's parallelism. Um, with compute, with these machines, with the right technique, you can do multiple things at the same time. In fact, as mentioned, this is a capability built directly into Claude Code. Claude Code is going to return some tokens here and these tokens are going to enable there it is parallel reads. Okay, so very cool. We can do the same thing here. Write a one-line summary at the top of each of those files in parallel. You can see with our prompt, right, with that IDK, right, that specific keyword, we're able to kick off a parallel read on the micro level, right? Where we're fully in control of our agentic coding tool, Claude Code. And on a more macro level, we saw that in Codex as well, right? So, you really want to be thinking about how you can parallelize your tasks. We can apply these old very consistent ideas of engineering, right? Parallelism. When you don't have blocking tasks, just apply parallelism to get more things done at the same time.""",
        "start_time": 1410,
        "end_time": 1560
    }
    
    # Chunk 15: Context Window Limitations
    chunk_15 = {
        "chunk_index": 15,
        "chapter_title": "Context Window Challenge and Future",
        "text": """Yeah. Like context, for example, is a big one where like a lot of times if you have a very long conversation and you compact a few times, maybe some of your original intent isn't as strongly present as it was when you first started. And so maybe the model like forgets some of what you originally told it to do. And so we're really excited about things like larger effective context windows so that you can have these like gnarly like really long hundreds of thousands of tokens long tasks and make sure that Claude Code is on track the whole way through. This is huge, right? This happens to me all the time. I'm sure it happens to you if you're using Claude Code, right? You always have to compact at some point. You know, they have this great auto-compact feature, but compact, just like RAG, always suffers from information loss. It's a band-aid, a decent one, but a band-aid for a problem that can only truly be solved by longer context. I think, you know, Anthropic realizes this. I think other orgs realize this. We can see this in some of the larger, you know, context window um language models. Right now, Sonnet stuck at 200k. I'm predicting that Anthropic puts out a new 500k-ish token context window model, Claude 4 Sonnet, and hopefully Claude 4 Opus. But we'll see, right? What we really need to do is get this larger keyword that Cat said there, effective context token window increased.""",
        "start_time": 1560,
        "end_time": 1680
    }
    
    # Chunk 16: Scaling Compute and Final Insights
    chunk_16 = {
        "chunk_index": 16,
        "chapter_title": "Scale Your Compute, Scale Your Success",
        "text": """What do all these powerful agentic tools mean on both ends of the spectrum? So, a couple things here. You can scale your compute even further. You want to be thinking about having compute working for you all the time, right? As much as possible. Background tasks, parallel tasks, local terminal tasks running. You want an app in every one of these categories that you can quickly jump into and get engineering work done. Ideally, you're always running something. Something's always getting completed for you in the background. Okay, this is a big theme on the channel. We're going to be exploring. This is our north star. Build a living software that works for us while we sleep. All these tools also mean that engineering velocity is going up. If you want to keep up, you have to scale your compute to scale your impact. You want to make sure that you have a low-level fully controllable terminal-based tool. And you really want to understand the terminal, right? This is the highest leverage point for engineering work. On the other end, you want to have a tool that's easy to use that you can quickly just spin up, fix bugs, fix issues, build out small to medium-sized tasks with a single prompt. We know that great planning is great prompting. And if you can write a great prompt or a plan, you can get a lot of engineering work done. Have your web app ready. The big theme here is the same. We've been talking about it week after week after week. To scale your success as an engineer, scale your compute.""",
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
        "video_id": "y-_xknNOapo",
        "title": "Claude Code INSIDERS: Codex FIRST Look and 5 AI Coding INSIGHTS",
        "channel": "IndyDevDan",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": avg_tokens
        }
    }
    
    output_file = Path("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_codex_claude_y-_xknNOapo.json")
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