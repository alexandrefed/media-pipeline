#!/usr/bin/env python3
"""
Extract High-Quality Knowledge Base Chunks

This script focuses on extracting the highest quality chunks from the deduplicated
transcript for the knowledge base system.
"""

import json
import re
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class KnowledgeChunk:
    """High-quality knowledge chunk for the database"""
    chunk_id: str
    text: str
    content_type: str
    quality_score: float
    mentioned_tools: List[str]
    key_concepts: List[str]
    actionable_insights: List[str]
    timestamp_start: float
    timestamp_end: float
    word_count: int
    source_segments: List[int]
    
    def to_dict(self) -> Dict:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "content_type": self.content_type,
            "quality_score": self.quality_score,
            "mentioned_tools": self.mentioned_tools,
            "key_concepts": self.key_concepts,
            "actionable_insights": self.actionable_insights,
            "timestamp_start": self.timestamp_start,
            "timestamp_end": self.timestamp_end,
            "word_count": self.word_count,
            "source_segments": self.source_segments
        }


class HighQualityExtractor:
    """Extract and enhance high-quality chunks for knowledge base"""
    
    # Enhanced tool patterns with common transcription errors
    TOOL_PATTERNS = {
        'MCP': r'\bMCP\b|\bMCP servers?\b|\bmcp\b',
        'Claude': r'\bClaude\b|\bClaude (?:4|Code)\b|\bclawed code\b|\bClaude AI\b',
        'Deepseek': r'\bDeepseek\b|\bDeep seek\b|\bDeepseek R1\.1\b',
        'n8n': r'\bn8n\b|\bmate and\b|\bmaten\b',  # Common transcription errors
        'Make.com': r'\bMake(?:\.com)?\b|\bmake\.com\b',
        'Zapier': r'\bZapier\b',
        'Cursor': r'\bCursor\b|\bcursor editor\b',
        'v0': r'\bv0\b|\bV0\b|\bvzero\b',
        'GitHub': r'\bGitHub\b|\bgithub\b',
        'VSCode': r'\bVSCode\b|\bVS Code\b|\bVisual Studio Code\b',
        'Notion': r'\bNotion\b',
        'Slack': r'\bSlack\b',
        'Discord': r'\bDiscord\b',
        'Opus': r'\bOpus\b|\bOpus 4\b',
        'Sonnet': r'\bSonnet\b|\bSonnet 4\b'
    }
    
    # Key MCP concepts to extract
    MCP_CONCEPTS = [
        'resources', 'tools', 'prompts', 'props',
        'capabilities', 'primitives', 'servers',
        'engineering velocity', 'agentic coding',
        'tool calling', 'context window',
        'autocomplete', 'templates', 'patterns'
    ]
    
    # Actionable patterns
    ACTIONABLE_PATTERNS = [
        r'you (?:can|should|need to|must|will be able to) (.{10,60})',
        r'(?:this|it) (?:allows|enables|helps|lets) you to (.{10,60})',
        r'to (\w+ .{10,50}), (?:you|we) (?:can|should|need to)',
        r'(?:instead of|rather than) (.{10,40}), (?:use|try|consider) (.{10,40})',
        r'the (?:best|right|correct) way to (.{10,50}) is',
        r'(?:always|never|make sure to|be sure to) (.{10,50})',
        r'(?:pro tip|tip|trick|hack): (.{10,60})'
    ]
    
    def __init__(self):
        self.chunk_counter = 0
    
    def extract_tools_with_correction(self, text: str) -> List[str]:
        """Extract tools with common transcription error corrections"""
        tools = []
        text_lower = text.lower()
        
        for tool, pattern in self.TOOL_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                tools.append(tool)
        
        # Special handling for n8n transcription errors
        if 'mate and' in text_lower and 'n8n' not in tools:
            tools.append('n8n')
        
        return list(set(tools))
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """Extract key MCP and engineering concepts"""
        concepts = []
        text_lower = text.lower()
        
        for concept in self.MCP_CONCEPTS:
            if concept in text_lower:
                # Find the context around the concept
                pattern = rf'(.{{0,30}}\b{concept}\b.{{0,30}})'
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                for match in matches[:2]:  # Limit to 2 per concept
                    clean_match = match.strip()
                    if len(clean_match.split()) > 3:
                        concepts.append(clean_match)
        
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for c in concepts:
            if c not in seen:
                seen.add(c)
                unique.append(c)
        
        return unique[:10]
    
    def extract_actionable_insights(self, text: str) -> List[str]:
        """Extract actionable insights and instructions"""
        insights = []
        
        for pattern in self.ACTIONABLE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Handle patterns with multiple capture groups
                    insight = ' '.join(m.strip() for m in match if m.strip())
                else:
                    insight = match.strip()
                
                # Clean and validate
                insight = re.sub(r'\s+', ' ', insight).strip()
                if len(insight) > 15 and len(insight.split()) > 3:
                    insights.append(insight)
        
        # Extract specific MCP instructions
        mcp_patterns = [
            r'MCP servers? (?:let you|allow you to|enable) (.{10,50})',
            r'with MCP (?:servers?|resources?|tools?), you can (.{10,50})',
            r'(?:resources?|tools?|prompts?) (?:in MCP|for MCP) (.{10,40})'
        ]
        
        for pattern in mcp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            insights.extend([m.strip() for m in matches if len(m.strip()) > 15])
        
        # Deduplicate
        seen = set()
        unique = []
        for insight in insights:
            insight_lower = insight.lower()
            if insight_lower not in seen:
                seen.add(insight_lower)
                unique.append(insight)
        
        return unique[:7]
    
    def calculate_enhanced_quality_score(self, text: str, tools: List[str], 
                                       concepts: List[str], insights: List[str]) -> float:
        """Calculate quality score with focus on knowledge base value"""
        score = 0.0
        
        # Base content quality (30%)
        word_count = len(text.split())
        if 50 <= word_count <= 200:
            score += 0.15
        elif 30 <= word_count <= 250:
            score += 0.10
        
        # Complete sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 10]
        if len(sentences) >= 2:
            score += 0.15
        elif len(sentences) >= 1:
            score += 0.10
        
        # Tool mentions (25%)
        if tools:
            tool_score = min(0.25, len(tools) * 0.08)
            if 'MCP' in tools:
                tool_score += 0.05
            score += tool_score
        
        # Key concepts (20%)
        if concepts:
            score += min(0.20, len(concepts) * 0.05)
        
        # Actionable insights (25%)
        if insights:
            score += min(0.25, len(insights) * 0.07)
        
        # Bonus for MCP-specific content
        mcp_keywords = ['resource', 'tool', 'prompt', 'prop', 'capability', 'primitive']
        mcp_count = sum(1 for kw in mcp_keywords if kw in text.lower())
        if mcp_count >= 3:
            score *= 1.2
        elif mcp_count >= 2:
            score *= 1.1
        
        return min(1.0, score)
    
    def merge_segments_intelligently(self, segments: List[Dict]) -> List[Dict]:
        """Merge segments into coherent chunks with improved logic"""
        merged = []
        i = 0
        
        while i < len(segments):
            # Start new chunk
            chunk_text = segments[i]['cleaned_text']
            chunk_segments = [segments[i]['index']]
            start_time = segments[i]['start_time']
            end_time = segments[i]['end_time']
            
            # Look ahead for related content
            j = i + 1
            while j < len(segments) and j < i + 8:  # Max 8 segments
                next_text = segments[j]['cleaned_text']
                combined = chunk_text + " " + next_text
                
                # Check if should merge
                should_merge = False
                
                # Merge if continuing a thought
                if not chunk_text.rstrip().endswith('.') and len(combined.split()) < 200:
                    should_merge = True
                
                # Merge if talking about same tool/concept
                current_tools = self.extract_tools_with_correction(chunk_text)
                next_tools = self.extract_tools_with_correction(next_text)
                if current_tools and next_tools and set(current_tools) & set(next_tools):
                    should_merge = True
                
                # Merge if short segments
                if len(chunk_text.split()) < 30 and len(next_text.split()) < 30:
                    should_merge = True
                
                # Don't merge if too long
                if len(combined.split()) > 250:
                    should_merge = False
                
                if should_merge:
                    chunk_text = combined
                    chunk_segments.append(segments[j]['index'])
                    end_time = segments[j]['end_time']
                    j += 1
                else:
                    break
            
            # Only keep chunks with meaningful content
            if len(chunk_text.split()) >= 20:
                merged.append({
                    'text': chunk_text,
                    'start_time': start_time,
                    'end_time': end_time,
                    'segments': chunk_segments
                })
            
            i = j
        
        return merged
    
    def process_transcript(self, input_file: str, output_file: str):
        """Process deduplicated transcript to extract high-quality chunks"""
        print(f"Loading deduplicated transcript from {input_file}...")
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        segments = data['segments']
        
        # First, merge segments intelligently
        print("Merging segments into coherent chunks...")
        merged_chunks = self.merge_segments_intelligently(segments)
        print(f"Created {len(merged_chunks)} merged chunks from {len(segments)} segments")
        
        # Process each chunk
        knowledge_chunks = []
        
        for chunk in merged_chunks:
            text = chunk['text']
            
            # Extract information
            tools = self.extract_tools_with_correction(text)
            concepts = self.extract_key_concepts(text)
            insights = self.extract_actionable_insights(text)
            
            # Calculate quality
            quality = self.calculate_enhanced_quality_score(text, tools, concepts, insights)
            
            # Determine content type based on content
            if insights and len(insights) >= 2:
                content_type = 'actionable_guide'
            elif 'mcp' in text.lower() and any(kw in text.lower() for kw in ['resource', 'tool', 'prompt']):
                content_type = 'mcp_capability'
            elif tools and len(tools) >= 2:
                content_type = 'tool_integration'
            elif concepts:
                content_type = 'conceptual'
            else:
                content_type = 'general'
            
            # Create knowledge chunk
            kc = KnowledgeChunk(
                chunk_id=f"chunk_{self.chunk_counter:04d}",
                text=text,
                content_type=content_type,
                quality_score=quality,
                mentioned_tools=tools,
                key_concepts=concepts[:5],  # Limit for storage
                actionable_insights=insights[:5],
                timestamp_start=chunk['start_time'],
                timestamp_end=chunk['end_time'],
                word_count=len(text.split()),
                source_segments=chunk['segments']
            )
            
            knowledge_chunks.append(kc)
            self.chunk_counter += 1
        
        # Sort by quality
        knowledge_chunks.sort(key=lambda x: x.quality_score, reverse=True)
        
        # Filter for knowledge base
        high_quality = [kc for kc in knowledge_chunks if kc.quality_score >= 0.6]
        medium_quality = [kc for kc in knowledge_chunks if 0.4 <= kc.quality_score < 0.6]
        
        print(f"\nQuality Analysis:")
        print(f"High quality chunks (>= 0.6): {len(high_quality)}")
        print(f"Medium quality chunks (0.4-0.6): {len(medium_quality)}")
        print(f"Total chunks for KB: {len(high_quality) + len(medium_quality)}")
        
        # Show top chunks
        print(f"\nTop 10 chunks for knowledge base:")
        for i, kc in enumerate(knowledge_chunks[:10], 1):
            print(f"\n{i}. {kc.chunk_id} (Score: {kc.quality_score:.2f})")
            print(f"   Type: {kc.content_type}")
            print(f"   Tools: {', '.join(kc.mentioned_tools) if kc.mentioned_tools else 'None'}")
            print(f"   Word count: {kc.word_count}")
            print(f"   Text preview: {kc.text[:120]}...")
            if kc.actionable_insights:
                print(f"   Key insight: {kc.actionable_insights[0]}")
        
        # Prepare output
        output_data = {
            'metadata': {
                'source_file': input_file,
                'total_chunks_processed': len(knowledge_chunks),
                'high_quality_chunks': len(high_quality),
                'medium_quality_chunks': len(medium_quality),
                'chunks_for_kb': len(high_quality) + len(medium_quality)
            },
            'knowledge_chunks': [
                kc.to_dict() for kc in knowledge_chunks 
                if kc.quality_score >= 0.4  # Only export chunks suitable for KB
            ]
        }
        
        # Save
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nHigh-quality chunks saved to {output_file}")
        
        # Generate summary statistics
        tool_stats = defaultdict(int)
        content_type_stats = defaultdict(int)
        
        for kc in knowledge_chunks:
            content_type_stats[kc.content_type] += 1
            for tool in kc.mentioned_tools:
                tool_stats[tool] += 1
        
        print("\nContent type distribution:")
        for ct, count in sorted(content_type_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ct}: {count}")
        
        print("\nTool mention distribution:")
        for tool, count in sorted(tool_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {tool}: {count}")


def main():
    """Main function"""
    extractor = HighQualityExtractor()
    
    # Use the enhanced deduplicated file
    extractor.process_transcript(
        'transcript_enhanced_dedup.json',
        'knowledge_base_chunks.json'
    )


if __name__ == '__main__':
    main()