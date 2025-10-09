#!/usr/bin/env python3
"""Manual chunking for IndyDevDan's AutoGen Multi-Agent Postgres video."""

import json
from pathlib import Path
import tiktoken

def count_tokens(text: str) -> int:
    """Count tokens in text."""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def create_manual_chunks():
    """Create manual chunks for the AutoGen multi-agent video."""
    
    chunks = []
    
    # Chunk 0: Introduction - Single Prompt Limitations
    chunks.append({
        "chunk_index": 0,
        "start_time": 0,
        "end_time": 60,
        "chapter_title": "The Single Prompt Wall and AutoGen Introduction",
        "text": "As we learned to utilize LLMs and AI tools to help us code faster, interact with our data more efficiently, and solve our engineering problems, we quickly run into one major issue: there's only so much you can do with a single prompt. There comes a point in time when no matter how great your prompt engineering is, you hit a wall. You can only solve problems of a certain size. Thankfully for us, the code bros at Microsoft have been cooking up AutoGen. In this video, we're going to walk through exactly how you can utilize AutoGen by making our Postgres data analytics AI agent multi-agent. This is the second video in our Postgres AI agent series. Feel free to backtrack."
    })
    
    # Chunk 1: What is AutoGen?
    chunks.append({
        "chunk_index": 1,
        "start_time": 60,
        "end_time": 120,
        "chapter_title": "AutoGen Definition: Prompts Working Together",
        "text": "And so first things first, what exactly is AutoGen? Remove the fluff and the pseudo marketing and AutoGen is simply this: a simple framework for building multi-agent applications that can help you solve your problem better than a single prompt can. Let's compress this idea even further. AutoGen enables you to build prompts that work together to solve a problem. Okay, so that sounds cool but what does that actually look like in practice? I think this image explains it really really well. So I'm just going to take a quick screenshot here so we can zoom in on this super simple example here."
    })
    
    # Chunk 2: Three Agent Example
    chunks.append({
        "chunk_index": 2,
        "start_time": 120,
        "end_time": 180,
        "chapter_title": "Three Agent Example: Commander, Writer, Safeguard",
        "text": "Right, we have three agents. We have a commander, a writer and a safeguard. Your request comes in. You want to generate some Python code. It comes into the commander and the commander says okay here's the code we want to generate. It sends the request to the writer and the writer is solely responsible for generating the code. After it generates the code, it sends it back to the commander. The commander then takes that code and sends it to the safeguard. The safeguard double checks the code. It looks for problems, it looks for bugs, and then it sends it back to the commander. If there are issues, it'll go right back to the writer for the writer to improve. Otherwise the commander will return the response back to you."
    })
    
    # Chunk 3: Multi-Agent Configurations
    chunks.append({
        "chunk_index": 3,
        "start_time": 180,
        "end_time": 240,
        "chapter_title": "Multi-Agent Configurations and Core Promise",
        "text": "As you can see here, there are many configurations of setting up structures of multi-agents to help you solve your problems, right? So they give the example of math problem solving, multi-agent coding, online decision-making, dynamic group chat, retrieval agent, etc. You can imagine a whole different set of configurations that are best suited to solve a certain problem. The core of this is that the combination of agents, AKA individual prompts with different functionality, vastly outperforms a single prompt with limited functionality. So that's the promise of AutoGen and other multi-agent frameworks."
    })
    
    # Chunk 4: Current Single Agent Demo
    chunks.append({
        "chunk_index": 4,
        "start_time": 240,
        "end_time": 360,
        "chapter_title": "Current Postgres Agent: Single Prompt Limitations",
        "text": "So enough talk. Let's upgrade our current version of our Postgres data analytics agent to be multi-agent. Let's close this, open up the terminal, open our app and let's just walk through at a high level what we've done so far. We have two environment variables here set up: our Postgres database URL and our OpenAI API key. If we open up TablePlus, you can see that we have two tables: a users table and a jobs table. With our current table and the current version of our application, we can do the following: poetry run start --prompt. And now we can in natural language query our database. So what I'll say is \"give me all Gmail users\" and as you can see here we have an array of all of our users that are Gmail users. So you can see here we have gmail.com and if we hop over to our table we can see that we have those exact three emails: Charlie, Bob, Alice. Bob, Alice, Charlie - there they are. So fantastic, right?"
    })
    
    # Chunk 5: How Single Agent Works
    chunks.append({
        "chunk_index": 5,
        "start_time": 360,
        "end_time": 420,
        "chapter_title": "Single Agent Architecture Overview",
        "text": "And how exactly did we do this? We set up a Postgres database module and an LLM module and that allowed us to get the definitions for our tables that allows us to run prompts against OpenAI GPT-4. We then use a delimiter and some prompt engineering to parse our SQL query, then we run that SQL query and then we dump the result. Again, if you want to see how this was built, check out the first video. In this video, we're going to push our agent further by making it multi-agent."
    })
    
    # Chunk 6: Installing AutoGen and Setup
    chunks.append({
        "chunk_index": 6,
        "start_time": 420,
        "end_time": 540,
        "chapter_title": "Installing AutoGen and Planning Agent Structure",
        "text": "First things first, let's install python-autogen. I'm using poetry so I'm going to run poetry add pyautogen. I'm going to go ahead and drop a bunch of imports at the top here. And now what I'm going to do is come into our code here and I'm going to get rid of some of our functionality. So since we're building out multi-agents, we want to have this functionality of parsing out the SQL completely handled by our agents. So I'm going to go ahead and get rid of this. I'm going to go ahead and get rid of our LLM prompt and basically everything else after our prompt is getting built with the tables. So what we're going to be left with here is just our database connection, our original prompt, adding our Postgres table definitions onto a prompt. And so from here what I'm going to do is write a couple comments and then we're going to open up once again our favorite AI coding assistant, Aider, and we're going to have Aider run through the code and generate a first pass at this for us. Build the GPT configuration object, build a function map, create our terminate message function, create a set of agents, then we're going to create a group chat and initiate the chat."
    })
    
    # Chunk 7: Agent Roles Definition
    chunks.append({
        "chunk_index": 7,
        "start_time": 540,
        "end_time": 660,
        "chapter_title": "Defining Agent Roles: Engineer, Analyst, Product Manager",
        "text": "So now let's walk through how exactly we want our agents to interact together. So admin user proxy agent, data engineer agent - this agent generates the SQL query. Senior data analyst - this will run the SQL, generate the response. Then I want to have a product manager validate the response. Then at the top here I'm just going to say our admin user proxy agent takes in prompt and manages group chat. Cool, so this is how our application is going to run. I want to get an example and I found a good one here. If you hop back to the AutoGen site and you go to docs examples, I really liked this complex task solving by group chat. This gave me a really great example of something that we would want to use here for our Postgres AI agent. And this is a really great example, right? So we have the GPT config and then we have several different agents that then get wrapped up into a group chat and a manager."
    })
    
    # Chunk 8: Using Aider for Initial Code
    chunks.append({
        "chunk_index": 8,
        "start_time": 660,
        "end_time": 780,
        "chapter_title": "Using Aider to Generate Multi-Agent Framework",
        "text": "So what I'm going to do here is use a kind of combination of prompting techniques and use our favorite AI coding tool Aider to help us generate a first pass without writing a single line of code here. So I'm just going to copy this and inside of our application here I'm just going to drop in example.txt and dump in this. I'll actually make this a Python file. As many of you know, Aider is a pair programming tool. We can go ahead and pop open their landing page. It's pretty incredible. It is basically your AI pair programming assistant directly in your terminal. Let's just go ahead and run an example with it. So I want to use Aider to read these comments, read the example we have here, and then replace our comments with a full built out example given the agents that I've specified here. So I'm going to export my OpenAI key. I'm going to commit existing code. Then I'm going to run Aider. Awesome. I'm going to go ahead and add the main file and the example so that Aider has it in its active memory. And then I'm going to go ahead and build a concise request, AKA prompt, to build out a first pass at our multi-agent Postgres AI agents. \"Use example.py and main.py starting at line build agents and mock out their prompts.\""
    })
    
    # Chunk 9: Aider Results and Function Map
    chunks.append({
        "chunk_index": 9,
        "start_time": 780,
        "end_time": 900,
        "chapter_title": "Building Function Map and Terminate Message",
        "text": "Okay, so it applies some updates. Let's go ahead and check them out. Okay, so this is pretty good. It got us a decent chunk of the way there. If we start from the top here, you can see it generated a GPT-4 config for us. This looks great. And then it left a couple TODOs here. It doesn't really know how to handle this, so I'm really glad that it just skipped over it. There's no function mapping here and this is something that we're going to want our GPT-4 configuration to have, so we'll get to that. And it doesn't exactly have any context for this terminate function message, so totally fine. I'm actually really glad that it left a blank instead of just guessing and hallucinating and making something up, right? But what it could do, it did. In this case maybe we got 40-50% of the way there. That's totally fine. Let's go ahead and knock out some of this work on our own. So import autogen. Let's go ahead and create our function map. So the function map allows our agents to be aware of outside code that it can run. I'm just going to go ahead and say function_map equals run_sql and then I'm going to pass it our database run_sql_query function. I'm going to modify our GPT config to also have a mapping to the functions. So functions SQL. Cool, so this completes our GPT-4 function map here. I'm going to go ahead and remove the seed. I'm going to add a new flag called use_cache. I'm going to set this to false so that we don't get repeat situations of our agent runs. I just want a brand new agent session every single time. I found that AutoGen almost only runs on GPT-4, so we're just going to use GPT-4 there and that's our configuration object."
    })
    
    # Chunk 10: Agent Configuration Details
    chunks.append({
        "chunk_index": 10,
        "start_time": 900,
        "end_time": 1020,
        "chapter_title": "Configuring Agents with Specific Roles and Capabilities",
        "text": "Now let's go ahead and create a terminate message. So what exactly is a terminate message? The terminate message functionality tells our multi-agent framework when it's time to stop generating and to end the termination. Cool. So basically all we're doing here is in whatever response we get from one of our LLMs, if it has the text \"approved\" inside of it, we're going to return true and that marks the end of our session with our multi-agent framework. So now let's go ahead and separate out the individual prompts. Each one of our agents is going to have... data engineer and this will be the data... All right, so we've done a couple things here. Let's go ahead and collapse the code so this is easier to read. We have all of our agents set up and ready to go. We have our primary user proxy agent - this is essentially us communicating with our LLMs. Then we have the data engineer, we have the senior analyst, and we have the product manager. Each has their own specific role. Our data engineer is going to generate SQL, our senior analyst is going to run the SQL and generate the response, and our product manager is going to validate the response to make sure it's correct and meets the requirements."
    })
    
    # Chunk 11: Agent Superpowers and Function Map
    chunks.append({
        "chunk_index": 11,
        "start_time": 1020,
        "end_time": 1140,
        "chapter_title": "Giving Agents Superpowers with Function Mapping",
        "text": "We then put them all together using a group chat. I'm going to drop the rounds down to 10. You can see here that we have the prompts for each agent and at the end they all have this completion prompt which aids our termination message. You can see here it says \"if everything looks good respond with approved\" and in our termination message we're checking to see if our content says \"approved\". So now I'm going to take our is_termination_message and function_map and do a little bit more configuration on our agents to make them work like we want them to work to be a cohesive data analyst team. I'm going to set our human_input_mode to \"never\". This is basically when it's going to ask us for more input. I don't want it to ask for any additional input throughout our run. I want it to run all on its own so that we can start building up to that true agentic software agent system. So now I'm going to make one tweak. I'm going to give our senior analyst the ability to run SQL. So I'm going to call function_map and set it equal to our function_map up here. And what this does is it gives this agent superpowers. It allows it to run arbitrary code. So now our senior analyst can execute the SQL created by the data engineer."
    })
    
    # Chunk 12: Running the Multi-Agent System
    chunks.append({
        "chunk_index": 12,
        "start_time": 1140,
        "end_time": 1260,
        "chapter_title": "Running Multi-Agent System and Debugging",
        "text": "Now that we have everything set up and good to go, we're going to reference our user proxy agent and we're going to initiate the chat. We're then going to pass in our manager which has the reference to our group chat and all of our other agents. We're going to run clear_history true. I don't want any history to be stored or saved between runs. And then finally we're going to pass in our prompt as the message parameter. And that should be everything we need to run our Postgres data analytics multi-agent application. Run the exact same command as we had before and poetry start. We're going to pass in the prompt and our prompt is going to be \"all Gmail\". All right, so we have an error here. I had to update the config list to be wrapped in this config_list_from_models function. No problem there. And now I'm getting one more error here. Basically the name I've specified for one of the agents doesn't match the regex format. So I'm going to go ahead and update that. I can't use spaces, so no problem at all. I'm just going to use underscores here. Let me just check the other agents, make sure there's no naming issues. Looks like it was running there. Let's go ahead here. Incredible!"
    })
    
    # Chunk 13: Agent Workflow Analysis
    chunks.append({
        "chunk_index": 13,
        "start_time": 1260,
        "end_time": 1320,
        "chapter_title": "Analyzing Multi-Agent Workflow Execution",
        "text": "So let's see exactly what happened during that run. So as you can see here, the first thing we get is the input for our command. Let me go ahead and just copy this all out so we can move this to a clean text file. Cool. So as you can see here, top to bottom, we ran our command and we see that the admin to the chat interface, so to the entire group, broadcast this message, right? So it passed in our prompt and as you can see here the exact details of the prompt from the CLI argument we passed in fill this database query. And then we use a capitalize reference to attach some memory to the top of our prompt. And just like in our first version of the agent, we want to put the table definitions right at the top there. So that's what we did so that our LLM has access to all the tables. In future videos we'll clean this up to support you know 10,000 plus tables because in reality you know we're going to have a ton more tables than just two. But for now this is totally fine. It'll fit in the GPT-4 memory."
    })
    
    # Chunk 14: Agent Specialization in Action
    chunks.append({
        "chunk_index": 14,
        "start_time": 1320,
        "end_time": 1380,
        "chapter_title": "Agent Specialization: Divide and Conquer",
        "text": "But you can see right after that the engineer does its job and it generates SQL. You can see that it passes it right afterward to the senior data analyst. It's going to go ahead and actually run our run_sql function that we passed in here, our function map, right? So we have that function map that we passed into just our senior data analyst, right? So this is really cool. You can really divide and conquer and give your agent specific functionality, right? Our analyst is the only one that can actually execute SQL. So after that you can see that it ran that SQL, it generated proper response thanks to our function, and then it passed it to the entire group chat and got marked as approved. Now this isn't perfect. I want it to be passed to the product manager but this also does the job and it also is actually good enough, right? If you don't need all the agents, if you don't need you know four, five agents, don't use them."
    })
    
    # Chunk 15: Prompt Orchestration Evolution
    chunks.append({
        "chunk_index": 15,
        "start_time": 1380,
        "end_time": 1440,
        "chapter_title": "From Prompt Engineering to Agent Orchestration",
        "text": "The kind of cool part about this is that you save a decent amount of code. After the upfront cost, then it's just about figuring out how you want to coordinate your agents. It's that big idea of prompt engineering moving to prompt orchestration and agent orchestration, right? It's kind of like the evolution here. You go from prompt engineering to now orchestrating several different agents with different abilities and that's what makes a really complex unit: a system of agents that can work on your behalf essentially while you sleep. So let's go ahead run one more example and I want to get all users with completed jobs. Now we have to do a join on jobs to get all users with completed jobs. So this is really cool and as you get comfortable with this, you can basically know that it's going to run very reliably, right? So I got this result back, getting more confident in the system."
    })
    
    # Chunk 16: Multi-Agent Framework Benefits
    chunks.append({
        "chunk_index": 16,
        "start_time": 1440,
        "end_time": 1500,
        "chapter_title": "Multi-Agent Framework Benefits and Real World Modeling",
        "text": "Let's talk about the pros and cons of a system like this, right? Is AutoGen the right move to make? Is it the right direction? Why is a multi-agent framework important? So this is important because it allows us to create a more accurate model of the world. If you think about the systems that you work in on a daily basis, you know, maybe your engineering job or your data analytics job, you're an engineer there, you work with a bunch of people, you work with a team, you work with marketers, you work with your own manager, you have co-workers and you work together essentially as a multi-agent framework that creates a product and produces output, right? There's almost no difference between the agents we're building now and the systems that we all operate in on a daily basis. The only question is what's the complexity and you know how many abstractions have we built in our system. Where multi-agent work is important: it allows us to create a more accurate model of the world that we live in. So another huge plus of why this is important: it enables us to become orchestrators, right? Which means less engineering and more product level work, right?"
    })
    
    # Chunk 17: Future Vision and Agentic Revolution
    chunks.append({
        "chunk_index": 17,
        "start_time": 1500,
        "end_time": 1560,
        "chapter_title": "The Agentic Revolution and Future Direction",
        "text": "So after we built this agent out, after we put the upfront cost in, we now have a Postgres data analytics agent at the ready, right? We can query, we can input anything into our prompt, right? It's the system is entirely dynamic because it has agents doing specific jobs in a flexible way as if a person was doing it, right? And I know, I know it's not perfect. There's hallucinations, there are things that are going to go wrong. It's not about where we are, it's about where this is going. It's about what's coming next, right? Always keep that in mind when dealing with this AI technology. It's about the general direction of where this is going and you want to be on top of this. You want to be utilizing agentic frameworks in your day-to-day engineering so that you can be on top of this and you can get a lot of the value that's going to be generated from this agentic revolution."
    })
    
    # Chunk 18: Pros, Cons, and Unix Philosophy
    chunks.append({
        "chunk_index": 18,
        "start_time": 1560,
        "end_time": 1620,
        "chapter_title": "Agent Specialization and Unix Philosophy",
        "text": "All right, so let's talk about some of the pros of using a framework like this, right? So we can assign functions and prompts to specific agents, right? Enabling specialization which yields better results. As we saw with our Postgres example here, we have a product manager that reviews work, we have the analyst that executes the SQL, and we have the data engineer that generates the SQL, right? We can definitely give more responsibility to one agent but why do it when it's better to have a specific prompt, one per agent? I think that's the right way to slice agentic frameworks in general. One agent gets one function and they do one thing, right? It's just like clean Unix philosophy. When you're building out your code, when you're building out your functions and your modules, make it do one thing. Make it do one thing but make it do it extraordinarily well."
    })
    
    # Chunk 19: Technical Challenges and Next Steps
    chunks.append({
        "chunk_index": 19,
        "start_time": 1620,
        "end_time": 1457,
        "chapter_title": "Technical Challenges and Future Improvements",
        "text": "So let's talk about a couple of cons. From a technical perspective, it's kind of an art on trying to figure out how many agents you need, what should they do, and how do you know that they're working? This is a pretty new territory. Some of the larger FAANG companies, everyone's trying to kind of figure this out. It's kind of a race to agentic frameworks, agentic functionality, because once you get it running, just like you saw here, right? Once we got our example running, we now essentially have infinite access to this small domain. Next thing, this can get pretty expensive and this scales linearly with the number of agents that you have, right? Because they're having a big conversation, they're creating real results, they're consuming resources. This can get expensive. I wouldn't worry about this too much but it is something to take into account. Lastly, these are just LLMs talking together in a pretty loose fashion so it can be pretty difficult to debug why things are going wrong. Is a multi-agent framework better than rolling your own? Yes. Is AutoGen the end all be all? Probably not. It has a potential to be but it's more likely to be a stepping stone for more accurate multi-agent frameworks. This doesn't mean I'm not going to use it. I'm going to continue using this. I think it's got a pretty great taste to it, a lot of great functionality. We now can just build out arbitrary agents and give our agents some specific functionality, which I think is really incredible. In the next video we're going to push our Postgres AI agent further by adding file writing, report generation, and we'll add some more tables to test some more advanced complex scenarios and requests. Since in reality, databases have 10, 50, hundreds of tables, we're going to make sure that our multi-agent Postgres data analytics agent can handle the reality of real data engineering. That's where we're headed. You know, be sure to like, be sure to sub, be sure to hit the notification bell so you keep your eye on how you can utilize this AI, these agents, this agentic framework AutoGen and whatever's coming next. I'm going to be here covering it for you guys, building out real valuable software that you can use and you can build on your own as well. You know, the whole goal here is to build out our own agentic software that can create value for us while we sleep. So thanks so much for watching."
    })
    
    # Calculate token counts and prepare output
    total_tokens = 0
    for chunk in chunks:
        token_count = count_tokens(chunk["text"])
        chunk["token_count"] = token_count
        total_tokens += token_count
    
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    output = {
        "video_id": "JjVvYDPVrAQ",
        "title": "One Prompt is NOT enough: Using AutoGen to code a Multi-Agent Postgres AI Tool",
        "channel": "IndyDevDan",
        "duration": 1457,
        "total_chunks": len(chunks),
        "avg_tokens_per_chunk": round(avg_tokens),
        "chunks": chunks
    }
    
    # Save to file
    output_file = Path("/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/processed/manual_chunks/manual_chunks_autogen_JjVvYDPVrAQ.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {len(chunks)} manual chunks")
    print(f"📊 Average tokens per chunk: {round(avg_tokens)}")
    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    create_manual_chunks()