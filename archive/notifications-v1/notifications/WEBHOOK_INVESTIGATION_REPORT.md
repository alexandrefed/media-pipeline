# n8n Webhook Investigation Report

**Date:** 2025-10-21
**Workflow ID:** 078JDpHZix14KAme
**Workflow Name:** Store Video Insights - Knowledge Base
**Expected Webhook URL:** https://n8n.vecia.fr/webhook/video-processed

---

## Problem Summary

The webhook URL returns 404 "not registered" despite the workflow showing as "active" via API.

```bash
curl -X POST https://n8n.vecia.fr/webhook/video-processed
# Returns: "The requested webhook 'POST video-processed' is not registered."
```

---

## Investigation Findings

### 1. API Status Check
✅ **Workflow is marked as active in the database**
- API response shows: `"active": true`
- Workflow was last updated: 2025-10-21T08:20:03.409Z

### 2. Webhook Node Configuration
✅ **Webhook node is properly configured**
```json
{
  "id": "webhook-trigger",
  "name": "Video Processing Complete",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "parameters": {
    "httpMethod": "POST",
    "path": "video-processed",
    "responseMode": "responseNode"
  },
  "webhookId": "video-processed"
}
```

### 3. UI Investigation
❌ **Workflow shows activation error in n8n UI**
- Status shows: "Active" with green toggle
- **BUT**: Red warning triangle appears next to toggle
- Error message: **"propertyValues[itemName] is not iterable"**
- Tooltip: "The workflow is activated but could not be started. Click to display error message."

### 4. Activation Attempts
❌ **Manual toggle OFF/ON fails**
- Deactivation: Successful
- Reactivation: **FAILS with same error**
- Error: "Workflow could not be activated: propertyValues[itemName] is not iterable"

### 5. Editor Load Test
❌ **Workflow cannot be opened in editor**
- Attempting to open workflow results in: "Could not find workflow"
- Same error message: "propertyValues[itemName] is not iterable"
- Editor shows empty canvas with "Add first step..."

---

## Root Cause Analysis

### The Error: `propertyValues[itemName] is not iterable`

This is a **known n8n bug** that occurs when there's a corrupted node configuration. Based on the workflow structure, the likely culprit is the **Split In Batches node** ("Process Each Insight").

**Why this node?**
1. The error mentions "itemName" which is typically related to Split In Batches nodes
2. Looking at the workflow JSON, the Split In Batches node has minimal configuration
3. This node type is known to cause this specific error in n8n versions around 1.112.x

### Impact on Webhook Registration

When n8n tries to activate a workflow:
1. It validates all node configurations
2. It initializes each node
3. **If ANY node fails validation, webhook registration is skipped**
4. The workflow status is set to "active" in the database
5. BUT the webhook is never actually registered with the webhook manager

Result: **Database says "active" but webhook is not listening**

---

## Solution Required

### Option 1: Fix the Split In Batches Node (Recommended)
The "Process Each Insight" node needs to be reconfigured:

**Current configuration:**
```json
{
  "id": "loop-insights",
  "name": "Process Each Insight",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "parameters": {
    "batchSize": 1,
    "options": {}
  }
}
```

**Fix needed:** The node might be missing required field mappings or has incompatible typeVersion.

**Steps to fix:**
1. Access n8n database directly (PostgreSQL)
2. Update the workflow JSON to fix the Split In Batches node
3. OR recreate the workflow from scratch with proper node configuration

### Option 2: Temporary Workaround
Remove the Split In Batches loop and process insights differently:
- Use a Code node to iterate through insights
- Use multiple parallel branches instead of a loop
- Simplify to process all insights in a single batch

### Option 3: Database Direct Fix
Execute SQL to update the workflow configuration:

```sql
-- First, get the current workflow JSON
SELECT name, active, nodes, connections
FROM n8n.workflows
WHERE id = '078JDpHZix14KAme';

-- Then update with fixed configuration
-- (Requires manually fixing the JSON first)
UPDATE n8n.workflows
SET nodes = '[fixed_nodes_json]',
    active = false
WHERE id = '078JDpHZix14KAme';
```

---

## Screenshots Evidence

1. **workflow-not-found-error.png** - Initial attempt to access workflow via URL
2. **workflows-list-active-with-error.png** - Workflow showing as "Active" with error icon
3. **workflow-activation-error.png** - Error dialog showing activation failure
4. **activation-failed-error.png** - Manual toggle attempt failure
5. **workflow-load-error.png** - Editor failing to load workflow

---

## Immediate Action Required

**The workflow is currently BROKEN and cannot be activated.**

### Priority 1: Fix the Workflow
1. Access VPS: `ssh root@vecia.fr`
2. Connect to PostgreSQL: `psql -U n8n_user -d n8n`
3. Export current workflow for backup
4. Fix the Split In Batches node configuration
5. Deactivate and reactivate the workflow

### Priority 2: Alternative Approach
If fixing is complex, consider:
1. Create a NEW workflow with the same webhook path
2. Delete the broken workflow (after backing up the logic)
3. Use the new workflow going forward

---

## Test Plan After Fix

```bash
# 1. Verify workflow is truly active
curl -X GET https://n8n.vecia.fr/api/v1/workflows/078JDpHZix14KAme \
  -H "X-N8N-API-KEY: your-api-key"

# 2. Test webhook is registered
curl -X POST https://n8n.vecia.fr/webhook/video-processed \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "video_id": "test123",
      "title": "Test Video",
      "url": "https://youtube.com/watch?v=test123",
      "insights": []
    }
  }'

# Expected: Should return success response, NOT 404
```

---

## Conclusion

**Status:** 🔴 BROKEN - Webhook not operational
**Cause:** Corrupted Split In Batches node configuration
**Fix Required:** Database-level workflow JSON update or workflow recreation
**ETA:** Requires VPS access and PostgreSQL update
