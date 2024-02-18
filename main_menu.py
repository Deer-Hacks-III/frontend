import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QLabel, \
    QSplashScreen, QMenu, QAction, QWidget, QVBoxLayout, \
    QComboBox, QPushButton, QMessageBox, QGridLayout, QLineEdit, QHBoxLayout
from barcode_scanner import QRScanner


class MainApplication(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Project Name")
        self.main_layout = QVBoxLayout()

        # Scan layouts
        self.current_window = None
        self.scan_layout = self.create_scan_layout()
        self.scan_button = QPushButton(f"Scanning")
        self.scan_button.clicked.connect(self.set_scan_layout)

        # Shopping Layouts
        self.list_layout = self.create_list_layout()
        self.list_button = QPushButton(f"Shopping List")
        self.list_button.clicked.connect(self.set_list_layout)

        # By default, be at the scan layout
        self.current_window = self.scan_layout

        self.update_layout()

    def create_scan_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        scanner = QRScanner()
        layout.addWidget(scanner)
        return layout

    def create_list_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Shopping list"))
        return layout

    def set_scan_layout(self) -> None:
        self.current_window = self.scan_layout
        self.update_layout()


    def set_list_layout(self) -> None:
        self.main_layout = self.list_layout
        self.update_layout()

    def update_layout(self) -> None:
        self.main_layout = QVBoxLayout()

        print(isinstance(self.current_window, QWidget))
        self.main_layout.addLayout(self.current_window)
        bottom_layout = QHBoxLayout()

        bottom_layout.addWidget(self.list_button)
        bottom_layout.addWidget(self.scan_button)

        self.main_layout.addLayout(bottom_layout)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
    app = QApplication(sys.argv)
    program = MainApplication()
    program.exec()
