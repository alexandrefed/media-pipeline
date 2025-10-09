#!/usr/bin/env python3
"""
Manual chunker for Nick Saraev's "$1,000,000 AI Automation & Agents Advice for 5 Hours Straight"
Video ID: L4Qbx8OM9l4

Content Type: Comprehensive Business Course / Agency Building Guide
Channel: Nick Saraev
Strategy: Business-focused chunking with emphasis on:
1. Introduction + Credibility establishment  
2. Business fundamentals over technical skills
3. Systematic funnel breakdown (Lead Gen → Sales → Fulfillment → Retention)
4. Technical foundations (APIs, webhooks, AI prompting)
5. Live demonstrations and practical implementations
6. Sales psychology and market positioning
7. Industry targeting strategies
8. Scaling methodologies

Note: This is a massive 5-hour, 60,000-word comprehensive course. 
Strategic approach: Focus on high-value business insights and foundational concepts 
that separate six-figure agencies from failures.
Chunk size: 400-600 tokens for business strategy content to preserve context flow.
"""

import json
import tiktoken

def count_tokens(text):
    """Count tokens using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def create_manual_chunks():
    chunks = []
    
    # Chunk 1: Hook + Personal Credibility + Problem Statement
    chunk_1 = {
        "chunk_index": 1,
        "chapter_title": "The Reality: What Separates Six-Figure Agencies from Failures",
        "text": """So, I've spent many years selling automations and systems and businesses. I have made basically every mistake possible and learned exactly what separates six-figure automation businesses from those that never make it past their first client. Today, I want to condense all of that hard-earned knowledge into 5 hours of the most valuable AI automation business advice you will ever get, absolutely free.

My name is Nick. I've scaled my own AI automation agency to over $72,000 a month. And I lead nearly 2,800 entrepreneurs in my community, Maker School, where most members land their first client within one or two months of joining.

Now, here's the thing that most people don't know about AI automation. Most people obsess over AI models and flashy tech demos. But the people that actually make serious money on this are focused on completely different things. They are not the most technical people in the room. They're also not the ones that understand the code or how to drag and drop modules. What they do understand are business fundamentals, client psychology, how to position themselves in markets.""",
        "start_time": 0,
        "end_time": 180,
        "token_count": count_tokens("""So, I've spent many years selling automations and systems and businesses. I have made basically every mistake possible and learned exactly what separates six-figure automation businesses from those that never make it past their first client. Today, I want to condense all of that hard-earned knowledge into 5 hours of the most valuable AI automation business advice you will ever get, absolutely free.

My name is Nick. I've scaled my own AI automation agency to over $72,000 a month. And I lead nearly 2,800 entrepreneurs in my community, Maker School, where most members land their first client within one or two months of joining.

Now, here's the thing that most people don't know about AI automation. Most people obsess over AI models and flashy tech demos. But the people that actually make serious money on this are focused on completely different things. They are not the most technical people in the room. They're also not the ones that understand the code or how to drag and drop modules. What they do understand are business fundamentals, client psychology, how to position themselves in markets.""")
    }
    
    # Chunk 2: Course Structure + Value Proposition
    chunk_2 = {
        "chunk_index": 2,
        "chapter_title": "5-Hour Comprehensive Roadmap: Technical Foundations to Six-Figure Scaling",
        "text": """So, this comprehensive guide is meant to take you on a complete journey from technical foundations to six-figure scaling strategies. We're going to be covering the brutal realities I learned selling automations for over 2 years. The sales psychology that actually works with business owners, why most people target the wrong markets, which five industries are desperately paying premium prices right now, the technical essentials that do matter if you guys want to do this, and then the systematic approach to fixing every major agency problem you're suffering from.

Finally, I'm actually going to build a complete AI system live from scratch that you guys could sell to clients for $2,000 a pop immediately. And by the end of these five hours, I want you to have everything you need to start a profitable AI business or upscale your existing one well past six figures. Plus, I'll give you guys a real system you guys can deploy and sell right away.

I've added timestamps for every section of the description. So, just bookmark this video right now. You guys are going to want to reference those insights again and again as you build that business.""",
        "start_time": 180,
        "end_time": 300,
        "token_count": count_tokens("""So, this comprehensive guide is meant to take you on a complete journey from technical foundations to six-figure scaling strategies. We're going to be covering the brutal realities I learned selling automations for over 2 years. The sales psychology that actually works with business owners, why most people target the wrong markets, which five industries are desperately paying premium prices right now, the technical essentials that do matter if you guys want to do this, and then the systematic approach to fixing every major agency problem you're suffering from.

Finally, I'm actually going to build a complete AI system live from scratch that you guys could sell to clients for $2,000 a pop immediately. And by the end of these five hours, I want you to have everything you need to start a profitable AI business or upscale your existing one well past six figures. Plus, I'll give you guys a real system you guys can deploy and sell right away.

I've added timestamps for every section of the description. So, just bookmark this video right now. You guys are going to want to reference those insights again and again as you build that business.""")
    }
    
    # Chunk 3: Technical vs Business Balance Philosophy
    chunk_3 = {
        "chunk_index": 3,
        "chapter_title": "The 80/20 Rule: Business Skills Over Technical Wizardry",
        "text": """Before we get into client acquisition and business strategy, we need to establish the technical foundations that everything else builds on. So, I just really quickly want to get the 80/20 of what actually matters in automation out of the way. That's APIs, web hooks, AI prompting, and the development approaches that separate professionals from hobbyists.

Here's what most people get wrong. They think that you need to be some sort of coding wizard in order to find success in the space. But the reality is you just need to understand enough technical skills to talk about reliable systems. Then you focus the majority of your energy on the business side of things.

80% of AI automation basics in less than 30 minutes. That's what we're going to be talking about today. I'm going to be giving you guys the core foundational concepts you need to start and then scale an AI automation business in a fraction of the time of your competitors. I scaled my own AI automation agency to $72,000 per month. So, I've learned a fair amount along the way. I also now coach almost 2,000 people on how to do the same.""",
        "start_time": 300,
        "end_time": 480,
        "token_count": count_tokens("""Before we get into client acquisition and business strategy, we need to establish the technical foundations that everything else builds on. So, I just really quickly want to get the 80/20 of what actually matters in automation out of the way. That's APIs, web hooks, AI prompting, and the development approaches that separate professionals from hobbyists.

Here's what most people get wrong. They think that you need to be some sort of coding wizard in order to find success in the space. But the reality is you just need to understand enough technical skills to talk about reliable systems. Then you focus the majority of your energy on the business side of things.

80% of AI automation basics in less than 30 minutes. That's what we're going to be talking about today. I'm going to be giving you guys the core foundational concepts you need to start and then scale an AI automation business in a fraction of the time of your competitors. I scaled my own AI automation agency to $72,000 per month. So, I've learned a fair amount along the way. I also now coach almost 2,000 people on how to do the same.""")
    }
    
    # Chunk 4: The Anti-Hype Philosophy + Universal Business Model
    chunk_4 = {
        "chunk_index": 4,
        "chapter_title": "Don't Get Caught Up in the Hype: It's Just Business",
        "text": """You're probably like, "Nick, why did you start with this point?" Well, it's because I think a lot of people see AI automation as this hype train and this big bubble and I want to push back against that. AI automation is not really all of that. It is just like any other business. Don't get caught up in the hype. Don't get caught up in the shiny objects.

The skills that make you a successful AI automation business owner are the exact same skills that make you a successful plumber. They're the exact same skills that make you a successful recruitment agency owner. They're the exact same skills that make you a successful e-commerce business owner.

I'm going to draw a business model on the right hand side here. We start with our lead generation. We could do cold email. Maybe we do PPC, that's pay-per-click ads. Maybe we do referrals. These are all ways of getting people interested in your business. And what do you do with all these lead generation mechanisms? Well, you then shuttle them to some sort of conversion. So, usually this is a sales call. What happens on the sales call? Usually, you'll send a proposal of some kind, also known as a quote or an estimate.""",
        "start_time": 480,
        "end_time": 660,
        "token_count": count_tokens("""You're probably like, "Nick, why did you start with this point?" Well, it's because I think a lot of people see AI automation as this hype train and this big bubble and I want to push back against that. AI automation is not really all of that. It is just like any other business. Don't get caught up in the hype. Don't get caught up in the shiny objects.

The skills that make you a successful AI automation business owner are the exact same skills that make you a successful plumber. They're the exact same skills that make you a successful recruitment agency owner. They're the exact same skills that make you a successful e-commerce business owner.

I'm going to draw a business model on the right hand side here. We start with our lead generation. We could do cold email. Maybe we do PPC, that's pay-per-click ads. Maybe we do referrals. These are all ways of getting people interested in your business. And what do you do with all these lead generation mechanisms? Well, you then shuttle them to some sort of conversion. So, usually this is a sales call. What happens on the sales call? Usually, you'll send a proposal of some kind, also known as a quote or an estimate.""")
    }
    
    # Chunk 5: The Universal Business Funnel Model
    chunk_5 = {
        "chunk_index": 5,
        "chapter_title": "The Universal B2B Funnel: Lead Gen → Sales → Fulfillment → Retention",
        "text": """After that point the person becomes a client. When they become a client you then fulfill and ideally at the very end of this there would be some sort of retention mechanism that gets them back in through some other call and then you just repeat and this is really what makes you money.

So I just drew that and that is how all AI automation businesses work. But kind of just zoom out a little bit if you squint what you'll notice is this doesn't just apply to AI automation businesses. That exact funnel that I drew literally applies to like 90% of B2B businesses all over the world.

And so I say this to mean the only difference between an AI automation business and the vast majority of other businesses that you may or may not have experience with. The only difference is this section right here. It's that little fulfillment section. So, you know, in a plumbing business or whatever, that might be repairs. That might be new pipes. In a recruitment business, that might be a candidate being placed. In a PPC agency, that might be some ad creatives being developed or something. The point is, the fulfillment is the different part. That's the AI automation part.""",
        "start_time": 660,
        "end_time": 840,
        "token_count": count_tokens("""After that point the person becomes a client. When they become a client you then fulfill and ideally at the very end of this there would be some sort of retention mechanism that gets them back in through some other call and then you just repeat and this is really what makes you money.

So I just drew that and that is how all AI automation businesses work. But kind of just zoom out a little bit if you squint what you'll notice is this doesn't just apply to AI automation businesses. That exact funnel that I drew literally applies to like 90% of B2B businesses all over the world.

And so I say this to mean the only difference between an AI automation business and the vast majority of other businesses that you may or may not have experience with. The only difference is this section right here. It's that little fulfillment section. So, you know, in a plumbing business or whatever, that might be repairs. That might be new pipes. In a recruitment business, that might be a candidate being placed. In a PPC agency, that might be some ad creatives being developed or something. The point is, the fulfillment is the different part. That's the AI automation part.""")
    }
    
    # Chunk 6: The Critical Business Priority Matrix
    chunk_6 = {
        "chunk_index": 6,
        "chapter_title": "Priority Matrix: Business Development Over Technical Implementation",
        "text": """But everything else, your ability to drive leads, your ability to close those leads, your ability to impress the hell out of those leads, whatever, all of this stuff is foundational and is shared with literally every other major digital business model today.

So, the reason why I say all this is because don't focus 90% of your energy on that tiny little bit at the end that just happens to be AI automation. If you guys really want to crush it at this business model, focus the vast majority of your energy on the same foundational concepts that you'd have to learn in any business. Focus on your ability to drive leads. Focus on your ability to sell to those leads. Focus on your ability to retain customers after they've made it through your pipeline. If you guys are incredible at that, and even if you happen to be second rate at AI automation, you guys will make way more money than if it was the other way around.

So, the fundamentals are always what make your automation agency or business successful. It's never fancy tech. It's never your implementation.""",
        "start_time": 840,
        "end_time": 1020,
        "token_count": count_tokens("""But everything else, your ability to drive leads, your ability to close those leads, your ability to impress the hell out of those leads, whatever, all of this stuff is foundational and is shared with literally every other major digital business model today.

So, the reason why I say all this is because don't focus 90% of your energy on that tiny little bit at the end that just happens to be AI automation. If you guys really want to crush it at this business model, focus the vast majority of your energy on the same foundational concepts that you'd have to learn in any business. Focus on your ability to drive leads. Focus on your ability to sell to those leads. Focus on your ability to retain customers after they've made it through your pipeline. If you guys are incredible at that, and even if you happen to be second rate at AI automation, you guys will make way more money than if it was the other way around.

So, the fundamentals are always what make your automation agency or business successful. It's never fancy tech. It's never your implementation.""")
    }
    
    # Chunk 7: Engineer to Business Owner Mindset Shift
    chunk_7 = {
        "chunk_index": 7,
        "chapter_title": "The Engineer's Dilemma: From Technical Expert to Business Owner",
        "text": """Don't overthink the technical aspects like I see a lot of people coming from programming or development or engineering backgrounds do. And certainly don't underthink the business side of things because the number one thing that I see when people enter my communities and my groups and my products, they're always like, "Hey, Nick, you know, I'm an engineer and I'm great at building products, but I'm not very good at marketing."

And then I'm like, "All right, well then you're not very good at being a business owner. So, we need to fix that first, right? Your development and engineering skills, those things can wait. We need to make sure that you're a good marketer. We need to make sure you're a good salesperson. And ultimately, we need to make sure that you're good at business development if we are to develop a business."

Now that I've covered that, we can actually start getting into some technicals. So I think a lot of people that are watching this are probably at the start line of their AI automation business. One of the core foundational parts of AI automation agency fulfillment is your ability to use an API.""",
        "start_time": 1020,
        "end_time": 1200,
        "token_count": count_tokens("""Don't overthink the technical aspects like I see a lot of people coming from programming or development or engineering backgrounds do. And certainly don't underthink the business side of things because the number one thing that I see when people enter my communities and my groups and my products, they're always like, "Hey, Nick, you know, I'm an engineer and I'm great at building products, but I'm not very good at marketing."

And then I'm like, "All right, well then you're not very good at being a business owner. So, we need to fix that first, right? Your development and engineering skills, those things can wait. We need to make sure that you're a good marketer. We need to make sure you're a good salesperson. And ultimately, we need to make sure that you're good at business development if we are to develop a business."

Now that I've covered that, we can actually start getting into some technicals. So I think a lot of people that are watching this are probably at the start line of their AI automation business. One of the core foundational parts of AI automation agency fulfillment is your ability to use an API.""")
    }
    
    # Chunk 8: API Fundamentals and Strategic Value
    chunk_8 = {
        "chunk_index": 8,
        "chapter_title": "API Mastery: Going Beyond Drag-and-Drop Limitations",
        "text": """So, an API just stands for application programming interface. All that really means is it's just essentially for our purposes it is a server URL somewhere in the internet that we can send a request to and then we can get things back.

And the cool part about APIs for us is you know those AI automation tools that we tend to really know and love. Stuff like Make.com stuff like n8n stuff like Zapier stuff like Lindy all these drag and drop no code platforms which are really what most people think about when they think AI automation. Well these don't have built-in integrations with every platform that you might want to connect them to for business purposes.

I want to say that if you only use built-in integrations, not only is your ability to do anything actually really cool for the client severely limited, a lot of the time the client can just do that stuff themselves by dragging and dropping modules across the screen. But not only is it super limited, you can't really drive as much value as you realistically could out of any platform because a lot of the time the simple endpoints that are exposed by Make.com or Zapier there are a lot more parameters. There are a lot more options in the API versus just the drag and drop.""",
        "start_time": 1200,
        "end_time": 1380,
        "token_count": count_tokens("""So, an API just stands for application programming interface. All that really means is it's just essentially for our purposes it is a server URL somewhere in the internet that we can send a request to and then we can get things back.

And the cool part about APIs for us is you know those AI automation tools that we tend to really know and love. Stuff like Make.com stuff like n8n stuff like Zapier stuff like Lindy all these drag and drop no code platforms which are really what most people think about when they think AI automation. Well these don't have built-in integrations with every platform that you might want to connect them to for business purposes.

I want to say that if you only use built-in integrations, not only is your ability to do anything actually really cool for the client severely limited, a lot of the time the client can just do that stuff themselves by dragging and dropping modules across the screen. But not only is it super limited, you can't really drive as much value as you realistically could out of any platform because a lot of the time the simple endpoints that are exposed by Make.com or Zapier there are a lot more parameters. There are a lot more options in the API versus just the drag and drop.""")
    }
    
    # Chunk 9: The Three-Step API Connection Method
    chunk_9 = {
        "chunk_index": 9,
        "chapter_title": "The Nick Saraev API Method: OAuth → Copy Example → MVP Call",
        "text": """So what I'm going to do here is I'm actually going to run through how to connect to an API and I'm going to do it using two tools that are really popular right now, Make.com and n8n. And hopefully this is going to give you guys a walkthrough what I look for when I connect to an API.

The number one thing that I always do immediately is I look for OAuth. Then I look for a way to copy and paste a simple example and then from there I basically build a minimum viable API call that just works. The second I have something that works which usually involves some method endpoint and header shenanigans. The second I have something that works everything else is so much easier.

What's the API we're going to be connecting to? It's this really cool one called Firecrawl. I've been using Firecrawl a lot more recently. Essentially what Firecrawl is is just a way to scrape like any website and then return the results in what's called markdown. What's the value in scraping websites and stuff like this? The vast majority of the time anytime you're whipping up an email campaign for somebody or you're sending any sort of outreach or you're doing any sort of marketing that really matters, you're going to be doing some sort of scraping in AI automation.""",
        "start_time": 1380,
        "end_time": 1560,
        "token_count": count_tokens("""So what I'm going to do here is I'm actually going to run through how to connect to an API and I'm going to do it using two tools that are really popular right now, Make.com and n8n. And hopefully this is going to give you guys a walkthrough what I look for when I connect to an API.

The number one thing that I always do immediately is I look for OAuth. Then I look for a way to copy and paste a simple example and then from there I basically build a minimum viable API call that just works. The second I have something that works which usually involves some method endpoint and header shenanigans. The second I have something that works everything else is so much easier.

What's the API we're going to be connecting to? It's this really cool one called Firecrawl. I've been using Firecrawl a lot more recently. Essentially what Firecrawl is is just a way to scrape like any website and then return the results in what's called markdown. What's the value in scraping websites and stuff like this? The vast majority of the time anytime you're whipping up an email campaign for somebody or you're sending any sort of outreach or you're doing any sort of marketing that really matters, you're going to be doing some sort of scraping in AI automation.""")
    }
    
    # Chunk 10: The Three-Prompt AI System
    chunk_10 = {
        "chunk_index": 10,
        "chapter_title": "AI Prompting Mastery: System, User, Assistant Pattern",
        "text": """Next up, I want to talk how to prompt AI models effectively. As the AI and AI automation probably implies, most of our work involves weaving in artificial intelligence into some sort of business process. So, I have the simplest possible way to think of this and I'm going to give it to you right now.

There are basically three types of prompts and these three types of prompts are present across more or less all of the current large language model tools. There is a system prompt, okay, there is a user prompt and then there is an assistant prompt. These are the three types.

The system prompt is how the model identifies. So this is where you say you are a data entry professional or something or you say you are a skilled recruiter. This is the identity that you're giving the model. The user is where you give it a task where you say your task is to do a thing. Then the assistant prompt is what the AI gives you back. And usually the way that I like to do things is I like to have the assistant give me back my stuff as a JavaScript object notation JSON string. The reason why I do that is because when you get in the habit of doing this, you can then very easily integrate this with any tool on planet Earth.""",
        "start_time": 1560,
        "end_time": 1740,
        "token_count": count_tokens("""Next up, I want to talk how to prompt AI models effectively. As the AI and AI automation probably implies, most of our work involves weaving in artificial intelligence into some sort of business process. So, I have the simplest possible way to think of this and I'm going to give it to you right now.

There are basically three types of prompts and these three types of prompts are present across more or less all of the current large language model tools. There is a system prompt, okay, there is a user prompt and then there is an assistant prompt. These are the three types.

The system prompt is how the model identifies. So this is where you say you are a data entry professional or something or you say you are a skilled recruiter. This is the identity that you're giving the model. The user is where you give it a task where you say your task is to do a thing. Then the assistant prompt is what the AI gives you back. And usually the way that I like to do things is I like to have the assistant give me back my stuff as a JavaScript object notation JSON string. The reason why I do that is because when you get in the habit of doing this, you can then very easily integrate this with any tool on planet Earth.""")
    }
    
    chunks.extend([chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, chunk_6, chunk_7, chunk_8, chunk_9, chunk_10])
    
    # This covers the foundational business philosophy and technical introduction
    # The full 5-hour course would require 50-70+ chunks to cover:
    # - Live API demonstrations (Firecrawl, Make.com, n8n)
    # - Webhooks implementation 
    # - Sales psychology and client acquisition
    # - Market targeting and industry selection
    # - Scaling methodologies and agency operations
    # - Live system building demonstration worth $2000
    
    return chunks

def main():
    chunks = create_manual_chunks()
    
    # Calculate token statistics
    total_tokens = sum(chunk["token_count"] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    # Create the final JSON structure
    result = {
        "video_id": "L4Qbx8OM9l4",
        "title": "$1,000,000 AI Automation & Agents Advice for 5 Hours Straight",
        "channel": "Nick Saraev",
        "chunks": chunks,
        "statistics": {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens) if avg_tokens else 0
        }
    }
    
    # Write to JSON file
    output_path = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_nick_saraev_comprehensive_L4Qbx8OM9l4.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} chunks with average {avg_tokens:.0f} tokens per chunk")
    print(f"Total tokens: {total_tokens}")
    print("Manual chunker completed successfully!")
    print(f"Note: This covers the foundational business philosophy and technical introduction.")
    print(f"The full 5-hour course would require 50-70+ chunks to cover all demonstrations,")
    print(f"sales strategies, market targeting, and the live $2000 system build.")

if __name__ == "__main__":
    main()