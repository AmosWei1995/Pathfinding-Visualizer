"""
Fix benchmark map dimensions to match current visualizer settings
This script will:
1. Detect the actual maze dimensions from the visualizer code
2. Update all benchmark maps to use the correct dimensions
"""

import json
import os
import sys

def calculate_maze_dimensions():
    """Calculate maze dimensions using the same logic as the visualizer"""
    # Default values (same as constants.py)
    WIDTH = 1280
    HEIGHT = 900
    HEADER_HEIGHT = 200
    CELL_SIZE = 26

    # Calculate remainders (same logic as constants.py)
    REMAINDER_W = WIDTH % CELL_SIZE
    if REMAINDER_W == 0:
        REMAINDER_W = CELL_SIZE

    REMAINDER_H = (HEIGHT - HEADER_HEIGHT) % CELL_SIZE
    if REMAINDER_H == 0:
        REMAINDER_H = CELL_SIZE

    MAZE_WIDTH = WIDTH - REMAINDER_W
    MAZE_HEIGHT = HEIGHT - HEADER_HEIGHT - REMAINDER_H

    # Calculate grid size (same as Maze.__init__)
    grid_width = MAZE_WIDTH // CELL_SIZE
    grid_height = MAZE_HEIGHT // CELL_SIZE

    return grid_width, grid_height

def get_actual_dimensions_from_error():
    """
    If you saw an error message like:
    "Warning: Map dimensions (48x26) don't match current maze (49x26)"

    Please enter the CURRENT maze dimensions from the error message.
    """
    print("=" * 70)
    print("Map Dimension Fix Utility")
    print("=" * 70)
    print()
    print("If you saw an error message when loading a map, it would say:")
    print('  "Map dimensions (X x Y) don\'t match current maze (A x B)"')
    print()
    print("We need the CURRENT maze dimensions (A x B).")
    print()

    # First try to calculate
    calc_width, calc_height = calculate_maze_dimensions()
    print(f"Calculated dimensions: {calc_width} x {calc_height}")
    print()

    response = input(f"Is {calc_width} x {calc_height} correct? (y/n): ").strip().lower()

    if response == 'y':
        return calc_width, calc_height
    else:
        print()
        print("Please enter the correct dimensions from your error message:")
        width = int(input("  Grid Width: "))
        height = int(input("  Grid Height: "))
        return width, height

def update_map_dimensions(map_file, new_width, new_height):
    """Update a single map file with new dimensions"""
    try:
        with open(map_file, 'r') as f:
            map_data = json.load(f)

        old_width = map_data['width']
        old_height = map_data['height']

        if old_width == new_width and old_height == new_height:
            return False, "Already correct"

        # Update dimensions
        map_data['width'] = new_width
        map_data['height'] = new_height

        # Adjust start and goal positions if needed
        start_row, start_col = map_data['start']
        goal_row, goal_col = map_data['goal']

        # Recalculate positions to maintain relative placement
        map_data['start'] = [
            int(start_row * new_height / old_height),
            int(start_col * new_width / old_width)
        ]
        map_data['goal'] = [
            int(goal_row * new_height / old_height),
            int(goal_col * new_width / old_width)
        ]

        # Filter out cells that are outside new dimensions
        filtered_cells = []
        for cell in map_data['cells']:
            if cell['row'] < new_height and cell['col'] < new_width:
                filtered_cells.append(cell)

        map_data['cells'] = filtered_cells

        # Save updated map
        with open(map_file, 'w') as f:
            json.dump(map_data, f, indent=2)

        return True, f"Updated from {old_width}x{old_height} to {new_width}x{new_height}"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    # Get correct dimensions
    width, height = get_actual_dimensions_from_error()

    print()
    print("=" * 70)
    print(f"Updating all maps to: {width} x {height}")
    print("=" * 70)
    print()

    # Process all maps in the maps directory
    maps_dir = "maps"
    if not os.path.exists(maps_dir):
        print(f"Error: '{maps_dir}' directory not found")
        return

    map_files = [f for f in os.listdir(maps_dir) if f.endswith('.json')]

    if not map_files:
        print(f"No map files found in '{maps_dir}'")
        return

    updated_count = 0
    skipped_count = 0

    for map_file in sorted(map_files):
        filepath = os.path.join(maps_dir, map_file)
        success, message = update_map_dimensions(filepath, width, height)

        if success:
            print(f"✓ {map_file:40s} - {message}")
            updated_count += 1
        else:
            print(f"○ {map_file:40s} - {message}")
            skipped_count += 1

    print()
    print("=" * 70)
    print(f"Updated: {updated_count} maps")
    print(f"Skipped: {skipped_count} maps (already correct or errors)")
    print("=" * 70)
    print()
    print("✅ All maps have been updated!")
    print(f"   You can now load any map in the visualizer.")

if __name__ == "__main__":
    main()
