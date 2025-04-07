# tabs.py
from PySide6.QtWebEngineWidgets import QWebEngineView

def update_tab_title(self, title):
    """Update the current tab's title based on the webpage title."""
    current_index = self.tabs.currentIndex()
    if current_index != -1:  # Ensure a tab is selected
        if title:  # Only update if there's a title, otherwise keep "New Tab"
            self.tabs.setTabText(current_index, title)
        else:
            self.tabs.setTabText(current_index, "New Tab")

def close_tab(self, index):
    """Close the tab at the given index."""
    self.tabs.removeTab(index)

def add_new_tab(self):
    """Create a new browser tab and set up its event listeners."""
    new_tab = QWebEngineView()
    new_tab.urlChanged.connect(self.track_history)
    new_tab.titleChanged.connect(lambda title: self.update_tab_title(title))  # Connect title change
    self.tabs.addTab(new_tab, "New Tab")
    self.tabs.setCurrentWidget(new_tab)
