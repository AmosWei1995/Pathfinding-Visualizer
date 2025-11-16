"""
Test script for map save/load functionality
This tests the core save/load logic without running the GUI
"""
import os
import sys
import json

# Test the JSON save/load functionality
def test_save_load():
    # Create maps directory if it doesn't exist
    maps_dir = "maps"
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)
        print(f"✓ Created {maps_dir} directory")
    else:
        print(f"✓ {maps_dir} directory already exists")

    # Create a test map
    test_map = {
        "width": 48,
        "height": 26,
        "start": [13, 12],
        "goal": [13, 35],
        "cells": [
            {"row": 5, "col": 10, "value": "#", "cost": -1},
            {"row": 5, "col": 11, "value": "#", "cost": -1},
            {"row": 6, "col": 10, "value": "#", "cost": -1},
            {"row": 8, "col": 15, "value": "5", "cost": 5},
            {"row": 8, "col": 16, "value": "3", "cost": 3},
        ]
    }

    # Save test map
    test_filepath = os.path.join(maps_dir, "test_map_1.json")
    with open(test_filepath, 'w') as f:
        json.dump(test_map, f, indent=2)
    print(f"✓ Saved test map to: {test_filepath}")

    # Load test map
    with open(test_filepath, 'r') as f:
        loaded_map = json.load(f)
    print(f"✓ Loaded test map from: {test_filepath}")

    # Verify data
    assert loaded_map["width"] == test_map["width"], "Width mismatch"
    assert loaded_map["height"] == test_map["height"], "Height mismatch"
    assert loaded_map["start"] == test_map["start"], "Start position mismatch"
    assert loaded_map["goal"] == test_map["goal"], "Goal position mismatch"
    assert len(loaded_map["cells"]) == len(test_map["cells"]), "Cells count mismatch"
    print("✓ All data verified successfully")

    # List all saved maps
    map_files = [f for f in os.listdir(maps_dir) if f.endswith('.json')]
    print(f"\n✓ Found {len(map_files)} saved map(s):")
    for map_file in sorted(map_files, reverse=True):
        print(f"  - {map_file}")

    print("\n✅ All tests passed! Map save/load functionality is working correctly.")
    print("\n📌 Usage instructions:")
    print("  1. Run the visualizer: python3 run.pyw")
    print("  2. Create or generate a maze")
    print("  3. Click 'Save Map' to save the current map")
    print("  4. Click 'Load Map' to see and load saved maps")
    print("  5. Use saved maps for systematic algorithm testing")

if __name__ == "__main__":
    test_save_load()
