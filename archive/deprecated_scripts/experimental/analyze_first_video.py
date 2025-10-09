"""
Analyze the first video in the database to determine if it needs reprocessing
with the new manual chunking approach.
"""

import asyncio
import json
import tiktoken
from datetime import datetime
from src.database.connection import DatabaseConnection, get_database


async def analyze_first_video():
    """Analyze the first video in the database."""
    db = get_database()
    await db.initialize()
    
    try:
        async with db.get_connection() as conn:
            # Get the first video
            video = await conn.fetchrow("""
                SELECT id, url, title, channel_name, duration_seconds, 
                       processing_status, quality_score
                FROM ai_kb.sources 
                ORDER BY id 
                LIMIT 1
            """)
            
            if not video:
                print("❌ No videos found in database")
                return
                
            print(f"📹 Analyzing first video:")
            print(f"   Title: {video['title']}")
            print(f"   URL: {video['url']}")
            print(f"   Channel: {video['channel_name']}")
            print(f"   Duration: {video['duration_seconds']} seconds")
            print(f"   Status: {video['processing_status']}")
            print(f"   Quality Score: {video['quality_score']}")
            print()
            
            # Get chunks for this video
            chunks = await conn.fetch("""
                SELECT id, content, chunk_index, start_time, end_time,
                       quality_score, mentioned_tools
                FROM ai_kb.chunks 
                WHERE source_id = $1
                ORDER BY chunk_index
            """, video['id'])
            
            print(f"📊 Chunk Analysis:")
            print(f"   Total chunks: {len(chunks)}")
            
            if chunks:
                # Analyze chunk sizes
                tokenizer = tiktoken.get_encoding("cl100k_base")
                token_counts = []
                
                for chunk in chunks:
                    tokens = len(tokenizer.encode(chunk['content']))
                    token_counts.append(tokens)
                
                avg_tokens = sum(token_counts) / len(token_counts)
                min_tokens = min(token_counts)
                max_tokens = max(token_counts)
                
                # Count undersized chunks
                undersized = sum(1 for t in token_counts if t < 200)
                oversized = sum(1 for t in token_counts if t > 800)
                
                print(f"   Average tokens: {avg_tokens:.0f}")
                print(f"   Min tokens: {min_tokens}")
                print(f"   Max tokens: {max_tokens}")
                print(f"   Undersized chunks (<200): {undersized} ({undersized/len(chunks)*100:.1f}%)")
                print(f"   Oversized chunks (>800): {oversized} ({oversized/len(chunks)*100:.1f}%)")
                print()
                
                # Show sample chunks
                print("📝 Sample chunks:")
                for i in [0, len(chunks)//2, -1]:
                    if 0 <= i < len(chunks):
                        chunk = chunks[i]
                        tokens = token_counts[i]
                        content = chunk['content'][:150] + "..." if len(chunk['content']) > 150 else chunk['content']
                        print(f"\n   Chunk {chunk['chunk_index']} ({tokens} tokens):")
                        print(f"   Time: {chunk['start_time']:.0f}s - {chunk['end_time']:.0f}s")
                        print(f"   Content: {content}")
                
                print("\n" + "="*70 + "\n")
                
                # Compare with manual chunking results
                print("🔄 Comparison with Manual Chunking Approach:")
                print("\n   Current (Algorithmic) Results:")
                print(f"   - Total chunks: {len(chunks)}")
                print(f"   - Average tokens: {avg_tokens:.0f}")
                print(f"   - Quality issues: {undersized} undersized chunks")
                
                print("\n   Expected Manual Chunking Results:")
                print(f"   - Estimated chunks: ~15-20 (based on {video['duration_seconds']}s duration)")
                print(f"   - Target tokens: 300-500 average")
                print(f"   - Quality: Semantically coherent chunks with complete thoughts")
                
                # Make recommendation
                print("\n" + "="*70)
                print("\n🎯 RECOMMENDATION:")
                
                if avg_tokens < 100 or undersized > len(chunks) * 0.3:
                    print("   ⚠️  This video should be REPROCESSED with manual chunking!")
                    print(f"   - Current chunks are too small ({avg_tokens:.0f} tokens avg)")
                    print(f"   - {undersized} chunks are undersized")
                    print("   - Manual chunking would reduce chunks by ~70% while improving quality")
                elif avg_tokens < 200:
                    print("   ⚡ This video could benefit from reprocessing")
                    print(f"   - Current chunks are below optimal size ({avg_tokens:.0f} tokens avg)")
                    print("   - Manual chunking would improve semantic coherence")
                else:
                    print("   ✅ This video has reasonable chunk sizes")
                    print(f"   - Current chunks are adequately sized ({avg_tokens:.0f} tokens avg)")
                    print("   - Reprocessing is optional")
                
                print("\n   To reprocess:")
                print(f"   1. Extract: uv run python main.py extract \"{video['url']}\"")
                print("   2. Enhance transcript in Claude Code")
                print("   3. Run manual chunking: uv run python manual_chunker.py")
                print("   4. Import to database (when implemented)")
                
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(analyze_first_video())