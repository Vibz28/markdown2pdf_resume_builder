"""Theme definitions for PDF generation."""

from reportlab.lib.colors import Color, white, black
from typing import Dict, Any

class Theme:
    """Base theme class."""
    
    def __init__(self, name: str):
        self.name = name
        self.colors = {}
        self.fonts = {}
        self.spacing = {}
    
    def get_color(self, key: str) -> Color:
        """Get color by key."""
        return self.colors.get(key, black)

class LightTheme(Theme):
    """Light theme matching the HTML template."""
    
    def __init__(self):
        super().__init__("light")
        self.colors = {
            'bg': Color(1, 1, 1),           # #ffffff
            'fg': Color(0.043, 0.059, 0.098),  # #0b0f19
            'muted': Color(0.29, 0.333, 0.408),  # #4a5568
            'accent': Color(0.184, 0.424, 0.922),  # #2f6ceb
            'chip_bg': Color(0.933, 0.949, 1),    # #eef2ff
            'chip_fg': Color(0.122, 0.231, 0.62),  # #1f3b9e
            'rule': Color(0.898, 0.906, 0.918),   # #e5e7eb
            'card': Color(1, 1, 1),         # #ffffff
            'link': Color(0.184, 0.424, 0.922),   # #2f6ceb
        }
        self.fonts = {
            'primary': 'Helvetica',
            'heading': 'Helvetica-Bold',
            'mono': 'Courier',
        }
        self.spacing = {
            'section': 14,
            'item': 8,
            'compact': 4,
        }

class DarkTheme(Theme):
    """Dark theme matching the HTML template."""
    
    def __init__(self):
        super().__init__("dark")
        self.colors = {
            'bg': Color(0.047, 0.059, 0.078),     # #0c0f14
            'fg': Color(0.902, 0.91, 0.933),     # #e6e8ee
            'muted': Color(0.604, 0.643, 0.698), # #9aa4b2
            'accent': Color(0.478, 0.635, 1),    # #7aa2ff
            'chip_bg': Color(0.09, 0.125, 0.212), # #172036
            'chip_fg': Color(0.804, 0.851, 1),   # #cdd9ff
            'rule': Color(0.133, 0.188, 0.286),  # #223049
            'card': Color(0.047, 0.059, 0.078),  # #0c0f14 (same as bg)
            'link': Color(0.2, 0.8, 1),          # Bright cyan for better contrast
        }
        self.fonts = {
            'primary': 'Helvetica',
            'heading': 'Helvetica-Bold',
            'mono': 'Courier',
        }
        self.spacing = {
            'section': 14,
            'item': 8,
            'compact': 4,
        }

def get_theme(theme_name: str) -> Theme:
    """Get theme by name."""
    themes = {
        'light': LightTheme(),
        'dark': DarkTheme(),
    }
    return themes.get(theme_name, LightTheme())
