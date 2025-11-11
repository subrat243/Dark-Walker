"""
Configuration module for Dark Web Monitoring Tool
Manages all configuration settings and environment variables
"""

import os
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class"""
    
    # Tor Configuration
    TOR_ENABLED = os.getenv('TOR_ENABLED', 'True').lower() == 'true'
    TOR_HOST = os.getenv('TOR_HOST', 'localhost')
    TOR_PORT = int(os.getenv('TOR_PORT', '9050'))
    TOR_CONTROL_PORT = int(os.getenv('TOR_CONTROL_PORT', '9051'))
    TOR_CONTROL_PASSWORD = os.getenv('TOR_CONTROL_PASSWORD', 'password')
    
    # Proxy Configuration
    USE_PROXY = os.getenv('USE_PROXY', 'True').lower() == 'true'
    PROXY_URL = f'socks5://{TOR_HOST}:{TOR_PORT}'
    
    # Request Configuration
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '5'))
    
    # Search Engines (Onion URLs)
    DARK_WEB_SEARCH_ENGINES: Dict[str, str] = {
        'ahmia': 'http://juhanurmihxlp77nfq6owps5p7eixxinewsvyat7yppk5as5rjohnq.onion',
        'torch': 'http://torchdeepdotnqzio3nl.onion',
        'darkweb_link': 'http://darkweblink.onion',
        'notevil': 'http://notevil.onion',
    }
    
    # Hidden Wiki URLs
    HIDDEN_WIKI_URLS: Dict[str, str] = {
        'main': 'http://thehiddenwiki.onion',
        'mirror1': 'http://3g2upl4pq6kufc4m.onion',  # DuckDuckGo
        'mirror2': 'http://zqktlwi4fd.onion',  # The Tor Project
    }
    
    # Monitoring Configuration
    MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', '3600'))  # 1 hour
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/darkweb_monitor.log')
    
    # Patterns and Keywords to Monitor
    MONITORED_PATTERNS: List[str] = [
        'leaked',
        'breach',
        'database',
        'ransomware',
        'exploit',
        'vulnerability',
        'malware',
        'credentials',
        'payment',
        'bitcoin',
    ]
    
    # Output Configuration
    RESULTS_DIR = os.getenv('RESULTS_DIR', './results')
    EXPORT_FORMAT = os.getenv('EXPORT_FORMAT', 'json')  # json, csv, txt
    
    # User Agent
    USER_AGENTS: List[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    ]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TOR_ENABLED = False
    USE_PROXY = False
    LOG_LEVEL = 'DEBUG'


def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('ENVIRONMENT', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)()
