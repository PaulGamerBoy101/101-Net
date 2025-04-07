# browser.py
import json
import os
from datetime import datetime
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QIcon  # Added QIcon import
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QMenu
from PySide6.QtWebEngineWidgets import QWebEngineView
from navigation import load_url, go_back, go_forward, go_home
from tabs import close_tab, add_new_tab
from menu import show_menu, open_bookmarks_page, open_history_page
from history import track_history, load_history

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
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon("arrow_back.svg"))
        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon("arrow_forward.svg"))
        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon("home.svg"))
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)  # Load URL when Enter is pressed
        self.new_tab_button = QPushButton()
        self.new_tab_button.setIcon(QIcon("new-tab.svg"))
        self.hamburger_button = QPushButton()
        self.hamburger_button.setIcon(QIcon("menu.svg"))

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
        self.bookmark_action.setIcon(QIcon("bookmarks.svg"))
        self.bookmark_action.setIconVisibleInMenu(True)
        self.history_action = QAction("History", self)
        self.history_action.setIcon(QIcon("history.svg"))
        self.history_action.setIconVisibleInMenu(True)

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

    # Bind methods from other files
    load_url = load_url
    go_back = go_back
    go_forward = go_forward
    go_home = go_home
    close_tab = close_tab
    add_new_tab = add_new_tab
    show_menu = show_menu
    open_bookmarks_page = open_bookmarks_page
    open_history_page = open_history_page
    track_history = track_history
    load_history = load_history