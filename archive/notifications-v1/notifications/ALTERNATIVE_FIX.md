# Alternative Fix: Recreate Workflow Without Split In Batches

## Problem
The Split In Batches node is causing the `propertyValues[itemName] is not iterable` error.

## Solution
Replace the loop with a Code node that processes all insights in one go.

## Implementation Steps

### 1. Via n8n API (Easiest)

Create a new simplified workflow:

```bash
# On VPS or local machine with access to n8n API
curl -X POST https://n8n.vecia.fr/api/v1/workflows \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: your-api-key" \
  -d @simplified_workflow.json
```

### 2. Simplified Workflow Structure

**Remove:** Split In Batches loop
**Replace with:** Code node that inserts all insights at once

**Flow:**
1. Webhook Trigger (POST video-processed)
2. Store Video Metadata
3. Check for Insights (IF node)
4. **NEW: Code Node** - Process All Insights
5. **NEW: Postgres Batch Insert** - Insert all insights
6. Create Notification Record
7. Send Telegram Notification
8. Mark Video as Notified
9. Update Notification Status
10. Success Response

### 3. Code Node Logic

Replace the Split In Batches + Loop with this Code node:

```javascript
// Process All Insights - Code Node
const insights = $input.item.json.body.insights || [];
const videoId = $input.item.json.body.video_id;

if (insights.length === 0) {
  return [];
}

// Transform insights into batch insert format
const insightRecords = insights.map(insight => ({
  video_id: videoId,
  insight_text: insight.text,
  insight_type: insight.type || 'concept',
  context: insight.context,
  category: insight.category,
  tags: insight.tags ? '{' + insight.tags.join(',') + '}' : '{}',
  timestamp_start: insight.timestamp_start,
  timestamp_end: insight.timestamp_end,
  quality_score: insight.quality_score || 0.7,
  priority_level: insight.priority || 'medium',
  actionable: insight.actionable !== false,
  next_review_date: new Date(Date.now() + 86400000).toISOString().split('T')[0]
}));

return insightRecords.map(record => ({ json: record }));
```

### 4. Postgres Batch Insert Configuration

**Operation:** Insert
**Table:** ai_kb.kb_insights
**Columns:** Map from incoming data
**Options:**
- Query Batching: `batch` (not `single`)
- Batch Size: `100`

### 5. Quick Fix via n8n UI

If you have n8n UI access:

1. **Duplicate the workflow**
   - Go to workflows list
   - Click "..." menu on "Store Video Insights - Knowledge Base"
   - Select "Duplicate"

2. **Edit the duplicated workflow**
   - Open the new workflow
   - Delete the "Process Each Insight" (Split In Batches) node
   - Delete the "Store Insight" node
   - Add a new Code node (see code above)
   - Add a new Postgres node for batch insert
   - Connect the nodes properly

3. **Update webhook path**
   - Click on webhook node
   - Change path to: `video-processed-v2` (temporary)
   - Save and activate

4. **Test the new workflow**
   ```bash
   curl -X POST https://n8n.vecia.fr/webhook/video-processed-v2 \
     -H "Content-Type: application/json" \
     -d '{"body":{"video_id":"test","title":"Test","url":"https://youtube.com/test","insights":[{"text":"Test insight","type":"concept"}]}}'
   ```

5. **If working, swap the webhook paths**
   - Deactivate OLD workflow
   - Change NEW workflow webhook path to: `video-processed`
   - Activate NEW workflow
   - Delete OLD workflow

### 6. Benefits of This Approach

✅ **Eliminates the buggy Split In Batches node**
✅ **Faster execution** (one database call instead of N calls)
✅ **Simpler workflow structure**
✅ **More reliable activation**
✅ **Easier to debug**

### 7. Migration Path

**Phase 1: Test (Today)**
- Create new workflow with `-v2` suffix
- Test with sample data
- Verify all insights are stored correctly

**Phase 2: Deploy (After successful test)**
- Deactivate old workflow
- Update new workflow to use original webhook path
- Update documentation

**Phase 3: Cleanup (Next week)**
- Delete old broken workflow
- Remove backup

---

## Estimated Time to Fix

- **Option A (API):** 15 minutes
- **Option B (UI Duplicate):** 30 minutes
- **Option C (Direct SQL Fix):** 45 minutes (if you can find the exact issue)

**Recommendation:** Use Option B (UI Duplicate) - fastest and safest.
