# Custom GPT Authentication Troubleshooting

## Error: "Invalid authentication credentials" (401)

This error means OpenAI is reaching your API but the authentication header isn't being sent correctly.

## Step-by-Step Fix

### 1. Verify Authentication Configuration

In your Custom GPT's Actions section:

1. Click on the Authentication dropdown
2. Select **"API Key"**
3. Configure exactly as follows:

```
Auth Type: Custom
Custom Header Name: X-API-Key
API Key: ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt
```

**Critical Points:**
- Header name must be exactly `X-API-Key` (case-sensitive)
- No spaces before or after the API key
- Must click "Save" after entering the key

### 2. Test Authentication Manually

Before testing in the GPT, verify your API works:

```bash
curl -X POST https://api.vecia.fr/api/v1/query \
  -H "X-API-Key: ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_results": 1}'
```

If this works but the GPT doesn't, the issue is in the GPT configuration.

### 3. Common Issues and Solutions

#### Issue 1: Header Name Case Sensitivity
- ❌ Wrong: `x-api-key`, `X-Api-Key`, `X-API-KEY`
- ✅ Correct: `X-API-Key`

#### Issue 2: Extra Spaces
Check for spaces:
- At the beginning or end of the API key
- In the header name field

#### Issue 3: Authentication Not Saved
After entering the API key:
1. Click outside the input field
2. Look for a "Save" or checkmark button
3. The configuration should persist when you navigate away

### 4. Alternative Setup (If Custom Header Fails)

If the custom header continues to fail, try the standard API Key configuration:

1. Change **Auth Type** from "Custom" to "API Key"
2. It might automatically use "Authorization" header
3. Enter the same API key

### 5. Debug Information

When testing fails, check:
- The error message details
- The "operation" field (should be "searchKnowledge")
- The path (should be "/api/v1/query")

### 6. Complete Reset

If nothing works:
1. Delete the current action
2. Re-import the OpenAPI schema from: `https://api.vecia.fr/openapi.json`
3. Reconfigure authentication from scratch
4. Test with a simple query

## Working Example

A successful request should return:
```json
{
  "query": "your query",
  "results": [...],
  "total_found": X,
  "search_time_ms": X
}
```

## Contact Support

If authentication continues to fail:
- Verify API is accessible: https://api.vecia.fr/health
- Check API logs on your server
- Contact: contact@vecia.fr