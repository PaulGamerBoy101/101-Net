# menu.py
from PySide6.QtWebEngineWidgets import QWebEngineView
import os
import json
from datetime import datetime  # Added missing import

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