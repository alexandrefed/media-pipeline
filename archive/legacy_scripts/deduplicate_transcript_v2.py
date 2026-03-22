#!/usr/bin/env python3
"""
Enhanced Transcript Deduplication and Quality Analysis Script

This version better handles overlapping duplications and cross-segment context.
"""

import json
import re
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from collections import Counter
import math


@dataclass
class CleanedSegment:
    """Represents a cleaned transcript segment with quality metrics"""
    index: int
    start_time: float
    end_time: float
    duration: float
    original_text: str
    cleaned_text: str
    content_type: str
    quality_score: float
    mentioned_tools: List[str]
    key_points: List[str]
    word_count: int
    
    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "original_text": self.original_text,
            "cleaned_text": self.cleaned_text,
            "content_type": self.content_type,
            "quality_score": self.quality_score,
            "mentioned_tools": self.mentioned_tools,
            "key_points": self.key_points,
            "word_count": self.word_count
        }


class EnhancedTranscriptDeduplicator:
    """Enhanced deduplication with cross-segment context awareness"""
    
    # Known AI tools to detect
    TOOL_PATTERNS = {
        'MCP': r'\bMCP\b|\bMCP servers?\b',
        'Claude': r'\bClaude\b|\bClaude (?:4|Code)\b|\bclawed code\b',
        'Deepseek': r'\bDeepseek\b|\bDeepseek R1\.1\b',
        'n8n': r'\bn8n\b',
        'Make.com': r'\bMake(?:\.com)?\b',
        'Zapier': r'\bZapier\b',
        'Cursor': r'\bCursor\b',
        'v0': r'\bv0\b',
        'GitHub': r'\bGitHub\b',
        'VSCode': r'\bVSCode\b|\bVS Code\b',
        'Notion': r'\bNotion\b',
        'Slack': r'\bSlack\b',
        'Discord': r'\bDiscord\b'
    }
    
    # Content type keywords - expanded
    CONTENT_TYPE_KEYWORDS = {
        'technical_instruction': ['how to', 'step by step', 'configure', 'setup', 'install', 
                                'implement', 'create', 'build', 'deploy', 'run'],
        'explanation': ['understand', 'concept', 'idea', 'principle', 'theory', 'meaning',
                       'definition', 'what is', 'why', 'because'],
        'demo': ['example', 'demonstrate', 'show you', 'let me show', 'watch as', 
                'see how', 'in action', 'real world'],
        'comparison': ['versus', 'vs', 'compared to', 'better than', 'difference between',
                      'alternative', 'instead of', 'rather than'],
        'best_practice': ['best practice', 'recommended', 'should', 'avoid', 'pro tip',
                         'always', 'never', 'important to', 'make sure'],
        'architecture': ['architecture', 'design', 'structure', 'pattern', 'framework',
                        'system', 'component', 'integration', 'workflow'],
        'capability': ['capability', 'feature', 'function', 'ability', 'power',
                      'primitive', 'resource', 'tool', 'prompt']
    }
    
    def __init__(self):
        self.duplication_stats = {
            'total_segments': 0,
            'duplicated_segments': 0,
            'duplication_patterns': Counter()
        }
        self.context_buffer = []  # Keep track of recent segments for context
    
    def advanced_deduplicate(self, text: str) -> str:
        """Advanced deduplication that handles nested and overlapping patterns"""
        words = text.split()
        if len(words) < 3:
            return text
        
        # Step 1: Find all duplicate sequences
        duplicates = []
        for length in range(2, min(15, len(words) // 2 + 1)):
            for i in range(len(words) - length):
                sequence = words[i:i+length]
                sequence_str = ' '.join(sequence)
                
                # Look for immediate repetition
                j = i + length
                count = 1
                while j + length <= len(words) and words[j:j+length] == sequence:
                    count += 1
                    j += length
                
                if count > 1:
                    duplicates.append((i, length, count))
        
        # Step 2: Sort duplicates by start position and length (prioritize longer sequences)
        duplicates.sort(key=lambda x: (x[0], -x[1]))
        
        # Step 3: Remove duplicates without overlapping
        result_words = []
        i = 0
        
        while i < len(words):
            # Find if current position starts a duplicate sequence
            dup_found = False
            for start, length, count in duplicates:
                if i == start:
                    # Add the sequence once
                    result_words.extend(words[i:i+length])
                    # Skip the repeated occurrences
                    i += length * count
                    dup_found = True
                    break
            
            if not dup_found:
                result_words.append(words[i])
                i += 1
        
        cleaned = ' '.join(result_words)
        
        # Step 4: Handle edge cases with regex for partial duplicates at boundaries
        # Pattern: "word word. Word word" -> "word. Word" 
        cleaned = re.sub(r'\b(\w+)\s+\1\b', r'\1', cleaned)
        
        # Update stats
        if len(duplicates) > 0:
            self.duplication_stats['duplicated_segments'] += 1
            max_count = max(d[2] for d in duplicates)
            self.duplication_stats['duplication_patterns'][max_count] += 1
        
        return cleaned.strip()
    
    def merge_with_context(self, segments: List[Dict], index: int) -> Optional[str]:
        """Check if segment should be merged with previous/next for better context"""
        if index == 0 or index >= len(segments) - 1:
            return None
            
        current = segments[index]
        prev_segment = segments[index - 1]
        next_segment = segments[index + 1]
        
        # Check if current segment is very short and seems incomplete
        if len(current['text'].split()) < 10:
            # Check if it continues a sentence from previous
            if not prev_segment['text'].rstrip().endswith('.'):
                return 'merge_prev'
            # Check if next segment continues this sentence
            if not current['text'].rstrip().endswith('.'):
                return 'merge_next'
        
        return None
    
    def extract_mentioned_tools(self, text: str) -> List[str]:
        """Extract AI tools mentioned in the text"""
        mentioned_tools = []
        for tool, pattern in self.TOOL_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                mentioned_tools.append(tool)
        return list(set(mentioned_tools))  # Remove duplicates
    
    def determine_content_type(self, text: str) -> str:
        """Enhanced content type determination"""
        text_lower = text.lower()
        scores = {}
        
        for content_type, keywords in self.CONTENT_TYPE_KEYWORDS.items():
            score = sum(2 if keyword in text_lower else 0 for keyword in keywords)
            # Bonus for certain patterns
            if content_type == 'technical_instruction' and re.search(r'\b(step \d+|first|then|next|finally)\b', text_lower):
                score += 3
            if content_type == 'capability' and 'mcp' in text_lower and any(word in text_lower for word in ['resource', 'tool', 'prompt']):
                score += 5
            
            if score > 0:
                scores[content_type] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'general'
    
    def extract_key_points(self, text: str) -> List[str]:
        """Enhanced key point extraction"""
        key_points = []
        
        # Extended patterns for better extraction
        patterns = [
            # Action patterns
            r'you (?:can|should|need to|must|will be able to) (\w+ .{10,50}?)(?:\.|,|$)',
            r'(?:this|it) (?:allows|enables|helps|lets) (?:you to )?(.{10,50}?)(?:\.|,|$)',
            
            # Important concepts
            r'(?:the )?(?:key|important|main|critical|essential) (?:thing|point|idea|concept) is (.{10,50}?)(?:\.|,|$)',
            r'(?:remember|note|understand) that (.{10,50}?)(?:\.|,|$)',
            
            # Definitions and explanations
            r'(\w+) (?:is|are) (?:the|a) (.{10,40}?)(?:\.|,|$)',
            r'(?:resources|tools|prompts|props) (?:are|is) (.{10,50}?)(?:\.|,|$)',
            
            # Comparisons and benefits
            r'(?:instead of|rather than) (.{10,40}?)(?:\.|,|$)',
            r'(?:dramatically|significantly) (?:increase|improve|enhance) (.{10,40}?)(?:\.|,|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                cleaned_match = match.strip().rstrip('.').strip()
                if len(cleaned_match) > 10 and len(cleaned_match.split()) > 3:
                    key_points.append(cleaned_match)
        
        # Look for MCP-specific insights
        if 'mcp' in text.lower():
            mcp_patterns = [
                r'MCP (?:servers? )?(.{10,50}?)(?:\.|,|$)',
                r'(?:resources|tools|prompts) (?:in MCP|for MCP) (.{10,40}?)(?:\.|,|$)'
            ]
            for pattern in mcp_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                key_points.extend([m.strip() for m in matches if len(m.strip()) > 10])
        
        # Remove duplicates and filter
        seen = set()
        unique_points = []
        for point in key_points:
            point_lower = point.lower()
            if point_lower not in seen and not point_lower.startswith('the '):
                seen.add(point_lower)
                unique_points.append(point)
        
        return unique_points[:7]  # Allow more key points for richer segments
    
    def calculate_quality_score(self, segment: Dict, cleaned_text: str, 
                              mentioned_tools: List[str], key_points: List[str],
                              content_type: str) -> float:
        """Enhanced quality scoring with more nuanced factors"""
        score = 0.0
        
        # Factor 1: Information density (adjusted for speaking rate)
        words_per_second = len(cleaned_text.split()) / max(segment['duration'], 0.1)
        if 1.5 <= words_per_second <= 3.0:  # Optimal speaking rate
            score += 0.15
        elif 1.0 <= words_per_second <= 3.5:
            score += 0.1
        
        # Factor 2: Tool mentions (more weight for multiple tools)
        if mentioned_tools:
            tool_score = min(0.25, len(mentioned_tools) * 0.08)
            if 'MCP' in mentioned_tools:  # Bonus for MCP mentions
                tool_score += 0.05
            score += tool_score
        
        # Factor 3: Key points (quality over quantity)
        if key_points:
            point_score = min(0.25, len(key_points) * 0.05)
            # Bonus for actionable points
            actionable_keywords = ['can', 'should', 'will be able to', 'allows', 'enables']
            if any(any(kw in point for kw in actionable_keywords) for point in key_points):
                point_score += 0.05
            score += point_score
        
        # Factor 4: Content type (heavily weight technical content)
        content_scores = {
            'technical_instruction': 0.25,
            'capability': 0.2,
            'demo': 0.2,
            'best_practice': 0.15,
            'architecture': 0.15,
            'explanation': 0.1,
            'comparison': 0.1,
            'general': 0.05
        }
        score += content_scores.get(content_type, 0.05)
        
        # Factor 5: Length and completeness
        word_count = len(cleaned_text.split())
        if 30 <= word_count <= 100:  # Ideal length for a chunk
            score += 0.1
        elif 20 <= word_count <= 150:
            score += 0.05
        
        # Factor 6: Sentence completeness
        sentences = re.split(r'[.!?]+', cleaned_text)
        complete_sentences = sum(1 for s in sentences if len(s.strip()) > 10)
        if complete_sentences >= 2:
            score += 0.05
        
        # Factor 7: Deduplication effectiveness
        original_words = len(segment['text'].split())
        cleaned_words = word_count
        dedup_ratio = cleaned_words / max(original_words, 1)
        
        if dedup_ratio < 0.4:  # Heavily duplicated (60%+ removed)
            score *= 0.8
        elif dedup_ratio > 0.9:  # Little to no duplication
            score += 0.05
        
        # Factor 8: Context richness (mentions of concepts)
        concept_keywords = ['resource', 'tool', 'prompt', 'prop', 'capability', 'primitive',
                           'engineer', 'velocity', 'value', 'intelligence']
        concept_count = sum(1 for kw in concept_keywords if kw in cleaned_text.lower())
        if concept_count >= 3:
            score += 0.1
        elif concept_count >= 2:
            score += 0.05
        
        return min(1.0, score)
    
    def process_segment(self, segment: Dict, all_segments: List[Dict], index: int) -> CleanedSegment:
        """Process a single segment with awareness of surrounding context"""
        self.duplication_stats['total_segments'] += 1
        
        # Advanced deduplication
        cleaned_text = self.advanced_deduplicate(segment['text'])
        
        # Extract information
        mentioned_tools = self.extract_mentioned_tools(cleaned_text)
        content_type = self.determine_content_type(cleaned_text)
        key_points = self.extract_key_points(cleaned_text)
        
        # Calculate quality score
        quality_score = self.calculate_quality_score(
            segment, cleaned_text, mentioned_tools, key_points, content_type
        )
        
        return CleanedSegment(
            index=segment['index'],
            start_time=segment['start_time'],
            end_time=segment['end_time'],
            duration=segment['duration'],
            original_text=segment['text'],
            cleaned_text=cleaned_text,
            content_type=content_type,
            quality_score=quality_score,
            mentioned_tools=mentioned_tools,
            key_points=key_points,
            word_count=len(cleaned_text.split())
        )
    
    def create_merged_chunks(self, cleaned_segments: List[CleanedSegment]) -> List[Dict]:
        """Create larger, more coherent chunks by merging related segments"""
        merged_chunks = []
        i = 0
        
        while i < len(cleaned_segments):
            # Start a new chunk
            chunk_segments = [cleaned_segments[i]]
            chunk_text = cleaned_segments[i].cleaned_text
            chunk_tools = set(cleaned_segments[i].mentioned_tools)
            chunk_points = cleaned_segments[i].key_points[:]
            
            # Look ahead to merge related segments
            j = i + 1
            while j < len(cleaned_segments) and j < i + 5:  # Max 5 segments per chunk
                next_seg = cleaned_segments[j]
                
                # Merge if:
                # 1. Total word count stays under 200
                # 2. Content types are compatible
                # 3. Quality scores are both decent (>= 0.3)
                compatible_types = {
                    'technical_instruction': ['explanation', 'demo', 'best_practice'],
                    'capability': ['explanation', 'architecture', 'technical_instruction'],
                    'explanation': ['technical_instruction', 'capability', 'demo'],
                    'demo': ['technical_instruction', 'explanation']
                }
                
                current_type = chunk_segments[-1].content_type
                next_type = next_seg.content_type
                
                word_count = len(chunk_text.split()) + next_seg.word_count
                
                should_merge = (
                    word_count <= 200 and
                    next_seg.quality_score >= 0.3 and
                    (next_type == current_type or 
                     next_type in compatible_types.get(current_type, []) or
                     current_type in compatible_types.get(next_type, []))
                )
                
                if should_merge:
                    chunk_segments.append(next_seg)
                    chunk_text += " " + next_seg.cleaned_text
                    chunk_tools.update(next_seg.mentioned_tools)
                    chunk_points.extend(next_seg.key_points)
                    j += 1
                else:
                    break
            
            # Create merged chunk
            if len(chunk_segments) > 1 or chunk_segments[0].quality_score >= 0.5:
                # Remove duplicate key points
                unique_points = []
                seen_points = set()
                for point in chunk_points:
                    if point.lower() not in seen_points:
                        unique_points.append(point)
                        seen_points.add(point.lower())
                
                # Calculate average quality score
                avg_quality = sum(s.quality_score for s in chunk_segments) / len(chunk_segments)
                
                # Boost quality for well-merged chunks
                if len(chunk_segments) > 2 and avg_quality >= 0.4:
                    avg_quality = min(1.0, avg_quality * 1.1)
                
                merged_chunk = {
                    'start_index': chunk_segments[0].index,
                    'end_index': chunk_segments[-1].index,
                    'start_time': chunk_segments[0].start_time,
                    'end_time': chunk_segments[-1].end_time,
                    'duration': chunk_segments[-1].end_time - chunk_segments[0].start_time,
                    'text': chunk_text.strip(),
                    'content_type': chunk_segments[0].content_type,  # Use primary type
                    'quality_score': avg_quality,
                    'mentioned_tools': list(chunk_tools),
                    'key_points': unique_points[:10],  # Limit to 10 points
                    'word_count': len(chunk_text.split()),
                    'segment_count': len(chunk_segments)
                }
                
                merged_chunks.append(merged_chunk)
            
            i = j
        
        return merged_chunks
    
    def process_transcript(self, input_file: str, output_file: str):
        """Process entire transcript file with enhanced deduplication"""
        print(f"Loading transcript from {input_file}...")
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        segments = data['segments']
        cleaned_segments = []
        
        print(f"Processing {len(segments)} segments...")
        
        for i, segment in enumerate(segments):
            cleaned_segment = self.process_segment(segment, segments, i)
            cleaned_segments.append(cleaned_segment)
            
            # Print progress every 50 segments
            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1}/{len(segments)} segments...")
        
        # Create merged chunks
        print("\nCreating merged chunks for better context...")
        merged_chunks = self.create_merged_chunks(cleaned_segments)
        
        # Sort by quality score
        high_quality_segments = [s for s in cleaned_segments if s.quality_score >= 0.7]
        high_quality_segments.sort(key=lambda x: x.quality_score, reverse=True)
        
        high_quality_chunks = [c for c in merged_chunks if c['quality_score'] >= 0.7]
        high_quality_chunks.sort(key=lambda x: x['quality_score'], reverse=True)
        
        print(f"\nDeduplication complete!")
        print(f"Total segments: {self.duplication_stats['total_segments']}")
        print(f"Segments with duplications: {self.duplication_stats['duplicated_segments']}")
        print(f"Duplication patterns: {dict(self.duplication_stats['duplication_patterns'])}")
        print(f"\nHigh-quality segments (score >= 0.7): {len(high_quality_segments)}")
        print(f"High-quality merged chunks (score >= 0.7): {len(high_quality_chunks)}")
        
        # Show top high-quality chunks
        if high_quality_chunks:
            print(f"\nTop {min(5, len(high_quality_chunks))} highest quality chunks:")
            for i, chunk in enumerate(high_quality_chunks[:5], 1):
                print(f"\n{i}. Chunk {chunk['start_index']}-{chunk['end_index']} (score: {chunk['quality_score']:.2f}):")
                print(f"   Type: {chunk['content_type']}")
                print(f"   Tools: {', '.join(chunk['mentioned_tools']) if chunk['mentioned_tools'] else 'None'}")
                print(f"   Segments merged: {chunk['segment_count']}")
                print(f"   Text preview: {chunk['text'][:150]}...")
                if chunk['key_points']:
                    print(f"   Key points:")
                    for j, point in enumerate(chunk['key_points'][:3], 1):
                        print(f"      {j}. {point}")
        
        # Save results
        output_data = {
            'metadata': {
                'original_file': input_file,
                'total_segments': len(segments),
                'cleaned_segments': len(cleaned_segments),
                'merged_chunks': len(merged_chunks),
                'high_quality_segments': len(high_quality_segments),
                'high_quality_chunks': len(high_quality_chunks),
                'duplication_stats': self.duplication_stats
            },
            'segments': [seg.to_dict() for seg in cleaned_segments],
            'merged_chunks': merged_chunks
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nEnhanced cleaned transcript saved to {output_file}")
        
        # Generate quality report
        quality_distribution = Counter()
        for seg in cleaned_segments:
            bucket = int(seg.quality_score * 10) / 10
            quality_distribution[bucket] += 1
        
        print("\nSegment quality score distribution:")
        for score in sorted(quality_distribution.keys()):
            count = quality_distribution[score]
            bar = '█' * min(50, int(count / 5))
            print(f"  {score:.1f}: {bar} ({count} segments)")
        
        # Chunk quality distribution
        chunk_quality_dist = Counter()
        for chunk in merged_chunks:
            bucket = int(chunk['quality_score'] * 10) / 10
            chunk_quality_dist[bucket] += 1
        
        print("\nMerged chunk quality score distribution:")
        for score in sorted(chunk_quality_dist.keys()):
            count = chunk_quality_dist[score]
            bar = '█' * min(50, count * 2)
            print(f"  {score:.1f}: {bar} ({count} chunks)")


def main():
    """Main function"""
    deduplicator = EnhancedTranscriptDeduplicator()
    deduplicator.process_transcript(
        'transcript_cleaned.json',
        'transcript_enhanced_dedup.json'
    )


if __name__ == '__main__':
    main()