"""
Recent Files Manager for CompPy
Tracks and provides quick access to recently opened files
"""
import json
import os
from pathlib import Path


class RecentFilesManager:
    def __init__(self, max_files=10):
        self.max_files = max_files
        self.recent_files = []
        self.config_file = self._get_config_path()
        self.load()
    
    def _get_config_path(self):
        """Get path to config file in user's home directory"""
        home = Path.home()
        config_dir = home / '.comppy'
        config_dir.mkdir(exist_ok=True)
        return config_dir / 'recent_files.json'
    
    def add_file(self, filepath):
        """Add a file to recent files list"""
        # Convert to absolute path
        filepath = os.path.abspath(filepath)
        
        # Remove if already exists
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        
        # Add to front
        self.recent_files.insert(0, filepath)
        
        # Trim to max size
        self.recent_files = self.recent_files[:self.max_files]
        
        # Remove files that no longer exist
        self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
        
        # Save
        self.save()
    
    def get_recent_files(self):
        """Get list of recent files (only those that still exist)"""
        # Filter out non-existent files
        self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
        return self.recent_files
    
    def clear(self):
        """Clear recent files list"""
        self.recent_files = []
        self.save()
    
    def save(self):
        """Save recent files to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.recent_files, f, indent=2)
        except Exception as e:
            print(f"Error saving recent files: {e}")
    
    def load(self):
        """Load recent files from config file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.recent_files = json.load(f)
                # Filter out non-existent files
                self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
        except Exception as e:
            print(f"Error loading recent files: {e}")
            self.recent_files = []
