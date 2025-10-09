"""
Manual Chunker for n8n Automation: Generate and Post AI Shorts
Creates high-quality semantic chunks for the n8n automated content generation tutorial.
"""

import json
from datetime import datetime
from typing import List, Dict
import tiktoken

# Video metadata
VIDEO_ID = "QJSE1yXoDxQ"
VIDEO_TITLE = "N8N Automation: Generate and Post AI Shorts! (N8N Tutorial)"
VIDEO_CHANNEL = "Productive Dude"
VIDEO_DURATION = 1726  # seconds
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def create_manual_chunks() -> List[Dict]:
    """Create manually curated chunks for the n8n automation video."""
    
    chunks = []
    
    # Chunk 1: Introduction and Value Proposition
    chunks.append({
        "text": """n8n Automation: Generate and Post AI Shorts by Productive Dude

Learn how to generate 100% automated content with this complete n8n system. The tutorial includes copy-paste resources available in the free AI Pioneers community, and a one-click install template in the paid AI Foundations community.

Right now is the perfect time to learn n8n and AI video generation as these topics are exploding. The passive income potential is significant - not only are you building valuable skills as an AI automation engineer, but you can generate passive income through automated video uploads. YouTube typically pays content creators $2,000 to $5,000 per month for uploaded videos with ads.

This system uses Kance, an impressive and affordable AI video generation model created by ByteDance (creators of TikTok). Some say it's even better than Google's V3 model while being more cost-effective.

The automation will: generate an idea, create a video prompt, create a title, generate the video with Kance, add ASMR-style audio, upload to YouTube/Instagram/TikTok, and log everything to Airtable.""",
        "start_time": 0,
        "end_time": 180,
        "topics": ["n8n", "AI video generation", "passive income", "Kance", "ByteDance", "automation overview"],
        "importance": "high",
        "context": "Introduction and value proposition"
    })
    
    # Chunk 2: Setting Up the Schedule Trigger
    chunks.append({
        "text": """Setting up the n8n workflow starts with a Schedule Trigger that determines posting frequency. From a fresh n8n workflow, add first step and type "schedule" to find the Schedule Trigger.

For optimal results, upload at most every 2 hours. This creates 12 videos per day without overwhelming YouTube or TikTok's systems. Platforms can be picky about automated upload frequency, so 2-hour intervals provide a good balance.

Configure the schedule trigger to run every 2 hours, then return to Canvas. This automation will now trigger automatically at your specified interval.""",
        "start_time": 180,
        "end_time": 280,
        "topics": ["n8n schedule trigger", "upload frequency", "platform limits"],
        "importance": "high",
        "context": "Initial workflow setup"
    })
    
    # Chunk 3: OpenAI Integration for Content Generation
    chunks.append({
        "text": """Add OpenAI integration for content generation. Click the plus button, type "OpenAI", select "Message a model". Create new credential named "demo" for this tutorial.

To get your OpenAI API key: visit the OpenAI developers platform, log in, go to Settings > Billing and load $5-$10 in credits if new, then go to API Keys. Create a new secret key, name it, select default project, and copy the key.

In n8n, paste the API key and save once connection tests successfully. Create three OpenAI nodes:
1. "idea" node - generates video ideas (system prompt from resources)
2. "prompt" node - creates video prompts based on ideas
3. "title" node - generates video titles

Use chatgpt-4o-latest model for all nodes. Set output content as JSON and configure system/user prompts from the provided resources.""",
        "start_time": 280,
        "end_time": 480,
        "topics": ["OpenAI", "API setup", "content generation", "GPT-4", "node configuration"],
        "importance": "high",
        "context": "AI content generation setup"
    })
    
    # Chunk 4: Airtable Database Configuration
    chunks.append({
        "text": """Configure Airtable for tracking video status. Create new workspace called "VideoHub". Set up columns:
- ID: Autonumber field (rename from first column)
- Title: Text field (rename from notes)
- Source: Attachment field (change from assignee)
- Status: Single select with options "in progress" and "posted"
- Prompt: Text field (duplicate of title field)

Delete unnecessary fields like attachments and attachment summary.

For n8n connection, create access token: go to profile > builder hub > create new token. Name it "demo", add all scopes, share with all current and future bases in workspace, create token and copy it.

In n8n, add Airtable node, create credential with the access token, rename node to "log". Select VideoHub base and table. Map title and prompt fields from OpenAI output, set status to "in progress".""",
        "start_time": 480,
        "end_time": 720,
        "topics": ["Airtable", "database setup", "video tracking", "access tokens", "field mapping"],
        "importance": "high",
        "context": "Database configuration for tracking"
    })
    
    # Chunk 5: Kance Video Generation via FAL
    chunks.append({
        "text": """Set up Kance video generation through FAL.ai. Add HTTP request node, change method to POST, URL: https://fal.run/fal-ai/bytedance/kance/v1/pro/text-to-video

Configure authentication: Generic credential type > Header auth. Create credential with:
- Name: authorization
- Value: Key [YOUR_FAL_API_KEY]

At fal.ai, create account, add $10-$20 credits in billing, generate API key. FAL connects to multiple AI services including MMO (audio) and Kance (video).

Add headers: content-type: application/json

Configure body parameters:
- prompt: map from prompt node
- resolution: 1080p
- duration: 10
- camera_fixed: false
- seed: -1
- aspect_ratio: 9x16 (for vertical videos)

Add "wait for video" node with 240 seconds wait time for video generation.""",
        "start_time": 720,
        "end_time": 960,
        "topics": ["FAL.ai", "Kance", "video generation", "API configuration", "HTTP requests"],
        "importance": "high",
        "context": "Video generation setup"
    })
    
    # Chunk 6: Audio Generation and Video Retrieval
    chunks.append({
        "text": """After video generation, retrieve the video with another HTTP request (GET method). URL uses expression: ${json.response.url}. Use same FAL authentication.

For audio generation, duplicate HTTP request and configure:
- Name: "audio generation"
- Method: POST
- URL: https://fal.run/fal-ai/mmo/audio-v2
- Body parameters:
  - video_url: ${json.url}
  - prompt: " " (single space - required but left blank)
  - duration: 10

Add "wait for audio" node with 80 seconds (60-70 works sometimes but 80 is safer).

Final retrieval: duplicate retrieve video node, name it "retrieve final video", turn off headers. This gets the video with audio applied.""",
        "start_time": 960,
        "end_time": 1200,
        "topics": ["audio generation", "MMO", "video retrieval", "timing considerations"],
        "importance": "high",
        "context": "Audio processing workflow"
    })
    
    # Chunk 7: Blotado Multi-Platform Upload
    chunks.append({
        "text": """Configure Blotado for multi-platform uploads. Blotado allows uploading to YouTube, Instagram, TikTok, and more without extra charges based on volume - they charge flat rate regardless of upload count.

Setup: Create Blotado account (paid plan required for API), log into all social platforms in separate tabs first, then connect accounts in Blotado settings. Copy API key from API access section.

In n8n, add HTTP request for upload:
- Name: "upload"
- Method: POST
- URL: https://api.blotado.com/media
- Authentication: Header auth with Authorization: [API_KEY]
- Body: url: ${json.url}

Add "set" node named "platforms" to configure account IDs. Create fields for YouTube, Instagram, and TikTok, paste respective account IDs from Blotado dashboard.""",
        "start_time": 1200,
        "end_time": 1440,
        "topics": ["Blotado", "multi-platform upload", "social media integration", "API setup"],
        "importance": "high",
        "context": "Social media distribution setup"
    })
    
    # Chunk 8: Platform-Specific Upload and Final Logging
    chunks.append({
        "text": """Create platform-specific upload nodes by duplicating the upload node. For each platform:
- Change URL from /media to /posts
- Use JSON body from provided resources
- YouTube: includes description field for promotion
- Instagram/TikTok: platform-specific JSON configurations

Each platform node can be included optionally - use only the platforms you need.

Final step: duplicate the initial Airtable log node, rename to "result", change operation to "update". Configure:
- Match on ID column (expression: $('log').id)
- Update status to "posted"
- Add source column with video URL in specific JSON format

Test the complete workflow with execute workflow. Full process takes about 5 minutes: idea generation, video creation, audio addition, multi-platform upload, and Airtable logging.

Activate the workflow to run automatically on schedule. Monitor results in Airtable with video previews and status tracking.""",
        "start_time": 1440,
        "end_time": 1726,
        "topics": ["platform uploads", "JSON configuration", "workflow testing", "automation activation"],
        "importance": "high",
        "context": "Upload configuration and workflow completion"
    })
    
    return chunks


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def main():
    """Generate the manual chunks and save to file."""
    chunks = create_manual_chunks()
    
    # Add metadata to each chunk
    for i, chunk in enumerate(chunks):
        chunk['chunk_id'] = f"{VIDEO_ID}_chunk_{i+1}"
        chunk['video_id'] = VIDEO_ID
        chunk['video_title'] = VIDEO_TITLE
        chunk['channel'] = VIDEO_CHANNEL
        chunk['video_url'] = VIDEO_URL
        chunk['processed_date'] = datetime.now().isoformat()
        chunk['token_count'] = count_tokens(chunk['text'])
        chunk['processing_method'] = 'manual_semantic'
    
    # Calculate statistics
    total_tokens = sum(chunk['token_count'] for chunk in chunks)
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    
    print(f"Created {len(chunks)} manual chunks")
    print(f"Total tokens: {total_tokens}")
    print(f"Average tokens per chunk: {avg_tokens:.0f}")
    print(f"Token range: {min(c['token_count'] for c in chunks)} - {max(c['token_count'] for c in chunks)}")
    
    # Save chunks
    output_file = f"manual_chunks_{VIDEO_ID}.json"
    output_data = {
        'video_metadata': {
            'video_id': VIDEO_ID,
            'title': VIDEO_TITLE,
            'channel': VIDEO_CHANNEL,
            'duration': VIDEO_DURATION,
            'url': VIDEO_URL,
            'processing_date': datetime.now().isoformat()
        },
        'chunks': chunks,
        'statistics': {
            'total_chunks': len(chunks),
            'total_tokens': total_tokens,
            'average_tokens': avg_tokens,
            'processing_method': 'manual_semantic'
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved manual chunks to: {output_file}")


if __name__ == "__main__":
    main()