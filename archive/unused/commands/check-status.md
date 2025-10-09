---
description: Quick check of video processing status and statistics
---

# Video Processing Status Check

!echo "=== COMPLETED VIDEOS ==="
!grep -c "✅ DONE" list.md

!echo -e "\n=== PENDING VIDEOS ==="
!grep -v "✅ DONE" list.md | grep -v "❌ NO SUBTITLES" | wc -l

!echo -e "\n=== CURRENT LEARNING SYSTEM VERSION ==="
!grep '"version"' learning/processing_knowledge_base.json

!echo -e "\n=== LAST PROCESSED VIDEO ==="
!tail -20 learning/processing_history.md | grep -A2 "### Video"

!echo -e "\n=== FILES IN WORK ==="
!ls -la pending/raw_transcripts/ 2>/dev/null || echo "No raw transcripts pending"
!ls -la pending/enhanced_no_chunks/ 2>/dev/null || echo "No enhanced transcripts pending"