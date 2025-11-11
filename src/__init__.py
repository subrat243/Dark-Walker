"""
__init__ file for src package
"""

from src.config import get_config, Config
from src.logger import get_logger
from src.pattern_scanner import PatternScanner, ScanResult
from src.dark_web_crawler import DarkWebCrawler
from src.monitor import DarkWebMonitor
from src.cli import DarkWebCLI

__version__ = "1.0.0"
__author__ = "Dark-Walker Team"
__all__ = [
    'get_config',
    'Config',
    'get_logger',
    'PatternScanner',
    'ScanResult',
    'DarkWebCrawler',
    'DarkWebMonitor',
    'DarkWebCLI',
]
