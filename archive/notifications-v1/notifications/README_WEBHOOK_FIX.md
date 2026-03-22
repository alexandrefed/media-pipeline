# n8n Webhook Not Registered - Investigation Complete

## Executive Summary

**Status:** 🔴 BROKEN
**Workflow ID:** 078JDpHZix14KAme
**Issue:** Webhook returns 404 despite workflow showing as "active"
**Root Cause:** Corrupted Split In Batches node causing activation failure
**Error:** `propertyValues[itemName] is not iterable`

---

## What Happened

The workflow appears "active" in the database but **webhooks are never registered** because:

1. n8n tries to activate the workflow
2. The "Process Each Insight" node (Split In Batches) has a configuration error
3. Activation fails during node validation
4. Webhook registration is **skipped**
5. Database still shows `active = true` (misleading!)
6. Result: API says "active" but webhook returns 404

---

## Evidence

**Test Result:**
```bash
$ curl -X POST https://n8n.vecia.fr/webhook/video-processed
{
  "code": 404,
  "message": "The requested webhook 'POST video-processed' is not registered."
}
```

**UI Shows:**
- Green "Active" toggle ✅
- Red warning triangle ⚠️
- Error: "The workflow is activated but could not be started"

**Screenshots:**
- `/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/.playwright-mcp/workflow-activation-error.png`
- `/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/.playwright-mcp/workflows-list-active-with-error.png`

---

## Fix Options

### ✅ RECOMMENDED: Recreate Workflow (30 min)

**Why:** Fastest and most reliable

1. Open n8n UI: https://n8n.vecia.fr
2. Duplicate the workflow
3. Delete the broken "Process Each Insight" (Split In Batches) node
4. Replace with a Code node (see `ALTERNATIVE_FIX.md`)
5. Use batch insert instead of loop
6. Test with new webhook path
7. Swap paths and delete old workflow

**Benefits:**
- Clean slate, no database corruption
- Simpler workflow (faster execution)
- Easy to test before deployment

---

### Option 2: Direct SQL Fix (45 min)

**Why:** Preserves workflow ID

1. SSH to VPS: `ssh root@vecia.fr`
2. Backup workflow: Run `fix_webhook_workflow.sql` (step 1)
3. Fix the node configuration via SQL
4. Manually reactivate in n8n UI

**Risk:** Might not fix the underlying issue

---

### Option 3: Delete and Rebuild (60 min)

**Why:** Nuclear option

1. Delete the broken workflow
2. Create from scratch
3. Reconfigure all nodes
4. Test thoroughly

**When to use:** If other options fail

---

## Files Created

1. **WEBHOOK_INVESTIGATION_REPORT.md** - Full investigation details
2. **ALTERNATIVE_FIX.md** - Step-by-step replacement workflow guide
3. **fix_webhook_workflow.sql** - SQL script for database fix
4. **README_WEBHOOK_FIX.md** - This file

---

## Next Steps

**IMMEDIATE (Today):**
1. Read `ALTERNATIVE_FIX.md`
2. Open n8n UI and duplicate the workflow
3. Implement the Code node replacement
4. Test with `-v2` webhook path

**AFTER SUCCESSFUL TEST:**
1. Deactivate old workflow
2. Update new workflow to use `video-processed` path
3. Delete old workflow

**VERIFICATION:**
```bash
# Should return success, not 404
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
```

---

## Questions?

Contact: Alex (report created 2025-10-21)

**Related Issues:**
- n8n GitHub: Similar issues with Split In Batches in v1.112.x
- Workaround: Use Code nodes for iteration instead of Split In Batches

---

## Lessons Learned

1. **Always verify webhook registration** after activation
2. **Test webhooks with curl** before relying on API status
3. **Watch for UI warning icons** - they indicate real problems
4. **Split In Batches is problematic** - prefer Code nodes for loops
5. **Database `active` flag is not reliable** - webhooks can fail silently
