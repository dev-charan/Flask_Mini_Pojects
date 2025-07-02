class Product:
    def __init__(self,product_id,name,price):
        self.product_id = product_id
        self.name = name
        self.price = price
    
    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Price: ₹{self.price}"
