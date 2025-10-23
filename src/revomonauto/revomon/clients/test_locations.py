"""
Simple test for LocationsClient
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.revomonauto.revomon.clients.locations_client import LocationsClient

def test_locations_client():
    print("Testing LocationsClient...")

    client = LocationsClient()
    print(f"Loading data from: {client.data_file}")

    success = client.load_data()
    if not success:
        print("❌ Failed to load data")
        return

    print(f"✅ Data loaded successfully: {client.count()} records")

    # Test getting all locations
    locations = client.get_all_spawn_locations()
    print(f"📍 Found {len(locations)} unique spawn locations")
    print(f"First 5 locations: {locations[:5]}")

    # Test getting Revomon by location
    if locations:
        test_location = locations[0]
        print(f"\n🔍 Testing location: {test_location}")

        revomon = client.get_revomon_by_location(test_location)
        print(f"Found {len(revomon)} Revomon in {test_location}")
        if revomon:
            print(f"Sample Revomon: {[r['name'] for r in revomon[:3]]}")

        # Get detailed info
        details = client.get_spawn_details(test_location)
        print(f"Location details: {details['revomon_count']} total, {details['unique_revomon']} unique")

    # Test statistics
    print("📊 Location Statistics:")
    stats = client.get_location_statistics()
    print(f"Total locations: {stats['total_locations']}")
    print(f"Total spawn entries: {stats['total_spawn_entries']}")
    print(f"Average Revomon per location: {stats['avg_revomon_per_location']:.1f}")

    print("\n✅ LocationsClient test completed successfully!")

if __name__ == "__main__":
    test_locations_client()
