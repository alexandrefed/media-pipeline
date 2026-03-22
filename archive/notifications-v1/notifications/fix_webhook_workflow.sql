-- Fix n8n Webhook Workflow (078JDpHZix14KAme)
-- Error: "propertyValues[itemName] is not iterable"
-- Date: 2025-10-21

-- Step 1: Backup the current workflow
CREATE TABLE IF NOT EXISTS workflow_backups (
    backup_date TIMESTAMP DEFAULT NOW(),
    workflow_id VARCHAR(255),
    workflow_data JSONB
);

INSERT INTO workflow_backups (workflow_id, workflow_data)
SELECT id, to_jsonb(workflows.*)
FROM workflows
WHERE id = '078JDpHZix14KAme';

-- Step 2: Deactivate the workflow first
UPDATE workflows
SET active = false
WHERE id = '078JDpHZix14KAme';

-- Step 3: Fix the Split In Batches node
-- The issue is with the "Process Each Insight" node
-- We need to update its configuration to be compatible

UPDATE workflows
SET nodes = jsonb_set(
    nodes,
    '{3}',  -- Index of "Process Each Insight" node in the array
    '{
      "id": "loop-insights",
      "name": "Process Each Insight",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [900, 240],
      "parameters": {
        "batchSize": 1,
        "options": {}
      }
    }'::jsonb
),
updated_at = NOW()
WHERE id = '078JDpHZix14KAme';

-- Alternative: If the above doesn't work, try downgrading typeVersion
-- UPDATE workflows
-- SET nodes = jsonb_set(
--     nodes,
--     '{3,typeVersion}',
--     '1'::jsonb
-- )
-- WHERE id = '078JDpHZix14KAme';

-- Step 4: Verify the update
SELECT
    id,
    name,
    active,
    nodes->3 as split_in_batches_node,
    updated_at
FROM workflows
WHERE id = '078JDpHZix14KAme';

-- Step 5: Reactivate the workflow
-- DO THIS MANUALLY via n8n UI to ensure proper webhook registration
-- UPDATE workflows
-- SET active = true
-- WHERE id = '078JDpHZix14KAme';

-- Verification query
SELECT
    id,
    name,
    active,
    created_at,
    updated_at
FROM workflows
WHERE id = '078JDpHZix14KAme';
