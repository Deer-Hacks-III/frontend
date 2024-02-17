import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog
from PyQt5.QtGui import QPixmap, QImage
import requests

class ProductPopup(QDialog):
    def __init__(self, product_name, product_image_url, product_score, parent=None):
        super(ProductPopup, self).__init__(parent)
        self.setWindowTitle("Product Information")
        self.layout = QVBoxLayout()

        # Product Name
        self.product_name_label = QLabel("Product Name:")
        self.product_name_edit = QLineEdit(product_name)
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_edit)

       # Product Image
        self.product_image_label = QLabel("Product Image:")
        self.product_image = QLabel()
        self.load_image_from_url(product_image_url)
        self.layout.addWidget(self.product_image_label)
        self.layout.addWidget(self.product_image)

        # Product Score
        self.product_score_label = QLabel("Product Score:")
        self.product_score_edit = QLineEdit(product_score)
        self.layout.addWidget(self.product_score_label)
        self.layout.addWidget(self.product_score_edit)

        # Set initial score color
        self.product_score_edit.setStyleSheet(f"background-color: yellow")

        # Change Score Color Button
        self.change_color_button = QPushButton("Change Score Color")
        self.change_color_button.clicked.connect(self.change_score_color)
        self.layout.addWidget(self.change_color_button)

        self.setLayout(self.layout)

    def load_image_from_url(self, url):
        response = requests.get(url)
        image = QImage()
        image.loadFromData(response.content)
        pixmap = QPixmap.fromImage(image)
        self.product_image.setPixmap(pixmap)

    def change_score_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.product_score_edit.setStyleSheet(f"background-color: {color.name()}")
            # Change text color based on luminance
            luminance = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
            text_color = "black" if luminance > 0.5 else "white"
            self.product_score_edit.setStyleSheet(f"background-color: {color.name()}; color: {text_color}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    product_name = "Product A"
    product_brand = "Brand X"
    product_image_url = "https://example.com/image.png"
    product_score = "8.5"
    score_color = "yellow"
    popup = ProductPopup(product_name, product_brand, product_image_url, product_score, score_color)
    popup.exec_()
