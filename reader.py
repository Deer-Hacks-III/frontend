from __future__ import annotations
import openfoodfacts
import random

class ProductReader:
    """

    """

    def __init__(self) -> None:
        self.openff = openfoodfacts.API()

    def get_product(self, code: str) -> Item:
        """
        Gets the information about a product. Returned in an item class
        :param code: The product's code
        :return:
        """

        product = self.openff.product.get(code)
        name = product['product'].get('product_name_en', product['product'].get("product_name", ""))
        # In case the product name was not filled
        if name == "":
            name = product['product']['ecoscore_data']['agribalyse']['name_en']

        image = product['product']['selected_images']['front']['display']
        # Pick a random image from the list of images
        keys = list(image.keys())
        image = image[random.choice(keys)]
        eco_grade = product['product']['ecoscore_grade']
        new_item = Item(name, image, eco_grade, code)
        return new_item


class Item:
    """
    A product item that should be instantiated by the <ProductReader> object.
    """
    name: str
    image: str
    eco_grade: str

    def __init__(self, name: str, image: str, eco_grade: str, upc: int = None) -> None:
        self.name = name
        self.image = image
        self.eco_grade = eco_grade
        self.upc = upc
    def __str__(self) -> str:
        return (f"{self.name}: \neco_grade: {self.eco_grade}"
              f"\nimage url:{self.image}")

    def get_name(self) -> str:
        """Return the item's name
        """
        return self.name

    def get_img(self) -> str:
        return self.image

    def get_score(self) -> str:
        return self.eco_grade
    
    def get_upc(self) -> int:
        return self.upc


if __name__ == "__main__":
    reader = ProductReader()
    product = reader.get_product('3045140105502')
    print(product)

