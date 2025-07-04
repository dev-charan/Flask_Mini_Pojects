# model.py
class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def get_product(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

# Store products in a list (temporary in-memory DB)
product_list = []

def add_product(product):
    product_list.append(product)

def get_all_products():
    result = []
    for p in product_list:
        result.append(p.get_product())
    return result
 
