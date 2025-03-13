import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import os


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tmeon Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Setup browser engine
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        # Create address bar
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Enter URL")
        self.address_bar.returnPressed.connect(self.navigate_to_url)

        # Navigation buttons
        self.back_btn = QPushButton("<", self)
        self.forward_btn = QPushButton(">", self)
        self.refresh_btn = QPushButton("Refresh", self)
        self.home_btn = QPushButton("Home", self)

        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.refresh_btn.clicked.connect(self.browser.reload)
        self.home_btn.clicked.connect(self.go_home)

        # Tab bar setup
        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.browser, "New Tab")
        self.tab_widget.currentChanged.connect(self.update_url_on_tab_switch)

        # Create menu bar and settings
        self.create_menu_bar()

        # Layout
        layout = QVBoxLayout()
        toolbar = QHBoxLayout()

        toolbar.addWidget(self.back_btn)
        toolbar.addWidget(self.forward_btn)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.home_btn)
        toolbar.addWidget(self.address_bar)

        layout.addLayout(toolbar)
        layout.addWidget(self.tab_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Default home page
        self.home_url = "https://www.google.com"
        self.setWindowIcon(QIcon("earth.ico"))  # Set the icon here

        self.show()

        # Listen for download events
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)

        new_window_action = QAction("New Window", self)
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)

        download_manager_action = QAction("Download Manager", self)
        download_manager_action.triggered.connect(self.open_download_manager)
        edit_menu.addAction(download_manager_action)

        # View Menu
        view_menu = menu_bar.addMenu("View")
        zoom_action = QAction("Zoom", self)
        zoom_action.triggered.connect(self.zoom)
        view_menu.addAction(zoom_action)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        current_tab = self.tab_widget.currentWidget()
        current_tab.setUrl(QUrl(url))

    def go_home(self):
        current_tab = self.tab_widget.currentWidget()
        current_tab.setUrl(QUrl(self.home_url))

    def new_tab(self):
        new_browser = QWebEngineView()
        self.tab_widget.addTab(new_browser, "New Tab")
        new_browser.setUrl(QUrl(self.home_url))
        new_browser.loadFinished.connect(self.update_url_on_tab_switch)

    def new_window(self):
        new_window = Browser()
        new_window.show()

    def update_url_on_tab_switch(self):
        current_tab = self.tab_widget.currentWidget()
        url = current_tab.url().toString()
        self.address_bar.setText(url)

    def zoom(self):
        self.browser.setZoomFactor(1)

    def zoom_in(self):
        current_zoom = self.browser.zoomFactor()
        self.browser.setZoomFactor(current_zoom + 0.1)

    def zoom_out(self):
        current_zoom = self.browser.zoomFactor()
        self.browser.setZoomFactor(current_zoom - 0.1)

    def open_settings(self):
        QMessageBox.information(self, "Settings", "Settings will be here.")

    def open_download_manager(self):
        QMessageBox.warning(self, "Download Manager", "Feature coming soon.")

    def show_about(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About Tmeon Browser")

        layout = QVBoxLayout()
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("tmeronlogo.png"))
        layout.addWidget(logo_label)

        details_label = QLabel("Tmeon Browser - Version 1.0\nDeveloped by Zohan Haque")
        layout.addWidget(details_label)

        close_button = QPushButton("Close", about_dialog)
        close_button.clicked.connect(about_dialog.accept)
        layout.addWidget(close_button)

        about_dialog.setLayout(layout)
        about_dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Close", "Are you sure you want to quit?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def on_download_requested(self, download):
        file_url = download.url().toString()
        file_name = os.path.basename(file_url)
        file_extension = file_name.split('.')[-1].lower()

        # Check if the file is an executable type
        executable_extensions = ['exe', 'msi', 'bat', 'cmd', 'sh']

        if file_extension in executable_extensions:
            response = QMessageBox.question(
                self,
                "Warning",
                f"Are you sure you want to download '{file_name}'? If it's executable, it might be a risk to your PC.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if response == QMessageBox.Yes:
                download.accept()
            else:
                download.cancel()
        else:
            download.accept()


class TmeonBrowser(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.setApplicationName("Tmeon Browser")
        self.browser = Browser()


if __name__ == '__main__':
    app = TmeonBrowser(sys.argv)
    sys.exit(app.exec_())

