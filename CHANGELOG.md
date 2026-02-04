# Changelog

## [2.0.0] - 2026-02-04 - UI/UX Enhancements

### Added

#### Tooltips & Context-Sensitive Help
- Added comprehensive tooltips for all 30+ input parameters
- Tooltips include parameter description, purpose, and valid ranges
- Real-time validation feedback integrated into tooltips
- Color-coded validation states with explanatory messages

#### Undo/Redo System
- Full undo/redo functionality for all parameter changes
- Keyboard shortcuts: `Ctrl+Z` (undo) and `Ctrl+Y` (redo)
- Stack-based implementation with 50-state history
- Menu items in File menu with enabled/disabled states
- Automatic clearing on file load or preset application

#### Parameter Presets
- 5 pre-configured compressor designs:
  - Micro Turbine - Single Stage (80,000 RPM, 50mm)
  - RC Ducted Fan - High Speed (30,000 RPM, 80mm)
  - Industrial Compressor - Low Speed (15,000 RPM, 300mm)
  - High Pressure Ratio - Multi-Stage (50,000 RPM, aggressive)
  - Educational Example - Simple (10,000 RPM, beginner-friendly)
- New "Presets" menu with one-click loading
- Confirmation dialog with preset descriptions
- Loads all Stage, Rotor, and Stator parameters

#### 3D Assembly Viewer
- Interactive 3D viewer showing all stages together in correct spacing
- Color-coded rendering: Blue (rotors), Orange (stators)
- Multiple camera views: Front, Side, Top, Isometric
- Rotation animation with start/stop control
- Cross-section mode for cutaway views
- Mouse controls: Right-click rotate, Left-click zoom
- Accessible via `Tools > Assembly Viewer` menu

#### Drag-and-Drop Stage Reordering
- Click and drag stages to reorder in the list
- Stage data automatically moves with the item
- Uses Qt's native drag-drop functionality

#### Enhanced Validation Feedback
- Real-time visual feedback as user types
- Color-coded status: Green (valid), Yellow (incomplete), Red (invalid)
- Dynamic tooltips showing what's wrong and valid ranges
- No need to click away or press Enter to see validation

#### New Menus
- **Presets** menu with 5 preset configurations
- **Tools** menu with Assembly Viewer
- Updated **File** menu with Undo/Redo commands

### Changed
- Enhanced `CheckState()` method with better validation feedback
- Improved tooltip system with context-sensitive messages
- Updated menu structure with new Presets and Tools menus
- Enhanced color validation to show helpful messages

### Technical Details

#### New Files
```
src/UndoRedo.py           - Undo/redo manager class
src/Tooltips.py           - Tooltip database and helpers
src/Presets.py            - Preset configurations
src/AssemblyViewer.py     - 3D assembly viewer widget
tests/test_ui_enhancements.py - Unit tests for new features
```

#### New Documentation
```
docs/UI_ENHANCEMENTS.md      - Complete user guide
docs/IMPLEMENTATION_SUMMARY.md - Technical documentation
docs/DEMO_SCRIPT.md          - Demo walkthrough
docs/README.md               - Documentation index
docs/ideas.md                - Updated with completion status
```

#### Modified Files
- `src/MainWindow.py` - Added ~350 lines for new functionality
- `README.rst` - Added New Features section

### Testing
- Added 14 new unit tests
- All 26 tests passing (14 new + 12 existing)
- Zero test failures
- All existing functionality preserved

### Documentation
- Complete user guide with how-to instructions
- Step-by-step demo script for presentations
- Technical implementation summary
- Updated README with feature highlights
- Comprehensive inline documentation

### Performance
- Tooltips cached on startup for fast access
- Undo stack limited to 50 items to manage memory
- Assembly viewer generates meshes on-demand
- No impact on existing feature performance

### Compatibility
- Works with both PyQt4 and PyQt5
- Compatible with existing .json file format
- Dark mode theme-aware throughout
- Cross-platform: Linux, Windows, macOS

### Benefits
- **Faster workflow** with presets and undo
- **Fewer errors** with real-time validation
- **Better understanding** via comprehensive tooltips
- **Visual inspection** with 3D assembly viewer
- **More intuitive** with drag-drop reordering
- **More forgiving** with full undo/redo

### Known Limitations
- Flow visualization not yet implemented (future enhancement)
- Assembly viewer requires matplotlib (already a dependency)
- Undo history cleared when loading files or presets

### Migration Notes
No migration needed. All existing functionality preserved. New features are additive.

### Usage Examples

#### Quick Start with Presets
```python
# 1. Start CompPy
# 2. Click: Presets > Educational Example - Simple
# 3. All fields auto-populate with valid values
# 4. Modify as needed
```

#### Using Undo/Redo
```python
# 1. Change RPM to 15000
# 2. Press Ctrl+Z to undo
# 3. Press Ctrl+Y to redo
```

#### Viewing Assembly
```python
# 1. Create 2-3 stages
# 2. Click: Tools > Assembly Viewer
# 3. Use view controls and animation
```

### Contributors
Implementation by GitHub Copilot CLI

### Related Issues
Implements features from `docs/ideas.md` UI/UX Improvements section

---

## [1.x] - Previous Versions

See git history for previous version changes.
