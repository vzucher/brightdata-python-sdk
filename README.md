# Bright Data Python SDK

[![Tests](https://img.shields.io/badge/tests-237%20passing-brightgreen)](https://github.com/vzucher/brightdata-sdk-python)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/quality-FAANG--level-gold)](https://github.com/vzucher/brightdata-sdk-python)

Modern async-first Python SDK for [Bright Data](https://brightdata.com) APIs with comprehensive platform support, hierarchical service access, and 100% type safety.

---

## ✨ Features

- 🚀 **Async-first architecture** with sync wrappers for compatibility
- 🌐 **Web scraping** via Web Unlocker proxy service
- 🔍 **SERP API** - Google, Bing, Yandex search results
- 📦 **Platform scrapers** - LinkedIn, Amazon, ChatGPT
- 🎯 **Dual namespace** - `scrape` (URL-based) + `search` (discovery)
- 🔒 **100% type safety** - Full TypedDict definitions
- ⚡ **Zero code duplication** - DRY principles throughout
- ✅ **237 comprehensive tests** - Unit, integration, and E2E
- 🎨 **Rich result objects** - Timing, cost tracking, metadata
- 🧩 **Extensible** - Registry pattern for custom platforms

---

## 📦 Installation

```bash
pip install brightdata-sdk
```

Or install from source:

```bash
git clone https://github.com/vzucher/brightdata-sdk-python.git
cd brightdata-sdk-python
pip install -e .
```

---

## 🚀 Quick Start

### Authentication

Set your API token as an environment variable:

```bash
export BRIGHTDATA_API_TOKEN="your_api_token_here"
```

Or pass it directly:

```python
from brightdata import BrightDataClient

client = BrightDataClient(token="your_api_token")
```

### Simple Web Scraping

```python
from brightdata import BrightDataClient

# Initialize client (auto-loads token from environment)
client = BrightDataClient()

# Scrape any website
result = client.scrape.generic.url("https://example.com")

print(f"Success: {result.success}")
print(f"Data: {result.data[:200]}...")
print(f"Time: {result.elapsed_ms():.2f}ms")
```

### Platform-Specific Scraping

#### Amazon Products

```python
# Scrape specific product URLs
result = client.scrape.amazon.products(
    url="https://amazon.com/dp/B0CRMZHDG8",
    sync=True,
    timeout=65
)

# Extract reviews with filters
result = client.scrape.amazon.reviews(
    url="https://amazon.com/dp/B0CRMZHDG8",
    pastDays=30,
    keyWord="quality",
    numOfReviews=100
)

# Scrape seller information
result = client.scrape.amazon.sellers(
    url="https://amazon.com/sp?seller=AXXXXXXXXX"
)
```

#### LinkedIn Data

```python
# URL-based extraction
result = client.scrape.linkedin.profiles(
    url="https://linkedin.com/in/johndoe",
    sync=True
)

result = client.scrape.linkedin.jobs(
    url="https://linkedin.com/jobs/view/123456"
)

result = client.scrape.linkedin.companies(
    url="https://linkedin.com/company/microsoft"
)

result = client.scrape.linkedin.posts(
    url="https://linkedin.com/feed/update/..."
)

# Discovery/search operations
result = client.search.linkedin.jobs(
    keyword="python developer",
    location="New York",
    remote=True,
    experienceLevel="mid"
)

result = client.search.linkedin.profiles(
    firstName="John",
    lastName="Doe"
)

result = client.search.linkedin.posts(
    profile_url="https://linkedin.com/in/johndoe",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

#### ChatGPT Interactions

```python
# Send prompts to ChatGPT
result = client.search.chatGPT(
    prompt="Explain Python async programming",
    country="us",
    webSearch=True,
    sync=True
)

# Batch prompts
result = client.search.chatGPT(
    prompt=["What is Python?", "What is JavaScript?", "Compare them"],
    webSearch=[False, False, True]
)
```

### Search Engine Results (SERP)

```python
# Google search
result = client.search.google(
    query="python tutorial",
    location="United States",
    language="en",
    num_results=20
)

# Access results
for item in result.data:
    print(f"{item['position']}. {item['title']}")
    print(f"   {item['url']}")

# Bing search
result = client.search.bing(
    query="python tutorial",
    location="United States"
)

# Yandex search
result = client.search.yandex(
    query="python tutorial",
    location="Russia"
)
```

### Async Usage

```python
import asyncio
from brightdata import BrightDataClient

async def scrape_multiple():
    async with BrightDataClient() as client:
        # Scrape multiple URLs concurrently
        results = await client.scrape.generic.url_async([
            "https://example1.com",
            "https://example2.com",
            "https://example3.com"
        ])
        
        for result in results:
            print(f"{result.url}: {result.success}")

asyncio.run(scrape_multiple())
```

---

## 🏗️ Architecture

### Hierarchical Service Access

The SDK provides a clean, intuitive interface organized by operation type:

```python
client = BrightDataClient()

# URL-based extraction (scrape namespace)
client.scrape.amazon.products(url="...")
client.scrape.linkedin.profiles(url="...")
client.scrape.generic.url(url="...")

# Parameter-based discovery (search namespace)
client.search.linkedin.jobs(keyword="...", location="...")
client.search.google(query="...")
client.search.chatGPT(prompt="...")
```

### Core Components

- **`BrightDataClient`** - Main entry point with authentication
- **`ScrapeService`** - URL-based data extraction
- **`SearchService`** - Parameter-based discovery
- **Result Models** - `ScrapeResult`, `SearchResult`, `CrawlResult`
- **Platform Scrapers** - Amazon, LinkedIn, ChatGPT with registry pattern
- **SERP Services** - Google, Bing, Yandex search
- **Type System** - 100% type safety with TypedDict

---

## 📚 API Reference

### Client Initialization

```python
client = BrightDataClient(
    token="your_token",              # Auto-loads from env if not provided
    timeout=30,                       # Default timeout in seconds
    web_unlocker_zone="sdk_unlocker", # Web Unlocker zone name
    serp_zone="sdk_serp",             # SERP API zone name
    validate_token=False              # Validate token on init
)
```

### Connection Testing

```python
# Test API connection
is_valid = await client.test_connection()
is_valid = client.test_connection_sync()  # Synchronous version

# Get account information
info = await client.get_account_info()
info = client.get_account_info_sync()

print(f"Zones: {info['zone_count']}")
print(f"Active zones: {[z['name'] for z in info['zones']]}")
```

### Result Objects

All operations return rich result objects with timing and metadata:

```python
result = client.scrape.amazon.products(url="...")

# Access data
result.success       # bool - Operation succeeded
result.data          # Any - Scraped data
result.error         # str | None - Error message if failed
result.cost          # float | None - Cost in USD
result.platform      # str | None - Platform name

# Timing information
result.elapsed_ms()              # Total time in milliseconds
result.get_timing_breakdown()    # Detailed timing dict

# Serialization
result.to_dict()                 # Convert to dictionary
result.to_json(indent=2)         # JSON string
result.save_to_file("result.json")  # Save to file
```

---

## 🔧 Advanced Usage

### Batch Operations

```python
# Scrape multiple URLs concurrently
urls = [
    "https://amazon.com/dp/B001",
    "https://amazon.com/dp/B002",
    "https://amazon.com/dp/B003"
]

results = client.scrape.amazon.products(url=urls)

for result in results:
    if result.success:
        print(f"{result.data['title']}: ${result.data['price']}")
```

### Platform-Specific Options

```python
# Amazon reviews with filters
result = client.scrape.amazon.reviews(
    url="https://amazon.com/dp/B123",
    pastDays=7,              # Last 7 days only
    keyWord="quality",       # Filter by keyword
    numOfReviews=50,         # Limit to 50 reviews
    sync=True
)

# LinkedIn jobs with extensive filters
result = client.search.linkedin.jobs(
    keyword="python developer",
    location="New York",
    country="us",
    jobType="full-time",
    experienceLevel="mid",
    remote=True,
    company="Microsoft",
    timeRange="past-week"
)
```

### Sync vs Async Modes

```python
# Sync mode (default) - immediate response
result = client.scrape.linkedin.profiles(
    url="https://linkedin.com/in/johndoe",
    sync=True,      # Immediate response (faster but limited timeout)
    timeout=65      # Max 65 seconds
)

# Async mode - polling for long operations
result = client.scrape.linkedin.profiles(
    url="https://linkedin.com/in/johndoe",
    sync=False,     # Trigger + poll (can wait longer)
    timeout=300     # Max 5 minutes
)
```

---

## 🧪 Testing

The SDK includes 237 comprehensive tests:

```bash
# Run all tests
pytest tests/

# Run specific test suites
pytest tests/unit/              # Unit tests
pytest tests/integration/       # Integration tests
pytest tests/e2e/               # End-to-end tests

# Run with coverage
pytest tests/ --cov=brightdata --cov-report=html
```

---

## 🏛️ Design Philosophy

- **Client is single source of truth** for configuration
- **Authentication "just works"** with minimal setup
- **Fail fast and clearly** when credentials are missing/invalid
- **Each platform is an expert** in its domain
- **Scrape vs Search distinction** is clear and consistent
- **Build for future** - registry pattern enables intelligent routing

---

## 📖 Documentation

- [Quick Start Guide](docs/quickstart.md)
- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api-reference/)
- [Contributing Guide](docs/contributing.md)
- [Implementation Plan](PLAN.md) - Original refactoring plan

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/vzucher/brightdata-sdk-python.git
cd brightdata-sdk-python

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

---

## 📊 Project Stats

- **Production Code:** ~7,500 lines
- **Test Code:** ~3,500 lines
- **Test Coverage:** 100% (237 tests passing)
- **Supported Platforms:** Amazon, LinkedIn, ChatGPT, Generic Web
- **Supported Search Engines:** Google, Bing, Yandex
- **Type Safety:** 100% (TypedDict everywhere)
- **Code Duplication:** 0%

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- [Bright Data](https://brightdata.com) - Get your API token
- [API Documentation](https://docs.brightdata.com)
- [GitHub Repository](https://github.com/vzucher/brightdata-sdk-python)
- [Issue Tracker](https://github.com/vzucher/brightdata-sdk-python/issues)

---

## 💡 Examples

### Complete Workflow Example

```python
from brightdata import BrightDataClient

# Initialize
client = BrightDataClient()

# Test connection
if client.test_connection_sync():
    print("✅ Connected to Bright Data API")
    
    # Get account info
    info = client.get_account_info_sync()
    print(f"Active zones: {info['zone_count']}")
    
    # Scrape Amazon product
    product = client.scrape.amazon.products(
        url="https://amazon.com/dp/B0CRMZHDG8"
    )
    
    if product.success:
        print(f"Product: {product.data['title']}")
        print(f"Price: {product.data['price']}")
        print(f"Rating: {product.data['rating']}")
        print(f"Cost: ${product.cost:.4f}")
    
    # Search LinkedIn jobs
    jobs = client.search.linkedin.jobs(
        keyword="python developer",
        location="San Francisco",
        remote=True
    )
    
    print(f"Found {jobs.row_count} jobs")
    
    # Search Google
    search_results = client.search.google(
        query="python async tutorial",
        location="United States",
        num_results=10
    )
    
    for i, item in enumerate(search_results.data, 1):
        print(f"{i}. {item['title']}")
```

### Interactive CLI Demo

Run the included demo to explore the SDK interactively:

```bash
python demo_sdk.py
```

---

## 🎯 Roadmap

- [x] Core client with authentication
- [x] Web Unlocker service
- [x] Platform scrapers (Amazon, LinkedIn, ChatGPT)
- [x] SERP API (Google, Bing, Yandex)
- [x] Comprehensive test suite
- [ ] Browser automation API
- [ ] Web crawler API
- [ ] Additional platforms (Instagram, Reddit, Twitter)

---

## 🙏 Acknowledgments

Built with best practices from:
- Modern Python packaging (PEP 518, 621)
- Async/await patterns
- Type safety (PEP 484, 544)
- FAANG-level engineering standards

---

**Ready to start scraping?** Get your API token at [brightdata.com](https://brightdata.com/cp/api_keys) and dive in!

