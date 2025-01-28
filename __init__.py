import json
import products
from cart import dao
from products import Product

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> dict:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return {}

    # Extract product IDs in a single step while ensuring safe JSON parsing
    product_ids = []
    for cart_detail in cart_details:
        try:
            product_ids.extend(json.loads(cart_detail['contents']))  # Avoids multiple set/list conversions
        except json.JSONDecodeError:
            continue  # Skip invalid JSON

    if not product_ids:
        return {}

    # Fetch only required fields (id, name, price) in one optimized batch query
    products_data = {p.id: {"name": p.name, "price": p.price} for p in products.get_products_bulk(product_ids)}

    return products_data

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)
