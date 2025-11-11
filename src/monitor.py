"""
Monitor module
Main monitoring orchestration and scheduling
"""

import os
import json
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
from dark_web_crawler import DarkWebCrawler
from pattern_scanner import PatternScanner, ScanResult
from config import get_config
from logger import get_logger


class DarkWebMonitor:
    """Main dark web monitoring orchestrator"""
    
    def __init__(self, search_patterns: List[str] = None):
        """Initialize monitor"""
        self.config = get_config()
        self.logger = get_logger()
        self.crawler = DarkWebCrawler(use_tor=self.config.TOR_ENABLED)
        self.scanner = PatternScanner(patterns=search_patterns)
        self.results: List[ScanResult] = []
        self._ensure_results_dir()
    
    def _ensure_results_dir(self):
        """Ensure results directory exists"""
        os.makedirs(self.config.RESULTS_DIR, exist_ok=True)
    
    def monitor_dark_web(self, search_query: str = None, 
                        search_engines: List[str] = None) -> Dict:
        """Monitor dark web for patterns"""
        self.logger.info("Starting dark web monitoring")
        
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'search_query': search_query,
            'search_engines': search_engines or list(self.config.DARK_WEB_SEARCH_ENGINES.keys()),
            'findings': [],
            'statistics': {
                'urls_crawled': 0,
                'patterns_found': 0,
                'errors': 0
            }
        }
        
        # Crawl Hidden Wiki
        if search_query or not search_engines:
            self.logger.info("Crawling Hidden Wiki")
            wiki_content = self.crawler.crawl_hidden_wiki()
            
            for wiki_name, content in wiki_content.items():
                if content:
                    scan_results = self.scanner.scan_text(content, f"hidden_wiki:{wiki_name}")
                    if scan_results:
                        monitoring_results['findings'].extend(
                            [r.to_dict() for r in scan_results]
                        )
                        monitoring_results['statistics']['patterns_found'] += len(scan_results)
        
        # Search dark web search engines
        engines_to_search = search_engines or list(self.config.DARK_WEB_SEARCH_ENGINES.keys())
        query = search_query or ' '.join(self.config.MONITORED_PATTERNS)
        
        for engine in engines_to_search:
            try:
                self.logger.info(f"Searching {engine}")
                search_results = self.crawler.search_dark_web(query, engine)
                
                if search_results.get('status') == 'success':
                    content = search_results.get('results', {}).get('text', '')
                    if content:
                        scan_results = self.scanner.scan_text(
                            content, 
                            f"search:{engine}:{query}"
                        )
                        if scan_results:
                            monitoring_results['findings'].extend(
                                [r.to_dict() for r in scan_results]
                            )
                            monitoring_results['statistics']['patterns_found'] += len(scan_results)
            except Exception as e:
                self.logger.error(f"Error searching {engine}: {str(e)}")
                monitoring_results['statistics']['errors'] += 1
        
        monitoring_results['statistics']['urls_crawled'] = len(self.crawler.get_visited_urls())
        
        self.logger.info(
            f"Monitoring complete. Found {monitoring_results['statistics']['patterns_found']} patterns"
        )
        
        return monitoring_results
    
    def monitor_specific_site(self, url: str) -> Dict:
        """Monitor a specific onion site"""
        self.logger.info(f"Monitoring specific site: {url}")
        
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'findings': [],
            'status': 'unknown'
        }
        
        try:
            content = self.crawler.fetch_url(url)
            
            if content:
                scan_results = self.scanner.scan_text(content, url)
                results['findings'] = [r.to_dict() for r in scan_results]
                results['status'] = 'success'
                self.logger.info(f"Found {len(scan_results)} patterns on {url}")
            else:
                results['status'] = 'failed'
                self.logger.warning(f"Failed to fetch content from {url}")
        
        except Exception as e:
            self.logger.error(f"Error monitoring {url}: {str(e)}")
            results['status'] = 'error'
            results['error'] = str(e)
        
        return results
    
    def save_results(self, results: Dict, filename: Optional[str] = None) -> str:
        """Save monitoring results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitor_{timestamp}"
        
        file_path = os.path.join(self.config.RESULTS_DIR, filename)
        
        try:
            if self.config.EXPORT_FORMAT == 'json':
                file_path += '.json'
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=2)
            
            elif self.config.EXPORT_FORMAT == 'csv':
                file_path += '.csv'
                self._save_as_csv(results, file_path)
            
            else:  # txt
                file_path += '.txt'
                self._save_as_txt(results, file_path)
            
            self.logger.info(f"Results saved to {file_path}")
            return file_path
        
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise
    
    def _save_as_csv(self, results: Dict, file_path: str):
        """Save results as CSV"""
        import csv
        
        findings = results.get('findings', [])
        
        if not findings:
            # Write empty file
            open(file_path, 'w').close()
            return
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=findings[0].keys())
            writer.writeheader()
            writer.writerows(findings)
    
    def _save_as_txt(self, results: Dict, file_path: str):
        """Save results as plain text"""
        with open(file_path, 'w') as f:
            f.write("=== Dark Web Monitoring Results ===\n\n")
            f.write(f"Timestamp: {results.get('timestamp')}\n")
            f.write(f"Search Query: {results.get('search_query')}\n\n")
            
            if 'statistics' in results:
                f.write("=== Statistics ===\n")
                for key, value in results['statistics'].items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")
            
            findings = results.get('findings', [])
            f.write(f"=== Findings ({len(findings)} total) ===\n\n")
            
            for i, finding in enumerate(findings, 1):
                f.write(f"{i}. Pattern: {finding.get('pattern')}\n")
                f.write(f"   Matched Text: {finding.get('matched_text')}\n")
                f.write(f"   Source: {finding.get('source_url')}\n")
                f.write(f"   Context: {finding.get('context')[:100]}...\n")
                f.write(f"   Timestamp: {finding.get('timestamp')}\n\n")
    
    def get_results(self) -> List[Dict]:
        """Get current scan results"""
        return [r.to_dict() for r in self.results]
    
    def clear_results(self):
        """Clear results"""
        self.results = []
        self.logger.info("Cleared scan results")
    
    def add_search_pattern(self, pattern: str, name: Optional[str] = None):
        """Add a custom search pattern"""
        self.scanner.add_custom_pattern(pattern, name)
    
    def get_search_patterns(self) -> List[str]:
        """Get all search patterns"""
        return self.scanner.get_patterns()
