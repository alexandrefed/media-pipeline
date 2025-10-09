"""
Adaptive Video Processor with Learning Capabilities
Processes YouTube videos while learning and improving from each one.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any
import tiktoken
from pathlib import Path


class AdaptiveVideoProcessor:
    """Processes videos with continuous learning and improvement."""
    
    def __init__(self):
        self.kb_path = Path("processing_knowledge_base.json")
        self.history_path = Path("processing_history.md")
        self.knowledge_base = self.load_knowledge_base()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def load_knowledge_base(self) -> Dict:
        """Load the knowledge base or create if doesn't exist."""
        if self.kb_path.exists():
            with open(self.kb_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_knowledge_base(self):
        """Save updated knowledge base."""
        self.knowledge_base['metadata']['last_updated'] = datetime.now().isoformat()
        with open(self.kb_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def apply_learned_corrections(self, text: str) -> Tuple[str, List[str]]:
        """Apply corrections from knowledge base with tracking."""
        corrections_made = []
        
        # Apply common error corrections
        for error, correction in self.knowledge_base['transcription_corrections']['common_errors'].items():
            if error in text.lower():
                # Case-insensitive replacement preserving original case where possible
                pattern = re.compile(re.escape(error), re.IGNORECASE)
                occurrences = len(pattern.findall(text))
                if occurrences > 0:
                    text = pattern.sub(correction, text)
                    corrections_made.append(f"'{error}' → '{correction}' ({occurrences} times)")
        
        # Apply contextual corrections
        for context, corrections in self.knowledge_base['transcription_corrections']['contextual_corrections'].items():
            for error, correction in corrections.items():
                if context == "followed_by_code" and f"{error} code" in text.lower():
                    text = re.sub(f"{error}\\s+code", f"{correction} Code", text, flags=re.IGNORECASE)
                    corrections_made.append(f"'{error} code' → '{correction} Code' (contextual)")
        
        return text, corrections_made
    
    def suggest_chunk_boundaries(self, text: str) -> List[Dict[str, Any]]:
        """Suggest chunk boundaries based on learned patterns."""
        suggestions = []
        
        # Find transition phrases
        for phrase in self.knowledge_base['chunk_patterns']['topic_transitions']:
            matches = list(re.finditer(phrase, text, re.IGNORECASE))
            for match in matches:
                suggestions.append({
                    'position': match.start(),
                    'type': 'transition',
                    'phrase': phrase,
                    'confidence': 0.8
                })
        
        # Find section indicators
        for indicator in self.knowledge_base['chunk_patterns']['section_indicators']:
            matches = list(re.finditer(f"\\b{indicator}\\b", text, re.IGNORECASE))
            for match in matches:
                suggestions.append({
                    'position': match.start(),
                    'type': 'section',
                    'phrase': indicator,
                    'confidence': 0.9
                })
        
        # Sort by position
        suggestions.sort(key=lambda x: x['position'])
        return suggestions
    
    def analyze_video_content(self, text: str, metadata: Dict) -> Dict[str, Any]:
        """Analyze video content and suggest processing approach."""
        analysis = {
            'estimated_content_type': self.detect_content_type(text),
            'detected_topics': self.detect_topics(text),
            'suggested_chunk_size': None,
            'confidence_level': 0.0,
            'similar_videos': []
        }
        
        # Determine optimal chunk size based on content type
        content_type = analysis['estimated_content_type']
        if content_type in self.knowledge_base['chunk_patterns']['optimal_sizes']:
            size_config = self.knowledge_base['chunk_patterns']['optimal_sizes'][content_type]
            analysis['suggested_chunk_size'] = size_config
            analysis['confidence_level'] = 0.85
        
        # Find similar videos in history
        # This would compare topics, channel, duration, etc.
        
        return analysis
    
    def detect_content_type(self, text: str) -> str:
        """Detect the type of content (tutorial, explanation, etc.)."""
        text_lower = text.lower()
        
        # Count indicators
        code_indicators = len(re.findall(r'(function|const|let|var|import|class|def|if|for|while)', text_lower))
        tutorial_indicators = len(re.findall(r'(let me show|check this out|example|demo|step \d+|first|second|finally)', text_lower))
        conceptual_indicators = len(re.findall(r'(concept|theory|understanding|principle|philosophy|approach)', text_lower))
        
        # Determine type based on indicators
        if code_indicators > 20:
            return 'code_walkthrough'
        elif tutorial_indicators > conceptual_indicators:
            return 'technical_tutorial'
        else:
            return 'conceptual_explanation'
    
    def detect_topics(self, text: str) -> List[str]:
        """Detect main topics discussed in the video."""
        topics = []
        
        # Check for known technical terms
        for category, terms in self.knowledge_base['transcription_corrections']['technical_terms'].items():
            for term in terms:
                if term.lower() in text.lower():
                    topics.append(term)
        
        return list(set(topics))  # Remove duplicates
    
    def generate_enhancement_suggestions(self, text: str, corrections_made: List[str]) -> Dict[str, Any]:
        """Generate suggestions for manual enhancement."""
        suggestions = {
            'auto_corrections_applied': corrections_made,
            'potential_corrections': [],
            'chunk_boundary_suggestions': self.suggest_chunk_boundaries(text),
            'quality_notes': []
        }
        
        # Find potential corrections that need human review
        # Look for patterns that might be errors
        potential_errors = [
            (r'\b[a-z]+ ai\b', 'Possible AI tool name that should be capitalized'),
            (r'\b[a-z]+ code\b', 'Possible tool name that should be capitalized'),
            (r'\bzero\b', 'Might be "v0" in context'),
            (r'\bmake\.com\b', 'Should be "Make.com"'),
        ]
        
        for pattern, note in potential_errors:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context = text[max(0, match.start()-30):min(len(text), match.end()+30)]
                suggestions['potential_corrections'].append({
                    'text': match.group(),
                    'position': match.start(),
                    'note': note,
                    'context': context
                })
        
        # Add quality notes
        word_count = len(text.split())
        if word_count < 1000:
            suggestions['quality_notes'].append("Short transcript - might benefit from more detailed chunks")
        
        return suggestions
    
    def update_knowledge_base(self, learnings: Dict[str, Any]):
        """Update knowledge base with new learnings."""
        # Update transcription corrections
        if 'new_corrections' in learnings:
            for error, correction in learnings['new_corrections'].items():
                self.knowledge_base['transcription_corrections']['common_errors'][error] = correction
        
        # Update chunk patterns
        if 'new_transitions' in learnings:
            for phrase in learnings['new_transitions']:
                if phrase not in self.knowledge_base['chunk_patterns']['topic_transitions']:
                    self.knowledge_base['chunk_patterns']['topic_transitions'].append(phrase)
        
        # Update statistics
        self.knowledge_base['metadata']['total_videos_processed'] += 1
        
        # Save updated knowledge base
        self.save_knowledge_base()
    
    def generate_processing_report(self, video_url: str, results: Dict) -> str:
        """Generate a processing report for documentation."""
        report = f"""
## Video Processing Report

**URL**: {video_url}
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Auto-Corrections Applied
{chr(10).join(f'- {c}' for c in results.get('corrections_made', []))}

### Content Analysis
- **Type**: {results.get('content_type', 'Unknown')}
- **Topics**: {', '.join(results.get('topics', []))}
- **Suggested Chunk Size**: {results.get('chunk_size', 'Default')}

### Enhancement Suggestions
{chr(10).join(f'- {s}' for s in results.get('suggestions', []))}

### Quality Notes
{chr(10).join(f'- {n}' for n in results.get('quality_notes', []))}
"""
        return report


def main():
    """Example usage of the adaptive processor."""
    processor = AdaptiveVideoProcessor()
    
    # Example: Process a transcript with learning
    sample_text = """
    So today we're going to talk about clawed code and how it integrates with mate and.
    Let me show you how to use zero for rapid prototyping. Check this out - 
    when you're using curser as your IDE, you can leverage the power of these AI tools.
    """
    
    # Apply learned corrections
    corrected_text, corrections = processor.apply_learned_corrections(sample_text)
    print(f"Corrections applied: {len(corrections)}")
    for c in corrections:
        print(f"  - {c}")
    
    # Analyze content
    analysis = processor.analyze_video_content(corrected_text, {})
    print(f"\nContent type: {analysis['estimated_content_type']}")
    print(f"Topics detected: {', '.join(analysis['detected_topics'])}")
    
    # Generate suggestions
    suggestions = processor.generate_enhancement_suggestions(corrected_text, corrections)
    print(f"\nChunk boundary suggestions: {len(suggestions['chunk_boundary_suggestions'])}")
    print(f"Potential corrections to review: {len(suggestions['potential_corrections'])}")


if __name__ == "__main__":
    main()