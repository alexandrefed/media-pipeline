"""
Manual Chunker for AI LABS - Claude Engineer is INSANE... Upgrade Your Claude Code Workflow
Video URL: https://www.youtube.com/watch?v=6Rg5M69bMgQ
Channel: AI LABS
Duration: 704 seconds (~11.7 minutes)

This video covers SuperClaude configuration framework and Claude Code Web UI
Demonstrates 18 structured commands, 9 personas, and cross-device access
"""

import json
import os

# Video metadata
VIDEO_ID = "6Rg5M69bMgQ"
CHANNEL = "AI LABS"
TITLE = "Claude Engineer is INSANE... Upgrade Your Claude Code Workflow"

def count_tokens(text):
    """Approximate token count (1 token ~= 4 characters)"""
    return len(text) // 4

# Define chunks based on the enhanced transcript structure
chunks = []

# Chunk 1: Introduction and Overview
chunk_1 = {
    "chunk_index": 1,
    "chapter_title": "Introduction: Two Free Tools to Supercharge Claude Code",
    "text": """I really love Claude Code. The coding agent that Anthropic has built gives you so much customization that it's crazy, but I keep finding new custom ways to make it even better. Today, I want to show you two free tools that supercharge Claude Code and may change how you use it. Both tools are completely free, and I think you're going to love what they can do. Let's jump right in.""",
    "start_time": 0,
    "end_time": 30,
    "token_count": count_tokens("""I really love Claude Code. The coding agent that Anthropic has built gives you so much customization that it's crazy, but I keep finding new custom ways to make it even better. Today, I want to show you two free tools that supercharge Claude Code and may change how you use it. Both tools are completely free, and I think you're going to love what they can do. Let's jump right in.""")
}
chunks.append(chunk_1)

# Chunk 2: The Customization Challenge
chunk_2 = {
    "chunk_index": 2,
    "chapter_title": "The Challenge: Creating Workflows for Vibe Coders",
    "text": """You know that Claude Code gives you an extreme level of customization. It has these custom commands and you can even modify the CLAUDE.md file to turn it into an agent specialized for your specific task. You can create workflows, but these workflows need to be tested and take a lot of time to create by yourself, especially if you're a vibe coder who doesn't know the full development process. In that case, you won't be able to make them very well.""",
    "start_time": 30,
    "end_time": 60,
    "token_count": count_tokens("""You know that Claude Code gives you an extreme level of customization. It has these custom commands and you can even modify the CLAUDE.md file to turn it into an agent specialized for your specific task. You can create workflows, but these workflows need to be tested and take a lot of time to create by yourself, especially if you're a vibe coder who doesn't know the full development process. In that case, you won't be able to make them very well.""")
}
chunks.append(chunk_2)

# Chunk 3: Introducing SuperClaude
chunk_3 = {
    "chunk_index": 3,
    "chapter_title": "SuperClaude: Configuration Framework with 18 Commands",
    "text": """This is where the first tool I want to show you comes in. It's a configuration framework, as the author calls it. And the funny thing is, it's even called SuperClaude. Basically, it allows Claude Code to gain a new set of abilities and skills that take it to the next level. Now, what does it give you? It provides 18 structured commands and they're all focused on one thing. Then there are flags. When used with the commands, the flags give you additional functionality.""",
    "start_time": 60,
    "end_time": 90,
    "token_count": count_tokens("""This is where the first tool I want to show you comes in. It's a configuration framework, as the author calls it. And the funny thing is, it's even called SuperClaude. Basically, it allows Claude Code to gain a new set of abilities and skills that take it to the next level. Now, what does it give you? It provides 18 structured commands and they're all focused on one thing. Then there are flags. When used with the commands, the flags give you additional functionality.""")
}
chunks.append(chunk_3)

# Chunk 4: Nine Development Personas
chunk_4 = {
    "chunk_index": 4,
    "chapter_title": "Nine Development Personas for Every Stage",
    "text": """For example, it has this persona flag and you can choose between nine of them. They all represent a specific part of the development life cycle. That in itself is an amazing feature. Like if you wanted to build a landing page or a UI component, you can implement the front-end persona for that. And there are personas for literally everything: Architecture planning, Backend development, Security analysis, Problem analysis, Frontend development, And more. It's really crazy.""",
    "start_time": 90,
    "end_time": 120,
    "token_count": count_tokens("""For example, it has this persona flag and you can choose between nine of them. They all represent a specific part of the development life cycle. That in itself is an amazing feature. Like if you wanted to build a landing page or a UI component, you can implement the front-end persona for that. And there are personas for literally everything: Architecture planning, Backend development, Security analysis, Problem analysis, Frontend development, And more. It's really crazy.""")
}
chunks.append(chunk_4)

# Chunk 5: Technical Implementation
chunk_5 = {
    "chunk_index": 5,
    "chapter_title": "Under the Hood: YAML Workflows and MCP Integrations",
    "text": """Now, how does this work? I opened it up and took a look. On the back end, the developer has written configuration files in the form of custom commands and even a set of rules and configured workflows in the form of YAML files. So, in a way, it's all just prompting, but that's how you program AI agents and models. For example, in the front-end persona, it gives Claude a really robust workflow that's super beneficial for creating UI. And the workflows that the author has written give Claude Code the context on how real developers go through the development cycle.""",
    "start_time": 120,
    "end_time": 180,
    "token_count": count_tokens("""Now, how does this work? I opened it up and took a look. On the back end, the developer has written configuration files in the form of custom commands and even a set of rules and configured workflows in the form of YAML files. So, in a way, it's all just prompting, but that's how you program AI agents and models. For example, in the front-end persona, it gives Claude a really robust workflow that's super beneficial for creating UI. And the workflows that the author has written give Claude Code the context on how real developers go through the development cycle.""")
}
chunks.append(chunk_5)

# Chunk 6: MCP Server Integration
chunk_6 = {
    "chunk_index": 6,
    "chapter_title": "Four Powerful MCP Integrations",
    "text": """And not only that, it actually takes advantage of MCPs as well. You can see we have: The Context7 MCP which gets external documentation, The Sequential MCP which basically allows multi-step reasoning, The MagicUI MCP, Puppeteer MCP as well which are really great. Also, if I open the CLAUDE.md file, the whole configuration has been set up on how to actually use everything. So, this is why it's called SuperClaude.""",
    "start_time": 180,
    "end_time": 210,
    "token_count": count_tokens("""And not only that, it actually takes advantage of MCPs as well. You can see we have: The Context7 MCP which gets external documentation, The Sequential MCP which basically allows multi-step reasoning, The MagicUI MCP, Puppeteer MCP as well which are really great. Also, if I open the CLAUDE.md file, the whole configuration has been set up on how to actually use everything. So, this is why it's called SuperClaude.""")
}
chunks.append(chunk_6)

# Chunk 7: Command Examples
chunk_7 = {
    "chunk_index": 7,
    "chapter_title": "Example Commands and Flags",
    "text": """To give you an example of how the slash commands and the flags are used, if I scroll down, you can see that we have workflows like: The /build command followed by flags like: --react (to use React), --magic (to use the MagicUI MCP), --watch (to monitor development continuously). You can also see the persona has been set with the --persona front-end flag.""",
    "start_time": 210,
    "end_time": 240,
    "token_count": count_tokens("""To give you an example of how the slash commands and the flags are used, if I scroll down, you can see that we have workflows like: The /build command followed by flags like: --react (to use React), --magic (to use the MagicUI MCP), --watch (to monitor development continuously). You can also see the persona has been set with the --persona front-end flag.""")
}
chunks.append(chunk_7)

# Chunk 8: The Documentation Problem
chunk_8 = {
    "chunk_index": 8,
    "chapter_title": "The Learning Curve Problem and My Solution",
    "text": """Now, all of this is super powerful, but I found one problem the author really should have taken care of, and that's that there's no proper way to learn to use this. When I installed it and watched other videos from YouTubers, they all just demoed it. I basically found no proper guide on how to actually use it. That creates a bit of a problem because there's a learning curve with this tool given the amount of flags and tools in this.""",
    "start_time": 240,
    "end_time": 270,
    "token_count": count_tokens("""Now, all of this is super powerful, but I found one problem the author really should have taken care of, and that's that there's no proper way to learn to use this. When I installed it and watched other videos from YouTubers, they all just demoed it. I basically found no proper guide on how to actually use it. That creates a bit of a problem because there's a learning curve with this tool given the amount of flags and tools in this.""")
}
chunks.append(chunk_8)

# Chunk 9: Automated Documentation with Cursor
chunk_9 = {
    "chunk_index": 9,
    "chapter_title": "Creating AI-Readable Documentation with Cursor",
    "text": """But not to worry, I found a workaround for this problem. I opened this folder with the configuration in Cursor. I asked Cursor to go ahead read all the configuration files, all of them, and make me a comprehensive guide on how to use them with Claude and when and where. Cursor's new search tool is really, really amazing. It found everything super easily, made the connections between files and gave me a really cool configuration guide. So I told Cursor to put everything into the docs.md file. It created a comprehensive file of around 450 words.""",
    "start_time": 270,
    "end_time": 330,
    "token_count": count_tokens("""But not to worry, I found a workaround for this problem. I opened this folder with the configuration in Cursor. I asked Cursor to go ahead read all the configuration files, all of them, and make me a comprehensive guide on how to use them with Claude and when and where. Cursor's new search tool is really, really amazing. It found everything super easily, made the connections between files and gave me a really cool configuration guide. So I told Cursor to put everything into the docs.md file. It created a comprehensive file of around 450 words.""")
}
chunks.append(chunk_9)

# Chunk 10: Practical Demonstration
chunk_10 = {
    "chunk_index": 10,
    "chapter_title": "Real-World Example: Next.js Story Generator with 11 Phases",
    "text": """Once I had this documentation ready, I gave it a task. I said I wanted to build a Next.js app with Eleven Labs API integration and the OpenAI API. The idea was to create a story generator that also has a narration feature. I asked Cursor what workflow I should follow based on the framework. Cursor gave me the commands but it was missing the prompts. So I told it to output the slash commands, flags, and prompts in a structured way. And it delivered exactly that. Phase 1, phase 2, phase 3, all the way to phase 11 for deployment. A complete project outline.""",
    "start_time": 330,
    "end_time": 390,
    "token_count": count_tokens("""Once I had this documentation ready, I gave it a task. I said I wanted to build a Next.js app with Eleven Labs API integration and the OpenAI API. The idea was to create a story generator that also has a narration feature. I asked Cursor what workflow I should follow based on the framework. Cursor gave me the commands but it was missing the prompts. So I told it to output the slash commands, flags, and prompts in a structured way. And it delivered exactly that. Phase 1, phase 2, phase 3, all the way to phase 11 for deployment. A complete project outline.""")
}
chunks.append(chunk_10)

# Chunk 11: Democratization of Development
chunk_11 = {
    "chunk_index": 11,
    "chapter_title": "Democratizing Development Through Shared Workflows",
    "text": """If you've seen my video on context engineering, you know these workflows are evolving quickly. People once thought non-developers couldn't build applications. But development knowledge can be embedded into frameworks like this and shared openly. Now, anyone, even vibe coders with little industry experience, can follow a guided workflow written by someone who does know the process. And speaking of sharing, I'll leave this documentation that Cursor created for me in the description below so you can use it for yourself as well.""",
    "start_time": 390,
    "end_time": 420,
    "token_count": count_tokens("""If you've seen my video on context engineering, you know these workflows are evolving quickly. People once thought non-developers couldn't build applications. But development knowledge can be embedded into frameworks like this and shared openly. Now, anyone, even vibe coders with little industry experience, can follow a guided workflow written by someone who does know the process. And speaking of sharing, I'll leave this documentation that Cursor created for me in the description below so you can use it for yourself as well.""")
}
chunks.append(chunk_11)

# Chunk 12: Live Workflow Execution
chunk_12 = {
    "chunk_index": 12,
    "chapter_title": "Live Demo: Workflow Execution with MCPs",
    "text": """Phase one is analysis and research. I'll copy the command with its flags and switch to my terminal. When I open the slash menu in Claude, you'll see all the extra commands from this framework listed above Claude's original commands. When I hit enter, you'll see Claude start to run. Claude recognizes this as a research task, knows which tools to use, like Context7 for external documentation, then creates to-dos. It's using Sequential MCP. Asks my permission to call the tool and proceeds. It's all just a workflow, nothing fundamentally new. But these workflows are packaged for you by the framework's author.""",
    "start_time": 420,
    "end_time": 480,
    "token_count": count_tokens("""Phase one is analysis and research. I'll copy the command with its flags and switch to my terminal. When I open the slash menu in Claude, you'll see all the extra commands from this framework listed above Claude's original commands. When I hit enter, you'll see Claude start to run. Claude recognizes this as a research task, knows which tools to use, like Context7 for external documentation, then creates to-dos. It's using Sequential MCP. Asks my permission to call the tool and proceeds. It's all just a workflow, nothing fundamentally new. But these workflows are packaged for you by the framework's author.""")
}
chunks.append(chunk_12)

# Chunk 13: Claude Code Web UI Introduction
chunk_13 = {
    "chunk_index": 13,
    "chapter_title": "Tool 2: Claude Code Web UI for Cross-Device Access",
    "text": """Now, what if you could access Claude Code from anywhere, like any device? That's where the second tool comes in. It's essentially a web-based GUI for Claude Code. This tool offers something entirely different: browser accessibility from any device. So, Claude Code and my projects could be running on my computer while I'm actually using Claude Code through a browser on my mobile. That's incredibly powerful and the setup is surprisingly simple.""",
    "start_time": 480,
    "end_time": 510,
    "token_count": count_tokens("""Now, what if you could access Claude Code from anywhere, like any device? That's where the second tool comes in. It's essentially a web-based GUI for Claude Code. This tool offers something entirely different: browser accessibility from any device. So, Claude Code and my projects could be running on my computer while I'm actually using Claude Code through a browser on my mobile. That's incredibly powerful and the setup is surprisingly simple.""")
}
chunks.append(chunk_13)

# Chunk 14: Web UI Installation
chunk_14 = {
    "chunk_index": 14,
    "chapter_title": "Web UI Installation and Network Configuration",
    "text": """You just copy this script for the installation. This is basically an executable app. Navigate to where you want it installed. Run the script. It handles everything for you. There are different startup methods. The default command launches it on localhost:8080 which only runs locally on your computer. But this lacks the network capabilities I'm describing. To make it accessible from anywhere on your network, use this command instead. You need your IP address for the current network.""",
    "start_time": 510,
    "end_time": 570,
    "token_count": count_tokens("""You just copy this script for the installation. This is basically an executable app. Navigate to where you want it installed. Run the script. It handles everything for you. There are different startup methods. The default command launches it on localhost:8080 which only runs locally on your computer. But this lacks the network capabilities I'm describing. To make it accessible from anywhere on your network, use this command instead. You need your IP address for the current network.""")
}
chunks.append(chunk_14)

# Chunk 15: Using the Web UI
chunk_15 = {
    "chunk_index": 15,
    "chapter_title": "Cross-Device Access and Web UI Limitations",
    "text": """Once you have this IP address, return to where the web UI is running. Copy the port number. Open your browser. This works on any device - mobile, another computer. They just need to be on the same network. Paste it in, remove the zeros, and add your IP address. And there's your web UI. It's quite basic, nothing fancy. The amazing part is cross-device accessibility. I use this to run Claude Code from anywhere in the house. I just pull it up on my phone and use Claude Code directly from there. Unfortunately, the SuperClaude configuration won't function here.""",
    "start_time": 570,
    "end_time": 630,
    "token_count": count_tokens("""Once you have this IP address, return to where the web UI is running. Copy the port number. Open your browser. This works on any device - mobile, another computer. They just need to be on the same network. Paste it in, remove the zeros, and add your IP address. And there's your web UI. It's quite basic, nothing fancy. The amazing part is cross-device accessibility. I use this to run Claude Code from anywhere in the house. I just pull it up on my phone and use Claude Code directly from there. Unfortunately, the SuperClaude configuration won't function here.""")
}
chunks.append(chunk_15)

# Chunk 16: SuperClaude Installation
chunk_16 = {
    "chunk_index": 16,
    "chapter_title": "SuperClaude Installation: Global vs Project-Specific",
    "text": """Now, for the installation of SuperClaude, you need to head over to its GitHub repo where you'll find the installer. Simply copy these lines and paste them wherever you want the framework downloaded. This will clone the repository to your system. Now you've got two installation options: Global Installation means every instance of Claude Code will have access to SuperClaude. Project-Specific Installation requires you to replace the path with your actual folder path. Here's the key thing to remember: Whatever folder you're targeting, you need to add .claude to the end of the path. The configuration files need to be inside that .claude folder.""",
    "start_time": 630,
    "end_time": 690,
    "token_count": count_tokens("""Now, for the installation of SuperClaude, you need to head over to its GitHub repo where you'll find the installer. Simply copy these lines and paste them wherever you want the framework downloaded. This will clone the repository to your system. Now you've got two installation options: Global Installation means every instance of Claude Code will have access to SuperClaude. Project-Specific Installation requires you to replace the path with your actual folder path. Here's the key thing to remember: Whatever folder you're targeting, you need to add .claude to the end of the path. The configuration files need to be inside that .claude folder.""")
}
chunks.append(chunk_16)

# Chunk 17: Conclusion
chunk_17 = {
    "chunk_index": 17,
    "chapter_title": "Conclusion: Two Free Tools to Transform Your Workflow",
    "text": """That brings us to the end of this video. We've covered SuperClaude with its 18 structured commands and 9 personas that give you professional development workflows out of the box. We've also explored the Claude Code Web UI that lets you access Claude Code from any device on your network. Both tools are completely free and can dramatically improve your Claude Code workflow. If you'd like to support the channel and help us keep making videos like this, you can do so by using the super thanks button below.""",
    "start_time": 690,
    "end_time": 704,
    "token_count": count_tokens("""That brings us to the end of this video. We've covered SuperClaude with its 18 structured commands and 9 personas that give you professional development workflows out of the box. We've also explored the Claude Code Web UI that lets you access Claude Code from any device on your network. Both tools are completely free and can dramatically improve your Claude Code workflow. If you'd like to support the channel and help us keep making videos like this, you can do so by using the super thanks button below.""")
}
chunks.append(chunk_17)

# Write chunks to JSON file
output_dir = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"manual_chunks_{CHANNEL.lower().replace(' ', '_')}_superclaude_{VIDEO_ID}.json")

chunk_data = {
    "video_id": VIDEO_ID,
    "channel": CHANNEL,
    "title": TITLE,
    "total_chunks": len(chunks),
    "chunks": chunks
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(chunk_data, f, indent=2, ensure_ascii=False)

# Print summary
total_tokens = sum(chunk['token_count'] for chunk in chunks)
print(f"Created {len(chunks)} chunks with average {total_tokens // len(chunks)} tokens per chunk")
print(f"Total tokens: {total_tokens}")
print(f"Manual chunker completed successfully!")
print(f"Note: This captures two distinct tools - SuperClaude framework with professional")
print(f"development workflows and Claude Code Web UI for cross-device access.")