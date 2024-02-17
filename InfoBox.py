import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QColor
import requests

class ProductInformation(QDialog):
    def __init__(self, product_name, product_image_url, product_score, parent=None):
        super(ProductInformation, self).__init__(parent)
        self.setWindowTitle("Product Information")
        self.layout = QVBoxLayout()

        # Product Name
        self.product_name_label = QLabel(f"<b>Product Name:</b> {product_name}")
        self.layout.addWidget(self.product_name_label)

        # Product Image
        self.product_image = QLabel()
        self.load_image_from_url(product_image_url)
        self.layout.addWidget(self.product_image)

        # Product Score
        self.product_score_label = QLabel(f"<b>Product Score:</b> {product_score}")
        self.layout.addWidget(self.product_score_label)

        # Set score color
        # Convert product_score into ascii value
        if product_score == "unknown":
            # make a gray color
            green = QColor(128, 128, 128)
        else:
            ascii = ord(product_score)
            # Make a very green color 
            green = QColor(0, 255, 0)
            # For every ascii value above ord(a), add red
            ascii -= ord('A')
            ascii *= 50
            green.setRed(ascii)
        self.setStyleSheet(f"background-color: {green.name()}")

        self.setLayout(self.layout)

    def load_image_from_url(self, url):
        response = requests.get(url)
        image = QImage()
        image.loadFromData(response.content)
        pixmap = QPixmap.fromImage(image)
        self.product_image.setPixmap(pixmap)

    def get_score_color(self, score):
        # Set color based on score
        if score >= 9.0:
            return "#2E8B57"  # Dark Green for A
        elif score >= 8.0:
            return "#3CB371"  # Medium Sea Green for B
        elif score >= 7.0:
            return "#8FBC8F"  # Dark Sea Green for C
        else:
            return "#DC143C"  # Crimson for D and below

if __name__ == '__main__':
    app = QApplication(sys.argv)
    product_name = "Product A"
    product_brand = "Brand X"
    product_image_url = "https://example.com/image.png"
    product_score = "8.5"
    product_info = ProductInformation(product_name, product_brand, product_image_url, product_score)
    product_info.exec_()
