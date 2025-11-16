# 🎯 Load Map Menu Scrolling Feature

## ✨ Overview

The Load Map menu now supports scrolling to display all saved maps, regardless of how many you have!

## 🖱️ How to Use

### Opening the Menu
1. Click the **"Load Map"** button (blue button in the top right area)
2. The menu will appear showing up to 10-25 maps at once (depending on screen size)

### Scrolling Through Maps
**Mouse Wheel**:
- Scroll **UP** → See earlier maps
- Scroll **DOWN** → See later maps

**Indicator**:
- Bottom of the menu shows: `(1-15 of 23) - Scroll for more`
- This tells you:
  - Currently viewing items 1-15
  - Total of 23 maps available
  - You can scroll to see more

### Selecting a Map
- Click on any visible map name to load it
- Menu will automatically close after selection
- Scroll position resets when menu closes

## 📊 Technical Details

### Adaptive Display
- **Screen Height**: Automatically calculates how many items fit
- **Minimum Items**: Always shows at least 10 items
- **Maximum Items**: Up to 25 items visible (depending on screen height)

### Compact Design
- **Font Size**: 14px (smaller for more items)
- **Padding**: 3px (compact spacing)
- **Item Height**: ~28px per map

### Smart Scrolling
- **Bounds Checking**: Can't scroll past first or last item
- **Smooth Scrolling**: One item per scroll wheel tick
- **Auto-Reset**: Scroll position resets when menu closes

## 🎨 Visual Indicators

```
┌─────────────────────────────────┐
│ Load Map                  ▼     │ ← Button
├─────────────────────────────────┤
│ benchmark_maze_1                │ ← Map 1
│ benchmark_maze_2                │ ← Map 2
│ ...                             │
│ dense_4_random_45pct            │ ← Map 15
├─────────────────────────────────┤
│ (1-15 of 23) - Scroll for more  │ ← Indicator
└─────────────────────────────────┘
    ↑ Scroll wheel here
```

## 📈 Capacity

**Before (Limited)**:
- Maximum 10 maps shown
- No way to see additional maps

**After (Scrollable)**:
- ✅ Shows ALL saved maps
- ✅ Scroll to navigate
- ✅ Clear indication of position
- ✅ Supports unlimited maps

## 💡 Tips

1. **Finding Your Map**
   - Maps are sorted by date (newest first)
   - Benchmark maps appear alphabetically
   - Use scroll wheel to browse quickly

2. **Screen Space**
   - Larger screens show more items at once
   - Menu automatically adapts to your screen height
   - Minimum 10 items always visible

3. **Quick Navigation**
   - Scroll fast by holding mouse button and wheeling
   - Position indicator helps you know where you are
   - Recent maps appear first (no scrolling needed)

## 🔧 Implementation Details

### Scroll State Management
```python
load_map_scroll_offset = 0  # Current scroll position
max_visible_items = 15      # Items visible at once
total_maps = 23             # Total maps available

# Visible range
start_idx = scroll_offset
end_idx = start_idx + max_visible_items
```

### Event Handling
```python
# Mouse wheel event
if event.type == pygame.MOUSEWHEEL:
    load_map_scroll_offset -= event.y
    # Clamp to valid range
    load_map_scroll_offset = max(0, min(max_scroll, load_map_scroll_offset))
    # Recreate menu with new position
    load_map_menu = create_load_map_menu()
```

## 🎯 Benefits

1. **Scalability**: Support for 100+ maps
2. **Usability**: Easy navigation with mouse wheel
3. **Visibility**: Clear indicators of position
4. **Performance**: Only renders visible items
5. **Adaptability**: Works on any screen size

## 📝 Example Usage

### With 20 Benchmark Maps
1. Click "Load Map"
2. See first 15 maps: `sparse_1_scattered` through `maze_1_simple_corridors`
3. Scroll down to see: `maze_2_complex_deadends` through `weighted_5_highcost_barrier`
4. Click desired map
5. Menu closes automatically

### With 50+ Maps
1. Click "Load Map"
2. Indicator shows: `(1-15 of 52) - Scroll for more`
3. Scroll wheel to navigate all 52 maps
4. Select any map from the entire collection

---

**Note**: This feature is automatically enabled - no configuration needed!
