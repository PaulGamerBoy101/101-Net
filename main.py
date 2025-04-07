# main.py
import sys
from PySide6.QtWidgets import QApplication
from browser import WebBrowser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    app.exec()