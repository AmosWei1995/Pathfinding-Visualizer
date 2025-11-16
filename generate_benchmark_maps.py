"""
Generate 20 benchmark maps for pathfinding algorithm testing.
4 categories with 5 maps each:
1. Sparse-obstacle maps
2. Dense-obstacle maps
3. Maze-like maps
4. Weighted maps
"""

import json
import os
import random

# Map dimensions (matching the visualizer)
WIDTH = 48
HEIGHT = 26

# Fixed start and goal positions for consistency
START = [13, 12]
GOAL = [13, 35]

def create_map_structure():
    """Create basic map structure"""
    return {
        "width": WIDTH,
        "height": HEIGHT,
        "start": START,
        "goal": GOAL,
        "cells": []
    }

def add_wall(cells, row, col):
    """Add a wall cell"""
    if (row, col) != (START[0], START[1]) and (row, col) != (GOAL[0], GOAL[1]):
        cells.append({"row": row, "col": col, "value": "#", "cost": -1})

def add_weighted_cell(cells, row, col, cost):
    """Add a weighted cell"""
    if (row, col) != (START[0], START[1]) and (row, col) != (GOAL[0], GOAL[1]):
        cells.append({"row": row, "col": col, "value": str(cost), "cost": cost})

def is_valid_pos(row, col):
    """Check if position is valid and not start/goal"""
    return (0 <= row < HEIGHT and 0 <= col < WIDTH and
            (row, col) != (START[0], START[1]) and
            (row, col) != (GOAL[0], GOAL[1]))

# ==================== SPARSE-OBSTACLE MAPS ====================

def generate_sparse_1():
    """Sparse map 1: Random scattered obstacles (10-15 obstacles)"""
    map_data = create_map_structure()
    num_obstacles = random.randint(10, 15)

    for _ in range(num_obstacles):
        row = random.randint(0, HEIGHT - 1)
        col = random.randint(0, WIDTH - 1)
        if is_valid_pos(row, col):
            add_wall(map_data["cells"], row, col)

    return map_data

def generate_sparse_2():
    """Sparse map 2: Small obstacle clusters"""
    map_data = create_map_structure()
    num_clusters = 4

    for _ in range(num_clusters):
        center_row = random.randint(2, HEIGHT - 3)
        center_col = random.randint(2, WIDTH - 3)
        # 3x3 cluster
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if random.random() < 0.6 and is_valid_pos(center_row + dr, center_col + dc):
                    add_wall(map_data["cells"], center_row + dr, center_col + dc)

    return map_data

def generate_sparse_3():
    """Sparse map 3: Short walls"""
    map_data = create_map_structure()
    num_walls = 5

    for _ in range(num_walls):
        start_row = random.randint(0, HEIGHT - 1)
        start_col = random.randint(0, WIDTH - 8)
        length = random.randint(3, 7)

        for i in range(length):
            if is_valid_pos(start_row, start_col + i):
                add_wall(map_data["cells"], start_row, start_col + i)

    return map_data

def generate_sparse_4():
    """Sparse map 4: Large obstacle blocks"""
    map_data = create_map_structure()
    num_blocks = 3

    for _ in range(num_blocks):
        start_row = random.randint(0, HEIGHT - 5)
        start_col = random.randint(0, WIDTH - 5)

        for dr in range(4):
            for dc in range(4):
                if is_valid_pos(start_row + dr, start_col + dc):
                    add_wall(map_data["cells"], start_row + dr, start_col + dc)

    return map_data

def generate_sparse_5():
    """Sparse map 5: Widely scattered single obstacles"""
    map_data = create_map_structure()

    for row in range(0, HEIGHT, 3):
        for col in range(0, WIDTH, 4):
            if random.random() < 0.3 and is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    return map_data

# ==================== DENSE-OBSTACLE MAPS ====================

def generate_dense_1():
    """Dense map 1: Random obstacles covering 35-40%"""
    map_data = create_map_structure()
    total_cells = WIDTH * HEIGHT
    num_obstacles = int(total_cells * 0.37)

    placed = 0
    attempts = 0
    while placed < num_obstacles and attempts < num_obstacles * 3:
        row = random.randint(0, HEIGHT - 1)
        col = random.randint(0, WIDTH - 1)
        if is_valid_pos(row, col):
            # Check if not already placed
            if not any(cell["row"] == row and cell["col"] == col for cell in map_data["cells"]):
                add_wall(map_data["cells"], row, col)
                placed += 1
        attempts += 1

    return map_data

def generate_dense_2():
    """Dense map 2: Dense clusters"""
    map_data = create_map_structure()
    num_clusters = 8

    for _ in range(num_clusters):
        center_row = random.randint(3, HEIGHT - 4)
        center_col = random.randint(3, WIDTH - 4)
        # 5x5 dense cluster
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if random.random() < 0.7 and is_valid_pos(center_row + dr, center_col + dc):
                    add_wall(map_data["cells"], center_row + dr, center_col + dc)

    return map_data

def generate_dense_3():
    """Dense map 3: Interlaced obstacle bands"""
    map_data = create_map_structure()

    # Vertical bands
    for col in range(5, WIDTH, 8):
        for row in range(HEIGHT):
            if random.random() < 0.8 and is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    # Horizontal bands
    for row in range(5, HEIGHT, 8):
        for col in range(WIDTH):
            if random.random() < 0.7 and is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    return map_data

def generate_dense_4():
    """Dense map 4: Random field covering 45%"""
    map_data = create_map_structure()

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if random.random() < 0.45 and is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    return map_data

def generate_dense_5():
    """Dense map 5: Checkerboard-like pattern"""
    map_data = create_map_structure()

    for row in range(HEIGHT):
        for col in range(WIDTH):
            # Create checkerboard with some randomness
            if (row + col) % 3 == 0 and random.random() < 0.8 and is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    return map_data

# ==================== MAZE-LIKE MAPS ====================

def generate_maze_1():
    """Maze map 1: Simple corridor maze"""
    map_data = create_map_structure()

    # Horizontal corridors
    for row in [5, 10, 15, 20]:
        for col in range(WIDTH):
            if col < 15 or col > 20:  # Leave gaps
                if is_valid_pos(row, col):
                    add_wall(map_data["cells"], row, col)

    # Vertical corridors
    for col in [10, 20, 30, 38]:
        for row in range(HEIGHT):
            if row < 8 or row > 12:  # Leave gaps
                if is_valid_pos(row, col):
                    add_wall(map_data["cells"], row, col)

    return map_data

def generate_maze_2():
    """Maze map 2: Complex maze with dead ends"""
    map_data = create_map_structure()

    # Create grid-based maze
    for row in range(0, HEIGHT, 4):
        for col in range(WIDTH):
            if is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    for col in range(0, WIDTH, 6):
        for row in range(HEIGHT):
            if is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    # Add openings
    openings = [(3, 12), (3, 24), (3, 36), (7, 6), (7, 18), (7, 30),
                (11, 12), (11, 24), (15, 6), (15, 18), (15, 30),
                (19, 12), (19, 24), (19, 36)]

    for row, col in openings:
        # Remove walls at openings
        map_data["cells"] = [c for c in map_data["cells"]
                            if not (c["row"] == row and c["col"] == col)]

    return map_data

def generate_maze_3():
    """Maze map 3: Spiral maze"""
    map_data = create_map_structure()

    # Outer walls
    for col in range(WIDTH):
        add_wall(map_data["cells"], 0, col)
        add_wall(map_data["cells"], HEIGHT - 1, col)

    for row in range(HEIGHT):
        add_wall(map_data["cells"], row, 0)
        add_wall(map_data["cells"], row, WIDTH - 1)

    # Spiral pattern
    layer = 0
    while layer < min(HEIGHT, WIDTH) // 4:
        # Top horizontal
        for col in range(3 + layer * 3, WIDTH - 3 - layer * 3):
            if is_valid_pos(3 + layer * 2, col):
                add_wall(map_data["cells"], 3 + layer * 2, col)

        # Right vertical
        for row in range(3 + layer * 2, HEIGHT - 3 - layer * 2):
            if is_valid_pos(row, WIDTH - 4 - layer * 3):
                add_wall(map_data["cells"], row, WIDTH - 4 - layer * 3)

        # Bottom horizontal
        for col in range(3 + layer * 3, WIDTH - 3 - layer * 3):
            if is_valid_pos(HEIGHT - 4 - layer * 2, col):
                add_wall(map_data["cells"], HEIGHT - 4 - layer * 2, col)

        layer += 1

    return map_data

def generate_maze_4():
    """Maze map 4: Branching maze"""
    map_data = create_map_structure()

    # Main horizontal corridors
    for row in [6, 13, 20]:
        for col in range(WIDTH):
            if is_valid_pos(row, col):
                add_wall(map_data["cells"], row, col)

    # Vertical branches
    branch_cols = [8, 16, 24, 32, 40]
    for col in branch_cols:
        for row in range(HEIGHT):
            if row not in [3, 10, 17, 23]:  # Leave gaps for passages
                if is_valid_pos(row, col):
                    add_wall(map_data["cells"], row, col)

    return map_data

def generate_maze_5():
    """Maze map 5: Recursive division style"""
    map_data = create_map_structure()

    def add_walls_recursive(min_col, max_col, min_row, max_row, cells):
        if max_col - min_col < 4 or max_row - min_row < 4:
            return

        # Choose random division points
        div_col = random.randint(min_col + 2, max_col - 2)
        div_row = random.randint(min_row + 2, max_row - 2)

        # Add vertical wall
        for row in range(min_row, max_row):
            if is_valid_pos(row, div_col):
                add_wall(cells, row, div_col)

        # Add horizontal wall
        for col in range(min_col, max_col):
            if is_valid_pos(div_row, col):
                add_wall(cells, div_row, col)

        # Add openings
        openings = [
            (random.randint(min_row, div_row - 1), div_col),
            (random.randint(div_row + 1, max_row - 1), div_col),
            (div_row, random.randint(min_col, div_col - 1)),
            (div_row, random.randint(div_col + 1, max_col - 1))
        ]

        for row, col in openings[:3]:  # Leave 3 openings
            cells[:] = [c for c in cells if not (c["row"] == row and c["col"] == col)]

        # Recurse
        add_walls_recursive(min_col, div_col, min_row, div_row, cells)
        add_walls_recursive(div_col + 1, max_col, min_row, div_row, cells)
        add_walls_recursive(min_col, div_col, div_row + 1, max_row, cells)
        add_walls_recursive(div_col + 1, max_col, div_row + 1, max_row, cells)

    add_walls_recursive(0, WIDTH, 0, HEIGHT, map_data["cells"])
    return map_data

# ==================== WEIGHTED MAPS ====================

def generate_weighted_1():
    """Weighted map 1: Random weights throughout"""
    map_data = create_map_structure()

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if random.random() < 0.4 and is_valid_pos(row, col):
                cost = random.randint(2, 9)
                add_weighted_cell(map_data["cells"], row, col, cost)

    return map_data

def generate_weighted_2():
    """Weighted map 2: Gradient weights (left to right)"""
    map_data = create_map_structure()

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if random.random() < 0.5 and is_valid_pos(row, col):
                # Cost increases from left to right
                cost = min(9, 2 + col // 6)
                add_weighted_cell(map_data["cells"], row, col, cost)

    return map_data

def generate_weighted_3():
    """Weighted map 3: Regional weights"""
    map_data = create_map_structure()

    # Define regions with different costs
    regions = [
        (0, 16, 0, 13, 3),      # Left region: cost 3
        (16, 32, 0, 13, 6),     # Middle-left: cost 6
        (32, WIDTH, 0, 13, 8),  # Right-top: cost 8
        (0, 16, 13, HEIGHT, 5), # Left-bottom: cost 5
        (16, 32, 13, HEIGHT, 4),# Middle-bottom: cost 4
        (32, WIDTH, 13, HEIGHT, 7) # Right-bottom: cost 7
    ]

    for min_col, max_col, min_row, max_row, cost in regions:
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                if random.random() < 0.6 and is_valid_pos(row, col):
                    add_weighted_cell(map_data["cells"], row, col, cost)

    return map_data

def generate_weighted_4():
    """Weighted map 4: Mixed weights and obstacles"""
    map_data = create_map_structure()

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if is_valid_pos(row, col):
                rand = random.random()
                if rand < 0.2:
                    add_wall(map_data["cells"], row, col)
                elif rand < 0.6:
                    cost = random.randint(2, 8)
                    add_weighted_cell(map_data["cells"], row, col, cost)

    return map_data

def generate_weighted_5():
    """Weighted map 5: High-cost surrounding low-cost path"""
    map_data = create_map_structure()

    # High cost background
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if is_valid_pos(row, col):
                add_weighted_cell(map_data["cells"], row, col, 8)

    # Low cost path in the middle
    for col in range(WIDTH):
        for dr in [-2, -1, 0, 1, 2]:
            row = HEIGHT // 2 + dr
            if is_valid_pos(row, col):
                # Remove high cost and add low cost
                map_data["cells"] = [c for c in map_data["cells"]
                                    if not (c["row"] == row and c["col"] == col)]
                add_weighted_cell(map_data["cells"], row, col, 2)

    # Add some obstacles to make it interesting
    for _ in range(10):
        row = random.randint(HEIGHT // 2 - 2, HEIGHT // 2 + 2)
        col = random.randint(0, WIDTH - 1)
        if is_valid_pos(row, col):
            map_data["cells"] = [c for c in map_data["cells"]
                                if not (c["row"] == row and c["col"] == col)]
            add_wall(map_data["cells"], row, col)

    return map_data

# ==================== MAIN GENERATION ====================

def main():
    """Generate all benchmark maps"""
    # Create maps directory if it doesn't exist
    maps_dir = "maps"
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)

    print("🎯 Generating 20 Benchmark Maps for Pathfinding Algorithm Testing\n")
    print("=" * 70)

    categories = [
        ("sparse", [
            ("sparse_1_scattered", generate_sparse_1),
            ("sparse_2_clusters", generate_sparse_2),
            ("sparse_3_short_walls", generate_sparse_3),
            ("sparse_4_large_blocks", generate_sparse_4),
            ("sparse_5_wide_spread", generate_sparse_5),
        ]),
        ("dense", [
            ("dense_1_random_40pct", generate_dense_1),
            ("dense_2_dense_clusters", generate_dense_2),
            ("dense_3_interlaced_bands", generate_dense_3),
            ("dense_4_random_45pct", generate_dense_4),
            ("dense_5_checkerboard", generate_dense_5),
        ]),
        ("maze", [
            ("maze_1_simple_corridors", generate_maze_1),
            ("maze_2_complex_deadends", generate_maze_2),
            ("maze_3_spiral", generate_maze_3),
            ("maze_4_branching", generate_maze_4),
            ("maze_5_recursive_division", generate_maze_5),
        ]),
        ("weighted", [
            ("weighted_1_random", generate_weighted_1),
            ("weighted_2_gradient", generate_weighted_2),
            ("weighted_3_regional", generate_weighted_3),
            ("weighted_4_mixed", generate_weighted_4),
            ("weighted_5_highcost_barrier", generate_weighted_5),
        ])
    ]

    total_maps = 0
    for category_name, maps in categories:
        print(f"\n📂 Category: {category_name.upper()}-OBSTACLE MAPS")
        print("-" * 70)

        for map_name, generator in maps:
            # Set seed for reproducibility
            random.seed(hash(map_name))

            map_data = generator()
            filepath = os.path.join(maps_dir, f"{map_name}.json")

            with open(filepath, 'w') as f:
                json.dump(map_data, f, indent=2)

            num_cells = len(map_data["cells"])
            print(f"  ✓ {map_name:30s} - {num_cells:4d} special cells")
            total_maps += 1

    print("\n" + "=" * 70)
    print(f"✅ Successfully generated {total_maps} benchmark maps!")
    print(f"📁 All maps saved in: {os.path.abspath(maps_dir)}/")
    print("\n📊 Map Statistics:")
    print("   - 5 Sparse-obstacle maps (10-30% coverage)")
    print("   - 5 Dense-obstacle maps (35-50% coverage)")
    print("   - 5 Maze-like maps (structured corridors)")
    print("   - 5 Weighted maps (varying traversal costs)")
    print("\n🧪 Ready for systematic algorithm testing!")

if __name__ == "__main__":
    main()
