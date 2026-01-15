# Flask Products API

A REST API built with Flask for managing products in a MySQL database with full CRUD operations and automatic database initialization.

## Tech Stack

- **Flask** - Web framework
- **MySQL** - Database
- **flask-mysqldb** - MySQL connector for Flask
- **python-dotenv** - Environment variable management

## Features

- ✅ Full CRUD operations for products
- ✅ Automatic database creation and seeding
- ✅ Environment-based configuration
- ✅ JSON API responses
- ✅ Error handling

## Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- pip

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/GiacomoZoet/flaskapi
   cd flaskapi
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   MYSQL_HOST=localhost
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DB=products_db
   ```

   ⚠️ **Important:** Add `.env` to your `.gitignore` file to keep credentials secure.

5. **Start MySQL server**

   Make sure your MySQL server is running on your machine.

## Running the Application

Start the development server:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## Database Initialization

Before using the API, initialize the database by visiting:

```
GET http://127.0.0.1:5000/createdb
```

This endpoint will:
- Check if the database exists
- Create the database if it doesn't exist
- Create the `products` table with schema: `id`, `name`, `price`, `quantity`
- Insert 15 sample products (Laptop, Mouse, Monitor, etc.)

**Response:**
```json
{
  "message": "Database products_db successfully created and example data automatically inserted"
}
```

## API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### General Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status check - returns "API" |
| GET | `/projects` | Projects page |
| GET | `/about` | About page |
| GET | `/createdb` | Initialize database and seed data |

### Products Endpoints

#### 1. Get All Products

**Request:**
```http
GET /products
```

**Response:** `200 OK`
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop",
      "price": 899,
      "quantity": 15
    },
    {
      "id": 2,
      "name": "Wireless Mouse",
      "price": 25,
      "quantity": 120
    }
  ],
  "message": "Product list"
}
```

#### 2. Get Single Product

**Request:**
```http
GET /products/Laptop
```

**Response:** `200 OK`
```json
{
  "product": {
    "id": 1,
    "name": "Laptop",
    "price": 899,
    "quantity": 15
  },
  "message": "One product"
}
```

**Error Response:** `200 OK`
```json
{
  "message": "product not found"
}
```

#### 3. Create New Product

**Request:**
```http
POST /products
Content-Type: application/json

{
  "name": "Gaming Mouse",
  "price": 59,
  "quantity": 30
}
```

**Response:** `201 Created`
```json
{
  "message": "Product added successfully!",
  "products": {
    "name": "Gaming Mouse",
    "price": 59,
    "quantity": 30
  }
}
```

#### 4. Update Product

**Request:**
```http
PUT /products/Laptop
Content-Type: application/json

{
  "name": "Laptop Pro",
  "price": 1299,
  "quantity": 10
}
```

**Note:** You can update individual fields - omitted fields will keep their current values.

**Response:** `200 OK`
```json
{
  "message": "Product updated successfully",
  "product": {
    "name": "Laptop Pro",
    "price": 1299,
    "quantity": 10
  }
}
```

**Error Response:** `404 Not Found`
```json
{
  "message": "Product not found"
}
```

#### 5. Delete Product

**Request:**
```http
DELETE /products/Laptop
```

**Response:** `204 No Content`
```json
{
  "message": "Product deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "message": "Product not found"
}
```

## Sample Products (Auto-seeded)

After running `/createdb`, the following products are automatically inserted:

- Laptop - $899
- Wireless Mouse - $25
- USB-C Cable - $12
- Monitor 27" - $349
- Mechanical Keyboard - $89
- Laptop Stand - $35
- Webcam HD - $59
- Headphones - $79
- External SSD 1TB - $129
- Phone Charger - $19
- HDMI Cable - $15
- Desk Lamp - $42
- Microphone - $109
- Portable Speaker - $55
- Power Bank - $38

## Database Schema

### products Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(255) | - |
| price | INT | - |
| quantity | INT | - |

## Error Handling

The API includes error handling for common scenarios:

- **404 Not Found:** Custom handler returns JSON response
- **Product Not Found:** Returns appropriate message when product doesn't exist
- **Database Errors:** Handled through MySQL connection

## Testing the API

### Using cURL

**Get all products:**
```bash
curl http://127.0.0.1:5000/products
```

**Create a product:**
```bash
curl -X POST http://127.0.0.1:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":99,"quantity":50}'
```

**Update a product:**
```bash
curl -X PUT http://127.0.0.1:5000/products/Laptop \
  -H "Content-Type: application/json" \
  -d '{"price":999}'
```

**Delete a product:**
```bash
curl -X DELETE http://127.0.0.1:5000/products/Laptop
```

### Using Postman or Insomnia

Import the endpoints above into your preferred API testing tool.

## Project Structure

```
flaskapi/
├── app.py              # Main application file with all routes
├── products.py         # Product data module
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (DO NOT COMMIT)
├── .gitignore         # Git ignore rules
├── venv/              # Virtual environment (DO NOT COMMIT)
└── README.md          # This file
```

## Security Best Practices

⚠️ **Important Security Notes:**

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use strong database passwords**
3. **Disable debug mode in production** - Change `debug=False`
4. **Use parameterized queries** - Already implemented to prevent SQL injection
5. **Rotate credentials** if accidentally exposed

### Recommended .gitignore

```gitignore
# Environment variables
.env

# Virtual environment
venv/
env/

# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/

# IDE
.vscode/
.idea/
```

## Development

### Debug Mode

The application runs in debug mode by default (`debug=True`). This provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

**⚠️ Disable debug mode in production!**

## Troubleshooting

### Common Issues

**MySQL Connection Error:**
- Verify MySQL server is running
- Check credentials in `.env` file
- Ensure MySQL port (default 3306) is accessible

**Module Not Found:**
```bash
pip install -r requirements.txt
```

**Database Already Exists:**
- `/createdb` will notify you if the database already exists
- Drop the database manually if you need to recreate it

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to use this project for learning and development.

## Author

Giacomo - Web Development Student

## Acknowledgments

- Flask documentation
- MySQL documentation
- python-dotenv for environment management
