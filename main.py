import json
import os
from PySide6.QtCore import Qt, QUrl  # Import QUrl
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QMenu, QMenuBar
from PySide6.QtWebEngineWidgets import QWebEngineView


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lime Green Web Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize bookmarks
        self.load_bookmarks()

        # Create main layout
        main_layout = QVBoxLayout()

        # Create navigation bar (second row)
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.forward_button = QPushButton("Forward")
        self.home_button = QPushButton("Home")
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.bookmark_button = QPushButton("Bookmark")
        self.new_tab_button = QPushButton("New Tab")  # New Tab button
        self.hamburger_button = QPushButton("Menu")

        # Add buttons to the nav layout
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.bookmark_button)
        nav_layout.addWidget(self.new_tab_button)  # Place New Tab button
        nav_layout.addWidget(self.hamburger_button)

        # Connect back and forward buttons to their respective actions
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.home_button.clicked.connect(self.go_home)

        # Connect the New Tab button
        self.new_tab_button.clicked.connect(self.add_new_tab)

        # Add navigation layout to main layout
        main_layout.addLayout(nav_layout)

        # Create tab widget for top row (tabs)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Add the tab widget (above the web content area)
        main_layout.addWidget(self.tabs)

        # Web content area (third section)
        self.web_view = QWebEngineView()
        self.tabs.addTab(self.web_view, "New Tab")

        # Set up the central widget and the main window
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Menu bar setup
        self.menu = QMenu("Menu", self)
        self.bookmark_action = QAction("Bookmarks", self)
        self.history_action = QAction("History", self)
        self.settings_action = QAction("Settings", self)

        # Connect menu actions
        self.bookmark_action.triggered.connect(self.open_bookmarks_page)

        self.menu.addAction(self.bookmark_action)
        self.menu.addAction(self.history_action)
        self.menu.addAction(self.settings_action)

        self.hamburger_button.clicked.connect(self.show_menu)

        # Apply QSS styles for buttons and url bar
        self.setStyleSheet("""
            QPushButton {
                background-color: #39ff14;  /* Neon Green */
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
                color: black;  /* Black text for URL bar */
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
        
        # Get the currently active tab and update its URL
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(url)

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
            current_tab.setUrl("https://www.example.com")

    def close_tab(self, index):
        """Close the selected tab."""
        self.tabs.removeTab(index)

    def add_new_tab(self):
        """Add a new tab with a web view."""
        new_tab = QWebEngineView()
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

        # Automatically focus the new tab
        self.url_bar.clear()  # Clear the URL bar when a new tab is opened
        new_tab.setUrl("https://www.example.com")  # You can set the home page URL here if needed

    def show_menu(self):
        """Display the menu when the hamburger button is clicked."""
        self.menu.exec_(self.hamburger_button.mapToGlobal(self.hamburger_button.rect().bottomLeft()))

    def open_bookmarks_page(self):
        """Open a new tab with the bookmarks page."""
        bookmarks_page = QWebEngineView()
        
        # Correctly handle file URL using QUrl
        file_url = QUrl.fromLocalFile(os.path.abspath("bookmarks.html"))
        bookmarks_page.setUrl(file_url)  # Set the file URL properly
        self.tabs.addTab(bookmarks_page, "Bookmarks")
        self.tabs.setCurrentWidget(bookmarks_page)

    def load_bookmarks(self):
        """Load bookmarks from bookmarks.json file."""
        if os.path.exists("bookmarks.json"):
            with open("bookmarks.json", "r") as f:
                self.bookmarks = json.load(f)
        else:
            self.bookmarks = []

    def save_bookmarks(self):
        """Save bookmarks to bookmarks.json file."""
        with open("bookmarks.json", "w") as f:
            json.dump(self.bookmarks, f)

    def toggle_bookmark(self):
        """Add or remove the current URL from bookmarks."""
        url = self.url_bar.text()
        if url in self.bookmarks:
            self.bookmarks.remove(url)
            self.bookmark_button.setText("Bookmark")
        else:
            self.bookmarks.append(url)
            self.bookmark_button.setText("Bookmarked")
        
        self.save_bookmarks()


if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.show()
    app.exec()
