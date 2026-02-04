# UI/UX Enhancements Documentation

This document describes the new UI/UX features added to CompPy.

## Features Implemented

### 1. Tooltips & Context-Sensitive Help

**What it does:** All input fields now have helpful tooltips that explain the parameter, its purpose, and valid ranges.

**How to use:**
- Hover your mouse over any input field
- A tooltip will appear with:
  - Parameter description
  - Usage guidance
  - Valid range of values

**Enhanced validation feedback:**
- 🟢 **Green**: Value is valid and acceptable
- 🟡 **Yellow**: Value is incomplete or approaching limits - tooltip shows valid range
- 🔴 **Red**: Value is invalid - tooltip shows error message and valid range

### 2. Undo/Redo Functionality

**What it does:** Track all parameter changes and revert them if needed.

**How to use:**
- Make changes to any parameter
- Press `Ctrl+Z` or use `File > Undo` to undo the last change
- Press `Ctrl+Y` or use `File > Redo` to redo an undone change
- Undo/redo buttons are disabled when there's nothing to undo/redo

**Features:**
- Tracks up to 50 changes
- Works across all stages
- Automatically clears when loading a file or preset

### 3. Parameter Presets

**What it does:** Quickly load pre-configured compressor designs for common applications.

**How to use:**
1. Click `Presets` in the menu bar
2. Choose from available presets:
   - **Micro Turbine - Single Stage**: Small high-speed compressor for micro gas turbines
   - **RC Ducted Fan - High Speed**: High-performance ducted fan for RC aircraft
   - **Industrial Compressor - Low Speed**: Large low-speed compressor for industrial use
   - **High Pressure Ratio - Multi-Stage**: Aggressive design for high pressure applications
   - **Educational Example - Simple**: Simple parameters for learning
3. Confirm loading the preset (this will replace current stage values)

**Benefits:**
- Jump-start your design with proven configurations
- Learn from example designs
- Quick comparison of different compressor types

### 4. Assembly Viewer (3D)

**What it does:** View all stages together in a 3D assembly with interactive controls.

**How to use:**
1. Create multiple stages in your compressor design
2. Click `Tools > Assembly Viewer`
3. Use the controls in the viewer:
   - **Front View**: View from the front
   - **Side View**: View from the side  
   - **Top View**: View from above
   - **Isometric**: 3D isometric view
   - **Start Animation**: Rotate rotors to see motion
   - **Cross Section**: Show half of assembly (cutaway view)

**Features:**
- Shows all stages correctly spaced
- Rotors in blue, stators in orange
- Real-time rotation animation
- Multiple camera views
- Mouse controls: Right-click to rotate, left-click to zoom

### 5. Drag-and-Drop Stage Reordering

**What it does:** Reorder stages by dragging them in the stage list.

**How to use:**
1. Click and hold on a stage in the list
2. Drag it to a new position
3. Release to drop it there

**Note:** Stage data moves with the stage name.

### 6. Real-time Validation Feedback

**What it does:** Immediate visual and text feedback when entering parameters.

**How it works:**
- As you type, the input field color changes
- Tooltip updates to show:
  - What you're entering
  - Whether it's valid
  - What the valid range is
- No need to click away or press Enter to see validation

### 7. Keyboard Shortcuts

New keyboard shortcuts for faster workflow:

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

## Tips and Best Practices

### Starting a New Design

1. **Use a preset** as starting point from `Presets` menu
2. **Modify parameters** to suit your needs
3. **Check tooltips** if unsure about a parameter
4. **Use undo** if you make a mistake

### Working with Multiple Stages

1. **Add stages** one at a time
2. **Fill parameters** for each stage
3. **Use Assembly Viewer** to see how stages fit together
4. **Reorder stages** by dragging if needed

### Validation

1. **Hover over yellow/red fields** to see what's wrong
2. **Check the tooltip** for valid ranges
3. **Fix invalid values** before rendering
4. Fields must be **green** to render successfully

### Presets

- Presets are **starting points**, not final designs
- Always **validate** preset values for your application
- **Modify** presets to match your specific requirements
- Consider **safety margins** for mechanical stress and temperatures

## Technical Details

### Undo/Redo Implementation

- Uses a stack-based approach
- Stores: stage index, field name, old value, new value
- Maximum 50 states in history
- Cleared on file load or preset application

### Tooltip System

- Centralized tooltip database in `Tooltips.py`
- Includes parameter descriptions and valid ranges
- Updates dynamically based on validation state
- Shows context-sensitive help

### Preset System

- Preset definitions in `Presets.py`
- Each preset includes:
  - Stage parameters (Reaction, Loading, Flow, RPM, Mean Line Radius)
  - Rotor parameters (all blade geometry)
  - Stator parameters (all vane geometry)
- Easy to add custom presets by editing `Presets.py`

### Assembly Viewer

- Uses matplotlib 3D rendering
- Meshes generated from existing blade rendering code
- Supports animation via matplotlib FuncAnimation
- Configurable views and cross-sections

## Troubleshooting

### Assembly Viewer won't open
- Ensure you have at least one stage created
- Check that matplotlib is installed: `pip install matplotlib`
- Try rendering individual stages first to verify geometry

### Undo/Redo not working
- Ensure you've made changes to input fields
- Check that fields have focus and values changed
- Undo only tracks user edits, not programmatic changes

### Tooltips not showing
- Ensure you're hovering over input fields (not labels)
- Wait a moment for tooltip to appear
- Check that input fields are enabled

### Preset won't load
- Ensure you have at least one stage created
- Confirm the preset selection in the dialog
- Check console for error messages

## Future Enhancements

Potential additions being considered:
- Save/load custom presets
- Export assembly to CAD formats
- Flow visualization in assembly viewer
- Parametric studies with preset variations
- Comparison view for multiple designs

## Feedback

If you encounter issues or have suggestions for improvements, please open an issue on the project repository.
