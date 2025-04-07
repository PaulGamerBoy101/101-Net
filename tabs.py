# tabs.py
from PySide6.QtWebEngineWidgets import QWebEngineView

def close_tab(self, index):
    """Close the tab at the given index."""
    self.tabs.removeTab(index)

def add_new_tab(self):
    """Create a new browser tab and set up its event listeners."""
    new_tab = QWebEngineView()
    new_tab.urlChanged.connect(self.track_history)
    self.tabs.addTab(new_tab, "New Tab")
    self.tabs.setCurrentWidget(new_tab)