"""Test connection and account info functionality."""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from brightdata import BrightDataClient, AuthenticationError, APIError


async def main():
    """Test connection and account info."""
    print("=" * 70)
    print("Bright Data SDK - Connection & Account Info Test")
    print("=" * 70)
    
    print("\n[1] Creating client...")
    try:
        client = BrightDataClient()
        print(f"[OK] Client created successfully")
        print(f"     Token: {client.token}")
        print(f"     Timeout: {client.timeout}s")
        print(f"     Default zone: {client.default_zone}")
    except Exception as e:
        print(f"[FAIL] Failed to create client: {e}")
        return
    
    print("\n[2] Testing connection and listing zones...")
    try:
        async with client:
            print("  Attempting connection test...")
            try:
                is_valid = await client.test_connection()
                if is_valid:
                    print("[OK] Connection test PASSED - credentials are valid")
                else:
                    print("[FAIL] Connection test returned False")
                    print("  Trying direct zones call to see error...")
                    try:
                        zones = await client.list_zones()
                        print(f"  [OK] Direct call worked! Found {len(zones)} zones")
                    except Exception as direct_error:
                        print(f"  [ERROR] Direct call failed: {direct_error}")
                        print(f"          Error type: {type(direct_error).__name__}")
                    return
            except Exception as test_error:
                print(f"[ERROR] Connection test raised exception:")
                print(f"  Error: {test_error}")
                print(f"  Type: {type(test_error).__name__}")
                import traceback
                traceback.print_exc()
                return
            
            print("\n[3] Listing zones...")
            zones = await client.list_zones()
            print(f"[OK] Zones retrieved successfully")
            print(f"     Found {len(zones)} active zone(s)")
            
            if zones and len(zones) > 0:
                print("\n" + "-" * 70)
                print("ACTIVE ZONES:")
                print("-" * 70)
                for i, zone in enumerate(zones[:5], 1):
                    if isinstance(zone, dict):
                        zone_name = zone.get('name', zone.get('zone_name', 'Unknown'))
                        zone_id = zone.get('id', zone.get('zone_id', 'N/A'))
                        zone_type = zone.get('type', zone.get('zone_type', 'N/A'))
                        print(f"  [{i}] {zone_name}")
                        print(f"      Type: {zone_type}, ID: {zone_id}")
                    else:
                        print(f"  [{i}] {zone}")
                if len(zones) > 5:
                    print(f"  ... and {len(zones) - 5} more zone(s)")
                print("-" * 70)
            else:
                print("  No zones found (this is normal for new accounts)")
            
            print("\n[4] Getting account information...")
            account_info = await client.get_account_info()
            print("[OK] Account info retrieved successfully")
            print("\n" + "-" * 70)
            print("ACCOUNT INFORMATION:")
            print("-" * 70)
            
            if isinstance(account_info, dict):
                for key, value in account_info.items():
                    if key == 'zones' and isinstance(value, list):
                        print(f"  {key}: {len(value)} zone(s) (see details above)")
                    elif isinstance(value, (dict, list)):
                        print(f"  {key}:")
                        if isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                print(f"    {sub_key}: {sub_value}")
                        else:
                            print(f"    {value}")
                    else:
                        print(f"  {key}: {value}")
            else:
                print(f"  Raw response: {account_info}")
            
            print("-" * 70)
    except AuthenticationError as e:
        print(f"[AUTH ERROR] Authentication failed:")
        print(f"  Message: {e.message if hasattr(e, 'message') else str(e)}")
        print("\n  This means:")
        print("  - The API token is invalid or expired")
        print("  - The token doesn't have required permissions")
        print("  - The authentication method is incorrect")
    except APIError as e:
        print(f"[API ERROR] API request failed:")
        print(f"  Status Code: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
        print(f"  Message: {e.message if hasattr(e, 'message') else str(e)}")
        if hasattr(e, 'response_text') and e.response_text:
            response_preview = e.response_text[:300] if len(e.response_text) > 300 else e.response_text
            print(f"  Response: {response_preview}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        print(f"        Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Test completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

