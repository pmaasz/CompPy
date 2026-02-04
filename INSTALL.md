# System Dependencies for CompPy

## Ubuntu/Debian

The application requires Qt platform plugins and X11 libraries. Install them with:

```bash
sudo apt update
sudo apt install -y python3-pyqt5 python3-pyqt5.qtwidgets libxcb-xinerama0 libxcb-cursor0
```

Or for a minimal install (recommended if using virtual environment):

```bash
sudo apt install -y libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 \
                    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
                    libxkbcommon-x11-0 libgl1-mesa-glx libdbus-1-3
```

## Alternative: Use System PyQt5

Instead of installing PyQt5 in the virtual environment, you can use the system PyQt5:

1. Install system packages:
```bash
sudo apt install python3-pyqt5
```

2. Create venv with system packages access:
```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install matplotlib numpy numpy-stl
```

## Verifying Installation

After installing dependencies, test the application:

```bash
source venv/bin/activate
python comppy.py
```

## Troubleshooting

### "Could not load Qt platform plugin xcb"

This means Qt's X11 integration libraries are missing. Install the xcb libraries:
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

### "XDG_SESSION_TYPE=wayland" warning

If running on Wayland, you can force Wayland mode:
```bash
QT_QPA_PLATFORM=wayland python comppy.py
```

Or force X11 mode:
```bash
QT_QPA_PLATFORM=xcb python comppy.py
```

### "QSocketNotifier: Can only be used with threads started with QThread" warning

This is a harmless Qt internal warning that doesn't affect functionality. You can:
- Ignore it completely (recommended)
- Suppress it with: `export QT_LOGGING_RULES="*.debug=false;qt.qpa.*=false"`
- Filter stderr: `python comppy.py 2>&1 | grep -v "QSocketNotifier"`

### Missing OpenGL

If you get OpenGL errors:
```bash
sudo apt install libgl1-mesa-glx
```
