from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

# Temporary product data
products = [
    {
        'id': 1,
        'name': 'MacBook Air',
        'price': 99900,
        'description': 'Designed to be portable and powerful',
        'image': 'Macbook Air.jpeg'
    },
    {
        'id': 2,
        'name': 'iPhone 15 Pro Titanium',
        'price': 134900,
        'description': 'Cutting-edge features and premium build',
        'image': 'iPhone 15 Pro Titanium.jpeg'
    },
    {
        'id': 3,
        'name': 'Apple Watch Series 9',
        'price': 41900,
        'description': 'Smarter, brighter, and mightier',
        'image': 'Apple Watch Series 9.jpeg'
    },
    {
        'id': 4,
        'name': 'iPad',
        'price': 39900,
        'description': 'Loveable, drawable, and magical',
        'image': 'iPad.jpeg'
    }
]

# Temporary cart data stored in a Python dictionary for each user
carts = {}

@app.route('/')
def home():
    return render_template('index.html')

# Routes for handling different API endpoints
@app.route('/display_products', methods=['GET'])
def get_products():
    sort_by = request.args.get('sort_by')
    if sort_by == 'price_asc':
        sorted_products = sorted(products, key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        sorted_products = sorted(products, key=lambda x: x['price'], reverse=True)
    elif sort_by == 'popularity':
        # Implement popularity-based sorting logic here
        sorted_products = sorted(products, key=lambda x: x['popularity'], reverse=True)
    else:
        sorted_products = products  # Default sorting by product ID

    return render_template('products.html', products=sorted_products)


@app.route('/display_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    new_product = {
        'id': len(products) + 1,
        'name': data.get('name'),
        'price': data.get('price'),
        'description': data.get('description')
    }
    products.append(new_product)
    return jsonify(new_product), 201

# Route for viewing the cart with total item quantity and total bill
@app.route('/view_cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    cart = carts.get(user_id, {})
    
    total_quantity = sum(item['quantity'] for item in cart.values())
    total_bill = sum(item['product']['price'] * item['quantity'] for item in cart.values())

    cart_data = {
        'products': cart,
        'total_quantity': total_quantity,
        'total_bill': total_bill
    }
    return render_template('cart.html', cart_data=cart_data)

@app.route('/add_to_cart/<user_id>/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    if user_id not in carts:
        carts[user_id] = {}

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    quantity = int(request.form.get('quantity', 0))  # Get quantity from form data

    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity specified'}), 400

    if product_id in carts[user_id]:
        carts[user_id][product_id]['quantity'] += quantity
    else:
        carts[user_id][product_id] = {
            'product': product,
            'quantity': quantity
        }
    return render_template('product_added.html', product_name=product['name'])

# Route for removing a specific quantity of a product from the cart
@app.route('/remove_from_cart/<user_id>/<int:product_id>', methods=['PUT'])
def remove_from_cart(user_id, product_id):
    if user_id not in carts or product_id not in carts[user_id]:
        return jsonify({'message': 'Product not found in the cart'}), 404

    data = request.get_json()
    if not data or 'quantity' not in data or not isinstance(data['quantity'], int) or data['quantity'] <= 0:
        return jsonify({'error': 'Invalid quantity specified'}), 400

    quantity_to_remove = data['quantity']
    current_quantity = carts[user_id][product_id]['quantity']

    if quantity_to_remove >= current_quantity:
        del carts[user_id][product_id]
    else:
        carts[user_id][product_id]['quantity'] -= quantity_to_remove

    return jsonify({'message': 'Quantity removed from cart'}), 200

@app.route('/search_product', methods=['GET'])
def search_product():
    # Get the search query from the query parameter
    query = request.args.get('query')
    if not query:
        return render_template('products.html', products=products)

    # Search for products containing the query string in their name
    search_results = [p for p in products if query.lower() in p['name'].lower()]
    return render_template('search_results.html', query=query, search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True)

