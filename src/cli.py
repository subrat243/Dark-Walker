"""
Command Line Interface for Dark Web Monitoring Tool
Provides user-friendly CLI interface
"""

import argparse
import sys
from typing import Optional, List, Dict
from tabulate import tabulate
from colorama import init, Fore, Back, Style
from monitor import DarkWebMonitor
from config import get_config
from logger import get_logger

# Initialize colorama for Windows compatibility
init(autoreset=True)


class DarkWebCLI:
    """Command line interface for dark web monitoring"""
    
    def __init__(self):
        """Initialize CLI"""
        self.config = get_config()
        self.logger = get_logger()
        self.monitor = None
    
    def print_header(self):
        """Print application header"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}{'  DARK WEB MONITORING TOOL':^60}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Fore.RED}[✗] {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Fore.CYAN}[i] {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
    
    def initialize_monitor(self, patterns: Optional[List[str]] = None):
        """Initialize monitoring tool"""
        try:
            self.monitor = DarkWebMonitor(search_patterns=patterns)
            self.print_success("Monitor initialized successfully")
            return True
        except Exception as e:
            self.print_error(f"Failed to initialize monitor: {str(e)}")
            return False
    
    def monitor_dark_web(self, query: Optional[str] = None, 
                        engines: Optional[List[str]] = None):
        """Monitor dark web for patterns"""
        if not self.monitor:
            self.print_error("Monitor not initialized. Use 'init' command first.")
            return
        
        self.print_info("Starting dark web monitoring...")
        print("This may take several minutes. Please be patient.\n")
        
        try:
            results = self.monitor.monitor_dark_web(
                search_query=query,
                search_engines=engines
            )
            
            self.display_results(results)
            
            # Save results
            file_path = self.monitor.save_results(results)
            self.print_success(f"Results saved to {file_path}")
        
        except Exception as e:
            self.print_error(f"Monitoring failed: {str(e)}")
    
    def monitor_specific_site(self, url: str):
        """Monitor a specific onion site"""
        if not self.monitor:
            self.print_error("Monitor not initialized. Use 'init' command first.")
            return
        
        self.print_info(f"Monitoring {url}...")
        
        try:
            results = self.monitor.monitor_specific_site(url)
            
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"Results for: {url}")
            print(f"Status: {Fore.GREEN if results['status'] == 'success' else Fore.RED}{results['status']}")
            print(f"Timestamp: {results['timestamp']}")
            print(f"{'='*60}{Style.RESET_ALL}\n")
            
            if results.get('findings'):
                self.display_findings(results['findings'])
            else:
                self.print_info("No patterns found")
            
            # Save results
            file_path = self.monitor.save_results(results, f"site_{url.replace('/', '_')}")
            self.print_success(f"Results saved to {file_path}")
        
        except Exception as e:
            self.print_error(f"Error monitoring site: {str(e)}")
    
    def display_results(self, results: Dict):
        """Display monitoring results"""
        stats = results.get('statistics', {})
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Monitoring Results{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Display statistics
        print(f"{Fore.YELLOW}Statistics:{Style.RESET_ALL}")
        stats_data = [
            [f"{Fore.WHITE}URLs Crawled{Style.RESET_ALL}", stats.get('urls_crawled', 0)],
            [f"{Fore.WHITE}Patterns Found{Style.RESET_ALL}", stats.get('patterns_found', 0)],
            [f"{Fore.WHITE}Errors{Style.RESET_ALL}", stats.get('errors', 0)],
        ]
        print(tabulate(stats_data, tablefmt="grid"))
        print()
        
        # Display findings
        findings = results.get('findings', [])
        if findings:
            self.display_findings(findings)
        else:
            self.print_warning("No patterns found in this monitoring session")
    
    def display_findings(self, findings: List[Dict]):
        """Display scan findings"""
        print(f"{Fore.YELLOW}Findings ({len(findings)} total):{Style.RESET_ALL}\n")
        
        table_data = []
        for finding in findings[:20]:  # Display first 20
            table_data.append([
                f"{Fore.MAGENTA}{finding.get('pattern', 'N/A')}{Style.RESET_ALL}",
                finding.get('matched_text', 'N/A')[:30] + '...',
                finding.get('source_url', 'N/A')[:30] + '...',
            ])
        
        headers = [
            f"{Fore.CYAN}Pattern{Style.RESET_ALL}",
            f"{Fore.CYAN}Matched Text{Style.RESET_ALL}",
            f"{Fore.CYAN}Source{Style.RESET_ALL}",
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        if len(findings) > 20:
            self.print_info(f"Showing 20 of {len(findings)} findings")
    
    def list_patterns(self):
        """List all search patterns"""
        if not self.monitor:
            self.print_error("Monitor not initialized.")
            return
        
        patterns = self.monitor.get_search_patterns()
        
        print(f"\n{Fore.CYAN}Search Patterns ({len(patterns)} total):{Style.RESET_ALL}\n")
        
        for i, pattern in enumerate(patterns, 1):
            print(f"{i:2d}. {Fore.MAGENTA}{pattern}{Style.RESET_ALL}")
    
    def add_pattern(self, pattern: str, name: Optional[str] = None):
        """Add a custom pattern"""
        if not self.monitor:
            self.print_error("Monitor not initialized.")
            return
        
        try:
            self.monitor.add_search_pattern(pattern, name)
            self.print_success(f"Pattern added successfully")
        except Exception as e:
            self.print_error(f"Failed to add pattern: {str(e)}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Dark Web Monitoring Tool - Monitor for patterns and keywords'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Initialize command
    subparsers.add_parser('init', help='Initialize the monitoring tool')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor dark web')
    monitor_parser.add_argument('-q', '--query', type=str, help='Search query')
    monitor_parser.add_argument(
        '-e', '--engines', 
        type=str, 
        nargs='+',
        help='Search engines to use (e.g., ahmia torch)'
    )
    
    # Monitor site command
    site_parser = subparsers.add_parser('site', help='Monitor specific onion site')
    site_parser.add_argument('url', type=str, help='Onion site URL')
    
    # Pattern commands
    subparsers.add_parser('patterns', help='List all search patterns')
    pattern_parser = subparsers.add_parser('add-pattern', help='Add custom pattern')
    pattern_parser.add_argument('pattern', type=str, help='Regex pattern')
    pattern_parser.add_argument('-n', '--name', type=str, help='Pattern name')
    
    # Info command
    subparsers.add_parser('info', help='Show configuration info')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = DarkWebCLI()
    cli.print_header()
    
    if args.command == 'init':
        cli.initialize_monitor()
    
    elif args.command == 'monitor':
        if cli.initialize_monitor():
            cli.monitor_dark_web(query=args.query, engines=args.engines)
    
    elif args.command == 'site':
        if cli.initialize_monitor():
            cli.monitor_specific_site(args.url)
    
    elif args.command == 'patterns':
        cli.initialize_monitor()
        cli.list_patterns()
    
    elif args.command == 'add-pattern':
        cli.initialize_monitor()
        cli.add_pattern(args.pattern, args.name)
    
    elif args.command == 'info':
        cli.print_info("Configuration Information:")
        print(f"  TOR Enabled: {cli.config.TOR_ENABLED}")
        print(f"  TOR Host: {cli.config.TOR_HOST}:{cli.config.TOR_PORT}")
        print(f"  Search Engines: {', '.join(cli.config.DARK_WEB_SEARCH_ENGINES.keys())}")
        print(f"  Results Directory: {cli.config.RESULTS_DIR}")
        print(f"  Export Format: {cli.config.EXPORT_FORMAT}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
