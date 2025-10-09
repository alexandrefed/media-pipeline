"""
AI Knowledge Base - Main Application Entry Point

This is the main entry point for the AI Knowledge Base system.
Provides CLI interface for video processing and knowledge querying.
"""

import asyncio
import sys
from typing import Optional

from src.database.connection import init_database, close_database
# from src.processing.video_processor import VideoProcessor  # TODO: Fix imports
from src.search.query_system import AIKnowledgeQuery
from src.processing.entity_correction import EntityCorrector
from src.pipeline.youtube_processor import YouTubeProcessor


# TODO: Fix VideoProcessor imports
# async def process_video(url: str) -> None:
#     """Process a single video through the pipeline."""
#     print(f"🎬 Processing video: {url}")
#     
#     processor = VideoProcessor()
#     try:
#         result = await processor.process_video(url)
#         
#         print(f"✅ Processing completed!")
#         print(f"📊 Status: {result['status']}")
#         print(f"🆔 Source ID: {result['source_id']}")
#         
#         if result['status'] == 'completed':
#             stats = result['processing_stats']
#             print(f"📄 Chunks created: {result['chunks_created']}")
#             print(f"📈 Average quality: {stats['average_chunk_quality']:.1f}")
#             print(f"🔧 Total corrections: {stats['corrected_segments']}")
#         
#     except Exception as e:
#         print(f"❌ Error processing video: {e}")
#     finally:
#         await processor.db.close()


async def query_knowledge(query: str) -> None:
    """Query the knowledge base."""
    print(f"🔍 Searching for: {query}")
    
    query_system = AIKnowledgeQuery()
    try:
        response = await query_system.search(query)
        
        print(f"✅ Found {response.total_found} results in {response.search_time_ms:.1f}ms")
        print(f"📊 Strategy: {response.search_strategy}")
        
        if response.detected_entities:
            print(f"🔧 Detected entities: {', '.join(response.detected_entities)}")
        
        print("\n📄 Results:")
        for i, result in enumerate(response.results[:5], 1):
            print(f"\n{i}. {result.source_title}")
            print(f"   Channel: {result.channel_name}")
            print(f"   Similarity: {result.similarity_score:.3f}")
            print(f"   Quality: {result.quality_score:.1f}")
            print(f"   Tools: {', '.join(result.mentioned_tools) if result.mentioned_tools else 'None'}")
            print(f"   Content: {result.content[:200]}...")
            print(f"   🔗 {result.source_url}&t={int(result.start_time)}s")
        
        if response.suggestions:
            print(f"\n💡 Suggestions:")
            for suggestion in response.suggestions[:3]:
                print(f"   - {suggestion}")
        
    except Exception as e:
        print(f"❌ Error querying knowledge base: {e}")
    finally:
        await query_system.db.close()


def test_entity_correction() -> None:
    """Test the entity correction system."""
    print("🔧 Testing Entity Correction System")
    
    corrector = EntityCorrector()
    
    test_cases = [
        "I'm using mate and for automation",
        "Curser is a great AI code editor",
        "The zero is perfect for prototyping",
        "Make dot com has good integrations"
    ]
    
    for test_case in test_cases:
        result = corrector.correct_text(test_case)
        print(f"Original: {test_case}")
        print(f"Corrected: {result.corrected_text}")
        print(f"Entities: {[e['corrected'] for e in result.detected_entities]}")
        print()


def extract_video_for_enhancement(url: str) -> None:
    """Extract video transcript for manual Claude Code enhancement."""
    print(f"📥 Extracting video for manual enhancement: {url}")
    
    processor = YouTubeProcessor()
    try:
        text_file = processor.process_for_manual_enhancement(url)
        print(f"✅ Text extracted and saved to: {text_file}")
        print(f"🔄 Next step: Enhance this text manually in Claude Code")
        print(f"🔄 Then run: python main.py enhance {text_file}")
    except Exception as e:
        print(f"❌ Error extracting video: {e}")


def process_enhanced_transcript(enhanced_file: str) -> None:
    """Process enhanced transcript through chunking pipeline."""
    print(f"📊 Processing enhanced transcript: {enhanced_file}")
    
    try:
        with open(enhanced_file, 'r', encoding='utf-8') as f:
            enhanced_text = f.read()
        
        processor = YouTubeProcessor()
        # Extract original URL from filename or ask user
        original_url = input("Enter the original YouTube URL: ").strip()
        
        result = processor.process_enhanced_text(enhanced_text, original_url)
        
        # Save result
        import json
        output_file = enhanced_file.replace('.txt', '_processed.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"✅ Enhanced transcript processed successfully!")
        print(f"📊 Generated {len(result['chunks'])} chunks")
        print(f"💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error processing enhanced transcript: {e}")


def process_video_pipeline(url: str) -> None:
    """Process video through complete pipeline."""
    print(f"🎬 Processing video through complete pipeline: {url}")
    
    processor = YouTubeProcessor()
    try:
        result = processor.process_video(url, save_intermediates=True)
        
        # Save final result
        import json
        video_id = processor.extract_video_id(url)
        output_file = f"final_processed_{video_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"✅ Video processed successfully!")
        print(f"📊 Generated {len(result['chunks'])} chunks")
        print(f"💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error processing video: {e}")


async def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("AI Knowledge Base - Usage:")
        print("\n🚀 STREAMLINED WORKFLOW (Recommended):")
        print("  python main.py streamlined <youtube_url>  - Complete workflow with agent analysis")
        print("\n📋 LEGACY WORKFLOW:")
        print("  python main.py process <youtube_url>      - Process a video (full pipeline)")
        print("  python main.py extract <youtube_url>      - Extract for manual enhancement")
        print("  python main.py enhance <text_file>        - Process enhanced transcript")
        print("\n🔍 QUERY & STATUS:")
        print("  python main.py query '<search_query>'     - Search knowledge base")
        print("  python main.py status                     - Check system status")
        print("  python main.py test-correction            - Test entity correction")
        return
    
    command = sys.argv[1]

    if command == "streamlined":
        if len(sys.argv) < 3:
            print("❌ Please provide a YouTube URL")
            return

        url = sys.argv[2]
        print("🚀 Running streamlined workflow...")
        print("   This uses the new agent-based analysis system")
        print()

        # Import and run streamlined process
        import subprocess
        subprocess.run([sys.executable, "scripts/streamlined_process.py", url])

    elif command == "process":
        if len(sys.argv) < 3:
            print("❌ Please provide a YouTube URL")
            return
        
        url = sys.argv[2]
        process_video_pipeline(url)
    
    elif command == "extract":
        if len(sys.argv) < 3:
            print("❌ Please provide a YouTube URL")
            return
        
        url = sys.argv[2]
        extract_video_for_enhancement(url)
    
    elif command == "enhance":
        if len(sys.argv) < 3:
            print("❌ Please provide a text file path")
            return
        
        text_file = sys.argv[2]
        process_enhanced_transcript(text_file)
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("❌ Please provide a search query")
            return
        
        query = sys.argv[2]
        await init_database()
        await query_knowledge(query)
        await close_database()
    
    elif command == "test-correction":
        test_entity_correction()
    
    elif command == "status":
        await init_database()
        
        from src.database.connection import get_database
        db = get_database()
        
        try:
            # Test database connection
            success = await db.test_connection()
            print(f"📊 Database connection: {'✅ OK' if success else '❌ Failed'}")
            
            # Get table info
            table_info = await db.get_table_info()
            print(f"📋 Tables found: {len(table_info)}")
            
            # Get some stats
            async with db.get_connection() as conn:
                source_count = await conn.fetchval("SELECT COUNT(*) FROM sources")
                chunk_count = await conn.fetchval("SELECT COUNT(*) FROM chunks")
                
                print(f"📹 Videos processed: {source_count}")
                print(f"📄 Chunks created: {chunk_count}")
                
                if chunk_count > 0:
                    avg_quality = await conn.fetchval("SELECT AVG(quality_score) FROM chunks")
                    print(f"📈 Average chunk quality: {avg_quality:.1f}")
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
        
        await close_database()
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())
