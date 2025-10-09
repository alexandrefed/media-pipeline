# Custom GPT Setup Guide for AI Knowledge Base

## Overview

This guide walks you through setting up a Custom GPT that connects to your AI Knowledge Base API. The Custom GPT will be able to search through your curated AI tool knowledge from YouTube videos and provide expert answers with source citations.

## Prerequisites

- OpenAI ChatGPT Plus subscription
- Access to create Custom GPTs
- API running at `https://api.vecia.fr`
- API key: `ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt`

## Step 1: Create Custom GPT

1. Go to [ChatGPT](https://chat.openai.com)
2. Click on "Explore GPTs" in the sidebar
3. Click "Create" to start building your Custom GPT

## Step 2: Configure Basic Information

### Name
```
AI Tools Knowledge Expert
```

### Description
```
Expert assistant for AI automation tools like n8n, Claude Code, Cursor, and more. Searches through curated YouTube content to provide accurate, source-cited answers about AI tool usage, integrations, and best practices.
```

### Instructions (System Prompt)
```
You are an AI Tools Knowledge Expert with access to a curated knowledge base of AI automation content from YouTube videos. Your role is to help users with questions about AI tools, automation, and best practices.

## Your Capabilities:
1. Search through 29+ processed videos covering tools like:
   - n8n (automation platform)
   - Claude Code (AI coding assistant)
   - Cursor (AI code editor)
   - v0 (UI prototyping)
   - Make.com (automation)
   - MCP (Model Context Protocol)
   - And more AI tools

2. Provide accurate answers with:
   - Direct quotes from source material
   - YouTube video links with timestamps
   - Quality-scored content (0.9+ average quality)
   - Context from surrounding chunks when relevant

## How to Use Your Knowledge:
1. When users ask questions, search the knowledge base using relevant keywords
2. Prioritize high-quality, recent content
3. Always cite sources with video titles and timestamps
4. Provide direct YouTube links for users to verify information
5. If multiple sources discuss a topic, synthesize the best information

## Search Strategies:
- For tool-specific questions: Include the tool name in your search
- For integration questions: Search for both tools involved
- For best practices: Use terms like "tutorial", "guide", "setup"
- For comparisons: Search for each tool separately, then synthesize

## Response Format:
1. Direct answer to the question
2. Supporting details from the knowledge base
3. Source citations with clickable timestamps
4. Related suggestions if applicable

## Important Notes:
- All content is from manually processed and quality-checked videos
- Transcription errors have been corrected (e.g., "mate and" → "n8n")
- Focus on practical, actionable information
- Quality score of 0.9 indicates high-quality manual chunks

Remember: You're not just searching - you're providing expert guidance based on curated, high-quality AI tool knowledge.
```

### Conversation Starters
1. "How do I connect n8n with databases?"
2. "What's the best AI code editor: Cursor or Claude Code?"
3. "Show me how to use MCP servers"
4. "Compare automation tools: n8n vs Make.com vs Zapier"

## Step 3: Configure Actions

1. In the GPT builder, navigate to "Configure" → "Actions"
2. Click "Create new action"
3. Choose "Import from URL" or paste the schema directly

### Import from URL
```
https://api.vecia.fr/openapi.json
```

If the import doesn't work automatically, copy the content from `openapi_schema.json` and paste it into the schema editor.

## Step 4: Configure Authentication

1. In the Actions configuration, find "Authentication"
2. Select "API Key"
3. Configure as follows:
   - **Auth Type**: API Key
   - **Header Name**: `X-API-Key`
   - **API Key**: `ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt`

## Step 5: Test the Actions

### Test 1: Health Check
Click "Test" next to the health endpoint. You should see:
```json
{
  "status": "healthy",
  "service": "AI Knowledge Base API",
  "version": "1.0.0"
}
```

### Test 2: Search Query
Test the query endpoint with:
```json
{
  "query": "n8n automation",
  "max_results": 3
}
```

### Test 3: Statistics
Test the stats endpoint. You should see database statistics with 29 videos and 435 chunks.

## Step 6: Privacy Policy & Terms

Since this is for internal/personal use, you can use simple URLs:
- **Privacy Policy**: `https://vecia.fr/privacy`
- **Terms of Service**: `https://vecia.fr/terms`

## Step 7: Advanced Settings

### Capabilities
- ✅ Web Browsing (optional - for following YouTube links)
- ✅ Code Interpreter (optional - for code examples)
- ❌ DALL·E Image Generation (not needed)

### Additional Settings
- **Use conversation data in your GPT to improve our models**: Your choice
- **Search indexing**: Private (unless you want to share publicly)

## Usage Examples

### Example 1: Tool-Specific Query
**User**: "How do I set up n8n with PostgreSQL?"

**GPT Actions**:
1. Calls `/api/v1/query` with `{"query": "n8n PostgreSQL setup database"}`
2. Receives relevant chunks about n8n database nodes
3. Synthesizes response with source citations

### Example 2: Comparison Query
**User**: "Compare Cursor and Claude Code for React development"

**GPT Actions**:
1. First query: `{"query": "Cursor React development"}`
2. Second query: `{"query": "Claude Code React"}`
3. Combines results for comprehensive comparison

### Example 3: Best Practices
**User**: "What are the best practices for AI automation?"

**GPT Actions**:
1. Calls `/api/v1/query` with `{"query": "AI automation best practices tutorial"}`
2. Filters for high-quality chunks (0.8+ quality score)
3. Provides structured recommendations

## Troubleshooting

### "Invalid host header" Error
If you see this error, ensure the API accepts requests from OpenAI's servers. This should be configured in the Docker container.

### No Results Found
- Check if your query terms match the content (e.g., use "n8n" not "n eight n")
- Try broader search terms
- Check the stats endpoint to verify database content

### Authentication Failed
- Verify the API key is correctly entered
- Ensure X-API-Key header is configured
- Check if the API server is running

### Timeout Errors
- The API typically responds in ~1100ms
- If timeouts occur, the server might be under load
- Try reducing max_results to speed up queries

### SSL Certificate
The API is now fully configured with HTTPS at `https://api.vecia.fr` - no port specification needed!

## Monitoring Usage

Use the `/api/v1/stats` endpoint to monitor:
- Total videos and chunks in the database
- Average quality scores
- Database health

## Future Enhancements

1. **Rate Limiting**: Can be configured via nginx if needed
2. **Additional Endpoints**: Video listing, chunk details, etc.
3. **Webhook Support**: For real-time updates when new content is added
4. **Caching**: Redis for frequently accessed queries

## Security Notes

- The API key is stored securely by OpenAI
- All requests use HTTPS encryption
- No personal data is stored in queries
- Database contains only public YouTube content

## Support

For issues or questions:
1. Check API health: `GET /health`
2. Verify database content: `GET /api/v1/stats`
3. Test with simple queries first
4. Review server logs if you have access

---

## Quick Start Checklist

- [ ] Create new Custom GPT
- [ ] Set name and description
- [ ] Paste system instructions
- [ ] Import OpenAPI schema
- [ ] Configure API key authentication
- [ ] Test all three endpoints
- [ ] Add conversation starters
- [ ] Save and publish GPT

Your Custom GPT is now ready to provide expert AI tool knowledge with source citations!