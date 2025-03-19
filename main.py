import json
import os
from datetime import datetime
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QMenu
from PySide6.QtWebEngineWidgets import QWebEngineView


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("101 Net")
        self.setGeometry(100, 100, 1200, 800)

        # Load history
        self.load_history()

        # Create main layout
        main_layout = QVBoxLayout()

        # Create navigation bar
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.forward_button = QPushButton("Forward")
        self.home_button = QPushButton("Home")
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.new_tab_button = QPushButton("New Tab")
        self.hamburger_button = QPushButton("Menu")

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.new_tab_button)
        nav_layout.addWidget(self.hamburger_button)

        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.home_button.clicked.connect(self.go_home)
        self.new_tab_button.clicked.connect(self.add_new_tab)

        main_layout.addLayout(nav_layout)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        main_layout.addWidget(self.tabs)

        # Web content area
        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.track_history)
        self.tabs.addTab(self.web_view, "New Tab")

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Menu setup
        self.menu = QMenu("Menu", self)
        self.bookmark_action = QAction("Bookmarks", self)
        self.history_action = QAction("History", self)
        self.settings_action = QAction("Settings", self)

        # Connect menu actions
        self.bookmark_action.triggered.connect(self.open_bookmarks_page)
        self.history_action.triggered.connect(self.open_history_page)

        self.menu.addAction(self.bookmark_action)
        self.menu.addAction(self.history_action)
        self.menu.addAction(self.settings_action)
        self.hamburger_button.clicked.connect(self.show_menu)

        self.setStyleSheet("""
            QPushButton {
                background-color: #39ff14;
                color: black;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                color: black;
            }
            QTabWidget {
                background-color: #f5f5f5;
            }
        """)

    def load_url(self):
        """Load the URL typed in the URL bar."""
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url

        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl(url))

    def go_back(self):
        """Go back in the browser history."""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.back()

    def go_forward(self):
        """Go forward in the browser history."""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.forward()

    def go_home(self):
        """Go to the home page."""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl("https://www.example.com"))

    def close_tab(self, index):
        """Close the selected tab."""
        self.tabs.removeTab(index)

    def add_new_tab(self):
        """Add a new tab."""
        new_tab = QWebEngineView()
        new_tab.urlChanged.connect(self.track_history)
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

    def show_menu(self):
        """Display the menu when the hamburger button is clicked."""
        self.menu.exec_(self.hamburger_button.mapToGlobal(self.hamburger_button.rect().bottomLeft()))

    def open_bookmarks_page(self):
        """Open the bookmarks page."""
        bookmarks_page = QWebEngineView()
        file_url = QUrl.fromLocalFile(os.path.abspath("bookmarks.html"))
        bookmarks_page.setUrl(file_url)
        self.tabs.addTab(bookmarks_page, "Bookmarks")
        self.tabs.setCurrentWidget(bookmarks_page)

    def open_history_page(self):
        """Open the history page."""
        history_page = QWebEngineView()
        file_url = QUrl.fromLocalFile(os.path.abspath("history.html"))
        history_page.setUrl(file_url)
        self.tabs.addTab(history_page, "History")
        self.tabs.setCurrentWidget(history_page)

    def track_history(self, url):
        """Save visited URLs to history.json."""
        if url.isEmpty():
            return

        url_str = url.toString()

        # Load existing history
        history = self.load_history()

        # Append new entry
        history.append({"url": url_str, "timestamp": datetime.utcnow().isoformat()})

        # Save history
        with open("history.json", "w") as f:
            json.dump(history, f, indent=4)

    def load_history(self):
        """Load browsing history from history.json."""
        if os.path.exists("history.json"):
            with open("history.json", "r") as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.show()
    app.exec()
