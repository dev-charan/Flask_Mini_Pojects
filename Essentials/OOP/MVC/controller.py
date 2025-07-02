from model import Product

class ProdcutController:
    def __init__(self):
        self.products=[]
        
    def create_product(self,product_id,name,price):
        product = Product(product_id,name,price)
        self.products.append(product)
        return " product created"
    
    def get_all_product(self):
        return self.products
    
    def update_product(self,product_id,new_name,new_price):
        for product in self.products:
            if product.product_id == product_id:
                product.name = new_name
                product.price = new_price
                return "Product updated"
        return "not updated"
    
    def delete_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                return "✅ Product deleted."
        return "❌ Product not found."
            
    