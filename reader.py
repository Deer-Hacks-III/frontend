from __future__ import annotations
import openfoodfacts
from typing import Union

class ProductReader:
    """
    A product reader class using the openfoodfacts API.
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
            name = item['product']['ecoscore_data']['agribalyse']['name_en']

        image = product['product']['selected_images']['front']['display']
        # Pick a random image from the list of images
        keys = list(image.keys())
        image = image[random.choice(keys)]
        eco_grade = product['product']['ecoscore_grade']
        new_item = Item(name, image, eco_grade, code)
        return new_item

    def _get_materials(self, item: dict) -> int:
        """
        Returns a list of all materials found
        """
        packaging = item['product']['ecoscore_data']['adjustments']['packaging']
        return packaging['non_recyclable_and_non_biodegradable_materials']

    def _get_categories(self, item: dict) -> list[str]:
        """
        Return a list of all categories associated with item.
        """
        result = []
        for i in item:
            result.append(i.replace('en:', ''))
        return result


class Item:
    """
    A product item that should be instantiated by the <ProductReader> object.

    === Public Attributes ===
    name: The name of the product
    image: The URL of the item's image
    eco_grade: The grade of the item

    categories: The categories this item is considered to be in
    materials: The number of non recycleable and biodegradable materials

    """
    name: str
    image: str
    eco_grade: str
    categories: list[str]
    materials: int

    def __init__(self, name: str, image: str, eco_grade: str,
                 materials: int, cat: list[str]) -> None:
        if name == "":
            name = "No Name Available"
        self.name = name
        self.image = image
        self.eco_grade = eco_grade
        self.materials = materials
        self.cat = cat
        self.upc = upc
    def __str__(self) -> str:
        return (f"{self.name}: \neco_grade: {self.eco_grade}"
              f"\nimage url:{self.image}\ncategories: {self.cat}\n"
                f"materials: {self.materials}")

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

    def get_mat(self) -> int:
        """
        Returns the number of recycleable materials this item has
        """
        return self.materials

    def get_cat(self) -> list[str]:
        """
        Returns a list of categories this item is considered to be in
        """
        return self.cat


if __name__ == "__main__":
    reader = ProductReader()
    product = reader.get_product('3045140105502')
    print(product)

