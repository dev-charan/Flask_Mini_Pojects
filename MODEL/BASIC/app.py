from flask import Flask, request, render_template
from model import Product,get_all_products,add_product

app = Flask(__name__) 
@app.route('/',methods=["GET","POST"])
def homepage():
    if request.method == "GET":
        return render_template('index.html'),200
        
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        price = request.form.get("price")
        
        stock = request.form.get("stock")
        product=Product(id=id,name=name,stock=stock,price=price)
        add_product(product)
        return "Product added"

@app.route('/products',methods=["GET"])
def allproduct():
    products = get_all_products()
    return products
if __name__ =='__main__':
    app.run(debug=True)