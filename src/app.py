from flask import Flask, jsonify, request
from products import products
from markupsafe import escape
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import MySQLdb.cursors

import os

load_dotenv()
app = Flask(__name__)
conn = MySQL(app)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv("MYSQL_DB")

@app.route('/')
def index():
    return 'API'

@app.route('/createdb')
def createdb():
    cursor = conn.connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    database_exists = False
    for database in databases:
        if MYSQL_DB in database:
            database_exists = True
            break
    
    if not database_exists:
        cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DB}")
        cursor.execute(f"CREATE DATABASE {MYSQL_DB}")
        cursor.execute(f"USE {MYSQL_DB}")
        cursor.execute(f"CREATE TABLE products (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), price INT, quantity INT)")
        cursor.execute('''INSERT INTO products (name, price, quantity) VALUES
                                                ('Laptop', 899, 15),
                                                ('Wireless Mouse', 25, 120),
                                                ('USB-C Cable', 12, 200),
                                                ('Monitor 27"', 349, 8),
                                                ('Mechanical Keyboard', 89, 45),
                                                ('Laptop Stand', 35, 67),
                                                ('Webcam HD', 59, 33),
                                                ('Headphones', 79, 52),
                                                ('External SSD 1TB', 129, 28),
                                                ('Phone Charger', 19, 150),
                                                ('HDMI Cable', 15, 95),
                                                ('Desk Lamp', 42, 18),
                                                ('Microphone', 109, 12),
                                                ('Portable Speaker', 55, 41),
                                                ('Power Bank', 38, 73);
''')
        conn.connection.commit()
        cursor.close()
        return jsonify({"message":f"Database {MYSQL_DB} successfully created and example data automatically inserted"}), 201

    else:
        return jsonify({"message":f"Database {MYSQL_DB} already exists"})



#Read all products
@app.route('/products', methods=['GET'])
def get_products():
    cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'use {MYSQL_DB}')
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify({"products": products,
                    "message": "Product list"})

#Read single product
@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name):
    # product_found = [product for product in products if product["name"] == product_name.lower()]
    # print(product_found)
    cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'use {MYSQL_DB}')
    cursor.execute("SELECT * FROM products WHERE name = %s", (product_name,))
    product_found = cursor.fetchone()
    conn.connection.commit()
    cursor.close()
    if product_found:

        return jsonify({"product": product_found,
                    "message": "One product"})
    else:
        return jsonify({"message": "product not found"})


# Create
@app.route('/products', methods=['POST'])
def add_product():
    # print(request.json)
    cursor = conn.connection.cursor()
    cursor.execute(f'use {MYSQL_DB}')
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    print(new_product)
    
    cursor.execute(
    "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
    (new_product['name'], new_product['price'], new_product['quantity'])
    )
    conn.connection.commit()
    cursor.close()
    return jsonify({"message": "Product added successfully!",
                    "products": new_product}), 201
    
    
## Update
@app.route('/products/<string:product_name>', methods=['PUT'])
def edit_product(product_name):
    # product_found = [product for product in products if product["name"] == product_name.lower()]
    # print(product_found)
    cursor = conn.connection.cursor()
    cursor.execute(f'use {MYSQL_DB}')
    cursor.execute("SELECT * FROM products WHERE name = %s", (product_name,))
    product_found = cursor.fetchone()
    if product_found:
        new_name = request.json.get('name', product_found[1])
        new_price = request.json.get('price', product_found[2])
        new_quantity = request.json.get('quantity', product_found[3])
        cursor.execute(
            "UPDATE products SET name = %s, price = %s, quantity = %s WHERE name = %s",
            (new_name, new_price, new_quantity, product_name)
        )
        conn.connection.commit()
        cursor.close()
        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "name": new_name,
                "price": new_price,
                "quantity": new_quantity
            }
        }), 200
    else:
        cursor.close()
        return jsonify({"message": "Product not found"}), 404

#Delete
@app.route('/products/<string:product_name>', methods=['DELETE'])
def delete_product(product_name):
    # product_found = [product for product in products if product["name"] == product_name.lower()]

    cursor = conn.connection.cursor()
    cursor.execute(f'use {MYSQL_DB}')
    cursor.execute("SELECT * FROM products WHERE name = %s", (product_name,))
    product_found = cursor.fetchone()
    if product_found:
        cursor.execute("DELETE FROM products WHERE name = %s", (product_name,))       
        conn.connection.commit()
        cursor.close()
        return jsonify({
            "message": "Product deleted successfully"
        }), 204 
    else:
        cursor.close()
        return jsonify({"message": "Product not found"}), 404

# @app.route('/<name>')
# def  hello(name):
#     return "Hello" + escape(name)

@app.route('/projects')
def projects():
    return "This is the projects paage!"

@app.route('/about')
def about():
    return "About us"

@app.errorhandler(404)
def not_found(error):
    return jsonify({"Message": "Not Found"}), 404

if __name__ == '__main__':
    
    app.run(debug=True)