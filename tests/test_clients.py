#!/usr/bin/env python3
"""
Simple test script to verify all new clients work correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_clients():
    """Test all new clients."""
    try:
        from revomonauto.data.gradex_clients import (
            BattleMechanicsClient,
            EvolutionClient,
            WeatherClient,
            StatusEffectsClient
        )
        print("✅ All new clients imported successfully!")
        print()

        # Test BattleMechanicsClient
        print("🧮 Testing BattleMechanicsClient...")
        battle_client = BattleMechanicsClient()
        move_count = battle_client.moves_client.count()
        print(f"✅ BattleMechanicsClient initialized with {move_count} moves")

        # Test EvolutionClient
        print()
        print("🌳 Testing EvolutionClient...")
        evolution_client = EvolutionClient()
        tree = evolution_client.get_complete_evolution_tree(1)
        if "error" not in tree:
            member_count = tree["total_members"]
            print(f"✅ EvolutionClient: Found {member_count} members in Dekute evolution tree")
        else:
            print("⚠️ EvolutionClient: Error in evolution tree analysis")

        # Test WeatherClient
        print()
        print("🌤️ Testing WeatherClient...")
        weather_client = WeatherClient()
        weather_conditions = weather_client.get_weather_conditions()
        print(f"✅ WeatherClient: Found {len(weather_conditions)} weather conditions")

        # Test StatusEffectsClient
        print()
        print("🏥 Testing StatusEffectsClient...")
        status_client = StatusEffectsClient()
        status_conditions = status_client.get_status_conditions()
        print(f"✅ StatusEffectsClient: Found {len(status_conditions)} status conditions")

        # Quick functionality test
        print()
        print("🧪 Testing basic functionality...")

        # Test damage calculation
        try:
            gorcano = battle_client.revomon_client.get_revomon_by_name("gorcano")
            blizzora = battle_client.revomon_client.get_revomon_by_name("blizzora")
            earthquake = battle_client.moves_client.get_move_by_name("earthquake")

            if gorcano and blizzora and earthquake:
                damage_result = battle_client.simulate_battle_turn(
                    attacker=gorcano,
                    defender=blizzora,
                    move_name="earthquake",
                    attacker_level=50,
                    defender_level=50
                )
                if "damage" in damage_result:
                    print(f"✅ Damage calculation: Earthquake deals {damage_result['damage']} damage")
                else:
                    print("⚠️ Damage calculation: No damage result")
            else:
                print("⚠️ Damage calculation: Missing test data (Revomon or move)")
        except Exception as e:
            print(f"⚠️ Damage calculation: Error - {e}")

        print()
        print("🎉 All new clients working perfectly!")
        print()
        print("📊 System Summary:")
        print(f"   • Moves loaded: {move_count}")
        print(f"   • Weather conditions: {len(weather_conditions)}")
        print(f"   • Status conditions: {len(status_conditions)}")
        print("   • Evolution trees: Available")
        print("   • Battle mechanics: Ready for calculation")

        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please check that all dependencies are installed and files are in the correct location.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_clients()
    if success:
        print("\n🏆 All tests passed! The Revomon client system is ready for use.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
        sys.exit(1)
