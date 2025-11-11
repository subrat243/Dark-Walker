# Dark-Walker: Complete Documentation

**Dark Web Monitoring Tool v1.0.0**  
*A comprehensive Python tool for monitoring dark web with pattern scanning, Hidden Wiki integration, and dark web search engine support.*

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [API Reference](#api-reference)
6. [Project Structure](#project-structure)
7. [Advanced Configuration](#advanced-configuration)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation (3 steps)

```bash
pip install -r requirements.txt
copy .env.example .env
python examples.py
```

### Basic Usage

```bash
python main.py monitor
```

### Python API

```python
from src.monitor import DarkWebMonitor

monitor = DarkWebMonitor()
results = monitor.monitor_dark_web()
monitor.save_results(results)
```

---

## Installation

### Prerequisites

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 256 MB minimum (512 MB recommended)
- **Storage**: 100 MB
- **Network**: Internet connection

### Platform-Specific Installation

#### Windows

1. **Install Python**
   - Download from: https://www.python.org/downloads/
   - Enable "Add Python to PATH" during installation

2. **Install Tor (Optional)**
   - Download: https://www.torproject.org/download/#windows
   - Extract and configure as needed

3. **Install Dark-Walker**
   ```bash
   cd Dark-Walker
   pip install -r requirements.txt
   ```

4. **Configure**
   ```bash
   copy .env.example .env
   notepad .env  # Edit as needed
   ```

#### macOS

1. **Install Python**
   ```bash
   brew install python3
   ```

2. **Install Tor (Optional)**
   ```bash
   brew install tor
   brew services start tor
   ```

3. **Install Dark-Walker**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure**
   ```bash
   cp .env.example .env
   nano .env  # Edit as needed
   ```

#### Linux

1. **Install Python**
   ```bash
   sudo apt-get install python3 python3-pip
   ```

2. **Install Tor (Optional)**
   ```bash
   sudo apt-get install tor
   sudo systemctl start tor
   ```

3. **Install Dark-Walker**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure**
   ```bash
   cp .env.example .env
   nano .env  # Edit as needed
   ```

### Verify Installation

```bash
python examples.py
```

---

## Configuration

### Environment Variables (.env)

Copy `.env.example` to `.env` and customize:

```env
# Tor Configuration
TOR_ENABLED=False
TOR_HOST=localhost
TOR_PORT=9050
TOR_CONTROL_PORT=9051
TOR_CONTROL_PASSWORD=password

# Proxy Configuration
USE_PROXY=False

# Request Configuration
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3
RETRY_DELAY=5

# Monitoring Configuration
MONITORING_INTERVAL=3600
LOG_LEVEL=INFO
LOG_FILE=./logs/darkweb_monitor.log

# Output Configuration
RESULTS_DIR=./results
EXPORT_FORMAT=json

# Environment
ENVIRONMENT=development
```

### Tor Setup

#### Windows Tor Configuration

1. Download Tor from: https://www.torproject.org/download/
2. Extract to folder (e.g., `C:\Tor`)
3. Run Tor:
   ```batch
   cd C:\Tor
   tor.exe --SocksPort 9050 --ControlPort 9051
   ```
4. In `.env`:
   ```env
   TOR_ENABLED=True
   TOR_HOST=localhost
   TOR_PORT=9050
   ```

#### Linux Tor Configuration

1. Install:
   ```bash
   sudo apt-get install tor
   sudo systemctl start tor
   ```
2. Edit `/etc/tor/torrc`:
   ```
   SocksPort 9050
   ControlPort 9051
   CookieAuthentication 1
   ```
3. Restart:
   ```bash
   sudo systemctl restart tor
   ```

#### macOS Tor Configuration

1. Install:
   ```bash
   brew install tor
   brew services start tor
   ```

---

## Usage

### Command Line Interface

#### Initialize Monitor

```bash
python main.py init
```

#### Monitor Dark Web

```bash
# Monitor with default keywords
python main.py monitor

# Monitor with specific search query
python main.py monitor -q "leaked database"

# Use specific search engines
python main.py monitor -q "vulnerability" -e ahmia torch

# Monitor multiple engines
python main.py monitor -e ahmia torch notevil
```

#### Monitor Specific Site

```bash
python main.py site http://example.onion
```

#### Manage Patterns

```bash
# List all patterns
python main.py patterns

# Add custom pattern
python main.py add-pattern "your_regex_pattern" -n "pattern_name"

# Add pattern for phishing
python main.py add-pattern "\bphishing\b" -n "phishing_detection"
```

#### View Configuration

```bash
python main.py info
```

### Python API Usage

#### Basic Monitoring

```python
from src.monitor import DarkWebMonitor

# Initialize
monitor = DarkWebMonitor()

# Monitor dark web
results = monitor.monitor_dark_web()

# Print findings
for finding in results.get('findings', []):
    print(f"Pattern: {finding['pattern']}")
    print(f"Found: {finding['matched_text']}")
    print(f"Source: {finding['source_url']}")
```

#### Pattern Scanning

```python
from src.pattern_scanner import PatternScanner

# Initialize scanner
scanner = PatternScanner()

# Scan text
text = "Contact us at admin@example.com"
results = scanner.scan_text(text, "source_url")

# Display results
for result in results:
    print(f"Pattern: {result.pattern}")
    print(f"Matched: {result.matched_text}")
```

#### Custom Patterns

```python
from src.monitor import DarkWebMonitor

monitor = DarkWebMonitor()

# Add custom patterns
monitor.add_search_pattern(r"\bdata\s+breach\b", "data_breach")
monitor.add_search_pattern(r"\bransomware\b", "ransomware")
monitor.add_search_pattern(r"\bzero-day\b", "zero_day")

# Monitor
results = monitor.monitor_dark_web()
```

#### Monitoring Specific Sites

```python
from src.monitor import DarkWebMonitor

monitor = DarkWebMonitor()

# Monitor one site
results = monitor.monitor_specific_site("http://example.onion")

# Monitor multiple sites
sites = [
    "http://site1.onion",
    "http://site2.onion",
    "http://site3.onion"
]

for site in sites:
    results = monitor.monitor_specific_site(site)
    monitor.save_results(results, f"site_{site.replace('/', '_')}")
```

#### Export Results

```python
from src.monitor import DarkWebMonitor

monitor = DarkWebMonitor()

# Monitor
results = monitor.monitor_dark_web()

# Save results (format based on .env EXPORT_FORMAT)
file_path = monitor.save_results(results, "scan_results")
print(f"Results saved to: {file_path}")
```

---

## API Reference

### DarkWebMonitor Class

Main orchestrator for dark web monitoring.

#### Methods

##### `monitor_dark_web(search_query=None, search_engines=None)`

Monitor dark web using search engines and Hidden Wiki.

**Parameters:**
- `search_query` (str): Search term to query
- `search_engines` (List[str]): Search engines to use

**Returns:** Dictionary with findings and statistics

**Example:**
```python
results = monitor.monitor_dark_web(
    search_query="security vulnerability",
    search_engines=['ahmia', 'torch']
)
```

##### `monitor_specific_site(url)`

Monitor a specific onion site.

**Parameters:**
- `url` (str): Onion URL to monitor

**Returns:** Dictionary with site findings

**Example:**
```python
results = monitor.monitor_specific_site("http://example.onion")
```

##### `save_results(results, filename=None)`

Save monitoring results to file.

**Parameters:**
- `results` (Dict): Results to save
- `filename` (str): Output filename (optional)

**Returns:** File path where results were saved

**Example:**
```python
file_path = monitor.save_results(results, "scan")
```

##### `add_search_pattern(pattern, name=None)`

Add custom regex pattern for monitoring.

**Parameters:**
- `pattern` (str): Regex pattern string
- `name` (str): Pattern name (optional)

**Example:**
```python
monitor.add_search_pattern(r"\bphishing\b", "phishing")
```

##### `get_search_patterns()`

Get all available search patterns.

**Returns:** List of pattern names

**Example:**
```python
patterns = monitor.get_search_patterns()
print(f"Total patterns: {len(patterns)}")
```

### PatternScanner Class

Scans text for sensitive patterns.

#### Methods

##### `scan_text(text, source_url, context_length=100)`

Scan text for patterns.

**Parameters:**
- `text` (str): Text to scan
- `source_url` (str): Source URL for reference
- `context_length` (int): Characters of context

**Returns:** List of ScanResult objects

**Example:**
```python
results = scanner.scan_text("admin@example.com", "http://source.onion")
```

##### `add_custom_pattern(pattern, name=None)`

Add custom regex pattern.

**Parameters:**
- `pattern` (str): Regex pattern
- `name` (str): Pattern name (optional)

**Raises:** ValueError if invalid regex

**Example:**
```python
scanner.add_custom_pattern(r"password[=:]\s*[\w]+", "password")
```

### DarkWebCrawler Class

Crawls dark web sites and retrieves content.

#### Methods

##### `fetch_url(url, timeout=None)`

Fetch content from URL.

**Parameters:**
- `url` (str): URL to fetch
- `timeout` (int): Request timeout

**Returns:** HTML content or None

**Example:**
```python
content = crawler.fetch_url("http://example.onion")
```

##### `search_dark_web(query, search_engine='ahmia')`

Search using dark web search engine.

**Parameters:**
- `query` (str): Search query
- `search_engine` (str): Search engine name

**Returns:** Dictionary with search results

**Example:**
```python
results = crawler.search_dark_web("leaked database", "ahmia")
```

##### `crawl_hidden_wiki()`

Crawl the Hidden Wiki.

**Returns:** Dictionary with wiki content

**Example:**
```python
wiki_content = crawler.crawl_hidden_wiki()
```

---

## Project Structure

```
Dark-Walker/
│
├── src/                           # Source code (7 modules)
│   ├── __init__.py
│   ├── config.py                  # Configuration management
│   ├── logger.py                  # Logging system
│   ├── pattern_scanner.py         # Pattern detection
│   ├── dark_web_crawler.py        # Web crawler
│   ├── monitor.py                 # Orchestrator
│   └── cli.py                     # CLI interface
│
├── tests/                         # Tests
│   └── test_monitor.py
│
├── logs/                          # Application logs (auto-created)
├── results/                       # Results (auto-created)
├── config/                        # Configuration directory
│
├── main.py                        # Entry point
├── examples.py                    # Code examples
├── requirements.txt               # Dependencies
├── .env.example                   # Configuration template
└── DOCUMENTATION.md               # This file
```

### Module Descriptions

#### config.py
Configuration management with environment-based settings.
- Tor configuration
- Search engine URLs
- Pattern definitions
- Logging settings

#### logger.py
Centralized logging system using singleton pattern.
- File logging
- Console logging
- Configurable levels
- Timestamp formatting

#### pattern_scanner.py
Pattern detection engine.
- 7+ built-in patterns
- Custom regex support
- Context-aware matching
- ScanResult data model

#### dark_web_crawler.py
Dark web crawling module.
- Tor proxy integration
- Search engine support
- Hidden Wiki crawling
- User-agent rotation
- Intelligent retries

#### monitor.py
Main monitoring orchestrator.
- Combines crawling + scanning
- Multi-format export
- Statistics tracking
- Site-specific monitoring

#### cli.py
Command-line interface.
- 6 main commands
- Colored output
- Interactive operation
- Result visualization

---

## Advanced Configuration

### Custom Regex Patterns

Add custom patterns for specific monitoring needs.

#### Database Connection Strings

```python
monitor.add_search_pattern(
    r'(mysql|postgres|mongodb):\/\/[^:]+:[^@]+@[^\s]+',
    'database_connection'
)
```

#### API Endpoints

```python
monitor.add_search_pattern(
    r'\/api\/v\d+\/[a-zA-Z0-9_\-\/]+',
    'api_endpoint'
)
```

#### Private Keys

```python
monitor.add_search_pattern(
    r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY',
    'private_key'
)
```

#### Telegram Bot Tokens

```python
monitor.add_search_pattern(
    r'\d{8,10}:[A-Za-z0-9_-]{35,}',
    'telegram_bot_token'
)
```

### Monitoring Profiles

#### Security Breach Detection

```python
monitor = DarkWebMonitor()

patterns = [
    r'\bleaked\s+database\b',
    r'\bcredential\s+dump\b',
    r'\bdata\s+breach\b',
    r'\bunleaked\b',
    r'\bcombos\b'
]

for pattern in patterns:
    monitor.add_search_pattern(pattern)

results = monitor.monitor_dark_web(
    search_query="database leak"
)
```

#### Malware & Exploit Detection

```python
patterns = [
    r'\bmalware\b',
    r'\brootkit\b',
    r'\bexploit\s+code\b',
    r'\bzero-day\b',
    r'\bpayload\b'
]

for pattern in patterns:
    monitor.add_search_pattern(pattern)

results = monitor.monitor_dark_web(
    search_query="malware kit"
)
```

#### Financial Threats

```python
patterns = [
    r'\bcredit\s+card\b',
    r'\bank\s+account\b',
    r'\bcryptocurrency\b',
    r'\bbitcoin\s+wallet\b'
]

for pattern in patterns:
    monitor.add_search_pattern(pattern)

results = monitor.monitor_dark_web(
    search_query="payment methods"
)
```

### Distributed Monitoring

```python
import concurrent.futures
from src.monitor import DarkWebMonitor

sites = [
    "http://site1.onion",
    "http://site2.onion",
    "http://site3.onion"
]

def monitor_site(site_url):
    monitor = DarkWebMonitor()
    return monitor.monitor_specific_site(site_url)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(monitor_site, site) for site in sites]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
```

### Scheduled Monitoring (APScheduler)

```python
from apscheduler.schedulers.background import BackgroundScheduler
from src.monitor import DarkWebMonitor

def scheduled_monitoring():
    monitor = DarkWebMonitor()
    results = monitor.monitor_dark_web()
    monitor.save_results(results)

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_monitoring, 'interval', hours=6)
scheduler.start()
```

### Slack Integration

```python
import requests

def notify_slack(findings, webhook_url):
    message = {
        'text': '🔍 Dark Web Scan Results',
        'attachments': []
    }
    
    for finding in findings[:10]:
        message['attachments'].append({
            'color': 'danger',
            'title': finding['pattern'],
            'text': finding['matched_text']
        })
    
    requests.post(webhook_url, json=message)
```

### SQLite Storage

```python
import sqlite3

def store_findings(findings, db_path='monitoring.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY,
            pattern TEXT,
            matched_text TEXT,
            source_url TEXT,
            timestamp DATETIME
        )
    ''')
    
    for finding in findings:
        cursor.execute('''
            INSERT INTO findings 
            (pattern, matched_text, source_url, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (
            finding['pattern'],
            finding['matched_text'],
            finding['source_url'],
            finding['timestamp']
        ))
    
    conn.commit()
    conn.close()
```

---

## Troubleshooting

### Installation Issues

#### Problem: Import Errors

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

#### Problem: Permission Denied

**Solution:**
```bash
# Linux/macOS
sudo pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Runtime Issues

#### Problem: Connection Timeouts

**Solution:** Increase timeout in `.env`:
```env
REQUEST_TIMEOUT=60
RETRY_ATTEMPTS=5
```

#### Problem: Tor Not Connecting

**Solution:** Verify Tor is running:
```bash
# Windows
netstat -an | findstr 9050

# Linux/macOS
netstat -an | grep 9050

# If not running, start Tor
# Windows: tor.exe --SocksPort 9050
# Linux: sudo systemctl start tor
# macOS: brew services start tor
```

#### Problem: No Results Found

**Solution:**
1. Use more specific search queries
2. Try different search engines
3. Check logs: `tail -f logs/darkweb_monitor.log`

#### Problem: Memory Issues

**Solution:**
1. Monitor smaller time intervals
2. Limit results size
3. Use pagination
4. Monitor one site at a time

### Configuration Issues

#### Problem: Pattern Not Working

**Verify regex:**
```python
import re
pattern = r"your_pattern_here"
re.compile(pattern)  # Will raise error if invalid
```

#### Problem: Search Engine Not Responding

**Solution:**
1. Check internet connection
2. Try different search engine
3. Verify Tor (if enabled)
4. Check firewall settings

### Performance Optimization

1. **Use specific search queries** - Reduces results
2. **Monitor during off-peak hours** - Faster responses
3. **Enable Tor only when needed** - Faster without Tor
4. **Limit context length** - Less memory usage
5. **Archive old results** - Better organization

---

## Features Summary

### Pattern Detection
✓ Email addresses  
✓ Bitcoin/Ethereum wallets  
✓ IP addresses  
✓ URLs  
✓ Social Security Numbers  
✓ Credit card numbers  
✓ API keys  
✓ Custom regex patterns  

### Dark Web Sources
✓ Ahmia search engine  
✓ Torch search engine  
✓ NotEvil search engine  
✓ DarkWeb Link directory  
✓ Hidden Wiki knowledge base  
✓ Tor proxy support  

### Export Formats
✓ JSON (structured)  
✓ CSV (spreadsheet)  
✓ TXT (human-readable)  

### Monitoring Types
✓ General surveillance  
✓ Site-specific  
✓ Pattern-based  
✓ Batch monitoring  
✓ Custom workflows  

---

## Security & Legal

### Security Considerations

✓ Use Tor for anonymous browsing  
✓ Use VPN in addition to Tor  
✓ Don't store sensitive data unencrypted  
✓ Run on isolated machine for sensitive work  
✓ Regularly update dependencies  

### Legal Notice

⚠️ **Important**: Use this tool responsibly and legally.

- Verify your jurisdiction allows this activity
- Only monitor sites and data you own or have permission to monitor
- Comply with all applicable laws and regulations
- Protect sensitive data properly
- Follow ethical guidelines

---

## Dependencies

- **requests** - HTTP client
- **beautifulsoup4** - HTML parsing
- **stem** - Tor control
- **pysocks** - SOCKS proxy
- **colorama** - Colored output
- **tabulate** - Table formatting
- **python-dotenv** - Environment variables
- **urllib3** - HTTP utilities
- **validators** - Data validation
- **selenium** - Browser automation (optional)
- **aiohttp** - Async HTTP (optional)

Install all:
```bash
pip install -r requirements.txt
```

---

## Support & Resources

### Documentation Files
- This file contains all documentation

### Code Examples
- See `examples.py` for working examples

### Tests
- See `tests/test_monitor.py` for test cases

### Logs
- Application logs: `logs/darkweb_monitor.log`
- Results: `results/` directory

---

## Version Information

- **Version**: 1.0.0
- **Python**: 3.8+
- **Status**: Production Ready ✅
- **Created**: November 12, 2025

---

## Quick Command Reference

```bash
# Initialize
python main.py init

# Monitor dark web
python main.py monitor

# Search specific terms
python main.py monitor -q "vulnerability" -e ahmia torch

# Monitor specific site
python main.py site http://example.onion

# List patterns
python main.py patterns

# Add custom pattern
python main.py add-pattern "regex" -n "name"

# Show configuration
python main.py info
```

---

**Dark-Walker: Bringing clarity to the shadows of the dark web.**
