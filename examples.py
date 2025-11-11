"""
Example usage of Dark Web Monitoring Tool
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from monitor import DarkWebMonitor
from pattern_scanner import PatternScanner


def example_1_basic_pattern_scanning():
    """Example 1: Basic pattern scanning"""
    print("=" * 60)
    print("Example 1: Basic Pattern Scanning")
    print("=" * 60)
    
    # Create scanner
    scanner = PatternScanner()
    
    # Sample text to scan
    sample_text = """
    For more information, contact us at admin@example.com
    Send payments to Bitcoin wallet: 1A1z7agoat2aZS8mkCvhQiiZwKHhzUUVLt
    Server IP: 192.168.1.1
    Visit https://www.example.com for details
    """
    
    # Scan the text
    results = scanner.scan_text(sample_text, "example_source")
    
    # Display results
    print(f"\nFound {len(results)} patterns:\n")
    for result in results:
        print(f"Pattern: {result.pattern}")
        print(f"Matched: {result.matched_text}")
        print(f"Context: {result.context[:50]}...")
        print("-" * 40)


def example_2_custom_patterns():
    """Example 2: Adding custom patterns"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Pattern Scanning")
    print("=" * 60)
    
    # Create scanner
    scanner = PatternScanner()
    
    # Add custom pattern for passwords
    scanner.add_custom_pattern(
        r'password["\']?\s*[:=]\s*["\']?([^"\';\n]+)',
        'password_detection'
    )
    
    # Sample text with password
    sample_text = 'database_password = "MySecurePassword123"'
    
    # Scan
    results = scanner.scan_text(sample_text, "config_file")
    
    print(f"\nFound {len(results)} patterns:\n")
    for result in results:
        print(f"Pattern: {result.pattern}")
        print(f"Matched: {result.matched_text}")


def example_3_monitoring_initialization():
    """Example 3: Initialize monitoring"""
    print("\n" + "=" * 60)
    print("Example 3: Monitor Initialization")
    print("=" * 60)
    
    # Initialize monitor
    monitor = DarkWebMonitor()
    
    print("\nMonitor initialized successfully!")
    print(f"Available search patterns: {len(monitor.get_search_patterns())}")
    print("Patterns:", monitor.get_search_patterns()[:5], "...")


def example_4_custom_search_patterns():
    """Example 4: Add custom search patterns to monitor"""
    print("\n" + "=" * 60)
    print("Example 4: Custom Search Patterns")
    print("=" * 60)
    
    monitor = DarkWebMonitor()
    
    # Add custom patterns
    patterns = [
        (r'\bdata\s+breach\b', 'data_breach'),
        (r'\bransomware\b', 'ransomware'),
        (r'\bzero-day\b', 'zero_day'),
    ]
    
    for pattern, name in patterns:
        monitor.add_search_pattern(pattern, name)
        print(f"Added pattern: {name}")
    
    print(f"\nTotal patterns: {len(monitor.get_search_patterns())}")


def example_5_results_export():
    """Example 5: Export results in different formats"""
    print("\n" + "=" * 60)
    print("Example 5: Results Export")
    print("=" * 60)
    
    monitor = DarkWebMonitor()
    
    # Sample results
    sample_results = {
        'timestamp': '2024-11-12T10:30:00',
        'search_query': 'example query',
        'findings': [
            {
                'pattern': 'email',
                'matched_text': 'test@example.com',
                'source_url': 'http://example.onion',
                'context': 'Contact: test@example.com',
                'timestamp': '2024-11-12T10:30:00'
            }
        ],
        'statistics': {
            'urls_crawled': 5,
            'patterns_found': 1,
            'errors': 0
        }
    }
    
    # Save results
    file_path = monitor.save_results(sample_results, 'example_results')
    print(f"\nResults saved to: {file_path}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " Dark Web Monitoring Tool - Examples ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        example_1_basic_pattern_scanning()
        example_2_custom_patterns()
        example_3_monitoring_initialization()
        example_4_custom_search_patterns()
        example_5_results_export()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
