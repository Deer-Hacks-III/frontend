import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QLabel, \
    QSplashScreen, QMenu, QAction, QWidget, QVBoxLayout, \
    QComboBox, QPushButton, QMessageBox, QGridLayout, QLineEdit

import barcode_scanner
import List
class MainMenu(QDialog):

    shop_list_caller: callable
    scan_caller: callable

    def __init__(self, shop_list_caller: callable, scan_caller: callable,
                 parent=None):
        super().__init__(parent)
        self.shop_list_caller = shop_list_caller
        self.scan_caller = scan_caller
        self.setWindowTitle("App Name")
        self.layout = QVBoxLayout()

        self.list_button = QPushButton(f"Shopping List")
        self.list_button.clicked.connect(self.shop_list_caller)
        self.list_button.width = 800

        self.layout.addWidget(self.list_button)

        self.scan_button = QPushButton(f"Scan Item")
        self.scan_button.clicked.connect(self.scan_caller)
        self.scan_button.width = 800
        self.layout.addWidget(self.scan_button)

        self.setLayout(self.layout)

def shop_list() -> None:
    l = List.ListScreen(List.UPCManager("http://127.0.0.1:5000"))
    l.exec()

def scan_menu() -> None:
    s = barcode_scanner.QRScanner()
    s.show()

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
    app = QApplication(sys.argv)
    menu = MainMenu(shop_list, scan_menu)
    menu.exec()


#app.setAttribute(Qt.AA_EnableHighDpiScaling)
