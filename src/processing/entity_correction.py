"""
Entity correction system for AI Knowledge Base.

This module corrects transcription errors in tool names using fuzzy matching,
addressing the core problem described in the PRD where tools like "n8n" become
"mate and" in transcriptions.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel
from rapidfuzz import fuzz, process


class EntityPattern(BaseModel):
    """A pattern for matching and correcting entity names."""
    canonical_name: str
    aliases: List[str]
    common_errors: List[str]
    patterns: List[str]  # Regex patterns for detection
    category: str
    confidence_threshold: float = 80.0


class CorrectionResult(BaseModel):
    """Result of entity correction."""
    original_text: str
    corrected_text: str
    detected_entities: List[Dict[str, Any]]
    confidence_score: float
    corrections_made: int


class EntityCorrector:
    """Corrects transcription errors in tool names and entities."""
    
    def __init__(self):
        """Initialize the entity corrector with predefined patterns."""
        self.patterns = self._load_entity_patterns()
        self.entity_lookup = self._build_entity_lookup()
        
    def _load_entity_patterns(self) -> List[EntityPattern]:
        """Load entity patterns for AI tools and common transcription errors."""
        return [
            # Automation Tools
            EntityPattern(
                canonical_name="n8n",
                aliases=["n8n", "n8n.io", "n8n workflow"],
                common_errors=["mate and", "n and n", "n eight n", "n-8-n", "n ate n"],
                patterns=[
                    r"\bmate\s+and\b",
                    r"\bn\s+and\s+n\b",
                    r"\bn\s+eight\s+n\b",
                    r"\bn[-_]8[-_]n\b",
                    r"\bn\s+ate\s+n\b"
                ],
                category="automation",
                confidence_threshold=75.0
            ),
            EntityPattern(
                canonical_name="Make.com",
                aliases=["Make.com", "Make", "Integromat"],
                common_errors=["make", "make dot com", "make com"],
                patterns=[
                    r"\bmake\s+dot\s+com\b",
                    r"\bmake\s+com\b",
                    r"\bintegromat\b"
                ],
                category="automation",
                confidence_threshold=85.0
            ),
            EntityPattern(
                canonical_name="Zapier",
                aliases=["Zapier", "Zapier.com"],
                common_errors=["zap pier", "zap year", "zapier"],
                patterns=[
                    r"\bzap\s+pier\b",
                    r"\bzap\s+year\b"
                ],
                category="automation",
                confidence_threshold=85.0
            ),
            
            # AI Development Tools
            EntityPattern(
                canonical_name="Cursor",
                aliases=["Cursor", "Cursor AI", "Cursor IDE"],
                common_errors=["curser", "cursor ai", "cursor ide"],
                patterns=[
                    r"\bcurser\b",
                    r"\bcursor\s+ai\b",
                    r"\bcursor\s+ide\b"
                ],
                category="development",
                confidence_threshold=90.0
            ),
            EntityPattern(
                canonical_name="Claude",
                aliases=["Claude", "Claude AI", "Anthropic Claude"],
                common_errors=["claud", "claude ai", "cloud"],
                patterns=[
                    r"\bclaud\b(?!\s+e)",
                    r"\bcloud\b(?=\s+ai)",
                    r"\banthropik\b"
                ],
                category="ai_model",
                confidence_threshold=85.0
            ),
            EntityPattern(
                canonical_name="v0",
                aliases=["v0", "v0.dev", "Vercel v0"],
                common_errors=["v zero", "v0 dev", "the zero", "vee zero"],
                patterns=[
                    r"\bv\s+zero\b",
                    r"\bthe\s+zero\b",
                    r"\bvee\s+zero\b",
                    r"\bv0\s+dev\b"
                ],
                category="development",
                confidence_threshold=80.0
            ),
            
            # Business Tools
            EntityPattern(
                canonical_name="Notion",
                aliases=["Notion", "Notion.so"],
                common_errors=["notion so", "notion dot so"],
                patterns=[
                    r"\bnotion\s+so\b",
                    r"\bnotion\s+dot\s+so\b"
                ],
                category="productivity",
                confidence_threshold=90.0
            ),
            EntityPattern(
                canonical_name="Airtable",
                aliases=["Airtable", "Air table"],
                common_errors=["air table", "airtable"],
                patterns=[
                    r"\bair\s+table\b"
                ],
                category="database",
                confidence_threshold=85.0
            ),
            
            # AI Models and Services
            EntityPattern(
                canonical_name="ChatGPT",
                aliases=["ChatGPT", "Chat GPT", "OpenAI GPT"],
                common_errors=["chat gpt", "chat g p t", "chatgpt"],
                patterns=[
                    r"\bchat\s+g\s+p\s+t\b",
                    r"\bchat\s+gpt\b"
                ],
                category="ai_model",
                confidence_threshold=85.0
            ),
            EntityPattern(
                canonical_name="OpenAI",
                aliases=["OpenAI", "Open AI"],
                common_errors=["open ai", "open a i"],
                patterns=[
                    r"\bopen\s+ai\b",
                    r"\bopen\s+a\s+i\b"
                ],
                category="ai_company",
                confidence_threshold=85.0
            ),
        ]
    
    def _build_entity_lookup(self) -> Dict[str, EntityPattern]:
        """Build a lookup dictionary for fast entity matching."""
        lookup = {}
        for pattern in self.patterns:
            # Add canonical name
            lookup[pattern.canonical_name.lower()] = pattern
            
            # Add aliases
            for alias in pattern.aliases:
                lookup[alias.lower()] = pattern
                
            # Add common errors
            for error in pattern.common_errors:
                lookup[error.lower()] = pattern
                
        return lookup
    
    def correct_text(self, text: str) -> CorrectionResult:
        """Correct entity names in the given text."""
        original_text = text
        corrected_text = text
        detected_entities = []
        corrections_made = 0
        
        # First pass: Pattern-based corrections
        for pattern in self.patterns:
            for regex_pattern in pattern.patterns:
                matches = re.finditer(regex_pattern, corrected_text, re.IGNORECASE)
                for match in matches:
                    matched_text = match.group()
                    
                    # Replace with canonical name
                    corrected_text = corrected_text.replace(matched_text, pattern.canonical_name)
                    corrections_made += 1
                    
                    detected_entities.append({
                        'original': matched_text,
                        'corrected': pattern.canonical_name,
                        'category': pattern.category,
                        'confidence': pattern.confidence_threshold,
                        'method': 'pattern'
                    })
        
        # Second pass: Fuzzy matching for missed entities
        words = corrected_text.split()
        corrected_words = []
        
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            
            # Skip very short words
            if len(clean_word) < 3:
                corrected_words.append(word)
                continue
            
            # Check if word needs correction
            best_match = self._find_best_match(clean_word)
            if best_match:
                entity_pattern, confidence = best_match
                if confidence >= entity_pattern.confidence_threshold:
                    corrected_words.append(entity_pattern.canonical_name)
                    corrections_made += 1
                    
                    detected_entities.append({
                        'original': word,
                        'corrected': entity_pattern.canonical_name,
                        'category': entity_pattern.category,
                        'confidence': confidence,
                        'method': 'fuzzy'
                    })
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        
        # Reconstruct text if fuzzy matching made changes
        if corrections_made > len([e for e in detected_entities if e['method'] == 'pattern']):
            corrected_text = ' '.join(corrected_words)
        
        # Calculate overall confidence
        if detected_entities:
            confidence_score = sum(e['confidence'] for e in detected_entities) / len(detected_entities)
        else:
            confidence_score = 100.0
        
        return CorrectionResult(
            original_text=original_text,
            corrected_text=corrected_text,
            detected_entities=detected_entities,
            confidence_score=confidence_score,
            corrections_made=corrections_made
        )
    
    def _find_best_match(self, word: str) -> Optional[Tuple[EntityPattern, float]]:
        """Find the best matching entity pattern for a word."""
        best_match = None
        best_score = 0
        
        for entity_name, pattern in self.entity_lookup.items():
            # Check exact match first
            if word == entity_name:
                return pattern, 100.0
            
            # Check fuzzy match
            score = fuzz.ratio(word, entity_name)
            if score > best_score and score >= pattern.confidence_threshold:
                best_match = (pattern, score)
                best_score = score
        
        return best_match
    
    def get_entity_suggestions(self, text: str) -> List[Dict[str, Any]]:
        """Get entity suggestions for a given text without correcting."""
        suggestions = []
        
        # Check for potential matches
        words = re.findall(r'\b\w+\b', text.lower())
        
        for word in words:
            if len(word) < 3:
                continue
                
            matches = process.extract(word, self.entity_lookup.keys(), limit=3)
            
            for match, score in matches:
                if score >= 70:  # Lower threshold for suggestions
                    pattern = self.entity_lookup[match]
                    suggestions.append({
                        'original': word,
                        'suggested': pattern.canonical_name,
                        'category': pattern.category,
                        'confidence': score,
                        'aliases': pattern.aliases
                    })
        
        return suggestions
    
    def add_custom_pattern(self, pattern: EntityPattern):
        """Add a custom entity pattern."""
        self.patterns.append(pattern)
        
        # Update lookup
        self.entity_lookup[pattern.canonical_name.lower()] = pattern
        for alias in pattern.aliases:
            self.entity_lookup[alias.lower()] = pattern
        for error in pattern.common_errors:
            self.entity_lookup[error.lower()] = pattern


def main():
    """Test the entity correction system."""
    corrector = EntityCorrector()
    
    # Test cases from the PRD
    test_cases = [
        "So I'm using mate and for my automation workflow",
        "Make sure to set up your curser IDE properly",
        "The zero is great for rapid prototyping",
        "I built this with make dot com integration",
        "Chat GPT helped me write this code",
        "You can connect this to notion so easily",
        "Zap pier is another automation tool",
        "Open AI released a new model",
        "This integrates with air table perfectly"
    ]
    
    print("🔧 Testing AI Entity Correction System")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Original: {test_case}")
        
        result = corrector.correct_text(test_case)
        
        print(f"   Corrected: {result.corrected_text}")
        print(f"   Confidence: {result.confidence_score:.1f}%")
        print(f"   Corrections: {result.corrections_made}")
        
        if result.detected_entities:
            print("   Detected entities:")
            for entity in result.detected_entities:
                print(f"     - {entity['original']} → {entity['corrected']} "
                      f"({entity['category']}, {entity['confidence']:.1f}%)")
    
    print("\n" + "=" * 50)
    print("✅ Entity correction testing completed")


if __name__ == "__main__":
    main()