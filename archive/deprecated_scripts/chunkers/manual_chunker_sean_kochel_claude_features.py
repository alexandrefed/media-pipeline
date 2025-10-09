#!/usr/bin/env python3
"""
Manual chunker for Sean Kochel's "Code 10x Better With These 5 Claude Code Features"
Video ID: eIUYSC6SilA

Content Type: Advanced Feature Tutorial / Workflow Optimization
Channel: Sean Kochel
Strategy: Five systematic features with detailed implementation:
1. Planning Mode - Thinking before action
2. Custom Commands - Workflow automation
3. Project Documentation - Context preservation 
4. MCP Server Integration - Real documentation access
5. Sub-agents - Parallel processing power

Note: This follows Sean Kochel's advanced tutorial format with emphasis on
professional workflow optimization and productivity gains.
Chunk size: 180-280 tokens for feature-focused content with implementation details.
"""

import json
import tiktoken

def count_tokens(text):
    """Count tokens using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def create_manual_chunks():
    chunks = []
    
    # Chunk 1: Hook + Problem Statement + Claude Code Superiority
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "Claude Code: King of AI Coding with Hidden Power",
        "text": """Claude Code is the absolute king of the hill when it comes to AI coding and that is a hill that I'm willing to die on. But the thing is most people are only really using 10% of its power because there's actually a few hidden features inside of Claude Code that unless you've done some real digging, you're probably not aware of. And in this video, I'm going to break down the ones that can impact your coding workflows the most.

So, let's see if we can get this bad boy done in less than 15 minutes. I'm going to break down each feature and how to use it in the context of a real project. And so this video is going to be great for you if you're already using Claude Code, Gemini CLI, Cursor, Windsurf, or some other agentic IDE, and you want to really level up how you are using them because we are rapidly moving toward a world where learning to wield the context of what you are building is the next valuable skill set that you need to have.""",
        "start_time": 0,
        "end_time": 90,
        "token_count": count_tokens("""Claude Code is the absolute king of the hill when it comes to AI coding and that is a hill that I'm willing to die on. But the thing is most people are only really using 10% of its power because there's actually a few hidden features inside of Claude Code that unless you've done some real digging, you're probably not aware of. And in this video, I'm going to break down the ones that can impact your coding workflows the most.

So, let's see if we can get this bad boy done in less than 15 minutes. I'm going to break down each feature and how to use it in the context of a real project. And so this video is going to be great for you if you're already using Claude Code, Gemini CLI, Cursor, Windsurf, or some other agentic IDE, and you want to really level up how you are using them because we are rapidly moving toward a world where learning to wield the context of what you are building is the next valuable skill set that you need to have.""")
    }
    
    # Chunk 2: Project Context + Old Workflow Problems
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "The Old Workflow Problem: Manual Prompt Chaining Waste",
        "text": """Okay, guys. So, we have this super simple boilerplate code for an app that I have been thinking up and obviously the UI is very ugly. Now the idea behind it is it is an app blocker that lets you choose the apps you want to block and then in order to actually unlock your phone you have to complete like productive educational type content. So we're going to use this app for showcasing some of these features.

My old workflows used to look something like this: go to Claude manually, run it through a series of different prompts, grab the outputs, send those outputs into some next prompt that I have, chain that along for a few times, and then eventually after step five, 6, 7, 8, send it to a tool that can handle doing actual task generation or code generation. Kind of a pain though, you would end up getting good outputs at the end. But still, it was a major workflow where you would waste 2 3 4 5 hours every single week having to repeat that process and switch context all the time.""",
        "start_time": 90,
        "end_time": 180,
        "token_count": count_tokens("""Okay, guys. So, we have this super simple boilerplate code for an app that I have been thinking up and obviously the UI is very ugly. Now the idea behind it is it is an app blocker that lets you choose the apps you want to block and then in order to actually unlock your phone you have to complete like productive educational type content. So we're going to use this app for showcasing some of these features.

My old workflows used to look something like this: go to Claude manually, run it through a series of different prompts, grab the outputs, send those outputs into some next prompt that I have, chain that along for a few times, and then eventually after step five, 6, 7, 8, send it to a tool that can handle doing actual task generation or code generation. Kind of a pain though, you would end up getting good outputs at the end. But still, it was a major workflow where you would waste 2 3 4 5 hours every single week having to repeat that process and switch context all the time.""")
    }
    
    # Chunk 3: Feature 1 Introduction - Planning Mode Concept
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "Feature 1: Planning Mode - Thinking Before Action",
        "text": """Well, one of Claude Code's surprisingly great features is planning. Now, a lot of people, especially vibe coders, make the mistake of just giving a super loaded prompt to Claude or Gemini and just expecting that it's going to be able to make you this amazing, spectacular thing in one shot.

Now, what I found is that giving thinking steps before we get to action steps actually gets you a much better result because all of the tokens that we have to work with are being focused on the specific context of thinking about the problem and the best way to implement a solution instead of using those tokens to generate the actual code for that solution. So imagine a world where you have 120,000 set tokens that you can use. Well, we would want to use them all for thinking about the problem as opposed to writing the actual code for the problem.""",
        "start_time": 180,
        "end_time": 270,
        "token_count": count_tokens("""Well, one of Claude Code's surprisingly great features is planning. Now, a lot of people, especially vibe coders, make the mistake of just giving a super loaded prompt to Claude or Gemini and just expecting that it's going to be able to make you this amazing, spectacular thing in one shot.

Now, what I found is that giving thinking steps before we get to action steps actually gets you a much better result because all of the tokens that we have to work with are being focused on the specific context of thinking about the problem and the best way to implement a solution instead of using those tokens to generate the actual code for that solution. So imagine a world where you have 120,000 set tokens that you can use. Well, we would want to use them all for thinking about the problem as opposed to writing the actual code for the problem.""")
    }
    
    # Chunk 4: Planning Mode Access + Professional Planning Principle
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Planning Mode Access: Shift+Tab and the 75% Rule",
        "text": """Now, the way that we're going to do that is when we're in our Claude Code terminal. So, we have different modes, and we can hit shift tab to toggle between them. One is like a generalized help mode, and then we have a auto apply these edits mode, and then we have a planning mode, which we're going to use.

Now, I tried to skip this process recently to see if the system could actually vibe code one shot without this planning stage, and the results were pretty miserable. I lost 6 hours of my life and eventually had to scrap the project and start over. Now, proper planning would have avoided that disaster altogether.

Here's the brutal truth. If you do not spend 75% of your time planning, you're going to end up spending 95% of your time fixing and then giving up and fixing ain't fun. Serious professionals spend 80% of their time planning and then the code flows through from there.""",
        "start_time": 270,
        "end_time": 360,
        "token_count": count_tokens("""Now, the way that we're going to do that is when we're in our Claude Code terminal. So, we have different modes, and we can hit shift tab to toggle between them. One is like a generalized help mode, and then we have a auto apply these edits mode, and then we have a planning mode, which we're going to use.

Now, I tried to skip this process recently to see if the system could actually vibe code one shot without this planning stage, and the results were pretty miserable. I lost 6 hours of my life and eventually had to scrap the project and start over. Now, proper planning would have avoided that disaster altogether.

Here's the brutal truth. If you do not spend 75% of your time planning, you're going to end up spending 95% of your time fixing and then giving up and fixing ain't fun. Serious professionals spend 80% of their time planning and then the code flows through from there.""")
    }
    
    # Chunk 5: Feature 2 Introduction - Custom Commands Motivation
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Feature 2: Custom Commands - Ending Repetitive Workflow Frustration",
        "text": """Feature two, probably one of my favorite features, Claude Code commands. You know, sometimes it feels like you just you go through some badass series of prompts, getting these dope outputs, you're like in total beast mode, and you feel like you're the and nothing can stop you. The only practical downside to that is that it takes time, right? And you got to be super locked into what you are doing. Now, if you have a job or if you run a business, you know that time is not exactly a luxurious commodity that we have to just throw around.

I'll give you an example from one of my own workflows. Anytime I get like a UX or a UI that I'm not really happy with, I tend to go through this series of steps. I ask the language model to dial it in based on number one, my app's style guide. Number two, brainstorming the various states that this screen could exist in. What happens if there's empty data? What happens if there's a failure? What happens if there's a bunch of data?""",
        "start_time": 360,
        "end_time": 450,
        "token_count": count_tokens("""Feature two, probably one of my favorite features, Claude Code commands. You know, sometimes it feels like you just you go through some badass series of prompts, getting these dope outputs, you're like in total beast mode, and you feel like you're the and nothing can stop you. The only practical downside to that is that it takes time, right? And you got to be super locked into what you are doing. Now, if you have a job or if you run a business, you know that time is not exactly a luxurious commodity that we have to just throw around.

I'll give you an example from one of my own workflows. Anytime I get like a UX or a UI that I'm not really happy with, I tend to go through this series of steps. I ask the language model to dial it in based on number one, my app's style guide. Number two, brainstorming the various states that this screen could exist in. What happens if there's empty data? What happens if there's a failure? What happens if there's a bunch of data?""")
    }
    
    # Chunk 6: UX Workflow Steps + Time Cost Analysis
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "The Time Cost: 30 Minutes Per Cycle = 3 Weeks Lost Per Year",
        "text": """What are my overall UX best practices and guidelines that the app should be following at all times? Number four, if you build new components, go lint them so that when I go to build this thing, it's not broken. Number five, can you confirm that the changes were actually made and that they specifically comply to numbers 1, two, and three that we just went through? Six, can you go through and now evaluate everything you just went through against the objective standard one more time? And then number seven, if it's all well and good, commit the changes.

Now, the standard process for that usually entails me giving a prompt and having to sit here to wait for it to finish what it's doing and then guide it to the next stage. So, if we sat here and honestly calculated how much time that takes, probably 30 minutes every time we need to go through one of these iterative cycles to really dial in on something we're happy with, five times a week, we'll say conservatively, we're talking about 3 weeks of loss time over the course of a year.""",
        "start_time": 450,
        "end_time": 540,
        "token_count": count_tokens("""What are my overall UX best practices and guidelines that the app should be following at all times? Number four, if you build new components, go lint them so that when I go to build this thing, it's not broken. Number five, can you confirm that the changes were actually made and that they specifically comply to numbers 1, two, and three that we just went through? Six, can you go through and now evaluate everything you just went through against the objective standard one more time? And then number seven, if it's all well and good, commit the changes.

Now, the standard process for that usually entails me giving a prompt and having to sit here to wait for it to finish what it's doing and then guide it to the next stage. So, if we sat here and honestly calculated how much time that takes, probably 30 minutes every time we need to go through one of these iterative cycles to really dial in on something we're happy with, five times a week, we'll say conservatively, we're talking about 3 weeks of loss time over the course of a year.""")
    }
    
    # Chunk 7: Custom Commands Setup + Implementation
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Setting Up Custom Commands: .claude/commands Directory",
        "text": """Well, custom Claude commands help us put an end to that frustration. So inside of our project, we have this directory that's .claude. And so if we open that up and right-click on it and make a new folder, we can call this folder or this directory commands. Now inside of this any markdown file that we create, so we can call this UI_UX_improver.md. And I can put that process that I was just describing to you guys in there, right?

So any markdown file that we put inside of this commands folder can be accessed via our command line right here. So if I was to go exit out of this for example and then I was to start Claude Code back up in the terminal and I hit this slash symbol, we're going to see that now I have this UI UX improver. So now when we go to the command line and we run that, we can access that save prompt and kick off Claude Code executing through all of those steps.""",
        "start_time": 540,
        "end_time": 630,
        "token_count": count_tokens("""Well, custom Claude commands help us put an end to that frustration. So inside of our project, we have this directory that's .claude. And so if we open that up and right-click on it and make a new folder, we can call this folder or this directory commands. Now inside of this any markdown file that we create, so we can call this UI_UX_improver.md. And I can put that process that I was just describing to you guys in there, right?

So any markdown file that we put inside of this commands folder can be accessed via our command line right here. So if I was to go exit out of this for example and then I was to start Claude Code back up in the terminal and I hit this slash symbol, we're going to see that now I have this UI UX improver. So now when we go to the command line and we run that, we can access that save prompt and kick off Claude Code executing through all of those steps.""")
    }
    
    # Chunk 8: Force Multiplier Effect + Context Consistency Problem
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "The Force Multiplier: Consistency at 11pm = Quality at 11am",
        "text": """So, this isn't just about saving prompts, right? It is a force multiplier where we can take existing workflows and scale our ability to loop through those without us needing to be there. And it's not just about time saved. It's also about the consistency of our outputs.

And the fact of the matter is these language models in their present state are always going to drop context at one point or another. So you need to build a habit of looping back through things that you know are important and making sure it still considers those things as you build. Because look, when it's 11 p.m. and you're tired and you're in front of your computer and you're trying to fix something, you are inevitably going to skip steps of your process. Maybe you get through two of the seven steps and then you go to bed and you wake up tomorrow and you're not 100% sure of where you left off.

So part of this is making sure that the work you do at 11 p.m. is just as much quality and done just as well as the work that you do at 11:00 a.m.""",
        "start_time": 630,
        "end_time": 720,
        "token_count": count_tokens("""So, this isn't just about saving prompts, right? It is a force multiplier where we can take existing workflows and scale our ability to loop through those without us needing to be there. And it's not just about time saved. It's also about the consistency of our outputs.

And the fact of the matter is these language models in their present state are always going to drop context at one point or another. So you need to build a habit of looping back through things that you know are important and making sure it still considers those things as you build. Because look, when it's 11 p.m. and you're tired and you're in front of your computer and you're trying to fix something, you are inevitably going to skip steps of your process. Maybe you get through two of the seven steps and then you go to bed and you wake up tomorrow and you're not 100% sure of where you left off.

So part of this is making sure that the work you do at 11 p.m. is just as much quality and done just as well as the work that you do at 11:00 a.m.""")
    }
    
    # Chunk 9: Feature 3 - Project Documentation Problem
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Feature 3: Project Documentation - Solving the Memory Problem",
        "text": """So feature three is initializing your Claude project to provide documentation to the system. One of the more frustrating things that you can experience when you're doing AI coding is solving a problem in one coding session and then running into that same exact problem again and again and again. And sometimes it feels like Claude Code has simply forgotten because when you clear the context it literally does.

So one of the things that was great about Cursor rules for example was the ability to kind of steer the ship with your own conventions. Well Claude Code gives us an even better version of Cursor rules called the CLAUDE.md file. So to get started, simply type /init into your Claude terminal and then hit enter. And what this is going to do is it is going to initialize this CLAUDE.md file and is going to actually document your codebase and place it in that file.""",
        "start_time": 720,
        "end_time": 810,
        "token_count": count_tokens("""So feature three is initializing your Claude project to provide documentation to the system. One of the more frustrating things that you can experience when you're doing AI coding is solving a problem in one coding session and then running into that same exact problem again and again and again. And sometimes it feels like Claude Code has simply forgotten because when you clear the context it literally does.

So one of the things that was great about Cursor rules for example was the ability to kind of steer the ship with your own conventions. Well Claude Code gives us an even better version of Cursor rules called the CLAUDE.md file. So to get started, simply type /init into your Claude terminal and then hit enter. And what this is going to do is it is going to initialize this CLAUDE.md file and is going to actually document your codebase and place it in that file.""")
    }
    
    # Chunk 10: CLAUDE.md Contents + Dynamic Memory Feature
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "CLAUDE.md Contents + Dynamic Memory with Context7 MCP",
        "text": """So once this thing goes through and generates again, it's going to create a comprehensive overview of our project from terminal commands that do certain things, the actual architecture and tech stack, the core architectural patterns of our project, important user flows, and other important pieces of information like our component patterns, how things are being built, what the data models look like, how the navigation is meant to work, how the testing is meant to work, and so on.

Now, one really cool feature here is that we can incorporate new documentation on the fly. Now, let's say for this app that we wanted to like add some agentic capabilities and so we wanted to make sure that it had all the documentation it needs for Crew AI. Well, we could tell Claude that every time it plans a new feature using Crew AI, it must check the most up-to-date documentation using the Context7 MCP.

So, if I hit this pound symbol, we can see that it goes into this memorize mode. So if I came through here now, I could say every time you enter the planning phase for a feature that includes Crew AI, you must check the most up-to-date documentation using the Context7 MCP server.""",
        "start_time": 810,
        "end_time": 900,
        "token_count": count_tokens("""So once this thing goes through and generates again, it's going to create a comprehensive overview of our project from terminal commands that do certain things, the actual architecture and tech stack, the core architectural patterns of our project, important user flows, and other important pieces of information like our component patterns, how things are being built, what the data models look like, how the navigation is meant to work, how the testing is meant to work, and so on.

Now, one really cool feature here is that we can incorporate new documentation on the fly. Now, let's say for this app that we wanted to like add some agentic capabilities and so we wanted to make sure that it had all the documentation it needs for Crew AI. Well, we could tell Claude that every time it plans a new feature using Crew AI, it must check the most up-to-date documentation using the Context7 MCP.

So, if I hit this pound symbol, we can see that it goes into this memorize mode. So if I came through here now, I could say every time you enter the planning phase for a feature that includes Crew AI, you must check the most up-to-date documentation using the Context7 MCP server.""")
    }
    
    # Chunk 11: Context Switching Cost + Feature 4 Introduction
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Death by a Thousand Cuts: Context Switching + MCP Integration",
        "text": """Because there's a big hidden cost in context switching. Meaning every single time you need to break out of your workflows to go pull documentation, have to tell it a specific prompt saying, "Hey, and by the way, don't screw up again." And like, "Can you please actually use the real documentation that I want you to use, right? Those small little things eat away at us, right? It's like death by a thousand cuts every 5 minutes that you have to take to go do something that could have been just integrated into your workflows automatically really kills your progress over time.

Claude Code can in fact interact with MCP servers. Probably the single most frustrating thing that can happen is when your AI coding tool uses a very outdated version of a tool or when it just makes something up entirely that doesn't even exist. I once had Cursor make up an entirely not real series of steps to configure a FastAPI server. And I had to spend 30 minutes sweating it out, wondering why my server wasn't starting up, wondering what had gone wrong, cursing myself to kingdom come, only to realize eventually that the functions it was giving me to instantiate the server were not actually real.""",
        "start_time": 900,
        "end_time": 990,
        "token_count": count_tokens("""Because there's a big hidden cost in context switching. Meaning every single time you need to break out of your workflows to go pull documentation, have to tell it a specific prompt saying, "Hey, and by the way, don't screw up again." And like, "Can you please actually use the real documentation that I want you to use, right? Those small little things eat away at us, right? It's like death by a thousand cuts every 5 minutes that you have to take to go do something that could have been just integrated into your workflows automatically really kills your progress over time.

Claude Code can in fact interact with MCP servers. Probably the single most frustrating thing that can happen is when your AI coding tool uses a very outdated version of a tool or when it just makes something up entirely that doesn't even exist. I once had Cursor make up an entirely not real series of steps to configure a FastAPI server. And I had to spend 30 minutes sweating it out, wondering why my server wasn't starting up, wondering what had gone wrong, cursing myself to kingdom come, only to realize eventually that the functions it was giving me to instantiate the server were not actually real.""")
    }
    
    # Chunk 12: MCP Setup + Clerk Authentication Example
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "MCP Setup: claude_desktop_config.json + Live Clerk Example",
        "text": """Now, obviously MCP servers like Context7 help solve that problem. And a cool fun fact is that Claude Code can actually integrate directly with other MCP servers. So, in order to do this, all you need to do is go to your root project directory where you're using Claude Code and create claude_desktop_config.json. And then once you have that file, you're just going to paste in like a basic MCP server configuration, right? where we specify, hey, these are the MCP servers and then we have an object for every single server.

Now, from here, you would just need to exit out of Claude Code, start it back up, and then boom, it is immediately ready to use inside of your project. And we could confirm this by typing /mcp and it's going to show you all of the MCP servers that it's currently connected to.

So let's say that we wanted to use Clerk for authentication. We could say I'd like to use Clerk for authentication in my Expo app. Please use Context7 MCP to fetch the documentation and build an implementation plan. And now boom, we're going to pop up. We're going to see that the tool is being used.""",
        "start_time": 990,
        "end_time": 1080,
        "token_count": count_tokens("""Now, obviously MCP servers like Context7 help solve that problem. And a cool fun fact is that Claude Code can actually integrate directly with other MCP servers. So, in order to do this, all you need to do is go to your root project directory where you're using Claude Code and create claude_desktop_config.json. And then once you have that file, you're just going to paste in like a basic MCP server configuration, right? where we specify, hey, these are the MCP servers and then we have an object for every single server.

Now, from here, you would just need to exit out of Claude Code, start it back up, and then boom, it is immediately ready to use inside of your project. And we could confirm this by typing /mcp and it's going to show you all of the MCP servers that it's currently connected to.

So let's say that we wanted to use Clerk for authentication. We could say I'd like to use Clerk for authentication in my Expo app. Please use Context7 MCP to fetch the documentation and build an implementation plan. And now boom, we're going to pop up. We're going to see that the tool is being used.""")
    }
    
    # Chunk 13: Advanced MCP Integration + Evaluator-Optimizer Loops
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "Advanced MCP Integration: Playwright Testing + Evaluator Loops",
        "text": """Now let's think back to those custom commands that we are making for the UX and the UI of our project. So if you remember in step five, we had this option for confirm the changes are applied. Now what it would do if we left it just like this is it would actually just look at the code and make sure that it did the thing that it thought it was doing. But what we could do for example now is say use the Playwright MCP server to make sure your outputs conform to the plan from steps one to three.

And then what we could do is we can come down here to step six where it grades. If the grade fails with a score of less than six out of 10, redevelop a plan, implement the plan and test again with Playwright until the score is above a seven.

So, how cool is something like this where we can give it a style guide and really clear UX guidelines. We can have it implement that plan, grade itself against the plan, take an actual snapshot of its adherence to the plan, and then use the language model's multimodal capabilities to give itself a grade and continue that process until we get an output that is actually high quality. These types of evaluator optimizer loops are really, really cool, and Claude commands help make that happen for us.""",
        "start_time": 1080,
        "end_time": 1170,
        "token_count": count_tokens("""Now let's think back to those custom commands that we are making for the UX and the UI of our project. So if you remember in step five, we had this option for confirm the changes are applied. Now what it would do if we left it just like this is it would actually just look at the code and make sure that it did the thing that it thought it was doing. But what we could do for example now is say use the Playwright MCP server to make sure your outputs conform to the plan from steps one to three.

And then what we could do is we can come down here to step six where it grades. If the grade fails with a score of less than six out of 10, redevelop a plan, implement the plan and test again with Playwright until the score is above a seven.

So, how cool is something like this where we can give it a style guide and really clear UX guidelines. We can have it implement that plan, grade itself against the plan, take an actual snapshot of its adherence to the plan, and then use the language model's multimodal capabilities to give itself a grade and continue that process until we get an output that is actually high quality. These types of evaluator optimizer loops are really, really cool, and Claude commands help make that happen for us.""")
    }
    
    # Chunk 14: Feature 5 Introduction - Sub-Agents Concept
    chunk_14 = {
        "chunk_index": 14,
        "chapter_title": "Feature 5: Sub-Agents - The 10x Productivity Dream",
        "text": """A lot of the time I've just wished that I could have like 10 instances of Cursor going at the same time. Like I see all these things that need to be done and it's like man I really got to sit here and just go piece by piece letting these things roll out their changes one by one and then move to the next one when I'm ready.

Now, one of the coolest features that is actually somewhat ambiguous, especially if you are a beginner and you downloaded this thing because you heard about it and you started coding with it and you're like, "Wow, this is awesome." One of the most totally amazing features that you might not be aware of is that you can actually kick off or spawn multiple sub agents at the same time. And the way that you do it is just by telling it to do it. What I mean is you can have multiple instances of Claude Code coding at the same exact time.""",
        "start_time": 1170,
        "end_time": 1230,
        "token_count": count_tokens("""A lot of the time I've just wished that I could have like 10 instances of Cursor going at the same time. Like I see all these things that need to be done and it's like man I really got to sit here and just go piece by piece letting these things roll out their changes one by one and then move to the next one when I'm ready.

Now, one of the coolest features that is actually somewhat ambiguous, especially if you are a beginner and you downloaded this thing because you heard about it and you started coding with it and you're like, "Wow, this is awesome." One of the most totally amazing features that you might not be aware of is that you might not be aware of is that you can actually kick off or spawn multiple sub agents at the same time. And the way that you do it is just by telling it to do it. What I mean is you can have multiple instances of Claude Code coding at the same exact time.""")
    }
    
    # Chunk 15: Real-World Sub-Agent Scenario
    chunk_15 = {
        "chunk_index": 15,
        "chapter_title": "Real Scenario: 4 Bugs + Personal Success Story",
        "text": """But let me break down like a real concrete scenario for this. Let's say you're working on your new project and you notice a few things. Number one, the UX that I got ah it's not really conforming to my guidelines, right? It's there, but it's not wowing me. Number two, my Clerk authentication seems to be working, but it's not actually storing the users into my database. Number three, the Stripe subscription seems to be working, but it's not actually storing the subscription plan ID in my database. And number four, I've got this really annoying bug where every time I type into an input box, it unfocuses it.

Now, last week, I literally had this exact same situation when I was working on my prompt wallet app. I had three to four dope features that I wanted to build out and I had 10 to 15 like really small bugs. Well, the old me, it would have been a full day of doing stuff, right? But new me spawn up a bunch of sub agents to go tackle each one of these tasks and then go into yolo mode while I go grab a cup of coffee from down the street and then I come back and everything is done. That's not a 2x productivity increase. That is any number of productivity increase 10x plus for sure.""",
        "start_time": 1230,
        "end_time": 1320,
        "token_count": count_tokens("""But let me break down like a real concrete scenario for this. Let's say you're working on your new project and you notice a few things. Number one, the UX that I got ah it's not really conforming to my guidelines, right? It's there, but it's not wowing me. Number two, my Clerk authentication seems to be working, but it's not actually storing the users into my database. Number three, the Stripe subscription seems to be working, but it's not actually storing the subscription plan ID in my database. And number four, I've got this really annoying bug where every time I type into an input box, it unfocuses it.

Now, last week, I literally had this exact same situation when I was working on my prompt wallet app. I had three to four dope features that I wanted to build out and I had 10 to 15 like really small bugs. Well, the old me, it would have been a full day of doing stuff, right? But new me spawn up a bunch of sub agents to go tackle each one of these tasks and then go into yolo mode while I go grab a cup of coffee from down the street and then I come back and everything is done. That's not a 2x productivity increase. That is any number of productivity increase 10x plus for sure.""")
    }
    
    # Chunk 16: Two Implementation Approaches + Live Example
    chunk_16 = {
        "chunk_index": 16,
        "chapter_title": "Sub-Agent Implementation: Multiple Terminals vs Tell Claude",
        "text": """Now there's two ways we could think about doing this, right? Number one is we could actually just come over here and create a new terminal every single time. Right? So I could come in here, I could say Claude, I could come in here, I could do another Claude, and I could use this to solve each of those problems. So in this specific case, I have three different versions of this up that could all go out there and start making changes.

Or another option, we can literally tell Claude to kick off sub agents for each of those problems. So let's look at an example of that. We could say kickoff sub agents to address each of the following. Research actual standard US best practices from FAANG style companies and B2B SaaS giants and grade our implementation against it. Number two, check out our style guide and ensure our app conforms to it screen by screen kicking off sub agents for each screen. Research performance optimization for Expo and see how our app structure can be optimized further. And then number four, use the Context7 MCP to check out Clerk's payments system and build a plan, but don't implement it for using them instead of Stripe.""",
        "start_time": 1320,
        "end_time": 1410,
        "token_count": count_tokens("""Now there's two ways we could think about doing this, right? Number one is we could actually just come over here and create a new terminal every single time. Right? So I could come in here, I could say Claude, I could come in here, I could do another Claude, and I could use this to solve each of those problems. So in this specific case, I have three different versions of this up that could all go out there and start making changes.

Or another option, we can literally tell Claude to kick off sub agents for each of those problems. So let's look at an example of that. We could say kickoff sub agents to address each of the following. Research actual standard US best practices from FAANG style companies and B2B SaaS giants and grade our implementation against it. Number two, check out our style guide and ensure our app conforms to it screen by screen kicking off sub agents for each screen. Research performance optimization for Expo and see how our app structure can be optimized further. And then number four, use the Context7 MCP to check out Clerk's payments system and build a plan, but don't implement it for using them instead of Stripe.""")
    }
    
    # Chunk 17: Combining All Features + Ultimate Workflow
    chunk_17 = {
        "chunk_index": 17,
        "chapter_title": "The Ultimate Workflow: Combining All 5 Features Together",
        "text": """Now we could take this even further, right? We could instruct the system to actually create new branches so that we're not worrying about files inadvertently running into each other and overwriting each other's changes. There's a lot of cool stuff that we could add on top of this process. And we can see this now in progress where these things are running in parallel and they are all rocking it.

Now, the cool piece is that we can obviously start layering all of these different features together. Maybe when we kick off in planning mode, we actually kick off a custom command that recursively goes through and does some really robust, thoughtful, in-depth planning for our project. And maybe in that custom command process, we're actually using MCP servers that go out and do deep research for our project. Maybe it's researching the main problems that we are probably going to run into here and the different design or architecture patterns that will actually help us overcome those challenges as our app starts to grow.

And then it can go off and spawn different sub agents to grade that plan against what we actually needed done. Start actually doing the plan and then maybe even start building the scaffolding or asking the user questions to clarify based on the gaps it found in its process. So these things start to become super super super powerful when combined together.""",
        "start_time": 1410,
        "end_time": 1500,
        "token_count": count_tokens("""Now we could take this even further, right? We could instruct the system to actually create new branches so that we're not worrying about files inadvertently running into each other and overwriting each other's changes. There's a lot of cool stuff that we could add on top of this process. And we can see this now in progress where these things are running in parallel and they are all rocking it.

Now, the cool piece is that we can obviously start layering all of these different features together. Maybe when we kick off in planning mode, we actually kick off a custom command that recursively goes through and does some really robust, thoughtful, in-depth planning for our project. And maybe in that custom command process, we're actually using MCP servers that go out and do deep research for our project. Maybe it's researching the main problems that we are probably going to run into here and the different design or architecture patterns that will actually help us overcome those challenges as our app starts to grow.

And then it can go off and spawn different sub agents to grade that plan against what we actually needed done. Start actually doing the plan and then maybe even start building the scaffolding or asking the user questions to clarify based on the gaps it found in its process. So these things start to become super super super powerful when combined together.""")
    }
    
    # Chunk 18: Conclusion + Channel Direction Question
    chunk_18 = {
        "chunk_index": 18,
        "chapter_title": "Conclusion: 10x Outputs + Channel Direction for 2025",
        "text": """So that's it guys. Five Claude Code features and workflows that will 10x your outputs overnight. So I have a question for anyone still watching. I'm trying to determine the next directional push for my channel for the rest of 2025. And so I have a question. If you can comment below, what would you rather see?

Number one, learning how to build and deploy production ready AI agents using actual code instead of tools like n8n and things like that. Or number two, back-end business-oriented automations and workflows to help you actually scale the operations of your business or whatever it is that you are building. Or number three, maybe a combination of both or something else entirely.

Let me know and make sure to subscribe to the channel either way so that you can stay up to date on all of those awesome things we're going to be building together. So that is it. I'll see you in the next video.""",
        "start_time": 1500,
        "end_time": 1600,
        "token_count": count_tokens("""So that's it guys. Five Claude Code features and workflows that will 10x your outputs overnight. So I have a question for anyone still watching. I'm trying to determine the next directional push for my channel for the rest of 2025. And so I have a question. If you can comment below, what would you rather see?

Number one, learning how to build and deploy production ready AI agents using actual code instead of tools like n8n and things like that. Or number two, back-end business-oriented automations and workflows to help you actually scale the operations of your business or whatever it is that you are building. Or number three, maybe a combination of both or something else entirely.

Let me know and make sure to subscribe to the channel either way so that you can stay up to date on all of those awesome things we're going to be building together. So that is it. I'll see you in the next video.""")
    }
    
    chunks.extend([chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, chunk_9, chunk_10, chunk_11, chunk_12, chunk_13, chunk_14, chunk_15, chunk_16, chunk_17, chunk_18])
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Calculate token statistics
    total_tokens = sum(chunk["token_count"] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    # Create the final JSON structure
    result = {
        "video_id": "eIUYSC6SilA",
        "title": "Code 10x Better With These 5 Claude Code Features",
        "channel": "Sean Kochel",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens) if avg_tokens else 0
        }
    }
    
    # Write to JSON file
    output_path = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_sean_kochel_claude_features_eIUYSC6SilA.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} chunks with average {avg_tokens:.0f} tokens per chunk")
    print(f"Total tokens: {total_tokens}")
    print("Manual chunker completed successfully!")
    print("Note: This captures the complete 5-feature Claude Code tutorial with practical")
    print("implementation details, time-saving calculations, and advanced workflow combinations.")

if __name__ == "__main__":
    main()