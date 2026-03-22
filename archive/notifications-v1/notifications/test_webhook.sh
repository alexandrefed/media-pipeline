#!/bin/bash
# Test n8n Webhook Registration
# Usage: ./test_webhook.sh [webhook-path]

set -e

WEBHOOK_PATH="${1:-video-processed}"
BASE_URL="https://n8n.vecia.fr/webhook"
FULL_URL="${BASE_URL}/${WEBHOOK_PATH}"

echo "================================================"
echo "n8n Webhook Registration Test"
echo "================================================"
echo "Testing webhook: ${FULL_URL}"
echo ""

# Test 1: Simple GET request (should return 405 Method Not Allowed if registered)
echo "Test 1: GET request (expect 405 or similar, NOT 404)"
echo "Command: curl -s -o /dev/null -w '%{http_code}' -X GET ${FULL_URL}"
GET_STATUS=$(curl -s -o /dev/null -w '%{http_code}' -X GET "${FULL_URL}")
echo "Status: ${GET_STATUS}"

if [ "${GET_STATUS}" = "404" ]; then
    echo "❌ FAIL: Webhook NOT registered (404 Not Found)"
    echo ""
    echo "This means the webhook path does not exist."
    echo "The workflow might not be active or has activation errors."
    exit 1
elif [ "${GET_STATUS}" = "405" ]; then
    echo "✅ PASS: Webhook is registered (405 Method Not Allowed)"
    echo ""
    echo "This is expected - webhook accepts POST, not GET."
else
    echo "⚠️  UNKNOWN: Got status ${GET_STATUS}"
fi

echo ""
echo "================================================"

# Test 2: POST request with minimal payload
echo "Test 2: POST request with test payload"
echo "Command: curl -X POST ${FULL_URL} -H 'Content-Type: application/json' -d '{...}'"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${FULL_URL}" \
    -H "Content-Type: application/json" \
    -d '{
        "body": {
            "video_id": "test_webhook_123",
            "title": "Webhook Test Video",
            "channel_name": "Test Channel",
            "channel_id": "UC_test",
            "url": "https://youtube.com/watch?v=test123",
            "duration_seconds": 60,
            "pipeline_type": "ai_tools",
            "total_chunks": 0,
            "insights": []
        }
    }')

STATUS_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "Status: ${STATUS_CODE}"
echo "Response:"
echo "${BODY}" | python3 -m json.tool 2>/dev/null || echo "${BODY}"

if [ "${STATUS_CODE}" = "404" ]; then
    echo ""
    echo "❌ FAIL: Webhook NOT registered"
    echo ""
    echo "The workflow is either:"
    echo "  1. Not active"
    echo "  2. Has activation errors"
    echo "  3. Webhook path is incorrect"
    echo ""
    echo "Check the workflow in n8n UI for error icons."
    exit 1
elif [ "${STATUS_CODE}" = "200" ]; then
    echo ""
    echo "✅ SUCCESS: Webhook is working!"
    echo ""
    echo "The workflow processed the request successfully."
    exit 0
elif [ "${STATUS_CODE}" = "500" ]; then
    echo ""
    echo "⚠️  PARTIAL SUCCESS: Webhook is registered but execution failed"
    echo ""
    echo "This could be due to:"
    echo "  1. Database connection issues"
    echo "  2. Missing credentials"
    echo "  3. Invalid data in the payload"
    echo ""
    echo "Check n8n execution logs for details."
    exit 1
else
    echo ""
    echo "⚠️  UNKNOWN: Got status ${STATUS_CODE}"
    echo "Check the response body above for details."
    exit 1
fi
