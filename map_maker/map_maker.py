import json
import random
import os
from collections import deque

# === 配置参数 ===
WIDTH = 49
HEIGHT = 26  # 保持修正后的高度

MAP_COUNTS = 5
OUTPUT_DIR = "generated_maps"


class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def _init_grid(self, fill_value=0):
        return [[fill_value for _ in range(self.width)] for _ in range(self.height)]

    # === 核心修改逻辑 ===

    # 1. Sparse (稀疏): 纯随机，低密度
    # "很碎的墙，但墙壁密度低"
    def generate_sparse(self, density=0.1):
        grid = self._init_grid(0)
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    grid[y][x] = 1
        return grid

    # 2. Dense (密集): 纯随机，高密度 (不再进行平滑演化)
    # "很碎的墙壁，并且墙壁密度大"
    def generate_dense(self, density=0.40):
        # 注意：这里直接使用随机分布，不再使用元胞自动机(Cellular Automata)
        # 这样墙壁就是“碎”的，而不是“块状”的。
        # density=0.40 意味着40%的格子是墙，对于随机图来说这个密度已经非常高了。
        grid = self._init_grid(0)
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    grid[y][x] = 1
        return grid

    # 3. Maze (迷宫): 保持不变，结构化墙壁
    def generate_maze(self):
        grid = self._init_grid(1)

        def carve(cx, cy):
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 1 <= ny < self.height - 1 and 1 <= nx < self.width - 1 and grid[ny][nx] == 1:
                    grid[cy + dy // 2][cx + dx // 2] = 0
                    grid[ny][nx] = 0
                    carve(nx, ny)

        # 选取奇数坐标开始
        start_y, start_x = 1, 1
        grid[start_y][start_x] = 0
        carve(start_x, start_y)
        return grid

    # 4. Weighted (加权): 保持不变
    def generate_weighted(self, num_zones=6):
        # 基础是稀疏障碍
        grid = self.generate_sparse(0.05)
        # 叠加随机权重区
        for _ in range(num_zones):
            cx = random.randint(0, self.width - 1)
            cy = random.randint(0, self.height - 1)
            radius = random.randint(3, 8)
            weight = random.randint(2, 9)

            for y in range(max(0, cy - radius), min(self.height, cy + radius)):
                for x in range(max(0, cx - radius), min(self.width, cx + radius)):
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                        if grid[y][x] == 0:
                            grid[y][x] = weight
        return grid


# === 连通性检查 (确保即使障碍物碎且密，也有路可走) ===

def get_valid_start_goal(grid, width, height):
    # 尝试寻找连通的起终点，最多尝试 2000 次
    # 在高密度随机图中，死路非常多，所以需要多试几次找到连通点
    for _ in range(2000):
        s = (random.randint(0, height - 1), random.randint(0, width - 1))
        g = (random.randint(0, height - 1), random.randint(0, width - 1))

        # 必须是空地
        if grid[s[0]][s[1]] == 1 or grid[g[0]][g[1]] == 1:
            continue

        # 必须有一定距离 (曼哈顿距离)
        dist = abs(s[0] - g[0]) + abs(s[1] - g[1])
        if dist < (width + height) // 3:
            continue

        # 必须连通
        if is_path_exists(grid, s, g, width, height):
            return s, g
    return None, None


def is_path_exists(grid, start, goal, width, height):
    q = deque([start])
    visited = set([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                # 0(路) 和 >1(权重) 都可以走，只有 1(墙) 不能走
                if grid[nr][nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
    return False


def save_map_json(grid, start, goal, width, height, filename):
    cells = []
    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            if val == 1:
                cells.append({"row": r, "col": c, "value": "#", "cost": -1})
            elif val > 1:
                cells.append({"row": r, "col": c, "value": str(val), "cost": val})

    data = {
        "width": width,
        "height": height,
        "start": [start[0], start[1]],
        "goal": [goal[0], goal[1]],
        "cells": cells
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    gen = MapGenerator(WIDTH, HEIGHT)
    categories = {
        "sparse": gen.generate_sparse,
        "dense": gen.generate_dense,
        "maze": gen.generate_maze,
        "weighted": gen.generate_weighted
    }

    print(f"开始生成地图 (Height={HEIGHT}, Width={WIDTH})...")
    print("注意：Dense 模式现在是高密度碎片墙，寻找可行路径可能需要多次重试，请稍候。")

    for cat_name, gen_func in categories.items():
        count = 0
        attempts = 0
        while count < MAP_COUNTS:
            attempts += 1
            grid = gen_func()

            # 尝试在这个网格中找路
            start, goal = get_valid_start_goal(grid, WIDTH, HEIGHT)

            if start and goal:
                count += 1
                filename = os.path.join(OUTPUT_DIR, f"{cat_name}_{count}.json")
                save_map_json(grid, start, goal, WIDTH, HEIGHT, filename)
                print(f"  [√] Generated: {filename}")
            else:
                # Dense 模式下，如果生成的图实在太堵（连通区域太小），就废弃这张图重生成
                if attempts % 10 == 0:
                    print(f"      ...{cat_name} 正在尝试生成可行解 (已尝试 {attempts} 次)...")
                pass

    print("\n所有 20 张地图生成完毕！")


if __name__ == "__main__":
    main()