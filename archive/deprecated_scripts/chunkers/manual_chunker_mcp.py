"""
Manual LLM-based chunker for MCP Servers YouTube transcript.
Creates properly-sized, semantically coherent chunks.
"""

import json
import tiktoken
from datetime import datetime
from typing import List, Dict, Tuple

class ManualChunkerMCP:
    """Creates high-quality chunks for MCP Servers video using LLM understanding of content."""
    
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.tokenizer.encode(text))
    
    def chunk_transcript(self, video_id: str, title: str, duration: int, text: str) -> Dict:
        """Create manual chunks for the MCP Servers video transcript."""
        
        # Define semantic chunks based on content understanding
        chunks_data = [
            {
                "title": "Introduction to MCP Servers and the Three Primitives",
                "content": """As you know, MCP servers let you build tools for everything. MCP servers are one of the three most important innovations for evolving your engineering from AI coding to agentic coding. With new models like Claude 4 and the brand new Deepseek R1.1, we have more intelligence to build than ever before. But the models are no longer the limiting factor for your engineering output that forces us to ask what's limiting us as engineers from creating more value faster than ever. It's our abilities to create capabilities for our agentic coding tools like Claude Code. That brings us full circle back to MCP servers. 

In this video, we're going to understand the most underutilized capability of MCP servers. Most engineers stop at tools. But once you understand this one simple idea, you'll be able to craft rich MCP servers that dramatically increase your engineering velocity as well as your teams. Resources, tools, and prompts. And the tier list in reverse order of capability, we have resources, tools, and prompts. Most engineers skip resources. They go all in on tools and completely miss out on the highest leverage primitive of MCP servers, prompts. Tool calling is just the beginning of your MCP server.""",
                "start_ratio": 0.0,
                "end_ratio": 0.09
            },
            {
                "title": "Quick Data MCP Server Introduction and Basic Tool Usage",
                "content": """Let me show you how to maximize the value of. If we type /mcp, you can see I have six MCP servers available. We're going to be operating in the quick data MCP server. Quick data gives your agent arbitrary data analysis capabilities on JSON and CSV files. We all know how tools work, but let's run a few to understand the quick data MCP server and showcase how limited tool calls really are. If we type /model, we're going to run this Sonnet 4 fast workhorse model for this. 

So, right away we have a problem. I have no idea what I can do with this MCP server. I have to rely on some type of documentation. Let's open up Cursor and break open the readme. If we scroll down here, I have a complete documented set of all the tools, resources, and prompts available for this MCP server. Let's just start with a couple simple ones. I'll run this load dataset. And now we need to pass in a JSON or a CSV file. I'll go back to Cursor. If I search for e-commerce orders. You can see we have this simple JSON list. I'll copy the reference to this file with command shift R. Then I'll hop back to Claude Code. Paste this in and have it load.""",
                "start_ratio": 0.09,
                "end_ratio": 0.16
            },
            {
                "title": "Demonstrating Tool Capabilities with E-commerce Data",
                "content": """All right. So, as expected, we have this load dataset MCP server tool. It has the file path and the dataset name e-commerce orders. This looks great. We'll go ahead and accept this. And you can see our JSON response. If we hit control-R, you can see the entire thing. columns, rows, dataset name. Looks great. So, let's go ahead and get a dataset breakdown. So, I'll paste. This also accepts the dataset name. So, go ahead, copy and paste this back in. And now we're just going to get some basic information about this dataset. We'll of course accept this tool call. And you can see we have the shape and key information about this dataset. 

So, so far this looks great. Let's run a couple more tools and then we're going to uplevel everything we're doing by looking at the most powerful capability you can add to your MCP server. Let's run suggest analysis paste and then I'll just say ecom... This is going to be autocompleted for us based on the current context. There it is. Suggest analysis. Let's see what we get. So we have a couple of ideas given to us based on that tool call. Run command number one. Fire this off. We're now going to get a segment breakdown by this product category column.""",
                "start_ratio": 0.16,
                "end_ratio": 0.22
            },
            {
                "title": "Product Category Analysis and Arbitrary Code Execution",
                "content": """So check this out. We have product category segmentation. We can see that electronics are producing a lot of value inside of this e-commerce orders.json file. So looking at this data from a business strategy perspective, we could if we wanted to cut down on sports and home garden product categories and go all in on electronics based on this insight. Okay. So there's one more cool tool. I want to share with you here. If we scroll down to the bottom, we can execute arbitrary code. We can have Claude Code running on Claude for Sonnet execute arbitrary code for us. 

So again, we can just come back in here, paste, we can say ecom... and let's find out the if we look at the dataset here, we have this region column and we also have order value. So let's find out the top order value by region. Find top three region order value. Yep, let's go ahead and fire that off. There we go. So you can see here we have custom code getting written based on our prompt. We'll hit yes and there is our executed code response. You can see here our top three regions by order volume. We have East Coast, West Coast and of course Midwest and last place. Pretty accurate training dataset, right?""",
                "start_ratio": 0.22,
                "end_ratio": 0.28
            },
            {
                "title": "Creating Visualizations and Introducing MCP Prompts",
                "content": """If we want to reuse that same MCP tool call, we can hit up and then I'll say then create a pie chart label by region value and percent. It's going to create a pie chart for us. Let's go ahead and run this. And bam, check this out. You can see we have East Coast, we have West Coast, Midwest, and then the South. We have a great breakdown here. And this was all just quickly created and managed with our MCP server for quick data analytics against JSON and CSV. 

So tools are great. We all know about their capabilities. We can build out tools for anything and tools for everything. But tools only scratch the surface of what you can do with your MCP server. To unlock the full capabilities of what you can do, we need to build MCP prompts. So in order to showcase the capabilities here, we're going to reset this Claude Code instance and really start from scratch. So let's open up Claude again. We'll run the same setup. So you can see here /mcp/mod, same deal. Sonnet 4.""",
                "start_ratio": 0.28,
                "end_ratio": 0.34
            },
            {
                "title": "MCP Prompts Discovery and Auto-completion Features",
                "content": """So now instead of looking through the documentation, right, we had this readme that thankfully detailed all of our tools, resources, and prompts, right? There's the codebase structure. We'll take a look at that in a second. Instead of doing any of this, instead of, you know, relying on codebase architecture, codebase structure, we can just use MCP server prompts to guide the entire discovery and use of the quick data MCP server. Let me show you exactly what I mean. 

To find all the prompts associated with this MCP server inside of Claude Code, we can type /quick-data. So, this is the name of the MCP server. And here you can see a ton of autocomplete suggestions with prompts. So, these are prompts built out in the MCP server. Now, we're going to run something really cool, something very useful that I highly recommend you set up inside of all your MCP servers. We're going to list available MCP server capabilities, including prompts, tools, and resources. So, this is a prompt that's going to give us a clear breakdown of what we can do with this tool.""",
                "start_ratio": 0.34,
                "end_ratio": 0.40
            },
            {
                "title": "Context Priming and Find Data Sources Workflow",
                "content": """Okay, check this out. So, Claude Code, our agentic coding tool, has now consumed everything that we can do with this tool. It's now loaded fresh in the context window, and we have a quick start flow to get started. So now if we want to we can just ask Claude Code what exactly these heat components are. Okay. So. I'm just going to say tools list as bullets. All right. So check this out. So now we can just you know query our agent right here are the prompts. Here are the tools. This is everything that we saw before. Let's go ahead and continue firing off these prompts to really understand what they can do for us. 

All right. So if we type /find, you can see we have another prompt. Find data sources prompts. This is going to discover available data files in the current directory and present them as load options. Now, see how much more helpful these prompts are than just having tools hidden somewhere. I'm going to hit tab. You can see here we have an argument, the directory path. I'll just hit dot for that and fire that off. So, this is going to automatically discover all available JSON and CSV files for our quick data MCP server.""",
                "start_ratio": 0.40,
                "end_ratio": 0.46
            },
            {
                "title": "The Big Three of AI Coding: Context, Model, Prompt",
                "content": """So, we had a prompt, also known as an agentic workflow, do this work for us automatically. You can see we also have take note of this this is really important ready to load with load dataset commands. So with the previous prompt and this prompt you can see every prompt we're running we're getting a suggestion or a for direction or a next step for what we can do with this MCP server. So what I'm going to do here is just type load ecom. So I have a really tight information dense keyword prompt literally just two words with the current context that we have set up thanks to our prompts and thanks to Claude Code running on Claude for Sonnet. I can be nearly 100% sure that this is going to run the right tool with the right information. 

Okay. And so I'll kick this off. And notice how I just, you know, ran through the big three of AI coding. Context, model, prompt. These never go away. That's why they're a principle of AI coding. They're always there whether you realize it or not. The more you can look and think from your agents perspective with the current available context model and prompt, the more you'll be able to hand off tons and tons of engineering work, which in the end results in your engineering velocity increase.""",
                "start_ratio": 0.46,
                "end_ratio": 0.52
            },
            {
                "title": "Dataset First Look and Correlation Investigation",
                "content": """So check this out. So, we have the file path here using the full absolute path. Looks great. And then we have the dataset name. Okay. With just typing slash, with just working through a few pre-existing prompts, we're moving a lot faster than if we were looking through, you know, the documentation going back and forth and back and forth. And that is a really important thing to call out here, right? We haven't left the terminal. We haven't left Claude Code. We're focused. We're moving quickly. And we're operating inside of this MCP server with minimal information. 

Okay, so we have that dataset loaded. If we scroll back up, you'll remember here at the top that we were given a concrete workflow. You can see uh find dataset to discover data files and then we can run load dataset and then explore data. So let's go ahead and run that. I'm going to type /first. This is our first look MCP prompt. I'll hit tab and you can see there the arguments are dataset name. I'll go ahead and just type ecom... and we should get auto completion there. Okay, there we go. So this prompt and we're going to take a look at the individual prompts in a second is kicking off one or more tools.""",
                "start_ratio": 0.52,
                "end_ratio": 0.58
            },
            {
                "title": "Exploring Prompt Architecture and Agentic Workflows",
                "content": """Let's go ahead. Let's run another prompt. So, we can do /quick data to see all of our prompts. Let's go ahead and run the correlation investigation prompt. So, this is going to find correlations inside of our dataset. We'll of course type ecom... And before we run this, let me show you exactly what these prompts look like inside of the MCP server. So, we'll open up Cursor and we're just going to search for that prompt. Notice how I just have a single method inside of this file. And since we're here, let's talk about codebase architecture. This is important. 

So, I have the codebase embedded in its own directory here. And on top, you can see the three essential directories for agentic coding. And you can see our trees directory for multi-agent parallel AI coding. Check out the previous video to see how we parallelize Claude Code into multiple trees to get work done at the same time. But if we click into architecture modular and we take a look at the architecture here, you can see we have our data there. Then we have source MCP server and we have the primitives of the MCP server, right? Tools, resources, and prompts. If we open up prompts, we can see our correlation investigation prompt here.""",
                "start_ratio": 0.58,
                "end_ratio": 0.64
            },
            {
                "title": "Prompt Implementation and Tool Composition",
                "content": """Inside of the single function, these are all single function Python files to keep everything nice and isolated and easily testable. So, if we hop up to this file, we can see something really cool. We're passing in the dataset name and then we're just running arbitrary code, which is effectively our agentic workflow. So, you can do anything you want here. The most important thing is to gather some type of prompt response and then return that back to your agent. Right? This is what's going to get passed right back into the agent. So you can see we have lots of detail on the correlation investigation. A couple of branches of logic here, a loop, and you can see we're loading that schema out of our existing dataset. 

So let's go ahead. Let's run this. This is going to run a really great analysis on our dataset. Okay, so we're going to close that. Let's run this. So, this prompt is kicking off a tool call. And this is super important. Inside of your prompts, you can kick off one or more tool calls. You can see here how the prompt allows you to compose sequences of tool calls very very quickly using a custom slash command here.""",
                "start_ratio": 0.64,
                "end_ratio": 0.69
            },
            {
                "title": "Loading Multiple Datasets and Correlation Analysis",
                "content": """Okay, so quick commands to start. You can see that we're picking this up automatically. This is getting returned into the context window. And now Claude Code running on Claude 4 wants to kick this off for us based on this prompt. Okay, so of course we'll hit yes. And you can see there we're getting some concrete feedback. Okay, we need at least two numerical columns for correlation analysis. Okay, so we can go ahead and kick this off. This is going to reexpose information back into our agent. So e-commerce orders cannot run this. Okay, so our tools are giving us feedback all guided by our prompt. 

Let's go ahead and load some more data. Right, we can very quickly thanks to our slash command just run /find and let's go ahead and find those other data sources that we have. I'll specify the directory here dot and this is going to reload all of our data sources. And so you can see here we can load these two additional data sources. Let's go ahead and load these. So I'm just going to say load all. So now we're going to get those two prompts. There's our employee survey dataset and here's our product performance dataset. We'll hit yes. Yes. Now you have multiple numerical columns cross datasets for correlation analysis.""",
                "start_ratio": 0.69,
                "end_ratio": 0.75
            },
            {
                "title": "Finding Correlations Between Satisfaction and Tenure",
                "content": """So I'll just say run analysis on employee product. Okay. So there it is. There's that find correlation lookup and you can see here it's queued up several calls, several tool calls that we can now kick off. So this is one way to, you know, activate this workflow. That's great. I'm going to hit escape here and I'm going to reuse the slash command that we were we were going for. So I'm going to type / um correlation investigation prompt. Looks great. And then I'll pass in let's use our employee survey. So I'll paste that in and let's run the investigation prompt here. This should kick off a similar workflow. There it is. 

So this prompt is exposing the potential columns that we can correlate. So I'm going to go ahead. I want to kick off this first flow that was revealed by this prompt. Super simple. It's a slash command that's exposed by our MCP server prompts that we just pass in one variable to work with. Okay. So go ahead and type uh run option one. Okay. So this should pop up find correlations. There it is. Let's fire off our correlations and let's see what we get here. So check this out. Strong correlation found. We have satisfaction score correlated with tenure years.""",
                "start_ratio": 0.75,
                "end_ratio": 0.81
            },
            {
                "title": "Visualizing Correlations and Understanding Prompt Power",
                "content": """All right. So if we open up this dataset just to take a look at this, you can see several columns. So you can see here tenure year satisfaction score simple CSV file and this prompt and the tools called by the prompt found this strong correlation. Okay, so there's a strong positive correlation between satisfaction score and tenure year. That means employees with high satisfaction scores tend to have longer tenure. And so this reveals, you know, not to get too specific into the weeds of this MCP server, but this is important because it's going to immediately reveal to us that satisfaction and retention are closely linked. Satisfied employees stay longer. Not a mind-blowing revelation, but this could be anything inside of your dataset. 

Okay, I'm just. I'm just putting together a small concise example that we can, you know, discuss to showcase the power of these MCP server prompts. Okay, do you want to visualize this with option two? I'll. I'll say go ahead and we'll just continue walking through create chart. Let's go and fire that off. We now have an additional chart set up here. We can open this up. So, we can copy this file path here. If we go into HTML preview mode, we can see this chart generated.""",
                "start_ratio": 0.81,
                "end_ratio": 0.87
            },
            {
                "title": "The Three Advantages of Prompts Over Tools",
                "content": """So, what does this all mean, right? Why are prompts inside of your MCP server so important? Right away, by using this MCP server, we were able to move a lot faster. If we close Claude here, reopen it, and we type /assets, we can get our agent back up and running with this MCP server very quickly. Okay, so prompts let you quickly set up your agent with everything they need to know to operate your MCP server. So this is just one simple way you can use MCP server prompts. Check this out. And we can look at this exact prompt, right? This is the list MCP assets prompt. So check this out. Look how simple this is. This is quite literally just returning essential information about this MCP server in a custom way to our agent. 

This prompt primes both your memory and your agents memory with everything it needs to know about your MCP server. Every MCP server I build out now has some type of prompt just like this. So now everything is exposed. We can quickly see and operate on things in a much faster way. We can always type /quick-dash and start understanding our datasets. Right? So you know we then ran our find and we passed in dot prompts allow us to prime our agent in powerful ways and run arbitrary Claude Code tools.""",
                "start_ratio": 0.87,
                "end_ratio": 0.93
            },
            {
                "title": "Prompts as Agentic Workflows and Final Recommendations",
                "content": """So inside of the find data sources prompt again we can just search this. I've isolated everything into its own file. This is another great pattern. I highly recommend you follow. We have our find data sources prompt which is running arbitrary code. Principal AI coding members know this as an ADW AI developer workflow. That's all these prompts are. They're end-to-end chains of prompts and code coupled together that end up in a simple string return value. So after we scan all the directories, we do something really powerful. We in multiple use cases, in multiple scenarios, we offer the agent suggestions. This is really really powerful. Our agent is ready for the next step, right?

Your prompts have three massive advantages that your tools don't have. You can with Claude Code reference all of your prompts in a clean, detailed way very quickly. Okay, so no more guessing so you can quickly get up and running with whatever MCP server you have. So second, your prompts can compose tools in your MCP server together. Okay, this is super super powerful. You saw multiple times here our prompt was then kicking off individual tools that exists underneath the prompts, right? That's why we have this tier list order of capability prompts greater than tools greater than resources.

And lastly, a super super underutilized element of prompts is that you can guide the experience. At the end, our agent is saying, "Use dataset first look to explore any dataset." So, our agent through the prompt that was run here, right? If we scroll up here, we have find data resources prompt, it triggered a whole slew of not just a sequence of tools, but also a guide and a direction for you, the engineer operating the tool. And more importantly, every single day, it's giving our agent the next steps.

With prompts, you can build out high quality MCP servers that do more than just call tools. Tool calling is just the beginning. Tools are the primitives of MCP servers, not the end state. You want to end up with prompts, right? Prompts represent end-to-end developer workflows that are truly agentic workflows or as I like to call them, AI developer workflows, right? They are quite literally doing developer work that you would do, but it's powered, of course, by Gen AI. You really want to be thinking about MCP servers as a way to solve a domain specific problem in an automated fashion with repeat solutions embedded inside of the prompts. The prompt is what the tools scale into. This codebase is linked in the description to give you a concrete example of how you can use prompts inside your MCP servers.""",
                "start_ratio": 0.93,
                "end_ratio": 1.0
            }
        ]
        
        # Create chunk objects
        chunks = []
        for i, chunk_data in enumerate(chunks_data):
            start_time = int(chunk_data["start_ratio"] * duration)
            end_time = int(chunk_data["end_ratio"] * duration)
            token_count = self.count_tokens(chunk_data["content"])
            
            chunk = {
                "id": f"manual_{i}",
                "chapter_index": 0,
                "chapter_title": chunk_data["title"],
                "chunk_index": i,
                "start_time": start_time,
                "end_time": end_time,
                "text": chunk_data["content"],
                "token_count": token_count,
                "sentences": chunk_data["content"].split(". "),
                "level": "manual",
                "overlap_with_previous": False
            }
            chunks.append(chunk)
            
        # Create output structure
        output = {
            "processing_timestamp": datetime.now().isoformat(),
            "video_metadata": {
                "id": video_id,
                "title": title,
                "channel_name": "IndyDevDan",
                "duration_seconds": duration,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            },
            "processing_stats": {
                "total_chunks": len(chunks),
                "chunk_sizes": {
                    "min_tokens": min(c["token_count"] for c in chunks),
                    "max_tokens": max(c["token_count"] for c in chunks),
                    "avg_tokens": sum(c["token_count"] for c in chunks) / len(chunks)
                },
                "manual_chunking": True
            },
            "chunks": chunks
        }
        
        return output


def main():
    """Process the enhanced transcript with manual chunking."""
    chunker = ManualChunkerMCP()
    
    # Video metadata
    video_id = "mKEq_YaJjPI"
    title = "How I build Agentic MCP Servers for Claude Code (Prompts CHANGE Everything)"
    duration = 1435  # seconds
    
    # Read enhanced transcript
    with open(f"enhanced_transcript_{video_id}.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Skip header lines
        text = ''.join(lines[6:])  # Skip the first 6 lines (metadata)
    
    # Create chunks
    result = chunker.chunk_transcript(video_id, title, duration, text)
    
    # Save result
    output_file = f"manual_chunks_{video_id}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"✅ Manual chunking complete!")
    print(f"📊 Created {len(result['chunks'])} high-quality chunks")
    print(f"📈 Token sizes: {result['processing_stats']['chunk_sizes']['min_tokens']}-{result['processing_stats']['chunk_sizes']['max_tokens']} (avg: {result['processing_stats']['chunk_sizes']['avg_tokens']:.0f})")
    print(f"💾 Saved to: {output_file}")


if __name__ == "__main__":
    main()