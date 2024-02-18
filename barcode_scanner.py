from typing import Optional
import os
import sys
import requests

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, \
    QMenu, QAction, QWidget, QVBoxLayout, \
    QComboBox, QPushButton, QMessageBox, QStatusBar, QDialog, QMenuBar
from pyzbar import pyzbar

from Reader import ProductReader, Item
from InfoBox import ProductInformation as ProductPopup
class QRScanner(QMainWindow):
    """
    Main application window class

    ==== Public Attributes ====
    None!
    """

    combo: Optional[QComboBox]
    camera: QtMultimedia.QCamera
    capture_button: QtWidgets.QPushButton
    camera_view: QtMultimediaWidgets.QCameraViewfinder

class QRScanner(QDialog):
    """
    Dialog for QR scanning
    """

    combo: Optional[QComboBox]
    camera: QtMultimedia.QCamera
    capture_button: QtWidgets.QPushButton
    camera_view: QtMultimediaWidgets.QCameraViewfinder

    def __init__(self) -> None:
        """
        Initialize the dialog
        """
        super().__init__()
        self.setWindowTitle("BargainPro Vbeta.1.0.0 - QR Scanner")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        self.camera = QtMultimedia.QCamera()
        self.camera_view = QtMultimediaWidgets.QCameraViewfinder()
        self.camera.setViewfinder(self.camera_view)
        self.camera.start()

        layout.addWidget(self.camera_view)

        # Add a button to capture an image
        self.capture_button = QPushButton("Scan")
        self.capture_button.setStyleSheet("QPushButton {background-color: rgb(194, 217, 255); border: 1px solid blue; border-radius: 10px; padding: 5px;} QPushButton:hover {background-color: rgb(121, 170, 252); border: 1px solid rgb(26, 56, 107);}")
        self.capture_button.clicked.connect(self.capture_image)
        layout.addWidget(self.capture_button)

        self.camera.setCaptureMode(QtMultimedia.QCamera.CaptureStillImage)
        self.current_index = 0

        # Add menu bar
        self.create_menu_bar()

        self.reader = ProductReader()


    def create_menu_bar(self):
        """
        Create and set the menu bar
        """
        menu_bar = QMenuBar(self)
        file_menu = QMenu("File", self)
        file_menu.setStyleSheet("background-color: rgb(194, 217, 255); selection-background-color: rgb(81, 128, 207);")
        menu_bar.addMenu(file_menu)
        
        # Add a change camera option to the file menu
        change_cam_action = QAction("Change Camera", self)
        change_cam_action.triggered.connect(self.change_cam)
        file_menu.addAction(change_cam_action)

        menu_bar.setStyleSheet("background-color: rgb(194, 217, 255); border: 1px solid blue; border-radius: 10px; padding: 5px;")

        self.layout().setMenuBar(menu_bar)

        
    def change_cam(self) -> None:
        """
        Method that changes the camera source
        Preconditions: There exists at least one camera attached to the computer
        """
        self.popup = QDialog()
        self.popup.setGeometry(100, 100, 200, 100)

        # Create the layout and add the dropdown menu and button
        layout = QVBoxLayout(self.popup)
        self.combo = QComboBox(self.popup)
        # Move it to the center of the screen
        self.popup.move(500, 500)
        # Add a label to the popup
        self.popup.setWindowTitle("Select Camera")
        self.popup.setWindowFlags(Qt.WindowStaysOnTopHint)
        # Increase size
        self.popup.resize(350, 100)
        label = QLabel(self.popup)
        label.setText("Select a camera to use:")
        label.setAlignment(Qt.AlignCenter)
        # Set font to segoe ui
        label.setFont(QtGui.QFont("Segoe UI", 10))
        # Add self.cams to the dropdown menu
        available_cameras = QtMultimedia.QCameraInfo.availableCameras()
        for camera in available_cameras:
            self.combo.addItem(camera.description())
        self.combo.setCurrentIndex(self.current_index)
        layout.addWidget(label)
        layout.addWidget(self.combo)
        button = QPushButton(self.popup)
        button.setText("OK")
        layout.addWidget(button)
        button.clicked.connect(self.on_cam_select)
        self.popup.exec()

    def on_cam_select(self) -> None:
        """
        Method that is called when the OK button is
        clicked in the Change Camera popup
        :return:
        """
        selection = self.combo.currentIndex()
        self.camera.stop()
        self.camera = QtMultimedia.QCamera(
            QtMultimedia.QCameraInfo.availableCameras()[selection])
        self.camera.setViewfinder(self.camera_view)
        self.camera.start()
        self.current_index = selection
        self.popup.close()

    def process_image(self, img: QImage) -> None:
        """
        Parses a QImage and returns the barcode data
        :param img: The image to parse, in QImage format
        :return:
        """
        img = img.convertToFormat(QImage.Format_Grayscale8)
        width, height = img.width(), img.height()
        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.array(ptr).reshape(height, width)
        barcodes = pyzbar.decode(arr)
        if len(barcodes) == 0:
            return
        barcode = barcodes[0]
        barcode_data = barcode.data.decode("utf-8")
        try:
            item = self.reader.get_product(barcode_data)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("An error occurred while trying to get the product information. Please try eigen, or check your internet connection.")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('tCketManage.png'))
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            return
        popup = ProductPopup(item)
        popup.exec_()


    def capture_image(self) -> None:
        """
        Captures an image from the camera and
        passes it to the process_image function
        :return:
        """
        self.process_image(self.camera_view.grab().toImage())



if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    # Step one: Check if the user has an internet connection
    try:
        # We're going to ping a really reliable website, Google
        # If we get a response, we know we have an internet connection
        requests.get('https://www.google.com', timeout=5)
    except requests.exceptions.ConnectionError:
        # make a QMessageBox saying that there is no internet connection
        msg = QMessageBox()
        msg.setWindowTitle("No Internet Connection")
        msg.setText("It looks like you're not connected to the internet. "
                    "BargainPro needs an internet connection to function. "
                    "Please connect to the internet and try again.")
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QtGui.QIcon('tCketManage.png'))
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()
        sys.exit(0)

    # Step Two: Check if the user has at least
    # one camera attached to their computer
    cameras = QtMultimedia.QCameraInfo.availableCameras()
    # If there are no cameras, make a QMessageBox saying
    # that there is no camera attached to the computer
    if len(cameras) == 0:
        msg = QMessageBox()
        msg.setWindowTitle("No Camera Detected")
        msg.setText("It looks like you don't have a camera attached"
                    " to your computer. Unfortunately, BargainPro "
                    "requires a camera to function. "
                    "Please attach a camera to your computer and try again.")
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()
        sys.exit(0)

    scanner = QRScanner()
    scanner.show()
    sys.exit(app.exec_())