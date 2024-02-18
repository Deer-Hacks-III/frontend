import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QLabel, \
    QSplashScreen, QMenu, QAction, QWidget, QVBoxLayout, \
    QComboBox, QPushButton, QMessageBox, QGridLayout, QLineEdit, QHBoxLayout,
                             QStackedLayout)
from barcode_scanner import QRScanner
from Database import UPCManager, UPCManagerLocal
from list import ListScreen, ListElement

class MainApplication(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Project Name")
        self.main_layout = QVBoxLayout()
        self.setGeometry(100, 100, 800, 650)
        # Scan layouts
        self.current_window = QStackedLayout()
        self.scan_button = QPushButton(f"Scanning")
        self.scan_button.setStyleSheet("QPushButton {background-color: rgb(217,237,247); border: 2px solid rgb(83, 115, 145); border-radius: 10px; padding: 5px;} \
                                    QPushButton:hover {background-color: rgb(175,217,238); border: 2px solid rgb(42, 82, 120);}")
        self.scan_button.clicked.connect(self.set_scan_layout)

        # Shopping Layouts
        self.list_button = QPushButton(f"Shopping List")
        self.list_button.setStyleSheet("QPushButton {background-color: rgb(217,237,247); border: 2px solid rgb(83, 115, 145); border-radius: 10px; padding: 5px;} \
                                    QPushButton:hover {background-color: rgb(175,217,238); border: 2px solid rgb(42, 82, 120);}")
        self.list_button.clicked.connect(self.set_list_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.list_button)
        self.bottom_layout.addWidget(self.scan_button)
        # By default, be at the scan layout

        self.current_window.addWidget(ListScreen(database))
        self.current_window.addWidget(QRScanner())
        self.current_window.setCurrentIndex(0)

        self.main_layout.addLayout(self.current_window)
        self.main_layout.addLayout(self.bottom_layout)
        self.setStyleSheet("MainApplication {background-color: rgb(230, 230, 250);}")
        self.setLayout(self.main_layout)

    def set_scan_layout(self) -> None:
        self.current_window.setCurrentIndex(1)
        #self.current_window = self.scan_layout
        #self.update_layout()

    def set_list_layout(self) -> None:
        self.current_window.setCurrentIndex(0)
        # Get the ListScreen
        self.current_window.widget(0).update_list(database.get_all_upcs())
        #self.current_window = self.list_layout
        #self.update_layout()

    def update_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.current_window.update()
        self.list_layout
        self.main_layout.addLayout(self.current_window)

        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)
        self.update()


if __name__ == "__main__":
    database = UPCManager("http://127.0.0.1:5000")
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
    app = QApplication(sys.argv)
    program = MainApplication()
    program.exec()
    sys.exit(app.exec_())
