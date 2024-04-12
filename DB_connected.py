from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os
app = Flask(__name__)

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["e-commerce"]  # Replace with your MongoDB database name
products_collection = db["products"]
carts_collection = db["carts"]

@app.route('/', methods=['GET'])
def landing_page():
    return render_template('landing_page.html')

# Function to display all products from the MongoDB database
@app.route('/display_products', methods=['GET'])
def display_products():
    products = list(products_collection.find({}, {"_id": 0}))
    sort_by = request.args.get('sort_by')
    if sort_by == 'price_asc':
        sorted_products = sorted(products, key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        sorted_products = sorted(products, key=lambda x: x['price'], reverse=True)
    else:
        sorted_products = products  # Default sorting by product ID

    return render_template('products.html', sorted_products=sorted_products)

@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No product data provided in the request'}), 400

        # Insert the products into the MongoDB collection
        products_collection.insert_one(data)
        return jsonify({'message': 'Products added successfully'})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        user_id = data.get('user_id')
        quantity = data.get('quantity', 1)
        product = products_collection.find_one({"id": product_id}, {"_id": 0})
        cart = carts_collection.find_one({"user_id":user_id},{"_id":0})
        if not product:
            return jsonify({'error': 'No product found for given id'}), 400

        # Insert the products into the MongoDB collection
        carts_collection.update_one({"user_id": user_id},{
        "$set": {
            f"products.{product_id}": {
                "product": product,
                "quantity": quantity
            }
        }
    }, upsert=True)
        cart = carts_collection.find_one({"user_id": user_id}, {"_id": 0, "products": 1})
        if not cart:
            return jsonify({'error': 'Cart not found for user'}), 404

        item_quantity = sum(product_data['quantity'] for product_data in cart['products'].values())

        carts_collection.update_one({"user_id": user_id}, {"$set": {"item_quantity": item_quantity}})
        
        return jsonify({'message': 'Product added to the cart'})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
@app.route('/cart/view', methods=['GET'])
def view_cart():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        cart = carts_collection.find_one({"user_id": user_id},{"_id":0})
        if not cart:
            return jsonify({'error': 'Cart not found for user'}), 404

        # Calculate total amount
        total_amount = sum(product_data['product']['price'] * product_data['quantity'] for product_data in cart['products'].values())

        # Add total amount to the cart document
        carts_collection.update_one({"user_id": user_id}, {"$set": {"total_amount": total_amount}})

        # Get updated cart
        cart = carts_collection.find_one({"user_id": user_id}, {"_id": 0})

        return jsonify({'cart': cart})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/cart/delete', methods=['DELETE'])
def delete_cart():
    # Get the user_id from the query parameter
    data = request.get_json()
    user_id = data.get('user_id')

    # Check if user_id is provided
    if user_id is None:
        return jsonify({'error': 'user_id parameter is missing'}), 400

    try:
        # Delete the user's cart from the carts collection in MongoDB
        result = carts_collection.delete_one({"user_id": user_id})

        if result.deleted_count == 1:
            return jsonify({'message': 'Cart deleted successfully'})
        else:
            return jsonify({'message': 'Cart not found'})

    except Exception as e:
        # Handle any exceptions that may occur
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)