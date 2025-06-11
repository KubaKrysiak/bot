# API Reference

## Core Modules

### Window Management (`windows_manager.py`)

#### `WindowsManager` Class
```python
class WindowsManager:
    def __init__(self)
    def add_window(self, window_title: str) -> bool
    def remove_window(self, window_title: str) -> bool
    def focus_window(self, window_title: str) -> bool
    def get_window_position(self, window_title: str) -> tuple
    def set_window_position(self, window_title: str, x: int, y: int) -> bool
    def resize_window(self, window_title: str, width: int, height: int) -> bool
```

### Input Automation

#### Keyboard (`keyboard_automation.py`)
```python
class KeyboardAutomation:
    def __init__(self)
    def press_key(self, key: str) -> bool
    def release_key(self, key: str) -> bool
    def type_text(self, text: str) -> bool
    def press_combination(self, keys: list) -> bool
```

#### Mouse (`mouse_automation.py`)
```python
class MouseAutomation:
    def __init__(self)
    def move_to(self, x: int, y: int) -> bool
    def click(self, x: int, y: int) -> bool
    def double_click(self, x: int, y: int) -> bool
    def drag_to(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool
```

### Vision System (`bot_vision.py`)
```python
class BotVision:
    def __init__(self)
    def find_template(self, template_path: str, threshold: float = 0.8) -> tuple
    def find_color(self, color: tuple, tolerance: int = 10) -> tuple
    def capture_screen(self) -> numpy.ndarray
    def analyze_region(self, x: int, y: int, width: int, height: int) -> dict
```

### Configuration System

#### Configuration Manager (`config.py`)
```python
class ConfigManager:
    def __init__(self, config_path: str)
    def load_config(self) -> dict
    def save_config(self, config: dict) -> bool
    def get_value(self, key: str) -> any
    def set_value(self, key: str, value: any) -> bool
    def validate_config(self, config: dict) -> bool
```

#### Configurator (`configurator.py`)
```python
class Configurator:
    def __init__(self)
    def show_config_dialog(self) -> dict
    def load_profile(self, profile_name: str) -> bool
    def save_profile(self, profile_name: str) -> bool
    def validate_input(self, input_data: dict) -> bool
```

### Session Management (`window_session.py`)
```python
class WindowSession:
    def __init__(self)
    def create_session(self, window_title: str) -> bool
    def restore_session(self, session_id: str) -> bool
    def save_session_state(self) -> bool
    def get_session_info(self, session_id: str) -> dict
```

## Utility Functions

### Screen Capture (`screen.py`)
```python
def capture_screen() -> numpy.ndarray
def capture_region(x: int, y: int, width: int, height: int) -> numpy.ndarray
def save_screenshot(path: str) -> bool
```

### Auto Login (`auto_login.py`)
```python
class AutoLogin:
    def __init__(self)
    def detect_login_screen(self) -> bool
    def perform_login(self, credentials: dict) -> bool
    def verify_login_success(self) -> bool
```

## Data Types

### Configuration
```python
Config = {
    'window_settings': {
        'title': str,
        'position': (int, int),
        'size': (int, int)
    },
    'automation_settings': {
        'keyboard_delay': float,
        'mouse_delay': float,
        'click_delay': float
    },
    'vision_settings': {
        'template_threshold': float,
        'color_tolerance': int
    }
}
```

### Session Data
```python
SessionData = {
    'session_id': str,
    'window_title': str,
    'state': dict,
    'timestamp': str
}
```

## Error Handling

### Custom Exceptions
```python
class WindowError(Exception)
class AutomationError(Exception)
class VisionError(Exception)
class ConfigError(Exception)
class SessionError(Exception)
```

## Constants

### Configuration Defaults
```python
DEFAULT_CONFIG = {
    'keyboard_delay': 0.1,
    'mouse_delay': 0.1,
    'click_delay': 0.1,
    'template_threshold': 0.8,
    'color_tolerance': 10
}
```

### Window States
```python
WINDOW_STATES = {
    'NORMAL': 0,
    'MINIMIZED': 1,
    'MAXIMIZED': 2
}
```

## Usage Examples

### Basic Window Management
```python
wm = WindowsManager()
wm.add_window("Target Window")
wm.focus_window("Target Window")
wm.set_window_position("Target Window", 100, 100)
```

### Input Automation
```python
kb = KeyboardAutomation()
mouse = MouseAutomation()

kb.type_text("Hello World")
mouse.move_to(100, 100)
mouse.click(100, 100)
```

### Vision System
```python
vision = BotVision()
template_pos = vision.find_template("template.png")
color_pos = vision.find_color((255, 0, 0))
```

### Configuration
```python
config = ConfigManager("config.json")
settings = config.load_config()
config.set_value("keyboard_delay", 0.2)
config.save_config(settings)
``` 