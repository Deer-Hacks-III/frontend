import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QColor
import requests
import Database
from Reader import ProductReader, Item

class ProductInformation(QDialog):
    def __init__(self, item, parent=None):
        self.item = item
        product_name = item.get_name()
        product_image_url = item.get_img()
        product_score = item.get_score()
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
        
        # Add an "add to list" button
        self.add_to_list_button = QPushButton("Add to List")
        self.layout.addWidget(self.add_to_list_button)
        self.add_to_list_button.clicked.connect(self.add_to_list)
        # add a "view alternatives" button
        self.view_alternatives_button = QPushButton("View Alternatives")
        self.layout.addWidget(self.view_alternatives_button)
        self.view_alternatives_button.clicked.connect(self.alternatives)
        
        
        # Set score color
        # Convert product_score into ascii value
        try:
            product_score = product_score.upper()
            ascii = ord(product_score)
            # Make a very green color 
            green = QColor(0, 255, 100)
            # For every ascii value above ord(a), add red
            ascii -= ord('A')
            ascii *= 50
            green.setRed(ascii)
        except:
            green = QColor(128, 128, 150)
        self.setStyleSheet(f"background-color: {green.name()}")

        self.setLayout(self.layout)

    def add_to_list(self):
        db = Database.UPCManager("http://127.0.0.1:5000")
        db.add_upc(self.item.get_upc())
        self.close()

    def alternatives(self):
        search = ','.join(self.item.cat)
        response = requests.get(f"https://world.openfoodfacts.net/api/v2/search?categories_tags={search}&sort_by=ecoscore_score")
        pr = ProductReader()
        products = []
        for item in response.json()["products"]:
            products.append(pr.get_product(item["_id"]))
        print(products)
        # TODO: list them in a box or pop up or smth


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
    product_image_url = "https://avatars.githubusercontent.com/u/62670577?v=4"
    product_score = "A"
    product_info = ProductInformation(product_name, product_image_url, product_score)
    product_info.exec_()
