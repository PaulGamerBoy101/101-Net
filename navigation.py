# navigation.py
from PySide6.QtCore import QUrl

def load_url(self):
    """Load the URL entered in the URL bar into the current tab."""
    url = self.url_bar.text()
    if not url.startswith("http"):
        url = "https://" + url  # Ensure URL has a proper scheme

    current_tab = self.tabs.currentWidget()
    if current_tab:
        current_tab.setUrl(QUrl(url))

def go_back(self):
    """Navigate back in history if possible."""
    current_tab = self.tabs.currentWidget()
    if current_tab:
        current_tab.back()

def go_forward(self):
    """Navigate forward in history if possible."""
    current_tab = self.tabs.currentWidget()
    if current_tab:
        current_tab.forward()

def go_home(self):
    """Navigate to the home page."""
    current_tab = self.tabs.currentWidget()
    if current_tab:
        current_tab.setUrl(QUrl("https://101-net-new-tabhome-page-13986765.codehs.me/"))