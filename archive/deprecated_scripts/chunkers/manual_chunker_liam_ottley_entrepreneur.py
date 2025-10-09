#!/usr/bin/env python3
"""
Manual chunker for Liam Ottley's "How to Learn AI as an Entrepreneur (3 Beginner Paths)"
Video ID: rOUs76wtv60

Content Type: Educational/Entrepreneurial - Three-path framework
Channel: Liam Ottley (new channel)
Strategy: Framework-based chunking around the three paths + introduction/Potentia sections
"""

import json
import tiktoken

def count_tokens(text):
    """Count tokens using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def create_manual_chunks():
    chunks = []
    
    # Chunk 1: Introduction and Personal Story
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "Introduction: Why Entrepreneurs Need AI Learning Clarity",
        "text": """Over the past few weeks, I've had a lot of run-ins with entrepreneurs of all sorts of backgrounds asking me how they can learn AI. Some of some big guys that you probably know by name, which I won't mention, but everyone's obviously looking at the AI opportunity, wanting to know how they can get into it, how they can learn it, how they can apply it to their business. And the question I keep getting is, how, Liam, how should I learn AI as an entrepreneur? If I'm already running my business, or I'm wanting to get into AI and start a business, how do I learn it? What's the pathway? Do I need to learn how to code? Do I need to watch all these tutorials?

And so in the process of me trying to help these people to get into AI, I've had to come up with a set of resources and a big sort of roadmap for them and how they can learn these skills. But the pattern that I've noticed across many different people have asked me the same question is that before you start doing all of this, you need to get very clear on why you were trying to get into AI. And that's the question that I always reflect back to them is like, okay, you're saying how can I learn AI? But my question to you is like why do you want to learn AI?""",
        "start_time": 0,
        "end_time": 120,
        "token_count": count_tokens("Over the past few weeks, I've had a lot of run-ins with entrepreneurs of all sorts of backgrounds asking me how they can learn AI. Some of some big guys that you probably know by name, which I won't mention, but everyone's obviously looking at the AI opportunity, wanting to know how they can get into it, how they can learn it, how they can apply it to their business. And the question I keep getting is, how, Liam, how should I learn AI as an entrepreneur? If I'm already running my business, or I'm wanting to get into AI and start a business, how do I learn it? What's the pathway? Do I need to learn how to code? Do I need to watch all these tutorials?\n\nAnd so in the process of me trying to help these people to get into AI, I've had to come up with a set of resources and a big sort of roadmap for them and how they can learn these skills. But the pattern that I've noticed across many different people have asked me the same question is that before you start doing all of this, you need to get very clear on why you were trying to get into AI. And that's the question that I always reflect back to them is like, okay, you're saying how can I learn AI? But my question to you is like why do you want to learn AI?")
    }
    
    # Chunk 2: Video Purpose and Background
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "Framework Overview: Three Different AI Learning Paths",
        "text": """And so in this video, I'm going to break down the sort of three core cases of why you as an entrepreneur may want to learn AI. And there's three very different strategies of how I'd recommend you to learn it depending on which one you are. So this video is really intended to be about saving you a ton of time and sending you down the wrong path of thinking that you need to learn how to code and do all this. There are much faster ways depending on what you're trying to do in the AI space that I'm going to reveal here.

And if you're new to the channel and don't know who I am, my name is Liam Ottley and two and a half years ago, I made the same transition and taught myself AI and shifted my whole entrepreneurial skill set into the AI space. Taught myself AI skills and have since built multiple different AI businesses on track to do over $10 million this year. So, that's a bit of context on me and why people are coming to me of all people to learn the stuff and want to know how they can make the same sort of transition.""",
        "start_time": 120,
        "end_time": 200,
        "token_count": count_tokens("And so in this video, I'm going to break down the sort of three core cases of why you as an entrepreneur may want to learn AI. And there's three very different strategies of how I'd recommend you to learn it depending on which one you are. So this video is really intended to be about saving you a ton of time and sending you down the wrong path of thinking that you need to learn how to code and do all this. There are much faster ways depending on what you're trying to do in the AI space that I'm going to reveal here.\n\nAnd if you're new to the channel and don't know who I am, my name is Liam Ottley and two and a half years ago, I made the same transition and taught myself AI and shifted my whole entrepreneurial skill set into the AI space. Taught myself AI skills and have since built multiple different AI businesses on track to do over $10 million this year. So, that's a bit of context on me and why people are coming to me of all people to learn the stuff and want to know how they can make the same sort of transition.")
    }
    
    # Chunk 3: Audience Understanding and Motivation
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "The Right Mindset: Genuine Interest vs Superficial Approaches",
        "text": """I see it in the eyes of people like you watching this video that you are intensely curious as I was about the technology. You don't want to be someone who's just coming in like I think there's these corny AI guys, right? Who don't actually have a sort of respect or appreciation for the technology. They don't want to learn the fundamentals. And from all the people who are asking me this, I do see that genuine interest in wanting to learn this stuff and seeing how important it's going to be for your career and for the future and that you can use it to shift into basically a new vehicle for your career.

Maybe you've been struggling or grinding away in sort of a stagnant industry for a long time and you see the opportunity that lies there if you can figure this AI stuff out. And so I'm making this video and I have made all of my other videos on this channel for you, for the person who wants to shift their skill set into a better vehicle. One of my sort of quotes that I live by these days is it's not about how hard you row, it's about the boat you're in.""",
        "start_time": 200,
        "end_time": 280,
        "token_count": count_tokens("I see it in the eyes of people like you watching this video that you are intensely curious as I was about the technology. You don't want to be someone who's just coming in like I think there's these corny AI guys, right? Who don't actually have a sort of respect or appreciation for the technology. They don't want to learn the fundamentals. And from all the people who are asking me this, I do see that genuine interest in wanting to learn this stuff and seeing how important it's going to be for your career and for the future and that you can use it to shift into basically a new vehicle for your career.\n\nMaybe you've been struggling or grinding away in sort of a stagnant industry for a long time and you see the opportunity that lies there if you can figure this AI stuff out. And so I'm making this video and I have made all of my other videos on this channel for you, for the person who wants to shift their skill set into a better vehicle. One of my sort of quotes that I live by these days is it's not about how hard you row, it's about the boat you're in.")
    }
    
    # Chunk 4: Personal Success Story
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Success Story: From E-commerce to AI ($10M Journey)",
        "text": """And I know firsthand how ridiculously powerful it can be to shift from a vehicle that is sort of a bit outdated or doesn't have as much upside, which I was in the e-commerce marketing world prior to the start of 2023. And then when I shifted my skills set over to AI, I already had all of the entrepreneurial skills. When I put the AI stuff on top, I just was able to like explode my success and growth rates in basically every area of my life.

So, I'm making this for you. You guys are so much closer than you think to being able to apply your entrepreneurial skill set in the AI space. And so, without further yapping, let's get into it. Breaking down the three different reasons why you'd want to move into the AI space. Then, I'm going to give you a strategy for each of those as to how you can do it. And if you wait to the end, I'm going to give you a full list of resources. So if you actually do just want to like sit there and learn it for like 3 to 6 months, I'm going to give you that exact roadmap that I would give to you, the same one that I basically use as well.""",
        "start_time": 280,
        "end_time": 360,
        "token_count": count_tokens("And I know firsthand how ridiculously powerful it can be to shift from a vehicle that is sort of a bit outdated or doesn't have as much upside, which I was in the e-commerce marketing world prior to the start of 2023. And then when I shifted my skills set over to AI, I already had all of the entrepreneurial skills. When I put the AI stuff on top, I just was able to like explode my success and growth rates in basically every area of my life.\n\nSo, I'm making this for you. You guys are so much closer than you think to being able to apply your entrepreneurial skill set in the AI space. And so, without further yapping, let's get into it. Breaking down the three different reasons why you'd want to move into the AI space. Then, I'm going to give you a strategy for each of those as to how you can do it. And if you wait to the end, I'm going to give you a full list of resources. So if you actually do just want to like sit there and learn it for like 3 to 6 months, I'm going to give you that exact roadmap that I would give to you, the same one that I basically use as well.")
    }
    
    # Chunk 5: Path 1 - AI for Existing Business
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "Path 1: Learn AI to Lead Your Existing Company's AI Adoption",
        "text": """So there's basically three different reasons that I've seen amongst entrepreneurs of why they want to get into AI or why they want to learn it in the first place. First one being that you have an existing business and you want to learn AI to be able to better lead your company in its own AI adoption. And so that's one type. You're happy with your vehicle. You like what you're doing, you love your work, you got a great team, you maybe you've spent a lot of effort sort of the past 5 or 10 years building this business. So it doesn't really make sense for you to scrap it all and go back to the bottom of the hill and try to start a whole new AI focused venture.

You're like, I'm good here, but I want to be able to lead my company better. I want to understand AI better so that I can implement it within my own company, get an edge in the market, sort of invest early so that you get the advantage and sort of rise up the ladder in your industry. That is one very popular reason why I get entrepreneurs asking me about learning AI.""",
        "start_time": 360,
        "end_time": 450,
        "token_count": count_tokens("So there's basically three different reasons that I've seen amongst entrepreneurs of why they want to get into AI or why they want to learn it in the first place. First one being that you have an existing business and you want to learn AI to be able to better lead your company in its own AI adoption. And so that's one type. You're happy with your vehicle. You like what you're doing, you love your work, you got a great team, you maybe you've spent a lot of effort sort of the past 5 or 10 years building this business. So it doesn't really make sense for you to scrap it all and go back to the bottom of the hill and try to start a whole new AI focused venture.\n\nYou're like, I'm good here, but I want to be able to lead my company better. I want to understand AI better so that I can implement it within my own company, get an edge in the market, sort of invest early so that you get the advantage and sort of rise up the ladder in your industry. That is one very popular reason why I get entrepreneurs asking me about learning AI.")
    }
    
    # Chunk 6: Path 2 - Sell AI to Your Industry
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Path 2: Sell AI Solutions Back to Your Industry",
        "text": """The second reason is a little bit different and this is that you want to learn AI so that you can sell AI stuff to your industry. Basically using your industry expertise and understanding and connections to figure out some kind of AI product or service that can be sold back to them. This also is one of the biggest areas of interest that I get people asking me about how they can pick up AI skills, bring a new product or service to market and sell it back to the people that they know and that they deeply understand.

So, it's basically just a vehicle or a model shift into the AI and using sort of the rapid growth and potential there to maybe build a software and get exits. It's just a shift and then selling back to the existing industry that you're coming from. This is super common in people who are already kind of tech-minded or very curious people and they're tinkering around with AI and I hear it all the time.""",
        "start_time": 450,
        "end_time": 530,
        "token_count": count_tokens("The second reason is a little bit different and this is that you want to learn AI so that you can sell AI stuff to your industry. Basically using your industry expertise and understanding and connections to figure out some kind of AI product or service that can be sold back to them. This also is one of the biggest areas of interest that I get people asking me about how they can pick up AI skills, bring a new product or service to market and sell it back to the people that they know and that they deeply understand.\n\nSo, it's basically just a vehicle or a model shift into the AI and using sort of the rapid growth and potential there to maybe build a software and get exits. It's just a shift and then selling back to the existing industry that you're coming from. This is super common in people who are already kind of tech-minded or very curious people and they're tinkering around with AI and I hear it all the time.")
    }
    
    # Chunk 7: Path 2 - Industry Opportunity Recognition
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "Path 2: The Industry Opportunity Gap",
        "text": """It's like man, I know we could build something the market is just waiting for something here like everyone is moving so slow they have no clue what going on they are miles behind when it comes to adoption for this stuff. I know that like I can see it. I just don't have enough knowledge about this technology to be able to fully spot the opportunity or to be able to like properly understand the feasibility. I see some opportunities, but I don't know if I want to take a big swing at it because I could end up wasting the next 3 to 5 years on this thing and just be completely off.

So, I get a lot of people coming to me asking, "Hey, Liam, could you like can you just give me a bit of a feasibility assessment or read on this? Am I completely dreaming or is this actually something that could have legs?" And technically is feasible. And I mean, for me, that's super easy for me to just sort of tell them point blank if it if it's good or has legs or not. But this is a very popular way that entrepreneurs are trying to get into AI.""",
        "start_time": 530,
        "end_time": 600,
        "token_count": count_tokens("It's like man, I know we could build something the market is just waiting for something here like everyone is moving so slow they have no clue what going on they are miles behind when it comes to adoption for this stuff. I know that like I can see it. I just don't have enough knowledge about this technology to be able to fully spot the opportunity or to be able to like properly understand the feasibility. I see some opportunities, but I don't know if I want to take a big swing at it because I could end up wasting the next 3 to 5 years on this thing and just be completely off.\n\nSo, I get a lot of people coming to me asking, \"Hey, Liam, could you like can you just give me a bit of a feasibility assessment or read on this? Am I completely dreaming or is this actually something that could have legs?\" And technically is feasible. And I mean, for me, that's super easy for me to just sort of tell them point blank if it if it's good or has legs or not. But this is a very popular way that entrepreneurs are trying to get into AI.")
    }
    
    # Chunk 8: Path 3 - Start New AI Business
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "Path 3: Launch an Entirely New AI Business",
        "text": """The third and final one is to start an entirely new AI business to jump fully out of your say you're in say you're in SMMA or you're running a marketing agency and you're like I'm sick of this. I want to get into something that has a bit more legs. I want to get a bit of a dev team under me. I want to start doing AI implementation and maybe consulting like we do at my agency and I really want to get into tapping into all of this demand for AI services like consulting and education and implementation and shift fully away from the sort of stagnant or old space that I'm in.

And this is a totally valid desire as well. That's basically what I did getting out of the marketing space and sort of retraining myself in AI and allowed me to start making content and build an agency around it and build a software and build an education business and build a big channel as well at the same time.""",
        "start_time": 600,
        "end_time": 680,
        "token_count": count_tokens("The third and final one is to start an entirely new AI business to jump fully out of your say you're in say you're in SMMA or you're running a marketing agency and you're like I'm sick of this. I want to get into something that has a bit more legs. I want to get a bit of a dev team under me. I want to start doing AI implementation and maybe consulting like we do at my agency and I really want to get into tapping into all of this demand for AI services like consulting and education and implementation and shift fully away from the sort of stagnant or old space that I'm in.\n\nAnd this is a totally valid desire as well. That's basically what I did getting out of the marketing space and sort of retraining myself in AI and allowed me to start making content and build an agency around it and build a software and build an education business and build a big channel as well at the same time.")
    }
    
    # Chunk 9: Strategy Overview - Fastest Methods
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "Strategy Introduction: Why Speed Matters Over Comprehensiveness",
        "text": """Okay, so for each of these methods, what is the fastest way for you to learn AI? I say fastest very deliberately because as I said in the introduction, there are I could send all of you down the route of here's a six-month roadmap of development courses and YouTube videos and projects you need to do and just a ton of stuff for you to learn and sit there and do. And I mean that's a totally valid route. And like I said, I'm going to give you a resource at the end of this on how if you want to take that route, you would and a clear roadmap to learn the skills.

But what's going to be more valuable for you is if from my experience, I can tell you what is actually the fastest way and the most sort of productive way of trying to learn AI given which of the three reasons you're trying to get into AI that we've just covered.""",
        "start_time": 680,
        "end_time": 750,
        "token_count": count_tokens("Okay, so for each of these methods, what is the fastest way for you to learn AI? I say fastest very deliberately because as I said in the introduction, there are I could send all of you down the route of here's a six-month roadmap of development courses and YouTube videos and projects you need to do and just a ton of stuff for you to learn and sit there and do. And I mean that's a totally valid route. And like I said, I'm going to give you a resource at the end of this on how if you want to take that route, you would and a clear roadmap to learn the skills.\n\nBut what's going to be more valuable for you is if from my experience, I can tell you what is actually the fastest way and the most sort of productive way of trying to learn AI given which of the three reasons you're trying to get into AI that we've just covered.")
    }
    
    # Chunk 10: Path 1 Strategy - Work with AI Agency
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "Path 1 Strategy: Partner with AI Agencies Instead of Self-Learning",
        "text": """So in terms of if you are trying to apply AI to your own business, I do not recommend you sitting there and taking courses you're a business owner, you're busy, you barely got enough time to do the fun and sort of free time things that you want to do. It's going to be very difficult for you to shave off like half the day every day for three months to learn this stuff because your goal is to learn AI in order to be able to lead your company better and sort of make sure that you guys are keeping up and find an advantage and an edge.

A much faster way of getting to that goal is to work with an agency. There's this huge AI agency market and ecosystem that's that's popped off the back of the videos that I made a few years ago when I started talking about what we were doing at Morningside AI in my agency. And now, thanks to me banging the drum for so long, there's a rapidly growing space of AI service providers who are intended to fill this gap in the market for you, which can help you to identify where AI can be useful in your business to educate your team and to build them for you as well.""",
        "start_time": 750,
        "end_time": 850,
        "token_count": count_tokens("So in terms of if you are trying to apply AI to your own business, I do not recommend you sitting there and taking courses you're a business owner, you're busy, you barely got enough time to do the fun and sort of free time things that you want to do. It's going to be very difficult for you to shave off like half the day every day for three months to learn this stuff because your goal is to learn AI in order to be able to lead your company better and sort of make sure that you guys are keeping up and find an advantage and an edge.\n\nA much faster way of getting to that goal is to work with an agency. There's this huge AI agency market and ecosystem that's that's popped off the back of the videos that I made a few years ago when I started talking about what we were doing at Morningside AI in my agency. And now, thanks to me banging the drum for so long, there's a rapidly growing space of AI service providers who are intended to fill this gap in the market for you, which can help you to identify where AI can be useful in your business to educate your team and to build them for you as well.")
    }
    
    # Chunk 11: Morningside AI Case Study
    chunk_11 = {
        "chunk_index": 11,
        "chapter_title": "Case Study: Morningside AI's Full-Cycle Transformation Process",
        "text": """Now, for example, my agency, Morningside AI, is what's considered an AI transformation partner. And so, we are a full cycle AI partner for our clients. We take them from the anywhere in your AI journey. We can start at the very like the first exposure to AI. What is this in your company? What does it mean? training the teams and start at that point by helping to train the leadership team, teach you and take you and your team through workshops.

Then we get into a discovery phase where we analyze your whole business, map all your processes and my team goes in and spots all the opportunities for AI implementation. And we identify quick wins where you can maybe apply an existing tool to a current process and it's going to massively improve the efficiency or free up a bunch of time. And then we also identify the big swings. What are the big systems that you can kind of rethink your acquisition or your customer support system? Those are the big swings that will take a lot more energy and effort and resources, but they are the big shifts that are going to give you the biggest competitive advantage long term.""",
        "start_time": 850,
        "end_time": 950,
        "token_count": count_tokens("Now, for example, my agency, Morningside AI, is what's considered an AI transformation partner. And so, we are a full cycle AI partner for our clients. We take them from the anywhere in your AI journey. We can start at the very like the first exposure to AI. What is this in your company? What does it mean? training the teams and start at that point by helping to train the leadership team, teach you and take you and your team through workshops.\n\nThen we get into a discovery phase where we analyze your whole business, map all your processes and my team goes in and spots all the opportunities for AI implementation. And we identify quick wins where you can maybe apply an existing tool to a current process and it's going to massively improve the efficiency or free up a bunch of time. And then we also identify the big swings. What are the big systems that you can kind of rethink your acquisition or your customer support system? Those are the big swings that will take a lot more energy and effort and resources, but they are the big shifts that are going to give you the biggest competitive advantage long term.")
    }
    
    # Chunk 12: Path 1 Strategy - Connection Offer
    chunk_12 = {
        "chunk_index": 12,
        "chapter_title": "Path 1 Solution: Connect with Expert AI Service Providers",
        "text": """And not to make this into a big sales pitch from agency, but we are very selective about who we work with. And it's typically companies bigger than 200 to 300 people. So, unless you're at that range, then we're probably not the best for you, but I have my accelerator program. I have my school community. So, I have access to all of the leading AI service providers in the basically the entire space right now. So, I'm going to be putting a form down in the description below. If you are a business owner wanting to learn AI from experts and have sort of them come in and audit your business, help train you and your team, I will have a form down below where you can leave your details and I'll be able to connect you up to the leading service providers out of my accelerator program.

So even though we won't be able to help you unless you're one of these bigger companies that we work with, I can definitely facilitate the connection between you and some of my students who can help you to achieve this because just them being there for you to hop on calls with and go through this consulting process and you probably have a ton of questions around, hey, can we do this? Why can't we do this? or just being able to have an expert there to talk to about this all the time is a massive win for you in terms of the goals that you're trying to achieve.""",
        "start_time": 950,
        "end_time": 1080,
        "token_count": count_tokens("And not to make this into a big sales pitch from agency, but we are very selective about who we work with. And it's typically companies bigger than 200 to 300 people. So, unless you're at that range, then we're probably not the best for you, but I have my accelerator program. I have my school community. So, I have access to all of the leading AI service providers in the basically the entire space right now. So, I'm going to be putting a form down in the description below. If you are a business owner wanting to learn AI from experts and have sort of them come in and audit your business, help train you and your team, I will have a form down below where you can leave your details and I'll be able to connect you up to the leading service providers out of my accelerator program.\n\nSo even though we won't be able to help you unless you're one of these bigger companies that we work with, I can definitely facilitate the connection between you and some of my students who can help you to achieve this because just them being there for you to hop on calls with and go through this consulting process and you probably have a ton of questions around, hey, can we do this? Why can't we do this? or just being able to have an expert there to talk to about this all the time is a massive win for you in terms of the goals that you're trying to achieve.")
    }
    
    # Chunk 13: Path 1 Summary
    chunk_13 = {
        "chunk_index": 13,
        "chapter_title": "Path 1 Recommendation: Skip Self-Learning, Go Straight to Implementation",
        "text": """So, if you are learning AI for the purpose of applying AI to your own business, I highly recommend you just cut the corner and just go straight for working with a really good agency who can train you and your team and identify all the best opportunities for AI implementation in your company and then also do the development as well.""",
        "start_time": 1080,
        "end_time": 1100,
        "token_count": count_tokens("So, if you are learning AI for the purpose of applying AI to your own business, I highly recommend you just cut the corner and just go straight for working with a really good agency who can train you and your team and identify all the best opportunities for AI implementation in your company and then also do the development as well.")
    }
    
    # Chunk 14: Path 2 Strategy - Partner with Technical Teams
    chunk_14 = {
        "chunk_index": 14,
        "chapter_title": "Path 2 Strategy: Leverage Your Industry Connections + Technical Partners",
        "text": """For the second one, if you're looking to sell AI stuff in your industry, again, I'm going to give you probably a little bit of a different angle to what you'd expect on this, but what I recommend here is kind of a similar strategy in that if you are an established business owner, you have maybe 10 or five or 10 years of experience, you have a lot of connections in a given industry. Like for example, I was just talking to a friend of mine who asked me the same question and he's talking about like, man, I've got all the connections. I'm one of the top people in my field. I've got all the social capital and all the knowhow about the industry and I want to get into AI somehow.

And what I ended up recommending to him is, yeah, sure, I'll give you this set of resources, which I'll give to you guys at the end. As I said, I'll give you this. You can just keep chipping away on that and sort of building up your skills. But the faster and more direct way is going to be realizing that you have a huge amount of cards on hand right now.""",
        "start_time": 1100,
        "end_time": 1180,
        "token_count": count_tokens("For the second one, if you're looking to sell AI stuff in your industry, again, I'm going to give you probably a little bit of a different angle to what you'd expect on this, but what I recommend here is kind of a similar strategy in that if you are an established business owner, you have maybe 10 or five or 10 years of experience, you have a lot of connections in a given industry. Like for example, I was just talking to a friend of mine who asked me the same question and he's talking about like, man, I've got all the connections. I'm one of the top people in my field. I've got all the social capital and all the knowhow about the industry and I want to get into AI somehow.\n\nAnd what I ended up recommending to him is, yeah, sure, I'll give you this set of resources, which I'll give to you guys at the end. As I said, I'll give you this. You can just keep chipping away on that and sort of building up your skills. But the faster and more direct way is going to be realizing that you have a huge amount of cards on hand right now.")
    }
    
    # Chunk 15: Path 2 - Technical Team Matching Problem
    chunk_15 = {
        "chunk_index": 15,
        "chapter_title": "Path 2: The Hidden Opportunity - Strong Teams Need Industry Partners",
        "text": """And I see it all the time in my program and in my free community as well. There are killer teams out there who are grinding away, struggling, just not being able to get the leads or they don't have a clear niche or they don't have a clear pathway for them to shoot down. It kills me to see these guys who are so capable technically and some of the most experienced minds for AI implementation for companies, but they just can't market themselves that well despite all of the guidance that I give them through my course material and the coaches, some people are just not that good at maybe the content creation stuff. And so there are like diamonds in the rough here. And among the thousands and thousands of agencies that are now popping up, there are actually hundreds of really good teams that are begging or waiting for someone like yourself to come along.""",
        "start_time": 1180,
        "end_time": 1250,
        "token_count": count_tokens("And I see it all the time in my program and in my free community as well. There are killer teams out there who are grinding away, struggling, just not being able to get the leads or they don't have a clear niche or they don't have a clear pathway for them to shoot down. It kills me to see these guys who are so capable technically and some of the most experienced minds for AI implementation for companies, but they just can't market themselves that well despite all of the guidance that I give them through my course material and the coaches, some people are just not that good at maybe the content creation stuff. And so there are like diamonds in the rough here. And among the thousands and thousands of agencies that are now popping up, there are actually hundreds of really good teams that are begging or waiting for someone like yourself to come along.")
    }
    
    # Chunk 16: Path 2 - Partnership Strategy Details
    chunk_16 = {
        "chunk_index": 16,
        "chapter_title": "Path 2 Partnership Model: Immediate Monetization + Learning",
        "text": """And in the case of the guy I was just talking about with all of his connections and his industry knowhow and he's like man. I just want to get. I just need the I need the way to get my power down to the road like where the rubber meets the road. I need to like get this power down and that's going to be done through a team who can actually deliver for him and provide that technical understanding to be the enough to ground his ideas and sort of channel all of his industry knowledge and expertise to productive means.

So if you have that background of solid connections, really deep understanding of your industry, there are agencies out there who would love for you to just sort of say, "Look, I know there's opportunity here. I've got these leads. Let me start introducing us. I want to be really involved in this process. I want you guys to teach me on the job." So you basically immediately can start monetizing your knowledge and your connections. And you're telling them, hey, look, I know that there's a few of these bottlenecks in all of these businesses that are similar to the ones that I've run. Can we come up with some a rough set of solutions that we could offer to people? I'll go to my warm connections. I'll be able to pull them in.""",
        "start_time": 1250,
        "end_time": 1350,
        "token_count": count_tokens("And in the case of the guy I was just talking about with all of his connections and his industry knowhow and he's like man. I just want to get. I just need the I need the way to get my power down to the road like where the rubber meets the road. I need to like get this power down and that's going to be done through a team who can actually deliver for him and provide that technical understanding to be the enough to ground his ideas and sort of channel all of his industry knowledge and expertise to productive means.\n\nSo if you have that background of solid connections, really deep understanding of your industry, there are agencies out there who would love for you to just sort of say, \"Look, I know there's opportunity here. I've got these leads. Let me start introducing us. I want to be really involved in this process. I want you guys to teach me on the job.\" So you basically immediately can start monetizing your knowledge and your connections. And you're telling them, hey, look, I know that there's a few of these bottlenecks in all of these businesses that are similar to the ones that I've run. Can we come up with some a rough set of solutions that we could offer to people? I'll go to my warm connections. I'll be able to pull them in.")
    }
    
    # Chunk 17: Path 2 - Natural Business Evolution
    chunk_17 = {
        "chunk_index": 17,
        "chapter_title": "Path 2 Growth Pattern: From Partnership to Niche AI Business",
        "text": """And we start a project off and if we do a few of these before you know it well one you the guy who's trying to get into AI is going to learn so much from that team in a very short amount of time and you're also going to be able to make money and before you know it you'll probably have identified a few really key plays that well this thing see this across all five clients we've taken on this this one particular thing and they are loving that so why don't we niche down even further to that why don't we get a sort of niche AI offer and start plugging in this this kind of AI system into more and more people and scaling it up with ads and before you know it you've got a very successful AI business that's selling stuff in your industry without having to go the super long road of learning it all yourself and building up.

And I guess the key bit of knowledge and value that I'm trying to give to you here is that there are teams out there looking for people like you begging for it. So if you're in this position particularly where you have a depth of industry knowledge in a given industry and you have a lot of connection as well that you can sell directly to or a way to help distribute this, you are in such an incredible position.""",
        "start_time": 1350,
        "end_time": 1430,
        "token_count": count_tokens("And we start a project off and if we do a few of these before you know it well one you the guy who's trying to get into AI is going to learn so much from that team in a very short amount of time and you're also going to be able to make money and before you know it you'll probably have identified a few really key plays that well this thing see this across all five clients we've taken on this this one particular thing and they are loving that so why don't we niche down even further to that why don't we get a sort of niche AI offer and start plugging in this this kind of AI system into more and more people and scaling it up with ads and before you know it you've got a very successful AI business that's selling stuff in your industry without having to go the super long road of learning it all yourself and building up.\n\nAnd I guess the key bit of knowledge and value that I'm trying to give to you here is that there are teams out there looking for people like you begging for it. So if you're in this position particularly where you have a depth of industry knowledge in a given industry and you have a lot of connection as well that you can sell directly to or a way to help distribute this, you are in such an incredible position.")
    }
    
    # Chunk 18: Path 2 - Partnership Facilitation Offer
    chunk_18 = {
        "chunk_index": 18,
        "chapter_title": "Path 2 Connection Service: Matching Industry Experts with Technical Teams",
        "text": """So, if you fill out the form in the description below, I will be able to connect you up with people in my accelerator program, the top students that I have there who are hungry for something like that. I'm more than happy to help facilitate some of you guys being paired up because I think you're going to do awesome stuff. It's great for my students as well. So, if you want to fill that out, I'm more than happy to help tea up some of those partnerships because you and a good capable development team is like a match made in heaven. You can just drop your details in the form in the description.""",
        "start_time": 1430,
        "end_time": 1480,
        "token_count": count_tokens("So, if you fill out the form in the description below, I will be able to connect you up with people in my accelerator program, the top students that I have there who are hungry for something like that. I'm more than happy to help facilitate some of you guys being paired up because I think you're going to do awesome stuff. It's great for my students as well. So, if you want to fill that out, I'm more than happy to help tea up some of those partnerships because you and a good capable development team is like a match made in heaven. You can just drop your details in the form in the description.")
    }
    
    # Chunk 19: Path 3 - New AI Business Challenge
    chunk_19 = {
        "chunk_index": 19,
        "chapter_title": "Path 3 Reality Check: The Challenge of Starting Fresh in AI",
        "text": """And now getting into the final one is that you just want to learn AI in order to be able to start an entirely new AI business. Shift out of what you're doing before and get into a new AI based business vehicle. So, for this, you are going to have to roll up your sleeves and get your hands dirty and get into this. And so, if this is really what you want to do, firstly, I respect it. It's a it's it's a bit of a scary thing to do to be looking down the barrel of a career shift and a full reskilling into a different area. But I can tell you it's been one of the most rewarding things that I've ever done and also one of the most value creating things for my career because what you guys need to understand is that you already have the entrepreneurial skills here.""",
        "start_time": 1480,
        "end_time": 1540,
        "token_count": count_tokens("And now getting into the final one is that you just want to learn AI in order to be able to start an entirely new AI business. Shift out of what you're doing before and get into a new AI based business vehicle. So, for this, you are going to have to roll up your sleeves and get your hands dirty and get into this. And so, if this is really what you want to do, firstly, I respect it. It's a it's it's a bit of a scary thing to do to be looking down the barrel of a career shift and a full reskilling into a different area. But I can tell you it's been one of the most rewarding things that I've ever done and also one of the most value creating things for my career because what you guys need to understand is that you already have the entrepreneurial skills here.")
    }
    
    # Chunk 20: Path 3 - Entrepreneurial Skills Advantage
    chunk_20 = {
        "chunk_index": 20,
        "chapter_title": "Path 3 Advantage: Your Existing Entrepreneurial Skills Are 67% of Success",
        "text": """I try to tell this to my students all the time, but there's to get into AI business. There's kind of the entrepreneur skills of like the discipline, the mindset that it takes to succeed, the understanding of like online business or fundamentals, funnels and paid ads and psychology and hooks, how to keep a P&L, all these kind of entrepreneurial skills that you will have picked up by now in your own journey. That is like a non-insignificant that's like two-thirds of the pie when it comes to starting a successful AI business.

And for most people coming in who don't have that and they don't have AI as well, they have a very long road ahead of them because they have to learn the whole thing. And entrepreneurial skills really, as I'm sure you'll know, they come through kind of a very gradual process of as you build the business, you get, oh, so now I have to learn how to do a P&L. Oh, okay. So now, oh, my hooks aren't good enough. Can I study hooks? And so it takes a long time for you to build that entrepreneurial skill set, but you have it. And so what we're really trying to do now for learning AI for you is just putting that that sort of cherry on top, that extra 30% of knowledge that's going to allow you to use that entrepreneurial skills base that you have to move into selling some sort of AI product or service.""",
        "start_time": 1540,
        "end_time": 1640,
        "token_count": count_tokens("I try to tell this to my students all the time, but there's to get into AI business. There's kind of the entrepreneur skills of like the discipline, the mindset that it takes to succeed, the understanding of like online business or fundamentals, funnels and paid ads and psychology and hooks, how to keep a P&L, all these kind of entrepreneurial skills that you will have picked up by now in your own journey. That is like a non-insignificant that's like two-thirds of the pie when it comes to starting a successful AI business.\n\nAnd for most people coming in who don't have that and they don't have AI as well, they have a very long road ahead of them because they have to learn the whole thing. And entrepreneurial skills really, as I'm sure you'll know, they come through kind of a very gradual process of as you build the business, you get, oh, so now I have to learn how to do a P&L. Oh, okay. So now, oh, my hooks aren't good enough. Can I study hooks? And so it takes a long time for you to build that entrepreneurial skill set, but you have it. And so what we're really trying to do now for learning AI for you is just putting that that sort of cherry on top, that extra 30% of knowledge that's going to allow you to use that entrepreneurial skills base that you have to move into selling some sort of AI product or service.")
    }
    
    # Chunk 21: Path 3 - Personal Success Story
    chunk_21 = {
        "chunk_index": 21,
        "chapter_title": "Path 3 Success Story: From ChatGPT Launch to $10M Business",
        "text": """And so like I said, this is what I did in early 2023. I saw the release of ChatGPT and I was like, "Holy shit this is the future." I just made a channel immediately and I just started going all in on learning whatever I could and making videos about it. And that's sort of long story short, that's how I got here. And I made a whole bunch of AI businesses in between.

And so the method that took me from where you are now to where I am now on track to do over $10 million in revenue across all businesses this year is a framework that I call Potentia. So that name and idea came from this tattoo that I have here which is a man sort of chiseling himself out of marble. And this is the sort of concept of the self-made man. And I see all of us as being essentially this big block of marble that is just waiting to be kind of revealed through work. And what I discovered in the AI space, this Potentia framework is by far the most efficient way to reveal the ultimate form or the masterpiece that's inside of you as fast as possible.""",
        "start_time": 1640,
        "end_time": 1720,
        "token_count": count_tokens("And so like I said, this is what I did in early 2023. I saw the release of ChatGPT and I was like, \"Holy shit this is the future.\" I just made a channel immediately and I just started going all in on learning whatever I could and making videos about it. And that's sort of long story short, that's how I got here. And I made a whole bunch of AI businesses in between.\n\nAnd so the method that took me from where you are now to where I am now on track to do over $10 million in revenue across all businesses this year is a framework that I call Potentia. So that name and idea came from this tattoo that I have here which is a man sort of chiseling himself out of marble. And this is the sort of concept of the self-made man. And I see all of us as being essentially this big block of marble that is just waiting to be kind of revealed through work. And what I discovered in the AI space, this Potentia framework is by far the most efficient way to reveal the ultimate form or the masterpiece that's inside of you as fast as possible.")
    }
    
    # Chunk 22: Potentia Framework Introduction
    chunk_22 = {
        "chunk_index": 22,
        "chapter_title": "Potentia Framework: The Proven Method for AI Business Success",
        "text": """And so what I'm about to share with you right now is some mega source. That is literally the key to how I got to this point so quickly. And this exact method has now been replicated by thousands and thousands of other people. Basically, anyone you see running a successful AI business has used this in some kind of way.

But Potentia is basically a personal and career development framework that combines the learning of AI skills with content creation and the creation of an AI business typically going to be the AI service based business. And it works by creating a powerful upward spiral that once you're in it, it's kind of hard to get out and it can just completely transform your life in space. All right, so here's how it works.""",
        "start_time": 1720,
        "end_time": 1780,
        "token_count": count_tokens("And so what I'm about to share with you right now is some mega source. That is literally the key to how I got to this point so quickly. And this exact method has now been replicated by thousands and thousands of other people. Basically, anyone you see running a successful AI business has used this in some kind of way.\n\nBut Potentia is basically a personal and career development framework that combines the learning of AI skills with content creation and the creation of an AI business typically going to be the AI service based business. And it works by creating a powerful upward spiral that once you're in it, it's kind of hard to get out and it can just completely transform your life in space. All right, so here's how it works.")
    }
    
    # Chunk 23: Three Hurdles Problem
    chunk_23 = {
        "chunk_index": 23,
        "chapter_title": "The Three Hurdles Every AI Entrepreneur Must Clear",
        "text": """So in order to start an AI business from scratch, there are three problems. The three hurdles is what I call them. You have technical expertise, you need to have some kind of knowledge gap or knowledge advantage over the people that you're trying to help because to get started, you're going to need to make some kind of AI service based business, whether it's education or consulting or development or all three. In order to do any of those things, you need to have some kind of knowledge gap is what I call it where your clients are here and you are here and here's the smartest guy in the world, but at least you're ahead of them, right? So the knowledge gap is where you make your money in the AI space. So the first hurdle is technical expertise. This is the foundation of your career in the AI space. And it starts with basic AI automation skills, which I'm going to touch on a little bit later.

The second hurdle is consistent lead flow. And if you're an entrepreneur, this is probably pretty self-explanatory. You need leads, like no leads, no business. And you need that to be consistent as well because you can't make key hires and scale if you can't get some sort of consistency with your leads where you can say, "Okay, well, next month I have 10 grand in outgoings. Well, this month we generated 50 leads. If we get anything like that or more, next month we'll be able to cover those costs." So consistent lead flow is hurdle number two.""",
        "start_time": 1780,
        "end_time": 1880,
        "token_count": count_tokens("So in order to start an AI business from scratch, there are three problems. The three hurdles is what I call them. You have technical expertise, you need to have some kind of knowledge gap or knowledge advantage over the people that you're trying to help because to get started, you're going to need to make some kind of AI service based business, whether it's education or consulting or development or all three. In order to do any of those things, you need to have some kind of knowledge gap is what I call it where your clients are here and you are here and here's the smartest guy in the world, but at least you're ahead of them, right? So the knowledge gap is where you make your money in the AI space. So the first hurdle is technical expertise. This is the foundation of your career in the AI space. And it starts with basic AI automation skills, which I'm going to touch on a little bit later.\n\nThe second hurdle is consistent lead flow. And if you're an entrepreneur, this is probably pretty self-explanatory. You need leads, like no leads, no business. And you need that to be consistent as well because you can't make key hires and scale if you can't get some sort of consistency with your leads where you can say, \"Okay, well, next month I have 10 grand in outgoings. Well, this month we generated 50 leads. If we get anything like that or more, next month we'll be able to cover those costs.\" So consistent lead flow is hurdle number two.")
    }
    
    # Chunk 24: Third Hurdle - Authority
    chunk_24 = {
        "chunk_index": 24,
        "chapter_title": "Hurdle 3: Authority and Credibility Through Personal Brand",
        "text": """And then hurdle number three that you have to get over to make a successful AI business is some source of authority or credibility. This typically comes from a personal brand. That's at least how I've done it. I don't really know any other ways of doing it. You could have a massive track record of successful projects for your agency and that's your source of credibility. But at the end of the day, that's going to be a lot harder to get and take a lot longer to get there than just building up a few thousand followers or making some good content. So authority and credibility is what's going to get those deals over the line. It's what's going to convince business owners that you are the person to work with. It's going to also for the long term make sure that you stand out above all of the other people trying to get into this right now. So, the personal brand is essential to the trust required to get these deals over the line with your AI service based business.""",
        "start_time": 1880,
        "end_time": 1950,
        "token_count": count_tokens("And then hurdle number three that you have to get over to make a successful AI business is some source of authority or credibility. This typically comes from a personal brand. That's at least how I've done it. I don't really know any other ways of doing it. You could have a massive track record of successful projects for your agency and that's your source of credibility. But at the end of the day, that's going to be a lot harder to get and take a lot longer to get there than just building up a few thousand followers or making some good content. So authority and credibility is what's going to get those deals over the line. It's what's going to convince business owners that you are the person to work with. It's going to also for the long term make sure that you stand out above all of the other people trying to get into this right now. So, the personal brand is essential to the trust required to get these deals over the line with your AI service based business.")
    }
    
    # Chunk 25: Traditional Approach Problem
    chunk_25 = {
        "chunk_index": 25,
        "chapter_title": "Why the Traditional Sequential Approach Fails",
        "text": """Now, the trick here with Potentia is that most people would just tackle these one by one, right? You'd go all right, I need to do the technical expertise. I'm going to go and spend 3 6 months working on courses and learning my AI skill set. And then once you've got that skill set, you go, "Okay, yeah, sweet. No, no, I guess I'll go market myself now. Maybe I'll go and set up some ads. I'll build a funnel. I'll set up a website. I'll start running ads. And I'll figure out some random offer that I saw on a YouTube video about what apparently what's selling right now. And I'll try to sell that. And then as for the final hurdle, authority and credibility. They've probably got nothing. They might put some bullshit up on their website or make some bogus claim in their VSL to try and get the booking or have a bit of credibility. But at the end of the day, you got no leg to stand on if they ask you, "Why should I trust you with my business?" Like, "What have you done before?"

So this piecemeal approach of just attacking one hurdle at a time is highly inefficient because you're going to spend so long maybe 3 6 months learning your skills and then another like two months setting up your funnel and testing it before you start getting it and finally realize that it's or testing offers and then realizing that it's not working because you have no authority and then maybe you're going to spend another 3 months after that trying to build a personal brand because you realize that no one's going to listen to you if you don't have one.""",
        "start_time": 1950,
        "end_time": 2100,
        "token_count": count_tokens("Now, the trick here with Potentia is that most people would just tackle these one by one, right? You'd go all right, I need to do the technical expertise. I'm going to go and spend 3 6 months working on courses and learning my AI skill set. And then once you've got that skill set, you go, \"Okay, yeah, sweet. No, no, I guess I'll go market myself now. Maybe I'll go and set up some ads. I'll build a funnel. I'll set up a website. I'll start running ads. And I'll figure out some random offer that I saw on a YouTube video about what apparently what's selling right now. And I'll try to sell that. And then as for the final hurdle, authority and credibility. They've probably got nothing. They might put some bullshit up on their website or make some bogus claim in their VSL to try and get the booking or have a bit of credibility. But at the end of the day, you got no leg to stand on if they ask you, \"Why should I trust you with my business?\" Like, \"What have you done before?\"\n\nSo this piecemeal approach of just attacking one hurdle at a time is highly inefficient because you're going to spend so long maybe 3 6 months learning your skills and then another like two months setting up your funnel and testing it before you start getting it and finally realize that it's or testing offers and then realizing that it's not working because you have no authority and then maybe you're going to spend another 3 months after that trying to build a personal brand because you realize that no one's going to listen to you if you don't have one.")
    }
    
    # Chunk 26: Potentia Solution
    chunk_26 = {
        "chunk_index": 26,
        "chapter_title": "Potentia's Simultaneous Solution: Clear All Three Hurdles at Once",
        "text": """And so what the Potentia framework is all about is combining all of those together into a strategy that clears all three hurdles at once. And this is how I've had such rapid success in the AI space and you are in the exact same position as I was with that entrepreneurial skills base and you apply this Potentia framework on top and I've seen it just like it's completely changed my life and I've seen it happen in front of my eyes over and over and over again. So Potentia is basically a system that clears all three of these at once.""",
        "start_time": 2100,
        "end_time": 2140,
        "token_count": count_tokens("And so what the Potentia framework is all about is combining all of those together into a strategy that clears all three hurdles at once. And this is how I've had such rapid success in the AI space and you are in the exact same position as I was with that entrepreneurial skills base and you apply this Potentia framework on top and I've seen it just like it's completely changed my life and I've seen it happen in front of my eyes over and over and over again. So Potentia is basically a system that clears all three of these at once.")
    }
    
    # Chunk 27: Potentia Implementation Steps
    chunk_27 = {
        "chunk_index": 27,
        "chapter_title": "How Potentia Works: Learn, Apply, Create Content Loop",
        "text": """And so here's how it works, right? So you start off with picking some kind of skill that interests you in the AI space whether that's AI agents or voice agents or AI automation or like these video generation models just anything in the AI space that interests you. AI automation is a good foundation to have and so you go out and you watch free courses like my AI agents guide which is like four hours long or my AI automation guide which is 2 hours long and I'll link those both in the description but you learn some sort of skills you get a bit of a base and then you try to solve either your own problems or the people around you or you sort of reach out to acquaintances you try to take that knowledge and apply it to the real world experiment with it and tinker with it beyond just the tutorials and in this process of learning by tutorials and then applying it to the real world or trying to solve your own problems with it. You are creating the material for creating some kind of content around what you were learning.""",
        "start_time": 2140,
        "end_time": 2220,
        "token_count": count_tokens("And so here's how it works, right? So you start off with picking some kind of skill that interests you in the AI space whether that's AI agents or voice agents or AI automation or like these video generation models just anything in the AI space that interests you. AI automation is a good foundation to have and so you go out and you watch free courses like my AI agents guide which is like four hours long or my AI automation guide which is 2 hours long and I'll link those both in the description but you learn some sort of skills you get a bit of a base and then you try to solve either your own problems or the people around you or you sort of reach out to acquaintances you try to take that knowledge and apply it to the real world experiment with it and tinker with it beyond just the tutorials and in this process of learning by tutorials and then applying it to the real world or trying to solve your own problems with it. You are creating the material for creating some kind of content around what you were learning.")
    }
    
    # Chunk 28: The Upward Spiral
    chunk_28 = {
        "chunk_index": 28,
        "chapter_title": "The Potentia Upward Spiral: Content Creation Drives Growth",
        "text": """So the upward spiral kicks in when you now take what you've learned and you start making videos on it. This is exactly what I did in the early stages of my channel. You can scroll down, scroll back and look. I just found this custom knowledge chatbot thing was interesting and I was like, "Oh, that's cool." So I just started experimenting with it, playing around with it. And then I started making videos on it and they get started getting a bunch of views and people like, "Wow, this is really cool. How do you do this? How do you do this?" And so I started making more videos and more videos and my channel just started to take off. And at the same time, of course, I start to get leads and interest. So, I start taking consulting calls. I start taking $300 consulting calls for 45 minutes. Before I know it's $500, before I know it, it's $1,000 for 45 minutes.""",
        "start_time": 2220,
        "end_time": 2300,
        "token_count": count_tokens("So the upward spiral kicks in when you now take what you've learned and you start making videos on it. This is exactly what I did in the early stages of my channel. You can scroll down, scroll back and look. I just found this custom knowledge chatbot thing was interesting and I was like, \"Oh, that's cool.\" So I just started experimenting with it, playing around with it. And then I started making videos on it and they get started getting a bunch of views and people like, \"Wow, this is really cool. How do you do this? How do you do this?\" And so I started making more videos and more videos and my channel just started to take off. And at the same time, of course, I start to get leads and interest. So, I start taking consulting calls. I start taking $300 consulting calls for 45 minutes. Before I know it's $500, before I know it, it's $1,000 for 45 minutes.")
    }
    
    # Chunk 29: The Incentivized Learning Loop
    chunk_29 = {
        "chunk_index": 29,
        "chapter_title": "Financial Incentivization: How Money Accelerates Learning",
        "text": """And you get sucked into this upward spiral where you get incentivized to learn new skills where it's like, hm, oh, there's this new thing that just came out. I'm going to go learn it, sort of apply it, and see what I can do with it, stretch it, play around with it. I'm going to make content that basically doesn't exist anywhere right now. And you're going to be rewarded by the market if you're making interesting content using most cases the newest stuff that's just come out. So instead of just learning for learning sake and being like, "Oh yeah, I'm just do tooling away learning," you can learn and then practice content creation and sort of create that into a video that can then grow your personal brand and start to build your authority and credibility to start to bring in leads and to build your technical expertise all at once. So you can see it's just clearing all of those hurdles in one go.""",
        "start_time": 2300,
        "end_time": 2380,
        "token_count": count_tokens("And you get sucked into this upward spiral where you get incentivized to learn new skills where it's like, hm, oh, there's this new thing that just came out. I'm going to go learn it, sort of apply it, and see what I can do with it, stretch it, play around with it. I'm going to make content that basically doesn't exist anywhere right now. And you're going to be rewarded by the market if you're making interesting content using most cases the newest stuff that's just come out. So instead of just learning for learning sake and being like, \"Oh yeah, I'm just do tooling away learning,\" you can learn and then practice content creation and sort of create that into a video that can then grow your personal brand and start to build your authority and credibility to start to bring in leads and to build your technical expertise all at once. So you can see it's just clearing all of those hurdles in one go.")
    }
    
    # Chunk 30: Monetization Flywheel
    chunk_30 = {
        "chunk_index": 30,
        "chapter_title": "The Complete Flywheel: Skills → Content → Authority → Revenue",
        "text": """And once you get the monetization piece fit in, whether it's an AI automation agency off the back or you're selling a course or you're selling consulting, you then have this financially incentivized loop where it's like, okay, well, if I go and learn new stuff and I make good videos on it and I sort of see how I can use it in interesting ways that people would be interested in watching or maybe help people to understand it as well. Say this new video generation BO3 model, you figure out a cool way to make like Yeti vlogs or something. Once you've figured that out, you make a video how to make Yeti vlogs as a beginner. And then it just starts to attract so many people to your channel, more leads, more credibility, more growth, and before you know it, you've got the AI skills you were looking for. You've got the personal brand that helps you to attract deals and also close them because of the authority that comes with it. And that is the powerful flywheel that took me from where you are now to where I am.""",
        "start_time": 2380,
        "end_time": 2460,
        "token_count": count_tokens("And once you get the monetization piece fit in, whether it's an AI automation agency off the back or you're selling a course or you're selling consulting, you then have this financially incentivized loop where it's like, okay, well, if I go and learn new stuff and I make good videos on it and I sort of see how I can use it in interesting ways that people would be interested in watching or maybe help people to understand it as well. Say this new video generation BO3 model, you figure out a cool way to make like Yeti vlogs or something. Once you've figured that out, you make a video how to make Yeti vlogs as a beginner. And then it just starts to attract so many people to your channel, more leads, more credibility, more growth, and before you know it, you've got the AI skills you were looking for. You've got the personal brand that helps you to attract deals and also close them because of the authority that comes with it. And that is the powerful flywheel that took me from where you are now to where I am.")
    }
    
    # Chunk 31: Framework Summary and Resources
    chunk_31 = {
        "chunk_index": 31,
        "chapter_title": "Potentia Summary: The Fastest Way to All Three Hurdles",
        "text": """To not drag this on too long, that is basically the way that I'd recommend for you to start a new AI business. If you are leaving your entrepreneurial vehicle and moving into a new one, that is the best way for you to learn the skills to get the lead flow consistently and also build your authority and credibility that you need to have an actual business. And I've learned this from all of my experience and from the thousands and thousands of people that have taught to do the same thing. This is the fastest way to clear those three hurdles.

So, as promised with this video, I will be attaching a resource down below that you guys can all get for free. It's going to break down this Potentia concept a bit more for you if you're looking to seriously consider it as a way for you to start your AI business, which I highly recommend. And I'll also include a how to learn AI guide for all of you entrepreneurs who having listened to everything that I've explained here is still like but if I wanted to spend three six months learning the stuff is the order that I should look to acquire these skills so that I can really give myself the best chance. I'm going to include that resource that I've given to a bunch of other entrepreneurs privately in that resource down below.""",
        "start_time": 2460,
        "end_time": 2580,
        "token_count": count_tokens("To not drag this on too long, that is basically the way that I'd recommend for you to start a new AI business. If you are leaving your entrepreneurial vehicle and moving into a new one, that is the best way for you to learn the skills to get the lead flow consistently and also build your authority and credibility that you need to have an actual business. And I've learned this from all of my experience and from the thousands and thousands of people that have taught to do the same thing. This is the fastest way to clear those three hurdles.\n\nSo, as promised with this video, I will be attaching a resource down below that you guys can all get for free. It's going to break down this Potentia concept a bit more for you if you're looking to seriously consider it as a way for you to start your AI business, which I highly recommend. And I'll also include a how to learn AI guide for all of you entrepreneurs who having listened to everything that I've explained here is still like but if I wanted to spend three six months learning the stuff is the order that I should look to acquire these skills so that I can really give myself the best chance. I'm going to include that resource that I've given to a bunch of other entrepreneurs privately in that resource down below.")
    }
    
    # Chunk 32: Final Motivation and Call to Action
    chunk_32 = {
        "chunk_index": 32,
        "chapter_title": "Final Encouragement: It's About the Boat You're In",
        "text": """But yeah, I am so excited for you guys to get into this. I mean, like I said, it's not about how hard you row, it's about what boat you're in. That's a Warren Buffett quote and there's nothing truer than that when it comes to shifting into the AI space. So I'm so excited for you guys to get into it. I hope this has been valuable and so yeah, I look forward to seeing you out there in the AI arena. If you want to learn no code AI automation, which I recommend is the best place for you to start with your skills space. It's kind of the meta skill that you need to do anything in the AI space these days. I'll put that video up there. 2-hour free course that I did recently. Absolute banger. Check that out. But aside from that, guys, thank you so much for watching. That is all and I'll see""",
        "start_time": 2580,
        "end_time": 2640,
        "token_count": count_tokens("But yeah, I am so excited for you guys to get into this. I mean, like I said, it's not about how hard you row, it's about what boat you're in. That's a Warren Buffett quote and there's nothing truer than that when it comes to shifting into the AI space. So I'm so excited for you guys to get into it. I hope this has been valuable and so yeah, I look forward to seeing you out there in the AI arena. If you want to learn no code AI automation, which I recommend is the best place for you to start with your skills space. It's kind of the meta skill that you need to do anything in the AI space these days. I'll put that video up there. 2-hour free course that I did recently. Absolute banger. Check that out. But aside from that, guys, thank you so much for watching. That is all and I'll see")
    }
    
    chunks.extend([chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, chunk_9, chunk_10, 
                   chunk_11, chunk_12, chunk_13, chunk_14, chunk_15, chunk_16, chunk_17, chunk_18, chunk_19, chunk_20,
                   chunk_21, chunk_22, chunk_23, chunk_24, chunk_25, chunk_26, chunk_27, chunk_28, chunk_29, chunk_30,
                   chunk_31, chunk_32])
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Calculate token statistics
    total_tokens = sum(chunk["token_count"] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks)
    
    # Create the final JSON structure
    result = {
        "video_id": "rOUs76wtv60",
        "title": "How to Learn AI as an Entrepreneur (3 Beginner Paths)",
        "channel": "Liam Ottley",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens)
        }
    }
    
    # Write to JSON file
    with open("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_liam_ottley_entrepreneur_rOUs76wtv60.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} chunks with average {avg_tokens:.0f} tokens per chunk")
    print(f"Total tokens: {total_tokens}")
    print("Manual chunker completed successfully!")

if __name__ == "__main__":
    main()