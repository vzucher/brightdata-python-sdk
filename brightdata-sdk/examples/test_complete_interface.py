"""Test complete BrightDataClient interface according to specifications."""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from brightdata import BrightDataClient


async def test_interface():
    """Test all interface requirements."""
    print("=" * 70)
    print("Bright Data SDK - Complete Interface Test")
    print("=" * 70)
    
    checks = []
    
    # 1. Simple instantiation
    print("\n[1] Testing simple instantiation...")
    try:
        client1 = BrightDataClient()
        checks.append(("Auto-load from env", True))
        print("  [OK] client = BrightDataClient() - Auto-loads from env")
    except Exception as e:
        checks.append(("Auto-load from env", False))
        print(f"  [FAIL] {e}")
    
    try:
        client2 = BrightDataClient(token="test_token_123")
        checks.append(("Explicit token", True))
        print("  [OK] client = BrightDataClient(token='...') - Explicit token")
    except Exception as e:
        checks.append(("Explicit token", False))
        print(f"  [FAIL] {e}")
    
    # 2. Service access
    print("\n[2] Testing service access...")
    client = BrightDataClient()
    
    try:
        scrape_service = client.scrape
        amazon_scraper = scrape_service.amazon
        checks.append(("client.scrape.amazon", True))
        print("  [OK] client.scrape.amazon - Accessible")
    except Exception as e:
        checks.append(("client.scrape.amazon", False))
        print(f"  [FAIL] client.scrape.amazon: {e}")
    
    try:
        search_service = client.search
        linkedin_search = search_service.linkedin
        checks.append(("client.search.linkedin", True))
        print("  [OK] client.search.linkedin - Accessible")
    except Exception as e:
        checks.append(("client.search.linkedin", False))
        print(f"  [FAIL] client.search.linkedin: {e}")
    
    try:
        crawler_service = client.crawler
        checks.append(("client.crawler", True))
        print("  [OK] client.crawler - Accessible")
    except Exception as e:
        checks.append(("client.crawler", False))
        print(f"  [FAIL] client.crawler: {e}")
    
    # 3. Method signatures
    print("\n[3] Testing method signatures...")
    
    try:
        if hasattr(amazon_scraper, 'products'):
            checks.append(("scrape.amazon.products()", True))
            print("  [OK] client.scrape.amazon.products() - Method exists")
        else:
            checks.append(("scrape.amazon.products()", False))
            print("  [FAIL] client.scrape.amazon.products() - Method missing")
    except Exception as e:
        checks.append(("scrape.amazon.products()", False))
        print(f"  [FAIL] {e}")
    
    try:
        if hasattr(linkedin_search, 'jobs'):
            checks.append(("search.linkedin.jobs()", True))
            print("  [OK] client.search.linkedin.jobs() - Method exists")
        else:
            checks.append(("search.linkedin.jobs()", False))
            print("  [FAIL] client.search.linkedin.jobs() - Method missing")
    except Exception as e:
        checks.append(("search.linkedin.jobs()", False))
        print(f"  [FAIL] {e}")
    
    try:
        if hasattr(crawler_service, 'discover'):
            checks.append(("crawler.discover()", True))
            print("  [OK] client.crawler.discover() - Method exists")
        else:
            checks.append(("crawler.discover()", False))
            print("  [FAIL] client.crawler.discover() - Method missing")
    except Exception as e:
        checks.append(("crawler.discover()", False))
        print(f"  [FAIL] {e}")
    
    # 4. Connection verification
    print("\n[4] Testing connection verification...")
    
    try:
        async with client:
            is_valid = await client.test_connection()
            if is_valid:
                checks.append(("test_connection()", True))
                print("  [OK] await client.test_connection() - Works")
            else:
                checks.append(("test_connection()", False))
                print("  [FAIL] test_connection() returned False")
    except Exception as e:
        checks.append(("test_connection()", False))
        print(f"  [FAIL] {e}")
    
    try:
        async with client:
            account_info = await client.get_account_info()
            if isinstance(account_info, dict):
                checks.append(("get_account_info()", True))
                print("  [OK] await client.get_account_info() - Works")
            else:
                checks.append(("get_account_info()", False))
                print("  [FAIL] get_account_info() returned wrong type")
    except Exception as e:
        checks.append(("get_account_info()", False))
        print(f"  [FAIL] {e}")
    
    # 5. Token management
    print("\n[5] Testing token management...")
    
    try:
        masked_token = client.token
        if masked_token and len(masked_token) > 0:
            checks.append(("Token property", True))
            print(f"  [OK] client.token - Returns masked token: {masked_token}")
        else:
            checks.append(("Token property", False))
            print("  [FAIL] client.token - Empty or invalid")
    except Exception as e:
        checks.append(("Token property", False))
        print(f"  [FAIL] {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    for name, status in checks:
        symbol = "[OK]" if status else "[FAIL]"
        print(f"  {symbol} {name}")
    
    print(f"\n  Total: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n  [SUCCESS] All interface requirements met!")
    else:
        print(f"\n  [WARNING] {total - passed} requirement(s) missing")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_interface())

