"""
Dark Web Crawler module
Handles crawling and fetching content from dark web sites
"""

import requests
import time
import random
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import get_config
from logger import get_logger

class DarkWebCrawler:
    """Crawls dark web sites and retrieves content"""
    
    def __init__(self, use_tor: bool = True):
        """Initialize crawler"""
        self.config = get_config()
        self.logger = get_logger()
        self.use_tor = use_tor and self.config.TOR_ENABLED
        self.session = self._create_session()
        self.visited_urls: List[str] = []
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()
        
        # Configure proxy if Tor is enabled
        if self.use_tor:
            proxies = {
                'http': self.config.PROXY_URL,
                'https': self.config.PROXY_URL,
            }
            session.proxies.update(proxies)
            self.logger.info(f"Using Tor proxy: {self.config.PROXY_URL}")
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.RETRY_ATTEMPTS,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def fetch_url(self, url: str, timeout: Optional[int] = None) -> Optional[str]:
        """Fetch content from a URL"""
        if url in self.visited_urls:
            self.logger.debug(f"URL already visited: {url}")
            return None
        
        timeout = timeout or self.config.REQUEST_TIMEOUT
        
        try:
            # Random delay to avoid detection
            time.sleep(random.uniform(1, 3))
            
            # Random user agent
            headers = {
                'User-Agent': random.choice(self.config.USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            self.visited_urls.append(url)
            self.logger.info(f"Successfully fetched: {url}")
            
            return response.text
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching {url}: {str(e)}")
            return None
    
    def parse_html(self, html_content: str) -> Dict:
        """Parse HTML content"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            parsed_data = {
                'title': soup.title.string if soup.title else 'No title',
                'text': soup.get_text(),
                'links': [link.get('href') for link in soup.find_all('a', href=True)],
                'paragraphs': [p.get_text() for p in soup.find_all('p')],
                'headings': [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])],
            }
            
            return parsed_data
        except Exception as e:
            self.logger.error(f"Error parsing HTML: {str(e)}")
            return {}
    
    def crawl_hidden_wiki(self) -> Dict[str, str]:
        """Crawl the Hidden Wiki for information"""
        wiki_content: Dict[str, str] = {}
        
        for wiki_name, wiki_url in self.config.HIDDEN_WIKI_URLS.items():
            self.logger.info(f"Crawling Hidden Wiki: {wiki_name}")
            
            content = self.fetch_url(wiki_url)
            if content:
                parsed = self.parse_html(content)
                wiki_content[wiki_name] = parsed.get('text', '')
        
        return wiki_content
    
    def search_dark_web(self, query: str, search_engine: str = 'ahmia') -> Dict:
        """Search dark web using specified search engine"""
        if search_engine not in self.config.DARK_WEB_SEARCH_ENGINES:
            self.logger.error(f"Unknown search engine: {search_engine}")
            return {}
        
        search_url = self.config.DARK_WEB_SEARCH_ENGINES[search_engine]
        
        try:
            # Search engine specific parameters
            search_params = {
                'ahmia': {'q': query},
                'torch': {'q': query},
            }
            
            params = search_params.get(search_engine, {'q': query})
            
            self.logger.info(f"Searching {search_engine} for: {query}")
            
            headers = {
                'User-Agent': random.choice(self.config.USER_AGENTS),
            }
            
            response = self.session.get(
                search_url,
                params=params,
                headers=headers,
                timeout=self.config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            parsed = self.parse_html(response.text)
            return {
                'search_engine': search_engine,
                'query': query,
                'results': parsed,
                'status': 'success'
            }
        
        except Exception as e:
            self.logger.error(f"Search error on {search_engine}: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def extract_onion_links(self, html_content: str) -> List[str]:
        """Extract .onion links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        onion_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and '.onion' in href:
                onion_links.append(href)
        
        return onion_links
    
    def get_visited_urls(self) -> List[str]:
        """Get list of visited URLs"""
        return self.visited_urls.copy()
    
    def clear_visited(self):
        """Clear visited URLs list"""
        self.visited_urls = []
        self.logger.info("Cleared visited URLs")
