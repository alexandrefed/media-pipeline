#!/usr/bin/env python3
"""
Interactive transcript viewer
"""

import json
import sys

def main():
    # Load cleaned transcript
    with open('transcript_mKEq_YaJjPI_cleaned.json', 'r') as f:
        data = json.load(f)
    
    segments = data['segments']
    
    print(f"=== {data['metadata']['title']} ===")
    print(f"Duration: {data['metadata']['duration_seconds']//60}m {data['metadata']['duration_seconds']%60}s")
    print(f"Total segments: {len(segments)}")
    print()
    
    # Show options
    print("Options:")
    print("  1. View all segments")
    print("  2. View high-quality segments only (>0.7)")
    print("  3. View segments with specific tool")
    print("  4. View segments by time range")
    print("  5. Search transcript")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        # Show all segments
        for i, seg in enumerate(segments):
            print(f"\n{i+1:4d}. [{seg['start_time']:6.1f}s] Q:{seg['quality_score']:.2f}")
            print(f"      {seg['text']}")
            if seg['tools_mentioned']:
                print(f"      Tools: {', '.join(seg['tools_mentioned'])}")
    
    elif choice == '2':
        # High quality segments
        high_quality = [s for s in segments if s['quality_score'] > 0.7]
        print(f"\nFound {len(high_quality)} high-quality segments:")
        for seg in high_quality:
            print(f"\n[{seg['start_time']:6.1f}s] Quality: {seg['quality_score']:.3f}")
            print(f"Tools: {', '.join(seg['tools_mentioned'])}")
            print(f"Text: {seg['text']}")
    
    elif choice == '3':
        # Segments with specific tool
        tool = input("Enter tool name (e.g., MCP, Claude Code, agent): ").strip()
        matching = [s for s in segments if tool in s['tools_mentioned']]
        print(f"\nFound {len(matching)} segments mentioning '{tool}':")
        for seg in matching[:20]:  # Show first 20
            print(f"\n[{seg['start_time']:6.1f}s] {seg['text']}")
    
    elif choice == '4':
        # Time range
        start = float(input("Start time (seconds): "))
        end = float(input("End time (seconds): "))
        matching = [s for s in segments if start <= s['start_time'] <= end]
        print(f"\nSegments from {start}s to {end}s:")
        for seg in matching:
            print(f"\n[{seg['start_time']:6.1f}s] {seg['text']}")
    
    elif choice == '5':
        # Search
        query = input("Enter search term: ").strip().lower()
        matching = [s for s in segments if query in s['text'].lower()]
        print(f"\nFound {len(matching)} segments containing '{query}':")
        for seg in matching[:20]:  # Show first 20
            print(f"\n[{seg['start_time']:6.1f}s] {seg['text']}")

if __name__ == "__main__":
    main()