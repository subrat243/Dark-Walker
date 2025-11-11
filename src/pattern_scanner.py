"""
Pattern Scanner module
Handles pattern matching and string scanning operations
"""

import re
from typing import List, Dict, Optional, Pattern
from dataclasses import dataclass, asdict
from logger import get_logger

@dataclass
class ScanResult:
    """Result of a pattern scan"""
    pattern: str
    matched_text: str
    source_url: str
    context: str
    timestamp: str
    confidence: float = 1.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


class PatternScanner:
    """Scans text content for patterns and keywords"""
    
    def __init__(self, patterns: List[str] = None):
        """Initialize scanner with patterns"""
        self.logger = get_logger()
        self.patterns: Dict[str, Pattern] = {}
        self.custom_patterns: List[str] = patterns or []
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns"""
        # Default critical patterns
        critical_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'bitcoin': r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}',
            'ip_address': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
            'credit_card': r'\b(?:\d[ -]*?){13,19}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'api_key': r'(?i)(api[_-]?key|token|secret)["\']?\s*[:=]\s*["\']?[a-zA-Z0-9\-_]{20,}',
        }
        
        # Add custom patterns
        for pattern_str in self.custom_patterns:
            try:
                self.patterns[pattern_str] = re.compile(pattern_str, re.IGNORECASE)
            except re.error as e:
                self.logger.warning(f"Invalid regex pattern '{pattern_str}': {str(e)}")
        
        # Add critical patterns
        for name, pattern_str in critical_patterns.items():
            try:
                self.patterns[name] = re.compile(pattern_str, re.IGNORECASE)
            except re.error as e:
                self.logger.error(f"Failed to compile critical pattern '{name}': {str(e)}")
    
    def scan_text(self, text: str, source_url: str, context_length: int = 100) -> List[ScanResult]:
        """Scan text for patterns"""
        results: List[ScanResult] = []
        
        if not text:
            return results
        
        for pattern_name, pattern_regex in self.patterns.items():
            matches = pattern_regex.finditer(text)
            
            for match in matches:
                start_pos = max(0, match.start() - context_length)
                end_pos = min(len(text), match.end() + context_length)
                context = text[start_pos:end_pos].strip()
                
                result = ScanResult(
                    pattern=pattern_name,
                    matched_text=match.group(),
                    source_url=source_url,
                    context=context,
                    timestamp=self._get_timestamp(),
                    confidence=1.0
                )
                results.append(result)
                self.logger.debug(f"Pattern '{pattern_name}' matched in {source_url}")
        
        return results
    
    def scan_multiple(self, text_blocks: Dict[str, str]) -> Dict[str, List[ScanResult]]:
        """Scan multiple text blocks"""
        all_results: Dict[str, List[ScanResult]] = {}
        
        for source_url, text in text_blocks.items():
            results = self.scan_text(text, source_url)
            if results:
                all_results[source_url] = results
        
        return all_results
    
    def add_custom_pattern(self, pattern: str, name: Optional[str] = None):
        """Add a custom regex pattern"""
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            pattern_name = name or f"custom_{len(self.patterns)}"
            self.patterns[pattern_name] = compiled_pattern
            self.logger.info(f"Added custom pattern '{pattern_name}'")
        except re.error as e:
            self.logger.error(f"Invalid regex pattern: {str(e)}")
            raise ValueError(f"Invalid regex pattern: {str(e)}")
    
    def remove_pattern(self, pattern_name: str):
        """Remove a pattern"""
        if pattern_name in self.patterns:
            del self.patterns[pattern_name]
            self.logger.info(f"Removed pattern '{pattern_name}'")
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_patterns(self) -> Dict[str, str]:
        """Get all pattern names"""
        return list(self.patterns.keys())
