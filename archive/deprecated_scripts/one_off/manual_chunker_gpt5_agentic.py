#!/usr/bin/env python3
"""Manual chunker for IndyDevDan's GPT-5 Agentic Coding video."""

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
    """Create manual chunks for the GPT-5 Agentic Coding video."""
    
    chunks = []
    
    # Chunk 1: Introduction and Multi-Model Setup
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "Multi-Model Agentic Architecture Introduction",
        "text": """It's incredible what you can do with a single prompt. We're running GPT-5 Mini, Nano right next to Opus, Opus 4.1, Sonnet, Haiku, and the new GPT OSS 20 billion and 120 billion that are running directly on my M4 Max. Sub-agent complete. MacBook Pro. Sub-agent. So, you can hear the agents are completing their work. Agent complete in parallel agent agent complete we have natural language responses coming back to us and at the end here we're going to get a concrete comparison of how these models performed across the most important three dimensions: performance, speed, and cost. We have a brand new agentic model lineup that we need to break down in this video. We're going to look at a concrete way of how we can flatten the playing field to really understand how these models perform side by side. All of our Claude Code sub-agents running in their own respective nano agents have finished their work.""",
        "start_time": 0,
        "end_time": 60
    }
    
    # Chunk 2: LLM as Judge System and Core Questions
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "LLM as Judge Evaluation Framework",
        "text": """All set and ready for the next step. Dan, we have concrete responses and concrete grades for every single model. So we are using Claude Code running Opus 4.1 in the LLM as a judge pattern to determine what models are giving us the best results. And you can see something really really awesome here. Total cost on GPT OSS: $0. In this video we dive into fundamental agentic coding and attempt to answer these questions. Can GPT-5 compete with Opus 4.1? Has useful on-device local LLM performance been achieved and what's the best way to organize all the compute available to you? If these questions interest you, stick around and let's see how our agents perform on fundamental.""",
        "start_time": 60,
        "end_time": 120
    }
    
    # Chunk 3: Beyond Benchmarks Philosophy
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "Deep Understanding Over Benchmark Regurgitation",
        "text": """So, as you've seen already, every single tech YouTuber, content creator, they've turned the camera on, recorded the screen, and literally just spat back out the benchmarks of all these brand new models back out to you. Just regurgitated exactly what the post tells you itself. Okay, if you've been with the channel for any amount of time, you know that we don't do that here. We dive deeper. We actually use this technology and we develop a deep understanding so that we can choose and select the best tool for the job at hand. There is one trend that matters above all. Right now, it doesn't matter if we're talking about GPT-5, whatever Anthropic has cooking next, the Cursor CLI or any other model that's getting put out right now, open source, closed source, there is one thing everyone is focused on. If you've been paying any attention, you know exactly what it is. It is the agent architecture.""",
        "start_time": 120,
        "end_time": 180
    }
    
    # Chunk 4: Agent Architecture and Tool Chaining
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Agent Tool Chaining vs Single Prompts",
        "text": """Why does everyone care so much about agents? First, let's understand how you and I, engineers with our boots on the ground, can have a better, deeper understanding of these models agentic performance. It's not about a single prompt call anymore. It's about how well your agent chains together multiple tools to accomplish real engineering results on your behalf. What just happened with this prompt? You can see here we have rankings. Surprisingly, we have Claude 3 Haiku outperforming all of our other models. If you look at this, it looks backward. We would expect these models to be on top and these other models to be on the bottom. What's going on?""",
        "start_time": 180,
        "end_time": 240
    }
    
    # Chunk 5: Nano Agent MCP Server Fair Playing Field
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Nano Agent MCP Server for Fair Evaluation",
        "text": """So, we're evaluating all of our models against each other in a fair playing field where we care about performance, speed, and cost as a collective. These agents are operating in a nano agent, a new MCP server to create a fair playing field where every one of these models is scaffolded with the same context and prompt, right? Two of the big three. And then we get to see how they truly perform. Right? If we put these models inside Claude Code, I can guarantee you Opus and Sonnet will outperform. But you can see here for this extremely simple task, what's the capital? we can see very different results out of the box. Okay. And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models.""",
        "start_time": 240,
        "end_time": 300
    }
    
    # Chunk 6: Higher Order Prompt Architecture
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Higher Order Prompt Multi-Model Evaluation",
        "text": """I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off. We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools. You can think of this server as like a micro Gemini CLI, a micro Codex, a micro Claude Code server that our agents can run against sub-agent complete in a fair playing field.""",
        "start_time": 300,
        "end_time": 360
    }
    
    # Chunk 7: Multi-Agent Communication Flow
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Multi-Agent Workflow Communication Pattern",
        "text": """You can see our agents are starting to respond here. sub-agent complete and then they return the results and of course sub-agent they report back to the primary agent and then our primary agent reports back to us. So this is the multi-model evaluation workflow. Higher order prompt lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. I and you need to evaluate agentic behavior against these models and understand the tradeoffs they all have. Right? performance, speed, cost. Okay, all of these mattered.""",
        "start_time": 360,
        "end_time": 420
    }
    
    # Chunk 8: Codebase Structure and GPT OSS Models
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "Nano Agent Codebase and On-Device Models",
        "text": """All right, you can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT-5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI, absolutely cooked on these models. Again, these are running right on my machine right now. Let's open up this. As usual, we have our primary agentic directories. We have our plans. We have our application specific nano agent here. We have our app docs, ai_docs, and most importantly, our commands and our agents.""",
        "start_time": 420,
        "end_time": 480
    }
    
    # Chunk 9: Prompt Orchestration Technique
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Higher and Lower Order Prompt Orchestration",
        "text": """Okay. So, if we open up commands, you can see we have this directory perf. So inside of perf you can see we have a hop a higher order prompt and we have lops okay lower order prompts. So sub-agent complete. So this is a powerful prompt orchestration or prompt engineering or context engineering whatever you want to call it. I don't care. This is a powerful prompt orchestration technique you can use to reuse complex prompts and pass in prompts as a lower level. We've covered this on the channel. You know subscribe, like, do all that good stuff so you don't miss out on these advanced prompt engineering techniques. But you can see here we have a simple grading system. All right, S through F where S is the best and F is the worst.""",
        "start_time": 480,
        "end_time": 540
    }
    
    # Chunk 10: LLM as Judge Grading System
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "Claude Code Opus 4.1 as LLM Judge",
        "text": """We have a classic prompt format. We can collapse everything to quickly understand it, right? Use the nano agent MCP server, execute and then report the results in the response format, right? And so you can see the response format is a simple grading scheme. We are using Claude Code Opus 4.1 as an LLM as a judge to manage all this for us. And then inside the evaluation details, we're just passing in the lops, the lower order prompts, right? The prompts that contain the detail that we want to swap in and out as we evaluate different agentic behavior.""",
        "start_time": 540,
        "end_time": 600
    }
    
    # Chunk 11: GPT-5 Sub-Agent Architecture
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Claude Code Sub-Agent Implementation",
        "text": """All right, if we open up the terminal again, we can see how we're doing here. Looks like we are waiting on GPT OSS 20 billion and everyone else has completed. Not a ton of surprises there, right? On device does take some time to run. There we go. We just got that completed and now Claude Code is going to formulate these results into a concrete response for us. It's going to do the evaluation. So you can see those tokens streaming in there. Hopefully I still have enough Opus for a great evaluation here. Let's see how that goes. But so we have a higher order prompt here and then you know here's our eval one that we ran. This is our dummy test. So you can see the structure here, right? We're firing off Claude Code sub-agents and we're having our sub-agents then fire off our nano agent server. So if we open up GPT-5 nano right so this is a Claude Code sub-agent and all it does is it takes whatever prompt was passed in it has access to a single tool right our MCP nano prompt nano agent tool and then we just pass in whatever our parent gives us right whatever the primary agent gives us so simple enough you can imagine that we all set ready for your next step just continue doing this along every other model we want to run so you can see here.""",
        "start_time": 600,
        "end_time": 720
    }
    
    # Chunk 12: On-Device Local Models Performance
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "128GB M4 Max On-Device Model Performance",
        "text": """Here's GPT-5 uh mini, right? But we can easily just swap this out, right? You can see here there's nano, here's mini, here's five. And then we repeat the same thing for the correct OpenAI local models, which are absolutely mind-blowing. We have 20 billion and 120 billion running right on my M4 Max, MacBook Pro. This is a 128 GB unified memory machine. This thing is absolutely cracked. you know these models run on the device and they are doing agentic coding work as you'll see in these results. Let's go ahead and hop back to the results. Pretty excited to share this with you here. But you can see how these prompts are set up right these these are our agents and our lower order prompts just detail the exact benchmark that we want run right so on our dummy test the prompt is what's the capital of the United States respond in all your JSON format structure so we can get all the auxiliary metadata coming out of the nano agent MCP server. All right that's how this is set up.""",
        "start_time": 720,
        "end_time": 780
    }
    
    # Chunk 13: Basic Read Test Agentic Task
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "First 10 and Last 10 Lines Agentic Test",
        "text": """We have another interesting result here. Okay, you know, we have the raw outputs. Here's all of our agents that executed, right? We had nine nano agents firing off. And then we have the respective responses. Um, you can see here we're looking for first 10 lines and last 10 lines in the specific prompt format. We can take a look at the result. Let me just quickly show you exactly what that prompt looked like. So this is a lower order prompt basic read. So if we look at this, we have instructions and then we have variables. And the prompt here is the most important. So we're saying read the readme file. Provide exactly the first 10 lines and the last 10 lines of the file. So this is an agentic task. This is a little more advanced. We're just stepping up the difficulty scale just a little bit from just asking a simple question. We just want it in this exact response format.""",
        "start_time": 780,
        "end_time": 840
    }
    
    # Chunk 14: Instruction Following and Tool Use Testing
    chunk_14 = {
        "chunk_index": 14,
        "chapter_title": "Agent Communication and Tool Use Evaluation",
        "text": """Right? So we're testing for instruction following. We're testing for tool use. Right? In a second here, I'll show you the exact tools that our nano agent MCP server can call. Then we fire off all of our agents and we have an expected output. Right? So, we're just sticking to great prompt patterns. We're writing extraordinarily clearly to our agent, both our primary agent and our sub-agents, and we're, you know, being really clear about the flow of communication between our agents, right? We need to make sure that we're orchestrating the communication extraordinarily well. So, that's what we're doing here. But the key here is right here's the agentic prompt that's running. Read the readme. Give me the first 10 lines and the last 10 lines. Okay. So this is what we're evaluating our models against.""",
        "start_time": 840,
        "end_time": 900
    }
    
    # Chunk 15: Performance Speed Cost Evaluation Framework
    chunk_15 = {
        "chunk_index": 15,
        "chapter_title": "Three-Dimensional Model Evaluation Results",
        "text": """So now we can say you know for this fundamental agentic coding task, how did our models perform? Okay. And we are evaluating on performance. So did it do the job? Speed and cost. Okay. And so, you know, obviously if the model can't do the job, it doesn't matter if it's fast or how much it costs or how cheap it is, right? All right. So, you can see kind of some rough grades here, right? If you look at the overall breakdown of this task, we have some rough grades. Okay? It's not all roses when you really flatten the playing field, right? Uh take a look at Opus for instance, right? We all know that Opus costs, but we don't really realize how much this model costs. It's extraordinarily expensive. Okay. And you can see here, for some reason, GPT-5 had to churn and turn and churn its output tokens to figure out how to get this response properly. Okay. So, terrible cost there. I'm actually surprised this chewed up that many tokens. I've seen this run much better, but I have seen some weirdness with GPT-5 through the API. It's taking a crap ton of time. Maybe it's just me. Looks like that model's getting slammed.""",
        "start_time": 900,
        "end_time": 1020
    }
    
    # Chunk 16: Claude 4 Sonnet Performance Analysis
    chunk_16 = {
        "chunk_index": 16,
        "chapter_title": "Unexpected Model Performance and Format Issues",
        "text": """But then we can see something else really interesting here, right? Um there are some good fast options and you know once again we can see they absolutely cracked benchmark ghosting model Claude 4 Sonnet you know performing really well. Let's look at that Claude 4 Sonnet grade here. It actually got a D. Wow. Why did it get a D? Performance does not look good. Right. So if we look for that Claude 4 response. Yeah. So you can see what's happening here. Right. It's not giving us that exact response format. Look at it's got this preamble. Right now I'll extract the first blah blah blah blah blah. Right. That's not what we asked for. So, we have to dock points. On the other hand, though, we have some really great nano and mini GPT-5 agents performing really well. Okay. So, why are these performing well when we combine an overall grade, right? It's because once again, we're not just looking at performance. GPT-5 Nano is giving us that exact response. We were looking for the first 10 lines and the last 10. And then we have last 10 right here. So, very clear, very clean.""",
        "start_time": 1020,
        "end_time": 1140
    }
    
    # Chunk 17: File Operations Test Introduction
    chunk_17 = {
        "chunk_index": 17,
        "chapter_title": "Advanced File Operations Agentic Test",
        "text": """Let me show you another interesting example where we can push these models to do more hop a file operations test. So not only are our models going to read, they're going to write files here. So let's fire this off and let's understand what this prompt does. So file operations, this prompt is a little more involved. Here's the prompt that we're passing in to every nano agent. Complete the following tasks. Read Claude settings JSON. Extract all the unique hook names. And then create a JSON file with this structure. It needs to be precise about the JSON structure. Create another file with the content model name was here. Successfully completed operations test. And then you list the current directory to show the files created. This is a really interesting one. Right. Again, we're just slowly pushing up the difficulty level for our agents to battle on a fair playing field. Okay. Okay, I think this is really really important for truly understanding agentic capability.""",
        "start_time": 1140,
        "end_time": 1200
    }
    
    # Chunk 18: On-Device GPT OSS Impressive Performance
    chunk_18 = {
        "chunk_index": 18,
        "chapter_title": "GPT OSS On-Device Agentic Coding Success",
        "text": """But if we scroll down to the bottom here, you can see our parallel sub-agents are getting to work here. There's a there's a Claude version, there's a Haiku version, there's GPT-5 mini, there's our OSS, right? Open-source 20 billion running right on my device. Right, we can click into this. Check this out. It has read the file and it outputted this like check. This is so incredible. I got to say out of all the models that were released, you know, Opus 4.1, GPT-5, so far I'm most impressed with the open source models from sub-agent. Uh this is a viable agentic coding happening on device right now. Okay, so this is sub-agent complete. Very very very crazy. Okay, very interesting. And let's close this, open up the terminal and see our agents working. You can see most of them have already finished. Our OSS 20 billion is still formulating its output response there.""",
        "start_time": 1200,
        "end_time": 1260
    }
    
    # Chunk 19: Surprising Results Analysis
    chunk_19 = {
        "chunk_index": 19,
        "chapter_title": "Mini and Nano Models Outperforming Expectations",
        "text": """All right, so let's see what we have here. Surprising results, right? Take a look at the results. Not what you would expect, right? These 5 nanos and 5 minis seem to be very good, very fast, accurate instruction following agents. We even got OSS 20 billion operating very very quickly. Okay. And so, you know, it's so interesting to see these results, right? Let's go ahead and take a look at the actual prompt we're looking for. And then we can, you know, double check some of this work, right? Let's look at this prompt in detail. You can see all these files, right? These are agentic tasks calling tools, right? Calling a list of tools to accomplish the result.""",
        "start_time": 1260,
        "end_time": 1320
    }
    
    # Chunk 20: Task Completion Verification
    chunk_20 = {
        "chunk_index": 20,
        "chapter_title": "GPT-5 Nano Perfect Task Execution",
        "text": """Let's look at the file operations. Okay, so read this file. We created summary model name JSON and then we created a model was here and then we listed all the results inside of the agent. Okay. So let's take one agent right let's let's take let's take our top and our worst performer right so GPT-5 nano how did this perform right so let's look for this we should have this here now so we have the model name GPT-5 nano here are all the Claude Code hook names pre-post notification stop sub pre blah blah blah right so perfect format there what else did we ask for model signature name let's open this up and again let's look for GPT nano and you can see GPT-5 nano was here successfully completed file operations. Okay, exactly what we were looking for. And then list directory. So very precise, right? You know, it read a file, it outputted a JSON structure, and then it wrote two files, right? It wrote these two files.""",
        "start_time": 1320,
        "end_time": 1380
    }
    
    # Chunk 21: Opus Performance vs Cost Trade-off
    chunk_21 = {
        "chunk_index": 21,
        "chapter_title": "Opus Perfect Performance but High Cost",
        "text": """What happened to our best model, right? Which is by the way costing me quite a bit, right? Every time I run this, what what happened here? Let's let's take a look, right? So let's start with summary opus. Uh you can see here results look great, right? Let's look for signature opus. And once again, it accomplished the task perfectly. Okay, so if we scroll here, right, our Opus 4 got an S, right? So it performed the task perfectly. But of course, we can see speed and cost brought the grade down quite a bit. And I was actually supposed to look for let's actually look for Opus 4.1. So what happened with Opus 4.1? 4.1. Um, Opus 1 does not have an output file. Okay, so uh that does it. For some reason, Opus 4.1 just does not have an output file. Maybe this was my fault.""",
        "start_time": 1380,
        "end_time": 1440
    }
    
    # Chunk 22: Debugging Individual Sub-Agents
    chunk_22 = {
        "chunk_index": 22,
        "chapter_title": "Atomized Compute Units for Testing",
        "text": """But um you know the great part about this architecture here is maybe this is a perfect thing to kind of showcase. We can right here in the terminal fire up a Claude instance. These are all individual sub-agents, right? It's really important to atomize your units of compute so that you can test. I have a base level MCP server that's getting called out of a Claude Code sub-agent. Right? I'm explicitly saying inside these prompts, use this MCP server. I'm passing the parameters. There is zero confusion about what's going on here. Right? So this agent will run this and then it's going to report the results as is. Right? So we can go ahead and just run this against our 4.1. There we go. So there's our nano agent. And now we pass in the prompt to execute.""",
        "start_time": 1440,
        "end_time": 1500
    }
    
    # Chunk 23: On-Device 120B Model Testing
    chunk_23 = {
        "chunk_index": 23,
        "chapter_title": "GPT OSS 120 Billion Parameter On-Device Test",
        "text": """I can just you know spin up a on-device sub-agent complete GPT OSS 20 billion parameter and you know just for fun let's do that right so if I hit up here and I switch out the agent uh let's do the 120 right so we'll have the 120 run this exact same prompt again and you know it did complete its work so I'm just going to delete it here so we can rerun this okay and we're going to fire that off it's going to have the nano agent perform these tasks right so this is a ultra powerful. We're composing powerful units of compute, right? We're using the great Claude Code agent architecture with powerful capabilities to to call tools in parallel to call sub-agents and call our specific sub-agents, right? We can open up our nano agent GPT OSS 120 billion and uh you know you can see exactly what's happening here, right? Very very powerful. This is agentic coding running on my device. This is mindblowing.""",
        "start_time": 1500,
        "end_time": 1620
    }
    
    # Chunk 24: First On-Device Agentic Success
    chunk_24 = {
        "chunk_index": 24,
        "chapter_title": "Historic On-Device Agentic Coding Achievement",
        "text": """Beautiful. Look at this. 120 completed this task for us. We should have those files back now. There it is. 120. All set and ready for the next challenge. Beautiful, right? 120B completed that task. Here it is. Right. All of the hooks once again recreated. There's the signature. Right. Successfully completed file operations. Right. This is agentic coding. Our agents are operating our device. They're doing engineering work. And for the first time, we have an on-device model that is completing work on our behalf. This model when this ran, aside from the Claude Code pieces of it, right? All that agentic work happened on my device which is insanely incredible right. I'm running on a llama by the way um let me break down exactly how this so the nano agent is quite simple if we open up main here and the nano agent. I have a simple MCP server okay and it has a single tool execute an autonomous agent with natural language task so this is just like uh Claude Code's task tool right?""",
        "start_time": 1620,
        "end_time": 1740
    }
    
    # Chunk 25: Nano Agent Technical Architecture
    chunk_25 = {
        "chunk_index": 25,
        "chapter_title": "Nano Agent MCP Server Architecture",
        "text": """When it spins up generic agents or specific sub-agents, it's kind of the same deal except here we're just passing in a prompt and then our prompt gets interpreted by our nano agent and it runs a specific tool. So you can see here we just have that one tool prompt nano agent and prompt nano agent takes an agentic prompt a model and a model provider. That's it. The agentic prompt is where all the magic happens inside the nano agent. We are actually running another agent. Right? If you remember the flow here, this is what's happening. our user calling a prompt. Our primary agent is kicking off all of these different models and model providers against our nano agent MCP server. And then you know if we had some space here we would see our nano agent itself consists of a few tools.""",
        "start_time": 1740,
        "end_time": 1800
    }
    
    # Chunk 26: Nano Agent Tool Selection
    chunk_26 = {
        "chunk_index": 26,
        "chapter_title": "Simple Tool Set for Fair Comparison",
        "text": """So let's go ahead and understand the tools our nano agent has. Okay. So execute nano agent. Um at some point here we're going to see our tool selection right here. And what do we have here? Right? Get nano agent tools. Check this out. This is all it has. Right? very simple, very concise, write a subset of, you know, modern agentic coding tools, tools. Um, but you can see, you know, just read, write, list, get file, edit file, just as you would imagine, right? And, you know, you can just see all those tools here. So, how does this all run? We are running on the OpenAI agent SDK. So, if I look at create agent here, uh, we should get at some point agent, which is coming right out of the OpenAI agent SDK.""",
        "start_time": 1800,
        "end_time": 1860
    }
    
    # Chunk 27: OpenAI Agent SDK Foundation
    chunk_27 = {
        "chunk_index": 27,
        "chapter_title": "OpenAI Agent SDK for Fair Model Testing",
        "text": """We can look at the pyproject, right? And this is it, right? So this is our agent scaffolding. They have some great tooling here. I highly recommend if you want to experiment, build out with some basic agents to really understand how the most important architecture of the year and probably of the next few years is built and how to use it and how to build, you know, your own agents. This is a great way to get started quickly. The OpenAI Agent SDK is fantastic. This allows to create a very fair and balanced way to compare models, right? Because in our provider config, uh we can specify, you know, is this an Anthropic model? This is an Ollama model, right? And then we can just update the endpoint. So great way to test on a fair playing field. These all call the respective tools and get work done on our behalf.""",
        "start_time": 1860,
        "end_time": 1920
    }
    
    # Chunk 28: Breakthrough Week Analysis
    chunk_28 = {
        "chunk_index": 28,
        "chapter_title": "Agentic Coding Options Explosion",
        "text": """So that's basically the nano agent, right? It's a generic prompt that calls one of several tools and these tools just do some operation, right? And the incredible part here is that uh I think the the playing field for agents has really opened up this week. Literally just this week, we have a ton of new options for agentic coding and to get work done both on and off device. To be ultra clear here, it isn't just the model that matters, right? There's a lot of work that goes into something like Claude Code to make it the best, most efficient, most scalable, most consistent. Consistency is really important, the most consistent agent. So, I think that, you know, all these models, right, you still want a top level state-of-the-art agent. That is clearly Claude Code. I'm by no means substituting Claude Code because there is no substitute.""",
        "start_time": 1920,
        "end_time": 1980
    }
    
    # Chunk 29: Performance Speed Cost Trade-offs
    chunk_29 = {
        "chunk_index": 29,
        "chapter_title": "Understanding When to Trade Off Model Capabilities",
        "text": """What we are doing here is understanding agentic model capability and taking some time to understand when and how we can start delegating some of our work from Claude Code to alternatives that are more specialized for certain tasks. Right? Of course, there are three things that we focus on. Performance, speed, and cost. You now have more options than ever to really decide what you want to trade off. Okay, a lot of the times when you're really working and churning, the only thing that matters is performance. Okay, now you can do some really powerful things with this new Opus 4.1 GPT-5 is, I think, comparable. I'm running into issues with this model at scale. I'm more impressed and and surprised with the mini nano and the OSS models than I am with GPT-5. Not to say that GPT-5 isn't a great model. Um, I just need to spend some more time with it. need to understand it at a deeper level.""",
        "start_time": 1980,
        "end_time": 2040
    }
    
    # Chunk 30: Top Models Still Dominating
    chunk_30 = {
        "chunk_index": 30,
        "chapter_title": "S-Tier Performance Still Belongs to Top Models",
        "text": """You can see here in this agentic prompt um GPT-5 actually performed pretty well, right? So once again, very interestingly, we have nano and mini in first place when we combine a conglomerate response. We're looking for the best overall grade across performance, speed, and cost, right? But as you can see here, right, the true colors are starting to show a little bit, right? Opus 4.1, Opus 4, Sonnet 4 S tier performance. And across the the the tests that I have done, I, you know, just got some time to set up this nano agent. You know, with the kind of few tests that I've had time to dig into to understand these models at a deeper fundamental unbiased level. Pretty clear and pretty consistent that these are still your top models, but we have new viable agentic coding models. Really happy to see this.""",
        "start_time": 2040,
        "end_time": 2100
    }
    
    # Chunk 31: Beyond Single Prompts to Agentic Sequences
    chunk_31 = {
        "chunk_index": 31,
        "chapter_title": "From Prompt Chains to Arbitrary Task Sequences",
        "text": """So, so again here we're just like testing the agentic behavior of these models with these kind of intricate step-by-step again agentic prompts, right? We're out of the world of just chatting. We're out of the world of prompt chaining in specific workflows. We want arbitrary long sequences of engineering tasks completed by our models. Okay, a single prompt eval is not enough anymore. It's about the string of tasks your system can accomplish. We've scaled far beyond the prompt, far beyond the prompt chain. We're now at this agentic architecture that interacts with this environment over and over and over. Okay.""",
        "start_time": 2100,
        "end_time": 2160
    }
    
    # Chunk 32: Real Understanding vs Benchmark Browsing
    chunk_32 = {
        "chunk_index": 32,
        "chapter_title": "Feel the Tools vs Just Reading Benchmarks",
        "text": """This looks incredible. It accomplished the task. The performance is there. Of course, on the OSS um running on device, it did take quite a bit more time than these other models, but again, look at the total cost is running on my device. Uh this is just so incredible, right? I know I'm glazing hard on these models, but I think this is a big big deal right now. And I don't think many engineers understand this because you know what what do most what do most of us do? We just, you know, look at the blog post. We just scroll scroll scroll. We look at the benchmarks and then we complain about how it's only two or 3% higher and you don't really understand what it means. Okay? Like most engineers don't actually understand what you know a 2% increase in agentic coding really looks and feels like okay over the previous generation right it it's it's actually massive okay and with every bump up on all these different benchmarks you get something incredible that you can't see by just looking at the benchmark right you need to feel these tools you need to run some type of you know specialized workflow you just spend time you don't even have to run evals right if you really want to understand the model definitely run an eval. But you don't even need to go that far. You just need to spend time running these models against real problems. Okay? Don't trust any individual benchmark. It's their job to tell you that they're doing a great job.""",
        "start_time": 2160,
        "end_time": 2280
    }
    
    # Chunk 33: Context Model Prompt Fundamentals
    chunk_33 = {
        "chunk_index": 33,
        "chapter_title": "The Big Three: Context, Model, and Prompt",
        "text": """This has been a breakthrough week. It's very clear to me that there is more compute than ever to tap into. I'm able to understand and move and work through these innovations because I understand the industry at a fundamental level. Right? Everything we do is based off just one concept. The big three context, model, and prompt. Everything is based off these. If you understand these, you can build evals, you can build benchmarks, you can build agents because they're all just scaffolded on top of these, right? So, if you're interested, you know, check out Principled AI Coding. This is my hand-crafted course that I built to help you understand how to excel and how to stay relevant with today's tools and tomorrows. Thousands of engineers have taken this. They've gotten serious value out of this. You've learned how to approach the industry.""",
        "start_time": 2280,
        "end_time": 2340
    }
    
    # Chunk 34: Course Promotion and Future Agentic Coding
    chunk_34 = {
        "chunk_index": 34,
        "chapter_title": "Principled AI Coding to Agentic Engineering",
        "text": """There's going to be a big bonus for anyone that takes Principled AI Coding. You'll get a discount on the next upcoming agentic coding course. Okay? You know, this course has been out for, you know, about half a year now. All the ideas are still relevant. You can use Claude Code or whatever agentic coding tool you want inside this course. If you're interested, but you want to be prepared for what's coming next, okay? And what's coming next is serious agentic coding. It's it's beyond that. It's agentic engineering, right? You see this here, right? Um I have local models performing agentic coding tasks on our behalf, right? They're accomplishing things that previously only Claude Code could do. Okay, things are changing. The landscape is shifting. What doesn't change is fundamental principles of AI coding. Okay, because agentic coding is just a superset of AI coding.""",
        "start_time": 2340,
        "end_time": 2400
    }
    
    # Chunk 35: Tool Call Chains and Trade-off Mastery
    chunk_35 = {
        "chunk_index": 35,
        "chapter_title": "Long Tool Call Chains and Model Trade-offs",
        "text": """So, we have more compute than ever. It's not about the prompt anymore. It's not about the individual model anymore. It's about what the model can do in long chains of tool calls, right? The true value proposition of models is being exposed. It's real work end to end. And the thing to keep an eye on is, do you know how to trade off performance, cost, and speed when the time is right? Because I can guarantee you, you don't always need Opus 4. Okay? You might be able to settle with GPT-5, which is much cheaper, by the way, than Opus 4, right? Or you might be able to go further, right? You can just use 5 mini. Maybe you need to scale to Sonnet 4 for that task. Fine. But maybe, you know, you can build your own specialized small agent, right? You can build off from the nano agent codebase that is going to be available to you. Link in the description. I'm going to clean this up and make sure it's available for you to you so that you can, you know, understand agentic coding at a fundamental level.""",
        "start_time": 2400,
        "end_time": 2520
    }
    
    # Chunk 36: Infrastructure for Future Readiness
    chunk_36 = {
        "chunk_index": 36,
        "chapter_title": "Building Infrastructure for Model Capability Assessment",
        "text": """But you know maybe you can go even further beyond and use a small on-device model. These are only going to get better. So you want to have the infrastructure in place and the tooling in place to understand the capabilities so when it's ready you can hop on it. I I can tell you right now I'm going to be investing more into you know these models across the board so I know what tasks can be accomplished by what model so I can make the right tradeoff. Okay. Engineering is all about tradeoffs. performance, speed, cost. At different times of the day, based on the task you're working on, different things matter. Okay, so super long one. Thanks for sticking with me here. Um, you know where to find me every single Monday.""",
        "start_time": 2520,
        "end_time": 2574
    }
    
    # Add chunks to list with token counts
    for chunk in [chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, 
                  chunk_9, chunk_10, chunk_11, chunk_12, chunk_13, chunk_14, chunk_15, chunk_16,
                  chunk_17, chunk_18, chunk_19, chunk_20, chunk_21, chunk_22, chunk_23, chunk_24,
                  chunk_25, chunk_26, chunk_27, chunk_28, chunk_29, chunk_30, chunk_31, chunk_32,
                  chunk_33, chunk_34, chunk_35, chunk_36]:
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
        "video_id": "tcZ3W8QYirQ",
        "title": "GPT-5 Agentic Coding with Claude Code",
        "channel": "IndyDevDan",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": avg_tokens
        }
    }
    
    output_file = Path("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_gpt5_agentic_tcZ3W8QYirQ.json")
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