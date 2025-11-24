import json
import random
import os
from collections import deque

# === 配置 ===
WIDTH = 49
HEIGHT = 26
MAP_COUNTS = 5
OUTPUT_DIR = "adversarial_maps_complex"


class SpecialMapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def _init_grid(self, fill_value=0):
        return [[fill_value for _ in range(self.width)] for _ in range(self.height)]

    # ---------------------------------------------------------
    # 1. 陷阱地图 (Trap): 5种变体，大幅提升复杂度
    # ---------------------------------------------------------
    def generate_trap(self, variant):
        # 尝试生成直到连通
        for _ in range(200):
            grid = self._init_grid(0)

            # 设置基本起终点 (Start左, Goal右)
            start = (self.height // 2, 2)
            goal = (self.height // 2, self.width - 3)

            # 核心：根据 variant 决定陷阱类型
            trap_type = variant % 5

            # --- Type A: The "G" Trap (倒钩) ---
            if trap_type == 0:
                wall_x = self.width // 2 + 8
                top_y = 4
                btm_y = self.height - 5
                # 背板
                for y in range(top_y, btm_y + 1): grid[y][wall_x] = 1
                # 侧翼
                for x in range(wall_x - 15, wall_x):
                    grid[top_y][x] = 1
                    grid[btm_y][x] = 1
                # 倒钩 (Hook) - 让它向内卷
                hook_len = 4
                for y in range(top_y, top_y + hook_len): grid[y][wall_x - 15] = 1
                for y in range(btm_y - hook_len, btm_y + 1): grid[y][wall_x - 15] = 1

                # 内部加一点干扰
                grid[self.height // 2][wall_x - 2] = 1

            # --- Type B: The Nested U (双层套娃) ---
            elif trap_type == 1:
                # 外层大 U (开口向左)
                outer_x = self.width // 2 + 12
                for y in range(2, self.height - 2): grid[y][outer_x] = 1
                for x in range(outer_x - 10, outer_x):
                    grid[2][x] = 1
                    grid[self.height - 3][x] = 1

                # 内层小 U (开口向右) - 挡在 Start 面前
                inner_x = self.width // 2 - 5
                for y in range(8, self.height - 8): grid[y][inner_x] = 1
                for x in range(inner_x, inner_x + 8):
                    grid[8][x] = 1
                    grid[self.height - 9][x] = 1

            # --- Type C: The Spiral (螺旋) ---
            elif trap_type == 2:
                # 把 Start 包起来
                c_x, c_y = start[0], start[1] + 5
                # 螺旋线绘制逻辑
                cursor = [c_y, c_x]  # x, y
                # 画一个方形螺旋
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
                lengths = [6, 12, 12, 16, 16]  # 逐渐变大

                # 简单手动绘制几层
                # 第一层(内)
                for y in range(6, 20): grid[y][10] = 1  # 左竖
                for x in range(10, 25): grid[6][x] = 1  # 上横
                for y in range(6, 20): grid[y][25] = 1  # 右竖
                for x in range(5, 25): grid[20][x] = 1  # 下横 (开口在左下)
                # 第二层(挡住开口)
                for y in range(20, 24): grid[y][5] = 1

            # --- Type D: The Broken Wall (参差不齐的墙) ---
            elif trap_type == 3:
                wall_x = self.width // 2 + 5
                # 生成一道锯齿状的墙
                for y in range(0, self.height):
                    # 墙体位置随机抖动
                    offset = random.randint(-1, 2)
                    grid[y][wall_x + offset] = 1
                    # 随机生成向左的“死胡同”分叉
                    if random.random() < 0.3:
                        branch_len = random.randint(2, 6)
                        for k in range(branch_len):
                            if wall_x + offset - k > 0:
                                grid[y][wall_x + offset - k] = 1

                # 强制挖一个极其隐蔽的洞 (在最上面或最下面)
                if random.random() > 0.5:
                    grid[1][wall_x - 1] = 0
                    grid[1][wall_x] = 0
                    grid[1][wall_x + 1] = 0
                else:
                    grid[self.height - 2][wall_x - 1] = 0
                    grid[self.height - 2][wall_x] = 0
                    grid[self.height - 2][wall_x + 1] = 0

            # --- Type E: The Debris Trap (乱石阵) ---
            elif trap_type == 4:
                # 标准深 U
                wall_x = self.width - 5
                for y in range(3, self.height - 3): grid[y][wall_x] = 1
                for x in range(10, wall_x):
                    grid[3][x] = 1
                    grid[self.height - 4][x] = 1

                # 内部填充大量随机碎石 (30% 密度)
                # 这会让算法在陷阱里“痛苦”地挣扎
                for y in range(4, self.height - 4):
                    for x in range(10, wall_x):
                        if random.random() < 0.25:
                            grid[y][x] = 1

            # 必须保证连通 (Type D 和 E 比较容易堵死，需要检查)
            if is_path_exists(grid, start, goal, self.width, self.height):
                return grid, start, goal
        return None, None, None

    # ---------------------------------------------------------
    # 2. 瓶颈地图: 增加房间内部的杂物，增加难度
    # ---------------------------------------------------------
    def generate_bottleneck(self, variant):
        for _ in range(100):
            grid = self._init_grid(0)
            start = (self.height // 2, 2)
            goal = (self.height // 2, self.width - 3)

            num_walls = random.randint(3, 5)  # 3-5个房间
            spacing = self.width // (num_walls + 1)

            for i in range(1, num_walls + 1):
                x = i * spacing + random.randint(-1, 1)
                for y in range(self.height):
                    grid[y][x] = 1

                # 开门
                door_y = random.randint(1, self.height - 2)
                grid[door_y][x] = 0
                grid[door_y - 1][x] = 0  # 门宽2

                # 在房间内部加一些随机柱子，阻碍视线
                prev_x = (i - 1) * spacing
                for _ in range(5):
                    rx = random.randint(prev_x + 2, x - 2)
                    ry = random.randint(2, self.height - 3)
                    grid[ry][rx] = 1

            if is_path_exists(grid, start, goal, self.width, self.height):
                return grid, start, goal
        return None, None, None

    # ---------------------------------------------------------
    # 3. 沼泽地图: 保持高对比度
    # ---------------------------------------------------------
    def generate_swamp(self, variant):
        grid = self._init_grid(0)
        start = (self.height // 2, 2)
        goal = (self.height // 2, self.width - 3)
        swamp_margin_top = 6
        swamp_margin_bottom = self.height - 7
        for y in range(self.height):
            for x in range(self.width):
                if swamp_margin_top < y < swamp_margin_bottom:
                    grid[y][x] = random.randint(20, 50)  # 极高权重
                else:
                    grid[y][x] = 0
        return grid, start, goal

    # ---------------------------------------------------------
    # 4. 锯齿森林: 增加噪点干扰
    # ---------------------------------------------------------
    def generate_jagged(self, variant):
        while True:
            grid = self._init_grid(0)
            start = (1, 1)
            goal = (self.height - 2, self.width - 2)

            # 混合模式：同时使用斜线和噪点
            spacing = random.randint(3, 4)
            direction = random.choice([1, -1])

            for y in range(self.height):
                for x in range(self.width):
                    # 基础斜线
                    if (x + direction * y) % spacing == 0:
                        if random.random() > 0.35:  # 65% 墙
                            grid[y][x] = 1

                    # 额外噪点 (增加不规则度)
                    if random.random() < 0.05:
                        grid[y][x] = 1

            # 保护起终点
            for r in range(start[0] - 2, start[0] + 3):
                for c in range(start[1] - 2, start[1] + 3):
                    if 0 <= r < self.height and 0 <= c < self.width: grid[r][c] = 0
            for r in range(goal[0] - 2, goal[0] + 3):
                for c in range(goal[1] - 2, goal[1] + 3):
                    if 0 <= r < self.height and 0 <= c < self.width: grid[r][c] = 0

            if is_path_exists(grid, start, goal, self.width, self.height):
                return grid, start, goal


# === 工具函数 ===
def is_path_exists(grid, start, goal, width, height):
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return False
    q = deque([start])
    visited = set([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal: return True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
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
    data = {"width": width, "height": height, "start": start, "goal": goal, "cells": cells}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    gen = SpecialMapGenerator(WIDTH, HEIGHT)
    map_types = {"trap": gen.generate_trap, "bottleneck": gen.generate_bottleneck,
                 "swamp": gen.generate_swamp, "jagged": gen.generate_jagged}
    print(f"开始生成高复杂度对抗地图 (output: {OUTPUT_DIR})...")
    for type_name, func in map_types.items():
        for i in range(1, MAP_COUNTS + 1):
            grid, start, goal = func(i)
            if grid:
                filename = os.path.join(OUTPUT_DIR, f"{type_name}_{i}.json")
                save_map_json(grid, start, goal, WIDTH, HEIGHT, filename)
                print(f"  [√] Generated: {type_name}_{i} (Type {i % 5 if type_name == 'trap' else 'Rand'})")
            else:
                print(f"  [X] Failed: {type_name}_{i}")


if __name__ == "__main__":
    main()