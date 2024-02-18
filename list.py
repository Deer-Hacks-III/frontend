import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, \
    QMenu, QAction, QWidget, QVBoxLayout, QHBoxLayout, \
    QComboBox, QPushButton, QMessageBox, QDialog, QSizePolicy
    
from Reader import ProductReader, Item
import requests
from Database import UPCManager, UPCManagerLocal

class ListScreen(QDialog):
    def __init__(self, db: UPCManager, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("BargainPro Vbeta.1.0.0 - List")
        # For every element in upcs, create a list element and add it to the layout
        self.db = db
        self.layout = None
        self.update_list(db.get_all_upcs())
        
    def update_list(self, upcs: list[str]):
        if self.layout is None:
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)
        else:
            # Clear the layout
            if self.layout.count() > 0:
                for i in reversed(range(self.layout.count())):
                    self.layout.itemAt(i).widget().setParent(None)
        self.items = []
        self.pr = ProductReader()
        for upc in upcs:
            item = self.pr.get_product(upc)
            self.items.append(item)
            self.layout.addWidget(ListElement(item, self))

class ListElement(QWidget):
    def __init__(self, item: Item, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.item = item

        layout = QHBoxLayout()  # Use QHBoxLayout instead of QVBoxLayout

        # Product Image
        image_label = QLabel()
        pixmap = self.load_image_from_url(item.get_img())
        image_label.setPixmap(pixmap.scaledToWidth(75))  # Adjust width as needed
        layout.addWidget(image_label, 1)  # Set stretch factor to 1 for the image

        # Product Name
        name_label = QLabel(item.get_name())
        layout.addWidget(name_label, 2)  # Set stretch factor to 2 for the name

        # Remove Button
        remove_button = QPushButton("Remove")
        remove_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy
        remove_button.clicked.connect(self.remove_from_list)
        layout.addWidget(remove_button, 1)  # Set stretch factor to 1 for the button

        layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins

        self.setLayout(layout)
    
    def remove_from_list(self):
        
        self._parent.db.delete_upc(self.item.get_upc())        
        # Oh my god this is the nastiest hack of the entire codebase
        # The sheer fact that this works is nothing short of a miracle
        # I'm so sorry to anyone who has to decipher this 
        self._parent.update_list(self._parent.db.get_all_upcs())
    
    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                return pixmap
            else:
                print(f"Failed to load image from URL: {url}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error loading image from URL: {url}, Error: {e}")
        return None

if __name__ == "__main__":
    app = QApplication([])
    database = UPCManagerLocal()
    database.upcs = ["8410199271396", "3168930158905"]
    ls = ListScreen(database)
    ls.show()
    sys.exit(app.exec_())