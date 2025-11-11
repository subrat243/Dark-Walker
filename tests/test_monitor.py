"""
Unit tests for the Dark Web Monitoring Tool
"""

import unittest
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pattern_scanner import PatternScanner, ScanResult
from dark_web_crawler import DarkWebCrawler


class TestPatternScanner(unittest.TestCase):
    """Test cases for PatternScanner"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scanner = PatternScanner()
    
    def test_email_pattern(self):
        """Test email pattern matching"""
        text = "Contact us at support@example.com"
        results = self.scanner.scan_text(text, "test_url")
        
        self.assertTrue(any(r.pattern == 'email' for r in results))
    
    def test_bitcoin_pattern(self):
        """Test bitcoin address pattern"""
        text = "Send payment to 1A1z7agoat2aZS8mkCvhQiiZwKHhzUUVLt"
        results = self.scanner.scan_text(text, "test_url")
        
        self.assertTrue(len(results) > 0)
    
    def test_ip_address_pattern(self):
        """Test IP address pattern"""
        text = "Server IP: 192.168.1.1"
        results = self.scanner.scan_text(text, "test_url")
        
        self.assertTrue(any(r.pattern == 'ip_address' for r in results))
    
    def test_url_pattern(self):
        """Test URL pattern"""
        text = "Visit https://www.example.com for more info"
        results = self.scanner.scan_text(text, "test_url")
        
        self.assertTrue(any(r.pattern == 'url' for r in results))
    
    def test_ssn_pattern(self):
        """Test SSN pattern"""
        text = "SSN: 123-45-6789"
        results = self.scanner.scan_text(text, "test_url")
        
        self.assertTrue(any(r.pattern == 'ssn' for r in results))
    
    def test_custom_pattern(self):
        """Test adding custom pattern"""
        self.scanner.add_custom_pattern(r'\b(password|passwd)\b', 'password')
        
        text = "Please enter your password"
        results = self.scanner.scan_text(text, "test_url")
        
        self.assertTrue(any(r.pattern == 'password' for r in results))
    
    def test_invalid_pattern(self):
        """Test invalid regex pattern"""
        with self.assertRaises(ValueError):
            self.scanner.add_custom_pattern(r'(invalid[', 'bad_pattern')
    
    def test_scan_result_to_dict(self):
        """Test ScanResult conversion to dictionary"""
        result = ScanResult(
            pattern='test',
            matched_text='test_text',
            source_url='http://test.onion',
            context='test context',
            timestamp=datetime.now().isoformat(),
        )
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['pattern'], 'test')
        self.assertEqual(result_dict['matched_text'], 'test_text')
        self.assertEqual(result_dict['source_url'], 'http://test.onion')


class TestDarkWebCrawler(unittest.TestCase):
    """Test cases for DarkWebCrawler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.crawler = DarkWebCrawler(use_tor=False)
    
    def test_crawler_initialization(self):
        """Test crawler initialization"""
        self.assertIsNotNone(self.crawler.session)
        self.assertEqual(len(self.crawler.visited_urls), 0)
    
    def test_visited_urls_tracking(self):
        """Test visited URLs tracking"""
        # Note: This is a mock test without actual network calls
        self.crawler.visited_urls.append('http://test.onion')
        
        self.assertEqual(len(self.crawler.visited_urls), 1)
        self.assertIn('http://test.onion', self.crawler.visited_urls)
    
    def test_clear_visited(self):
        """Test clearing visited URLs"""
        self.crawler.visited_urls.append('http://test.onion')
        self.crawler.clear_visited()
        
        self.assertEqual(len(self.crawler.visited_urls), 0)
    
    def test_extract_onion_links(self):
        """Test extracting onion links"""
        html = """
        <a href="http://example.onion">Link 1</a>
        <a href="http://test.onion">Link 2</a>
        <a href="http://regular.com">Link 3</a>
        """
        
        links = self.crawler.extract_onion_links(html)
        
        self.assertEqual(len(links), 2)
        self.assertTrue(all('.onion' in link for link in links))


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_scanner_with_multiple_patterns(self):
        """Test scanner with multiple pattern types"""
        scanner = PatternScanner()
        
        text = """
        Contact: support@example.com
        IP: 192.168.1.1
        URL: https://www.example.com
        Bitcoin: 1A1z7agoat2aZS8mkCvhQiiZwKHhzUUVLt
        SSN: 123-45-6789
        """
        
        results = scanner.scan_text(text, "test_source")
        
        # Should find multiple patterns
        self.assertTrue(len(results) > 0)
        
        # Check for specific patterns
        patterns_found = set(r.pattern for r in results)
        self.assertTrue(len(patterns_found) > 1)


if __name__ == '__main__':
    unittest.main()
