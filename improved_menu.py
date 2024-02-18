import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QLabel, \
    QSplashScreen, QMenu, QAction, QWidget, QVBoxLayout, \
    QComboBox, QPushButton, QMessageBox, QGridLayout, QLineEdit, QHBoxLayout,
                             QStackedLayout, QScrollArea)
from barcode_scanner import QRScanner
from Database import UPCManager, UPCManagerLocal
from list2 import ListScreen, ListElement

class MainApplication(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("GreenCart")
        self.main_layout = QVBoxLayout()
        self.setGeometry(0, 0, 800, 650)
        # Scan layouts
        self.current_window = QStackedLayout()
        self.scan_button = QPushButton("Scanning")
        self.scan_button.setIcon(QIcon('icons/barcode.svg'))
        self.scan_button.setFixedHeight(50)
        self.scan_button.setFixedWidth(400)
        self.scan_button.setStyleSheet("QPushButton {background-color: rgb(217,237,247); border: 2px solid rgb(83, 115, 145); border-radius: 10px; padding: 5px;} \
                                    QPushButton:hover {background-color: rgb(175,175,255); border: 2px solid rgb(42, 82, 120);}")
        self.scan_button.clicked.connect(self.set_scan_layout)

        # Shopping Layouts

        self.list_button = QPushButton("Shopping List")
        self.list_button.setIcon(QIcon('icons/shoplist.svg'))
        self.list_button.setFixedHeight(50)
        self.list_button.setFixedWidth(400)
        self.list_button.setStyleSheet("QPushButton {background-color: rgb(217,237,247); border: 2px solid rgb(83, 115, 145); border-radius: 10px; padding: 5px;} \
                                    QPushButton:hover {background-color: rgb(150,255,200); border: 2px solid rgb(42, 82, 120);}")
        self.list_button.clicked.connect(self.set_list_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.list_button)
        self.bottom_layout.addWidget(self.scan_button)
        self.bottom_layout.setAlignment(Qt.AlignBottom)
        # By default, be at the scan layout
        self.current_window.addWidget(ListScreen(database))
        scanner = QRScanner()
        self.current_window.addWidget(scanner)
        scanner.stop_camera()
        self.current_window.setCurrentIndex(0)

        self.main_layout.addLayout(self.current_window)
        self.main_layout.addLayout(self.bottom_layout)
        self.setStyleSheet("MainApplication {background-color: rgb(230, 230, 250);}")
        self.setLayout(self.main_layout)
    


    def set_scan_layout(self) -> None:
        if self.current_window.currentIndex() != 1:
            self.current_window.widget(1).start_camera()
        self.current_window.setCurrentIndex(1)
        self.update()

    def set_list_layout(self) -> None:
        if self.current_window.currentIndex() != 0:
            self.current_window.widget(1).stop_camera()
        self.current_window.setCurrentIndex(0)
        # Get the ListScreen
        self.current_window.widget(0).update_list(database.get_all_upcs())
        self.update()



if __name__ == "__main__":
    database = UPCManager("http://127.0.0.1:5000")
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
    app = QApplication(sys.argv)
    program = MainApplication()
    program.show()
    #program.exec()
    sys.exit(app.exec_())
