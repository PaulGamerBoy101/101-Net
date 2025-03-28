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

        # Set main window properties
        self.setWindowTitle("101 Net")
        self.setGeometry(100, 100, 1200, 800)

        # Create the main layout
        main_layout = QVBoxLayout()

        # Navigation bar setup
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.forward_button = QPushButton("Forward")
        self.home_button = QPushButton("Home")
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)  # Load URL when Enter is pressed
        self.new_tab_button = QPushButton("New Tab")
        self.hamburger_button = QPushButton("Menu")

        # Add widgets to the navigation bar layout
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.new_tab_button)
        nav_layout.addWidget(self.hamburger_button)

        # Connect button actions to respective methods
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.home_button.clicked.connect(self.go_home)
        self.new_tab_button.clicked.connect(self.add_new_tab)

        main_layout.addLayout(nav_layout)

        # Create tab widget for managing multiple tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)  # Handle tab closing
        main_layout.addWidget(self.tabs)

        # Web content area (first tab)
        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.track_history)  # Track visited URLs
        self.web_view.setUrl(QUrl("https://101-net-new-tabhome-page-13986765.codehs.me/"))

        self.tabs.addTab(self.web_view, "New Tab")

        # Set the main layout inside a central widget
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Menu setup
        self.menu = QMenu("Menu", self)
        self.bookmark_action = QAction("Bookmarks", self)
        self.history_action = QAction("History", self)

        # Connect menu actions
        self.bookmark_action.triggered.connect(self.open_bookmarks_page)
        self.history_action.triggered.connect(self.open_history_page)

        # Add actions to the menu
        self.menu.addAction(self.bookmark_action)
        self.menu.addAction(self.history_action)
        self.hamburger_button.clicked.connect(self.show_menu)

        # Apply styles to buttons and UI elements
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

    def close_tab(self, index):
        """Close the tab at the given index."""
        self.tabs.removeTab(index)

    def add_new_tab(self):
        """Create a new browser tab and set up its event listeners."""
        new_tab = QWebEngineView()
        new_tab.urlChanged.connect(self.track_history)
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

    def show_menu(self):
        """Show the hamburger menu when clicked."""
        self.menu.exec_(self.hamburger_button.mapToGlobal(self.hamburger_button.rect().bottomLeft()))

    def open_bookmarks_page(self):
        """Open the bookmarks page and load bookmarks from bookmarks.json."""
        bookmarks_page = QWebEngineView()

        # Generate the HTML content dynamically
        bookmarks_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bookmarks</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #121212;
                    color: #e0e0e0;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                .header {
                    background-color: #1e1e1e;
                    color: #39ff14;
                    padding: 15px;
                    width: 100%;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    border-bottom: 3px solid #39ff14;
                }
                .table-container {
                    width: 90%;
                    max-width: 900px;
                    margin-top: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    background-color: #1e1e1e;
                    border-radius: 10px;
                    overflow: hidden;
                }
                td {
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #333;
                }
                a {
                    color: #39ff14;
                    text-decoration: none;
                    transition: color 0.2s ease;
                }
                a:hover {
                    color: #00ff00;
                }
            </style>
        </head>
        <body>
            <div class="header">Bookmarks</div>
            <div class="table-container">
                <table>
        """
        # Load bookmarks from bookmarks.json
        if os.path.exists("bookmarks.json"):
            with open("bookmarks.json", "r") as f:
                bookmarks = json.load(f)
                for bookmark in bookmarks:
                    bookmarks_html += f"""
                        <tr>
                            <td>{bookmark['name']}</td>
                            <td><a href="{bookmark['url']}" target="_blank">{bookmark['url']}</a></td>
                        </tr>
                    """
        bookmarks_html += """
                </table>
            </div>
        </body>
        </html>
        """
        bookmarks_page.setHtml(bookmarks_html)
        self.tabs.addTab(bookmarks_page, "Bookmarks")
        self.tabs.setCurrentWidget(bookmarks_page)

    def open_history_page(self):
        """Open the history page and load history from history.json."""
        history_page = QWebEngineView()

        # Generate the HTML content dynamically
        history_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Browsing History</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #121212;
                    color: white;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    width: 80%;
                    max-width: 600px;
                    background: #1e1e1e;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 15px #39ff14;
                }
                h1 {
                    text-align: center;
                    color: #39ff14;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    background: #252525;
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 5px;
                    box-shadow: 0 0 5px #39ff14;
                }
                a {
                    color: #39ff14;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Browsing History</h1>
                <ul>
        """
        # Load history from history.json
        if os.path.exists("history.json"):
            with open("history.json", "r") as f:
                history = json.load(f)
                # Sort history by most recent entries
                history.sort(key=lambda x: datetime.fromisoformat(x["timestamp"]), reverse=True)
                for entry in history:
                    history_html += f"""
                        <li><a href="{entry['url']}" target="_blank">{entry['url']}</a></li>
                    """
        history_html += """
                </ul>
            </div>
        </body>
        </html>
        """
        history_page.setHtml(history_html)
        self.tabs.addTab(history_page, "History")
        self.tabs.setCurrentWidget(history_page)

    def track_history(self, url):
        """Save visited URLs to history.json."""
        if url.isEmpty():
            return  # Ignore empty URLs

        url_str = url.toString()

        # Load existing history
        history = self.load_history()

        # Append new entry
        history.append({"url": url_str, "timestamp": datetime.utcnow().isoformat()})

        # Save updated history
        with open("history.json", "w") as f:
            json.dump(history, f, indent=4)

    def load_history(self):
        """Load browsing history from history.json file."""
        if os.path.exists("history.json"):
            with open("history.json", "r") as f:
                return json.load(f)
        return []  # Return empty list if no history file exists


if __name__ == "__main__":
    # Initialize and run the application
    app = QApplication([])
    browser = WebBrowser()
    browser.show()
    app.exec()
