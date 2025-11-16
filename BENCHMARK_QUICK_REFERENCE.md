# 🎯 Benchmark Maps Quick Reference

## 📋 Complete Map List

### 🟢 SPARSE-OBSTACLE (10-30% coverage)
```
✓ sparse_1_scattered          (12 cells)   - Random scattered obstacles
✓ sparse_2_clusters           (18 cells)   - Small clustered obstacles
✓ sparse_3_short_walls        (26 cells)   - Short wall segments
✓ sparse_4_large_blocks       (48 cells)   - Large rectangular blocks
✓ sparse_5_wide_spread        (38 cells)   - Widely distributed obstacles
```

### 🔴 DENSE-OBSTACLE (35-50% coverage)
```
✓ dense_1_random_40pct        (461 cells)  - 40% random coverage
✓ dense_2_dense_clusters      (131 cells)  - Multiple dense clusters
✓ dense_3_interlaced_bands    (227 cells)  - Vertical/horizontal bands
✓ dense_4_random_45pct        (560 cells)  - 45% random coverage
✓ dense_5_checkerboard        (338 cells)  - Checkerboard pattern
```

### 🔵 MAZE-LIKE (Corridors & Dead Ends)
```
✓ maze_1_simple_corridors     (252 cells)  - Basic corridor structure
✓ maze_2_complex_deadends     (529 cells)  - Complex with dead ends
✓ maze_3_spiral               (531 cells)  - Spiral maze pattern
✓ maze_4_branching            (252 cells)  - Branching corridors
✓ maze_5_recursive_division   (469 cells)  - Recursive division
```

### 🟡 WEIGHTED (Varying Costs)
```
✓ weighted_1_random           (517 cells)  - Random weights 2-9
✓ weighted_2_gradient         (634 cells)  - Left-to-right gradient
✓ weighted_3_regional         (790 cells)  - Regional cost zones
✓ weighted_4_mixed            (742 cells)  - Mixed weights + obstacles
✓ weighted_5_highcost_barrier (1246 cells) - High cost barrier
```

## 🏆 Algorithm Expectations by Category

| Category | BFS | DFS | Dijkstra | GBFS | A* |
|----------|-----|-----|----------|------|-----|
| **Sparse** | ⭐⭐⭐ Optimal | ⭐⭐ Fast | ⭐⭐⭐ Optimal | ⭐⭐⭐ Fast | ⭐⭐⭐ Optimal+Fast |
| **Dense** | ⭐⭐ Slow | ⭐ May fail | ⭐⭐ Optimal but slow | ⭐⭐ Fast | ⭐⭐⭐ Best balance |
| **Maze** | ⭐⭐ Explores all | ⭐ Deep paths | ⭐⭐ Optimal | ⭐⭐⭐ Good heuristic | ⭐⭐⭐ Excellent |
| **Weighted** | ⭐ Wrong cost | ⭐ Not optimal | ⭐⭐⭐ Optimal | ⭐⭐ Fast | ⭐⭐⭐ Optimal+Fast |

## 📊 Testing Priority Order

### For Beginners (Start Here)
1. `sparse_1_scattered` - Easiest map
2. `weighted_1_random` - See weight effects
3. `maze_1_simple_corridors` - Basic maze

### For Complete Testing
**Day 1**: Sparse + Dense (10 maps)
```bash
sparse_1_scattered → sparse_2_clusters → ... → dense_5_checkerboard
```

**Day 2**: Maze + Weighted (10 maps)
```bash
maze_1_simple_corridors → ... → weighted_5_highcost_barrier
```

### For Specific Comparisons

**BFS vs A\*** (Show heuristic benefit):
- `dense_4_random_45pct`
- `maze_2_complex_deadends`

**Dijkstra vs A\*** (Weighted graphs):
- `weighted_2_gradient`
- `weighted_3_regional`
- `weighted_5_highcost_barrier`

**GBFS vs A\*** (Optimality trade-off):
- `maze_3_spiral`
- `weighted_4_mixed`

## 🎯 Testing Modes

### Mode 1: Single Map, All Algorithms
```
Load Map → "Run All" → "Current Maze"
⏱️ Time: ~2 minutes per map
📊 Output: Comparison table
```

### Mode 2: All Maps, Single Algorithm
```
Select Algorithm → "Run All" → "Different Mazes"
⏱️ Time: ~10 minutes (5 mazes × 2 min)
📊 Output: Average performance
```

### Mode 3: Manual Individual Testing
```
Load Map → Select Algorithm → "VISUALISE"
⏱️ Time: ~1 minute per test
📊 Output: Detailed visualization
```

## 💾 File Locations

```
maps/
├── sparse_1_scattered.json
├── sparse_2_clusters.json
├── sparse_3_short_walls.json
├── sparse_4_large_blocks.json
├── sparse_5_wide_spread.json
├── dense_1_random_40pct.json
├── dense_2_dense_clusters.json
├── dense_3_interlaced_bands.json
├── dense_4_random_45pct.json
├── dense_5_checkerboard.json
├── maze_1_simple_corridors.json
├── maze_2_complex_deadends.json
├── maze_3_spiral.json
├── maze_4_branching.json
├── maze_5_recursive_division.json
├── weighted_1_random.json
├── weighted_2_gradient.json
├── weighted_3_regional.json
├── weighted_4_mixed.json
└── weighted_5_highcost_barrier.json
```

## 🔑 Key Insights to Look For

### Sparse Maps
- **All algorithms perform similarly**
- Small differences in steps explored
- Good baseline for comparison

### Dense Maps
- **A\* significantly outperforms BFS**
- Heuristic guidance becomes crucial
- DFS may struggle

### Maze Maps
- **Heuristic algorithms excel**
- BFS explores methodically
- Shows benefit of informed search

### Weighted Maps
- **Only Dijkstra/A\* guarantee optimal cost**
- BFS finds short path, not cheap path
- Best demonstration of A* superiority

## 📈 Expected Results Summary

| Metric | Best Algorithm | Worst Algorithm |
|--------|---------------|-----------------|
| **Steps Explored** | A* | BFS (dense) |
| **Path Optimality** | Dijkstra, A* | DFS, GBFS |
| **Execution Speed** | GBFS | BFS (dense) |
| **Overall Balance** | **A\*** | DFS |

## ⚡ Quick Test Sequence (30 min)

```
1. sparse_1_scattered      → Run All → Record
2. dense_4_random_45pct    → Run All → Record
3. maze_2_complex_deadends → Run All → Record
4. weighted_3_regional     → Run All → Record
5. weighted_5_highcost_barrier → Run All → Record
```

These 5 maps cover all categories and show clear algorithm differences!

---

**Total Maps**: 20
**Total Tests**: 100 (20 maps × 5 algorithms)
**Estimated Time**: 40-60 minutes (automated) | 2-3 hours (manual)

🎓 **Remember**:
- Sparse = Easy baseline
- Dense = Algorithm stress test
- Maze = Heuristic showcase
- Weighted = Optimality test
