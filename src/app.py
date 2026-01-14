from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

@app.route('/')
def index():
    return 'API'

@app.route('/ping')
def ping():
    
    return jsonify({"message":"PONG!"})

#Read all products
@app.route('/products', methods=['GET'])
def get_products():


    return jsonify({"products": products,
                    "message": "Product list"})

#Read single product
@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name):
    product_found = [product for product in products if product["name"] == product_name.lower()]
    print(product_found)
    
    
    if product_found:

        return jsonify({"product": productFound[0],
                    "message": "One product"})
    else:
        return jsonify({"message": "product not found"})


# Create
@app.route('/products', methods=['POST'])
def add_product():
    # print(request.json)
    
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    print(new_product)
    products.append(new_product)
    return jsonify({"message": "Product added successfully!",
                    "products": products}), 201
    
    
## Update
@app.route('/products/<string:product_name>', methods=['PUT'])
def edit_product(product_name):
    product_found = [product for product in products if product["name"] == product_name.lower()]
    print(product_found)
    
    
    if product_found:
        product_found[0]['name'] = request.json['name']
        product_found[0]['price'] = request.json['price']
        product_found[0]['quantity'] = request.json['quantity']
        return jsonify({"product": product_found[0],
                    "message": "One product"})
    else:
        return jsonify({"message": "product not found"})

#Delete
@app.route('/products/<string:product_name>', methods=['DELETE'])
def delete_product(product_name):
    product_found = [product for product in products if product["name"] == product_name.lower()]

    if product_found:
        
        products.remove(product_found[0])

        return jsonify({"product": products,
                    "message": "Product deleted"}), 204
    else:
        return jsonify({"message": "product not found"})

if __name__ == '__main__':
    
    app.run(debug=True)