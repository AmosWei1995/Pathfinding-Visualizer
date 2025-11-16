# 🧪 Benchmark Testing Guide

## Overview

This guide provides instructions for systematic testing of pathfinding algorithms using 20 carefully designed benchmark maps.

## 🎯 Test Setup

### Algorithms Under Test
1. **Breadth-First Search (BFS)** - Uninformed search
2. **Depth-First Search (DFS)** - Uninformed search
3. **Dijkstra's Algorithm** - Optimal path finder
4. **Greedy Best-First Search (GBFS)** - Heuristic search
5. **A\* Search** - Optimal heuristic search

### Map Categories (5 maps each)

#### 1️⃣ Sparse-Obstacle Maps
**Characteristics**: Large open spaces with minimal obstacles (10-30% coverage)

| Map Name | Description | Special Cells |
|----------|-------------|---------------|
| `sparse_1_scattered` | Randomly scattered obstacles | 12 |
| `sparse_2_clusters` | Small clustered obstacles | 18 |
| `sparse_3_short_walls` | Short wall segments | 26 |
| `sparse_4_large_blocks` | Large rectangular blocks | 48 |
| `sparse_5_wide_spread` | Widely distributed obstacles | 38 |

**Expected Behavior**:
- BFS: Should find shortest path quickly
- DFS: May find non-optimal paths
- Dijkstra: Optimal path (same as BFS for uniform cost)
- GBFS: Fast but may not be optimal
- A*: Optimal path with good performance

#### 2️⃣ Dense-Obstacle Maps
**Characteristics**: Many obstacles creating complex navigation (35-50% coverage)

| Map Name | Description | Special Cells |
|----------|-------------|---------------|
| `dense_1_random_40pct` | 40% random obstacle coverage | 461 |
| `dense_2_dense_clusters` | Multiple dense obstacle clusters | 131 |
| `dense_3_interlaced_bands` | Interlaced vertical/horizontal bands | 227 |
| `dense_4_random_45pct` | 45% random obstacle coverage | 560 |
| `dense_5_checkerboard` | Checkerboard-like pattern | 338 |

**Expected Behavior**:
- BFS: Reliable but slower due to many nodes
- DFS: May get stuck in dead ends
- Dijkstra: Optimal but explores many nodes
- GBFS: May find path quickly but suboptimal
- A*: Good balance of optimality and performance

#### 3️⃣ Maze-Like Maps
**Characteristics**: Structured corridors, dead ends, and narrow passages

| Map Name | Description | Special Cells |
|----------|-------------|---------------|
| `maze_1_simple_corridors` | Basic corridor structure | 252 |
| `maze_2_complex_deadends` | Complex with many dead ends | 529 |
| `maze_3_spiral` | Spiral maze pattern | 531 |
| `maze_4_branching` | Branching corridors | 252 |
| `maze_5_recursive_division` | Recursive division algorithm | 469 |

**Expected Behavior**:
- BFS: Explores level by level, guaranteed optimal
- DFS: May explore deep dead ends first
- Dijkstra: Same as BFS for uniform cost
- GBFS: May follow heuristic into dead ends
- A*: Efficient with good heuristic

#### 4️⃣ Weighted Maps
**Characteristics**: Varying traversal costs representing different terrain

| Map Name | Description | Special Cells |
|----------|-------------|---------------|
| `weighted_1_random` | Random weights (2-9) | 517 |
| `weighted_2_gradient` | Gradient from left to right | 634 |
| `weighted_3_regional` | Different cost regions | 790 |
| `weighted_4_mixed` | Mixed weights and obstacles | 742 |
| `weighted_5_highcost_barrier` | High cost surrounds low cost path | 1246 |

**Expected Behavior**:
- BFS: May not find optimal path (ignores weights)
- DFS: Not suitable for weighted graphs
- Dijkstra: **Guaranteed optimal** path by total cost
- GBFS: Fast but may choose high-cost paths
- A*: **Optimal** with better performance than Dijkstra

## 📊 Testing Procedure

### Option 1: Manual Testing

1. **Load Map**
   ```
   Click "Load Map" → Select map (e.g., sparse_1_scattered)
   ```

2. **Select Algorithm**
   ```
   Click "Algorithms" → Choose algorithm (e.g., A* Search)
   ```

3. **Run Visualization**
   ```
   Click "VISUALISE" → Observe animation
   ```

4. **Record Results**
   - Steps explored
   - Path length
   - Path cost
   - Time taken

5. **Repeat for All Algorithms**

### Option 2: Automated Comparison

1. **Load Map**
   ```
   Click "Load Map" → Select map
   ```

2. **Run All Algorithms**
   ```
   Click "Run All" → "Current Maze"
   ```

3. **View Comparison Results**
   - Automatically runs all 5 algorithms
   - Displays comparison table
   - Shows rankings by time

## 📈 Data Collection Template

### Per-Map Results Table

| Algorithm | Steps Explored | Path Length | Path Cost | Time (ms) | Optimal? |
|-----------|---------------|-------------|-----------|-----------|----------|
| BFS       |               |             |           |           |          |
| DFS       |               |             |           |           |          |
| Dijkstra  |               |             |           |           |          |
| GBFS      |               |             |           |           |          |
| A*        |               |             |           |           |          |

### Category Summary Template

**Category**: [Sparse/Dense/Maze/Weighted]

| Algorithm | Avg Steps | Avg Path Length | Avg Time | Win Rate |
|-----------|-----------|----------------|----------|----------|
| BFS       |           |                |          |          |
| DFS       |           |                |          |          |
| Dijkstra  |           |                |          |          |
| GBFS      |           |                |          |          |
| A*        |           |                |          |          |

## 🔬 Analysis Guidelines

### Key Metrics to Compare

1. **Steps Explored**
   - Number of nodes visited during search
   - Lower is better (more efficient)
   - Shows search space efficiency

2. **Path Length**
   - Number of steps in final path
   - Important for uniform-cost graphs
   - BFS and A* should be optimal

3. **Path Cost**
   - Total cost of traversing the path
   - Critical for weighted graphs
   - Dijkstra and A* should be optimal

4. **Time Taken**
   - Execution time in milliseconds
   - Real-world performance metric
   - Includes both search and path construction

### Expected Patterns

**Sparse Maps**:
- All algorithms should perform well
- Small differences in steps explored
- Similar path lengths for most algorithms

**Dense Maps**:
- BFS explores many nodes
- A* should significantly outperform BFS
- DFS may fail to find optimal paths

**Maze Maps**:
- Heuristic algorithms (GBFS, A*) excel
- BFS explores level by level
- DFS may explore deep paths first

**Weighted Maps**:
- **Only Dijkstra and A* guarantee optimal path**
- BFS finds shortest path but not lowest cost
- A* should be faster than Dijkstra

## 🎓 Research Questions

1. **Performance vs. Optimality Trade-off**
   - How much faster is GBFS than A*?
   - What is the cost in path quality?

2. **Heuristic Effectiveness**
   - In which map types does A* show the most improvement over Dijkstra?
   - When does the heuristic mislead GBFS?

3. **Worst-Case Scenarios**
   - Which maps cause the most divergence between algorithms?
   - When does DFS perform particularly poorly?

4. **Scalability**
   - How do algorithms scale with obstacle density?
   - Which algorithm is most robust across all categories?

## 📋 Testing Checklist

- [ ] Generate all 20 benchmark maps
- [ ] Test each algorithm on all 5 sparse maps
- [ ] Test each algorithm on all 5 dense maps
- [ ] Test each algorithm on all 5 maze maps
- [ ] Test each algorithm on all 5 weighted maps
- [ ] Record results for all 100 tests (20 maps × 5 algorithms)
- [ ] Calculate category averages
- [ ] Analyze patterns and trends
- [ ] Identify best/worst case scenarios
- [ ] Document findings

## 🚀 Quick Start

```bash
# 1. Generate maps (already done!)
python3 generate_benchmark_maps.py

# 2. Start visualizer
python3 run.pyw

# 3. Load first map
Click "Load Map" → sparse_1_scattered

# 4. Run all algorithms
Click "Run All" → "Current Maze"

# 5. Save results and move to next map
```

## 💡 Tips

1. **Use "Run All"** for quick comparisons on single maps
2. **Use "Different Mazes"** to test one algorithm across all maps in a category
3. **Save interesting results** by taking screenshots
4. **Reset between tests** using "Clear Walls" if needed
5. **Consistent testing** - use the same speed setting for all tests

## 📊 Expected Timeline

- **Per map (manual)**: ~5 minutes (1 min per algorithm)
- **Per map (automated)**: ~2 minutes
- **Full benchmark**: ~40 minutes (20 maps × 2 min)
- **With analysis**: ~2-3 hours

Good luck with your experiments! 🎯
