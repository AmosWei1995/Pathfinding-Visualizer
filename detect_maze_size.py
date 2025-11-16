"""
Detect the actual maze size used by the visualizer
"""
import sys
import pygame

# Initialize pygame to get display info
pygame.font.init()
pygame.display.init()

# Copy the same logic from constants.py
WINDOW_INFO = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_INFO.current_w, WINDOW_INFO.current_h
WIDTH = 1280 if SCREEN_WIDTH >= 1280 else SCREEN_WIDTH - 150
HEIGHT = 900 if SCREEN_HEIGHT >= 900 else SCREEN_HEIGHT - 150
HEADER_HEIGHT = 200

# Cell size (default)
CELL_SIZE = 26
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.startswith("--cell-size:"):
        size = int(arg.split(":")[1])
        if 10 <= size <= 90:
            CELL_SIZE = size

# Calculate maze dimensions (same as constants.py)
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

print("=" * 60)
print("Current Maze Dimensions Detection")
print("=" * 60)
print(f"Screen Size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
print(f"Window Size: {WIDTH}x{HEIGHT}")
print(f"Cell Size: {CELL_SIZE}")
print(f"Header Height: {HEADER_HEIGHT}")
print("-" * 60)
print(f"REMAINDER_W: {REMAINDER_W}")
print(f"REMAINDER_H: {REMAINDER_H}")
print(f"MAZE_WIDTH: {MAZE_WIDTH}")
print(f"MAZE_HEIGHT: {MAZE_HEIGHT}")
print("-" * 60)
print(f"✓ Grid Width: {grid_width}")
print(f"✓ Grid Height: {grid_height}")
print("=" * 60)
print(f"\nUse these values for benchmark maps:")
print(f"WIDTH = {grid_width}")
print(f"HEIGHT = {grid_height}")
print("\nRecommended start/goal positions:")
print(f"START = [{grid_height // 2}, {grid_width // 4}]")
print(f"GOAL = [{grid_height // 2}, {grid_width - grid_width // 4 - 1}]")
