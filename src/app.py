from flask import Flask, jsonify
from products import products

app = Flask(__name__)

@app.route('/ping')
def ping():
    
    return jsonify({"message":"PONG!"})

@app.route('/products', methods=['GET'])
def get_products():


    return jsonify({"products": products,
                    "message": "Product list"})

@app.route('/product/<string:product_name>', methods=['GET'])
def get_product(product_name):
    productFound = [product for product in products if product["name"] == product_name]
    print(productFound)
    
    return "OK"

if __name__ == '__main__':
    
    app.run(debug=True)