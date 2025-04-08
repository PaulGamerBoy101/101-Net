# menu.py
from PySide6.QtWebEngineWidgets import QWebEngineView
import os
import json
from datetime import datetime
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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

def open_settings_page(self):
    """Open the settings page with version info and update check as embedded HTML."""
    settings_page = QWebEngineView()

    # Define the current version (hardcoded for now)
    CURRENT_VERSION = "1.3.0"  # Matches your latest tag without "Version-" prefix

    # HTML content with embedded CSS and JS
    settings_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Settings</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #121212;
                color: #e0e0e0;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
            }}
            .header {{
                background-color: #1e1e1e;
                color: #39ff14;
                padding: 15px;
                width: 100%;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                border-bottom: 3px solid #39ff14;
            }}
            .content {{
                margin-top: 20px;
                font-size: 18px;
                text-align: center;
            }}
            button {{
                background-color: #39ff14;
                color: black;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #1a8000;
            }}
        </style>
    </head>
    <body>
        <div class="header">Settings</div>
        <div class="content">
            <p>Browser Version: {CURRENT_VERSION}</p>
            <button id="checkUpdate">Check for Update</button>
            <p id="updateStatus"></p>
        </div>
        <script>
            document.getElementById("checkUpdate").addEventListener("click", function() {{
                checkForUpdate();
            }});

            function checkForUpdate() {{
                const currentVersion = "{CURRENT_VERSION}";
                const repo = "PaulGamerBoy101/101-Net";
                fetch(`https://api.github.com/repos/${{repo}}/releases/latest`)
                    .then(response => {{
                        if (!response.ok) throw new Error('Network response was not ok: ' + response.status);
                        return response.json();
                    }})
                    .then(data => {{
                        const latestTag = data.tag_name;  // e.g., "Version-1.2.1"
                        const latestVersion = latestTag.replace("Version-", "");  // e.g., "1.2.1"
                        const versionComparison = compareVersions(latestVersion, currentVersion);
                        let statusMessage;
                        if (versionComparison > 0) {{
                            statusMessage = `A new version (${{latestVersion}}) is available! Visit GitHub to download.`;
                        }} else if (versionComparison === 0) {{
                            statusMessage = "You are on the latest version.";
                        }} else {{
                            statusMessage = "It Looks Like You Are Using A Nightly Build.";
                        }}
                        document.getElementById("updateStatus").innerText = statusMessage;
                    }})
                    .catch(error => {{
                        document.getElementById("updateStatus").innerText = 
                            `Failed to check for updates: ${{error.message}}`;
                    }});
            }}

            function compareVersions(v1, v2) {{
                const parts1 = v1.split('.').map(Number);
                const parts2 = v2.split('.').map(Number);
                for (let i = 0; i < 3; i++) {{
                    const n1 = parts1[i] || 0;
                    const n2 = parts2[i] || 0;
                    if (n1 > n2) return 1;
                    if (n1 < n2) return -1;
                }}
                return 0;
            }}
        </script>
    </body>
    </html>
    """

    # Set the HTML content
    settings_page.setHtml(settings_html)

    # Add the settings page to the tabs
    self.tabs.addTab(settings_page, "Settings")
    self.tabs.setCurrentWidget(settings_page)
