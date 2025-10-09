#!/usr/bin/env python3
"""
Manual chunker for Liam Ottley's "9 AI Tools That Will Separate Winners from Losers in 2025"
Video ID: Tw9HButMNu8

Content Type: Educational AI Tools Guide / Framework-based Tutorial
Channel: Liam Ottley
Strategy: Four Powers framework with tool-specific implementation:
1. Introduction + Personal credibility + Extinction reality
2. Four Powers framework (Build, Automate, Create, Connect)
3. Nine tools mapped to powers with specific use cases
4. Practical implementation strategies for each tool
5. Community funnel and resource guide

Note: This follows Liam Ottley's classic educational framework structure but focused 
on practical AI tool mastery rather than business strategy.
Chunk size: 200-350 tokens for tool-focused content to preserve context and implementation details.
"""

import json
import tiktoken

def count_tokens(text):
    """Count tokens using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def create_manual_chunks():
    chunks = []
    
    # Chunk 1: Hook + Personal Credibility + AI Generalist Thesis
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "The AI Generalist Advantage: $5M in 2 Years",
        "text": """In the AI age, the winners won't be the marketers, the developers, or the designers. They'll be AI generalists who can do it all. I know because I've done it. In the past just two years, I've made over $5 million by mastering a specific set of AI tools that have turned me into a one-person army. In this video, I'll show you why AI generalists will dominate every industry in the coming years. I'll explain the four powers of AI generalists and the nine AI tools that anyone can learn in order to become one.

This isn't just another AI tools video. This is your blueprint to becoming unstoppable in 2025 and beyond. If you're new to the channel and don't know who I am, my name is Liam Ottley and I've been an entrepreneur for the past 6 years. For the past two of which I've been focused specifically on building AI businesses, learning the following AI tools that I'm about to share has completely changed my life.""",
        "start_time": 0,
        "end_time": 90,
        "token_count": count_tokens("""In the AI age, the winners won't be the marketers, the developers, or the designers. They'll be AI generalists who can do it all. I know because I've done it. In the past just two years, I've made over $5 million by mastering a specific set of AI tools that have turned me into a one-person army. In this video, I'll show you why AI generalists will dominate every industry in the coming years. I'll explain the four powers of AI generalists and the nine AI tools that anyone can learn in order to become one.

This isn't just another AI tools video. This is your blueprint to becoming unstoppable in 2025 and beyond. If you're new to the channel and don't know who I am, my name is Liam Ottley and I've been an entrepreneur for the past 6 years. For the past two of which I've been focused specifically on building AI businesses, learning the following AI tools that I'm about to share has completely changed my life.""")
    }
    
    # Chunk 2: The Extinction Reality - Pandas vs Raccoons Analogy
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "The Extinction Reality: Specialists Become Dinosaurs",
        "text": """The reality is that right now your job, education, or business may be on its way out. AI is changing jobs faster than ever. Whole teams of experts are now being replaced by machines. And career paths that were once stable 5 years ago are disappearing or already gone. This all seems scary and new, but it's exactly like what we see in nature. 99% of all animals that have ever existed on Earth are now extinct.

Think of giant pandas, right? They only eat one thing, bamboo. So, if the bamboo's gone overnight, they're in trouble. Or you have the dinosaurs who needed a specific climate in order to live. You can think of dinosaurs as being similar to what doctors, lawyers, and coders are going to be when we look back in 10 years from now. They are specialists. People who have spent years and decades just to learn one type of thing. And now AI can do 80% as well as they can as specialists.

So we want to be adapters instead, like clever raccoons who can basically eat anything to survive and live anywhere. We want to be AI generalists who don't take years to just learn one skill or do one career path. With AI, we try to pick up entirely new skills and career paths in a week.""",
        "start_time": 90,
        "end_time": 240,
        "token_count": count_tokens("""The reality is that right now your job, education, or business may be on its way out. AI is changing jobs faster than ever. Whole teams of experts are now being replaced by machines. And career paths that were once stable 5 years ago are disappearing or already gone. This all seems scary and new, but it's exactly like what we see in nature. 99% of all animals that have ever existed on Earth are now extinct.

Think of giant pandas, right? They only eat one thing, bamboo. So, if the bamboo's gone overnight, they're in trouble. Or you have the dinosaurs who needed a specific climate in order to live. You can think of dinosaurs as being similar to what doctors, lawyers, and coders are going to be when we look back in 10 years from now. They are specialists. People who have spent years and decades just to learn one type of thing. And now AI can do 80% as well as they can as specialists.

So we want to be adapters instead, like clever raccoons who can basically eat anything to survive and live anywhere. We want to be AI generalists who don't take years to just learn one skill or do one career path. With AI, we try to pick up entirely new skills and career paths in a week.""")
    }
    
    # Chunk 3: Nassim Taleb's Antifragile Philosophy + Personal Success Story
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "Antifragile Philosophy: $10M Revenue Through AI Adaptation",
        "text": """The famous author and philosopher Nassim Taleb put it this way. Most people are scared to be fragile. Instead, you should learn skills that make you antifragile. And he said, "Some people benefit from shocks. They thrive and grow when exposed to randomness, disorder, and stresses." So, you don't want to risk being a student for 7 years, then go into a job that might get replaced or start a business in an industry that has largely been automated away. Instead, with your career, you need to follow a model that gets stronger the more things change.

And that's what I did over 2 years ago. Gaining the four powers of an AI generalist has allowed me to build a business that is on track to do $10 million in revenue this year to build this channel to 500,000 subscribers in just over 2 years and to ultimately build my dream life. The key to gaining each of these powers is learning a handful of incredibly powerful AI tools which allow you to get the skills of a coder, a designer, or a writer in days or weeks rather than years or decades.""",
        "start_time": 240,
        "end_time": 360,
        "token_count": count_tokens("""The famous author and philosopher Nassim Taleb put it this way. Most people are scared to be fragile. Instead, you should learn skills that make you antifragile. And he said, "Some people benefit from shocks. They thrive and grow when exposed to randomness, disorder, and stresses." So, you don't want to risk being a student for 7 years, then go into a job that might get replaced or start a business in an industry that has largely been automated away. Instead, with your career, you need to follow a model that gets stronger the more things change.

And that's what I did over 2 years ago. Gaining the four powers of an AI generalist has allowed me to build a business that is on track to do $10 million in revenue this year to build this channel to 500,000 subscribers in just over 2 years and to ultimately build my dream life. The key to gaining each of these powers is learning a handful of incredibly powerful AI tools which allow you to get the skills of a coder, a designer, or a writer in days or weeks rather than years or decades.""")
    }
    
    # Chunk 4: Power #1 - The Power to Build + Vibe Coding Concept
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Power #1: The Power to Build - Vibe Coding Revolution",
        "text": """First, there's the power to build. And this is where you make apps and websites in hours, not weeks or months. No coding needed at all. This goes along with a big trend right now called vibe coding. And vibe coding means that you don't need to know every technical detail. You don't need to be a developer necessarily. You can just share the vibe or the idea of what you want to build. All of you will have ideas for little softwares or tools that you want to make when you couldn't do it until now. And now AI can do it for you.

Now this idea isn't just theory. It actually comes straight from Andrej Karpathy, a superstar in the tech world, particularly AI. He was one of the founding members of OpenAI where were the creators of ChatGPT. He led the AI self-driving efforts of Tesla. And he says that vibe coding is for everyone, even the programmers at the highest level. The old way to build custom apps and software was to pay tons of money to a developer and then wait forever for them to finish it. Or it would be to spend 4 years learning how to code yourself. But now with Vibe Coding, you can build software just by saying what you want.""",
        "start_time": 360,
        "end_time": 480,
        "token_count": count_tokens("""First, there's the power to build. And this is where you make apps and websites in hours, not weeks or months. No coding needed at all. This goes along with a big trend right now called vibe coding. And vibe coding means that you don't need to know every technical detail. You don't need to be a developer necessarily. You can just share the vibe or the idea of what you want to build. All of you will have ideas for little softwares or tools that you want to make when you couldn't do it until now. And now AI can do it for you.

Now this idea isn't just theory. It actually comes straight from Andrej Karpathy, a superstar in the tech world, particularly AI. He was one of the founding members of OpenAI where were the creators of ChatGPT. He led the AI self-driving efforts of Tesla. And he says that vibe coding is for everyone, even the programmers at the highest level. The old way to build custom apps and software was to pay tons of money to a developer and then wait forever for them to finish it. Or it would be to spend 4 years learning how to code yourself. But now with Vibe Coding, you can build software just by saying what you want.""")
    }
    
    # Chunk 5: Tool #1 - Lovable AI Implementation and Use Cases
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Tool #1: Lovable AI - Lightning Speed App Development",
        "text": """So let's check out the best tool to unlock this superpower. It's called Lovable AI and it's the ultimate AI assisted app development platform. Lovable AI is a game changer in building apps and websites without code because it can turn your ideas into real websites and apps at lightning speed. You just tell it what you want and it gets to work. It's really pretty incredible when you try it for the first time. And we use this all the time at my agency, Morningside AI, to build custom AI tools for our team to use internally.

If you're a student, you could create a custom study and flashcards quiz app in just 10 minutes. You can put your notes in it and have it create quizzes for you, update your progress on a dashboard and everything like that. If you're an employee, you can build custom AI tools or a custom dashboard for your team even to impress your boss and your clients without having to hire a costly dev team. Or for you entrepreneurs, you could launch a whole business overnight with a beautiful landing page and something to test your product, get some early customers, and grow the business without spending thousands and thousands of development fees.""",
        "start_time": 480,
        "end_time": 600,
        "token_count": count_tokens("""So let's check out the best tool to unlock this superpower. It's called Lovable AI and it's the ultimate AI assisted app development platform. Lovable AI is a game changer in building apps and websites without code because it can turn your ideas into real websites and apps at lightning speed. You just tell it what you want and it gets to work. It's really pretty incredible when you try it for the first time. And we use this all the time at my agency, Morningside AI, to build custom AI tools for our team to use internally.

If you're a student, you could create a custom study and flashcards quiz app in just 10 minutes. You can put your notes in it and have it create quizzes for you, update your progress on a dashboard and everything like that. If you're an employee, you can build custom AI tools or a custom dashboard for your team even to impress your boss and your clients without having to hire a costly dev team. Or for you entrepreneurs, you could launch a whole business overnight with a beautiful landing page and something to test your product, get some early customers, and grow the business without spending thousands and thousands of development fees.""")
    }
    
    # Chunk 6: Power #2 - The Power to Automate + Strategic Value
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Power #2: The Power to Automate - Tireless Digital Workers",
        "text": """Now, let's carry this forward to the next skill of the AI age, which is the power to automate. This means taking away the boring, repetitive work that you do every day. For example, if you're an entrepreneur, automation can handle customer follow-ups after a sale. Kind of like having a tireless assistant who books more deals while you sleep. That is straight up money in your pocket without the extra hours.

With this power as a student, you can get it to automate your study to automatically research and craft assignment for you. And if you're at work, you can automate almost any task that you do on a daily basis, like writing reports, updating databases, or sending follow-ups. Your workday could get shorter, and you could snag a promotion by spending that extra time by knocking out higher priority projects.""",
        "start_time": 600,
        "end_time": 690,
        "token_count": count_tokens("""Now, let's carry this forward to the next skill of the AI age, which is the power to automate. This means taking away the boring, repetitive work that you do every day. For example, if you're an entrepreneur, automation can handle customer follow-ups after a sale. Kind of like having a tireless assistant who books more deals while you sleep. That is straight up money in your pocket without the extra hours.

With this power as a student, you can get it to automate your study to automatically research and craft assignment for you. And if you're at work, you can automate almost any task that you do on a daily basis, like writing reports, updating databases, or sending follow-ups. Your workday could get shorter, and you could snag a promotion by spending that extra time by knocking out higher priority projects.""")
    }
    
    # Chunk 7: Tool #2 - Relevance AI + AI Tools vs Agents
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Tool #2: Relevance AI - Building AI Tools and Agents",
        "text": """Our first AI tool that you can use to gain the power to automate is Relevance AI which is a fantastic no code platform. It lets you do two things. Firstly, create AI tools and then create AI agents that use those tools. No tech skills or coding required. It's like having a magic kit that can basically automate everything.

What are AI tools? They are systems that automate a specific task and they are actually run or operated by you as a human or by an agent. They basically save you time by doing one job super well. For example, you could summarize long textbook chapters in minutes for a test. It sorts through tons of customer emails or customer feedback and find pain points or it can scan social media to locate qualified customers based on your criteria.

But relevance gets more powerful when you combine those tools with AI agents that can reason and have memory and can take actions on their own. So, if you combine agents with multiple tools you create in relevance, you can create your own personal sidekick. Or for businesses where potential customers reach out and the agent could read their email, update the CRM for you, and draft an email and then assign a salesperson for follow-up.""",
        "start_time": 690,
        "end_time": 840,
        "token_count": count_tokens("""Our first AI tool that you can use to gain the power to automate is Relevance AI which is a fantastic no code platform. It lets you do two things. Firstly, create AI tools and then create AI agents that use those tools. No tech skills or coding required. It's like having a magic kit that can basically automate everything.

What are AI tools? They are systems that automate a specific task and they are actually run or operated by you as a human or by an agent. They basically save you time by doing one job super well. For example, you could summarize long textbook chapters in minutes for a test. It sorts through tons of customer emails or customer feedback and find pain points or it can scan social media to locate qualified customers based on your criteria.

But relevance gets more powerful when you combine those tools with AI agents that can reason and have memory and can take actions on their own. So, if you combine agents with multiple tools you create in relevance, you can create your own personal sidekick. Or for businesses where potential customers reach out and the agent could read their email, update the CRM for you, and draft an email and then assign a salesperson for follow-up.""")
    }
    
    # Chunk 8: Tool #3 - n8n + AI Agent Builder Advantage
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "Tool #3: n8n - The New King of AI Workflow Automation",
        "text": """Our next tool that allows you to gain the power to automate is an AI workflow automation platform called n8n. You may have heard of things like Zapier or Make.com even. And these are workflow automation platforms that allow you to use things like ChatGPT within your workflows. It's very handy for being able to plug in AI into any kind of workflow you want to automate.

But there's really a new king on the block that's a bit better suited to AI automation and that's n8n. It has almost all of the features of Make.com or Zapier. But what makes it stand out is the super powerful AI agent builder that it comes with. So you can build your own automations that actually use AI agents inside of them. It's like a double whammy really.

AI workflow automations run all on their own and they're triggered by events or they're set up on schedules with really no human in the loop. For example, students can set up n8n automation to automatically scan your course emails, extract assignment due dates, and then compile them into a weekly digest that organizes all the upcoming deadlines. Or if you're on a sales team, you can use n8n to pull sales leads from a form, add them to the team CRM, and then organize it based on the data submitted.""",
        "start_time": 840,
        "end_time": 990,
        "token_count": count_tokens("""Our next tool that allows you to gain the power to automate is an AI workflow automation platform called n8n. You may have heard of things like Zapier or Make.com even. And these are workflow automation platforms that allow you to use things like ChatGPT within your workflows. It's very handy for being able to plug in AI into any kind of workflow you want to automate.

But there's really a new king on the block that's a bit better suited to AI automation and that's n8n. It has almost all of the features of Make.com or Zapier. But what makes it stand out is the super powerful AI agent builder that it comes with. So you can build your own automations that actually use AI agents inside of them. It's like a double whammy really.

AI workflow automations run all on their own and they're triggered by events or they're set up on schedules with really no human in the loop. For example, students can set up n8n automation to automatically scan your course emails, extract assignment due dates, and then compile them into a weekly digest that organizes all the upcoming deadlines. Or if you're on a sales team, you can use n8n to pull sales leads from a form, add them to the team CRM, and then organize it based on the data submitted.""")
    }
    
    # Chunk 9: Tools #4-5 - PromptMetheus + Postman (Prompt Engineering + API Integration)
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Tools #4-5: PromptMetheus + Postman - Professional Prompting + API Mastery",
        "text": """Which leads us into the next great tool for getting the power to automate, and that is called PromptMetheus. This represents a skill of prompt engineering, which is just learning how to tell the AI exactly what you want in the best way possible. The quality of what you get out of these AI models depends heavily on what you put in. PromptMetheus is the best platform to really stretch the limits of what you can do with these models with professional grade prompting software.

Having just a good prompt can be the difference between getting something that quickly takes you 70% of the way there but still requires three more hours of refinement versus a great prompt which can get you like 95% of the way there and meaning you only have to spend 30 minutes in finalizing your report or the output.

Finally, Postman is essential for API integration. If the future is all about software then you need to know how to get the apps and systems that run reality to talk to one another. APIs are essentially like bridges that connect different software together. Postman helps you to test APIs without needing to be a coding expert. It's like having a map to link up all the digital tools and test if they're working before you build too far.""",
        "start_time": 990,
        "end_time": 1140,
        "token_count": count_tokens("""Which leads us into the next great tool for getting the power to automate, and that is called PromptMetheus. This represents a skill of prompt engineering, which is just learning how to tell the AI exactly what you want in the best way possible. The quality of what you get out of these AI models depends heavily on what you put in. PromptMetheus is the best platform to really stretch the limits of what you can do with these models with professional grade prompting software.

Having just a good prompt can be the difference between getting something that quickly takes you 70% of the way there but still requires three more hours of refinement versus a great prompt which can get you like 95% of the way there and meaning you only have to spend 30 minutes in finalizing your report or the output.

Finally, Postman is essential for API integration. If the future is all about software then you need to know how to get the apps and systems that run reality to talk to one another. APIs are essentially like bridges that connect different software together. Postman helps you to test APIs without needing to be a coding expert. It's like having a map to link up all the digital tools and test if they're working before you build too far.""")
    }
    
    # Chunk 10: Power #3 - The Power to Create + Tool #6 ChatGPT 4.0
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "Power #3: Create + Tool #6: ChatGPT 4.0 Image Generation Pro Hack",
        "text": """Now, let's explore the power to create, which is a game-changing skill in the AI age. Think about all of the content that a modern business or a creative needs these days. You need designs, videos, B-roll, music, images, graphics, and diagrams. Even simple projects these days need basically professional grade content in order to stand out and actually make any money. The old way was to spend years learning these complex creative tools yourself or to hire expensive freelancers or creative agencies. A single video ad or a new ad campaign could cost thousands of dollars.

Here is the best tool for gaining this power of creation, and that is ChatGPT 4.0, specifically the image generation model that comes with it. It can make incredible pictures and designs incredibly fast. It's like having an experienced digital artist ready to create anything that you imagine. It can create incredible graphics, logos, icons, or even product photography.

The top hack that I've been using lately with this image generation model is to tell it roughly what you want and then ask ChatGPT to write you a super-detailed design brief, one that you'd be able to just give to your designer. Tell ChatGPT to include things like spacing and styles and sizes and typography, colors and pallets. And once it gives you this huge brief, then send it back to ChatGPT and say, "Great, now generate this image." It works incredibly well.""",
        "start_time": 1140,
        "end_time": 1290,
        "token_count": count_tokens("""Now, let's explore the power to create, which is a game-changing skill in the AI age. Think about all of the content that a modern business or a creative needs these days. You need designs, videos, B-roll, music, images, graphics, and diagrams. Even simple projects these days need basically professional grade content in order to stand out and actually make any money. The old way was to spend years learning these complex creative tools yourself or to hire expensive freelancers or creative agencies. A single video ad or a new ad campaign could cost thousands of dollars.

Here is the best tool for gaining this power of creation, and that is ChatGPT 4.0, specifically the image generation model that comes with it. It can make incredible pictures and designs incredibly fast. It's like having an experienced digital artist ready to create anything that you imagine. It can create incredible graphics, logos, icons, or even product photography.

The top hack that I've been using lately with this image generation model is to tell it roughly what you want and then ask ChatGPT to write you a super-detailed design brief, one that you'd be able to just give to your designer. Tell ChatGPT to include things like spacing and styles and sizes and typography, colors and pallets. And once it gives you this huge brief, then send it back to ChatGPT and say, "Great, now generate this image." It works incredibly well.""")
    }
    
    # Chunk 11: Tools #7-8 - UX Pilot + Descript (Design + Video)
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Tools #7-8: UX Pilot + Descript - UI Design + Video Mastery",
        "text": """The next AI tool is called UX Pilot and it's for nailing the skill of AI UI design. This builds on what we learned about Lovable and building web apps earlier where UX pilot acts as the perfect partner to create amazing designs for your apps before you have to go and actually build it in Lovable. So, it's like having a full UI UX designer on your team. The biggest limiter with tools like Lovable is being able to give great prompts and get really beautiful designs out of it. UX Pilot focuses on making UI designs for your apps. Not just pretty, but also easy to use.

The third AI tool for the power to create is called Descript. It's a fantastic tool for the skill of AI editing and enhancement. Video is the most powerful medium out there for sharing ideas and growing a personal brand. The video has been a driving factor in my success with this YouTube channel, having over 500,000 subscribers and generating over $5 million in the past 2 years has come from me sharing videos on YouTube.

Descript is all about making video and audio editing super simple. It turns raw clips that you film like this into finish pieces without needing fancy editing skills. It's like having an editor in your pocket that can automatically make your audio sound great, remove pauses and retakes, and even cut up clips for social media automatically.""",
        "start_time": 1290,
        "end_time": 1440,
        "token_count": count_tokens("""The next AI tool is called UX Pilot and it's for nailing the skill of AI UI design. This builds on what we learned about Lovable and building web apps earlier where UX pilot acts as the perfect partner to create amazing designs for your apps before you have to go and actually build it in Lovable. So, it's like having a full UI UX designer on your team. The biggest limiter with tools like Lovable is being able to give great prompts and get really beautiful designs out of it. UX Pilot focuses on making UI designs for your apps. Not just pretty, but also easy to use.

The third AI tool for the power to create is called Descript. It's a fantastic tool for the skill of AI editing and enhancement. Video is the most powerful medium out there for sharing ideas and growing a personal brand. The video has been a driving factor in my success with this YouTube channel, having over 500,000 subscribers and generating over $5 million in the past 2 years has come from me sharing videos on YouTube.

Descript is all about making video and audio editing super simple. It turns raw clips that you film like this into finish pieces without needing fancy editing skills. It's like having an editor in your pocket that can automatically make your audio sound great, remove pauses and retakes, and even cut up clips for social media automatically.""")
    }
    
    # Chunk 12: Power #4 + Tool #9 - The Power to Connect + Poppy AI
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "Power #4 + Tool #9: Connect with Poppy AI - Scaling Your Voice",
        "text": """At the end of the day, the most brilliant apps or business ideas is going to be worthless if nobody uses it or hears about it. The best automation that you create is going to be meaningless if your business isn't getting any leads. And the best visuals are going to be wasted if they don't reach an audience. AI gives us some incredible new tools we now have at our disposal in order to break through the noise. This is what the power to connect is all about.

Being able to create content and connect with people and write is an incredibly powerful skill in this day and age. The biggest limiter of reaching more people is scaling your thinking and your ideas to reach more people. So this is exactly how I grew such a large following in just two years.

So that's where Poppy AI comes in and it represents the skill of AI enhanced writing. It's like having a master writer who knows just what to say who's writing along with you. Poppy AI can remember who you are and writes in a way that feels like you. For example, here's my Poppy template that I duplicate at the start of planning each video. I've given it context about me, my YouTube channel, and my businesses. I give it a system prompt on who it is and how it should write and how it should be helping me. So anything that I throw into Poppy, I can then just hook into a chat window and it remembers everything that it needs to know about me to write great content from my perspective.""",
        "start_time": 1440,
        "end_time": 1590,
        "token_count": count_tokens("""At the end of the day, the most brilliant apps or business ideas is going to be worthless if nobody uses it or hears about it. The best automation that you create is going to be meaningless if your business isn't getting any leads. And the best visuals are going to be wasted if they don't reach an audience. AI gives us some incredible new tools we now have at our disposal in order to break through the noise. This is what the power to connect is all about.

Being able to create content and connect with people and write is an incredibly powerful skill in this day and age. The biggest limiter of reaching more people is scaling your thinking and your ideas to reach more people. So this is exactly how I grew such a large following in just two years.

So that's where Poppy AI comes in and it represents the skill of AI enhanced writing. It's like having a master writer who knows just what to say who's writing along with you. Poppy AI can remember who you are and writes in a way that feels like you. For example, here's my Poppy template that I duplicate at the start of planning each video. I've given it context about me, my YouTube channel, and my businesses. I give it a system prompt on who it is and how it should write and how it should be helping me. So anything that I throw into Poppy, I can then just hook into a chat window and it remembers everything that it needs to know about me to write great content from my perspective.""")
    }
    
    # Chunk 13: Conclusion - Roadmap + Community Funnel
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "Your Roadmap to AI Generalist Mastery + Free Resources",
        "text": """And here's what I'll do to put you on the right path to get insane results in your own life using these AI tools. I've already spent thousands of hours testing all of these different tools and strategies. And then I've distilled everything I've learned over the past 2 years into a clear road map for you to acquire the four powers of an AI generalist using the tools that we've talked about today.

So to speed up your learning, you'll want to check out the resource guide in the description below. It's boiled down to a clear road map for mastering each of these four powers and the nine AI tools that unlock each of them. The first link in the description will take you to my free Skool community. It'll take a few minutes for you to get accepted in, but once you're in there, you can search for the title of this video in the search bar, and then it will pop up, and you'll be able to find all of the resources.

As promised, I put together the best free step-by-step tutorials for each tool, as well as my most-used workflows that I haven't shared anywhere. So, use my templates and my prompts, follow the real use cases from my team and the community, and become future proof. As William Gibson said, the future is here, it's just not evenly distributed. And the question is this, will you be one of the first to step into the AI future?""",
        "start_time": 1590,
        "end_time": 1800,
        "token_count": count_tokens("""And here's what I'll do to put you on the right path to get insane results in your own life using these AI tools. I've already spent thousands of hours testing all of these different tools and strategies. And then I've distilled everything I've learned over the past 2 years into a clear road map for you to acquire the four powers of an AI generalist using the tools that we've talked about today.

So to speed up your learning, you'll want to check out the resource guide in the description below. It's boiled down to a clear road map for mastering each of these four powers and the nine AI tools that unlock each of them. The first link in the description will take you to my free Skool community. It'll take a few minutes for you to get accepted in, but once you're in there, you can search for the title of this video in the search bar, and then it will pop up, and you'll be able to find all of the resources.

As promised, I put together the best free step-by-step tutorials for each tool, as well as my most-used workflows that I haven't shared anywhere. So, use my templates and my prompts, follow the real use cases from my team and the community, and become future proof. As William Gibson said, the future is here, it's just not evenly distributed. And the question is this, will you be one of the first to step into the AI future?""")
    }
    
    chunks.extend([chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, chunk_9, chunk_10, chunk_11, chunk_12, chunk_13])
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Calculate token statistics
    total_tokens = sum(chunk["token_count"] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    # Create the final JSON structure
    result = {
        "video_id": "Tw9HButMNu8",
        "title": "9 AI Tools That Will Separate Winners from Losers in 2025",
        "channel": "Liam Ottley",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens) if avg_tokens else 0
        }
    }
    
    # Write to JSON file
    output_path = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_liam_ottley_9_tools_Tw9HButMNu8.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} chunks with average {avg_tokens:.0f} tokens per chunk")
    print(f"Total tokens: {total_tokens}")
    print("Manual chunker completed successfully!")
    print("Note: This captures the complete Four Powers framework with all nine AI tools")
    print("and their practical implementation strategies for becoming an AI generalist.")

if __name__ == "__main__":
    main()