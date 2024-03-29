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
        'image': 'Macbook Air.jpeg',
        'specifications': {
            'Chip': 'Apple M2 chip (8-core CPU, 8-core or 10-core GPU, 16-core Neural Engine, 100GB/s memory bandwidth)',
            'Display': 'Liquid Retina display, 13.6-inch (diagonal) LED-backlit display with IPS technology, 2560x1664 native resolution at 224 pixels per inch, 500 nits brightness',
            'Memory': '8GB unified memory (configurable to 16GB or 24GB)',
            'Battery and Power': 'Up to 18 hours Apple TV app movie playback, Up to 15 hours wireless web, 52.6-watt-hour lithium-polymer battery',
            'Storage': '256GB or 512GB SSD (configurable to 512GB, 1TB, or 2TB)',
            'Ports': 'MagSafe 3 charging port, 3.5mm headphone jack, Two Thunderbolt / USB 4 ports (charging, DisplayPort, Thunderbolt 3, USB 4)'
        }
    },
    {
        'id': 2,
        'name': 'iPhone 15 Pro Titanium',
        'price': 134900,
        'description': 'Cutting-edge features and premium build',
        'image': 'iPhone 15 Pro Titanium.jpeg',
        'specifications': {
            'Design': 'Available in Black Titanium, White Titanium, Blue Titanium, and Natural Titanium finishes. Ceramic Shield front and textured matte glass back.',
            'Capacity': 'Storage options include 128GB, 256GB, 512GB, and 1TB.',
            'Size and Weight': 'iPhone 15 Pro: Width: 2.78 inches (70.6 mm), Height: 5.77 inches (146.6 mm), Depth: 0.32 inch (8.25 mm), Weight: 6.60 ounces (187 grams). iPhone 15 Pro Max: Width: 3.02 inches (76.7 mm), Height: 6.29 inches (159.9 mm), Depth: 0.32 inch (8.25 mm), Weight: 7.81 ounces (221 grams).',
            'Display': 'Super Retina XDR display: iPhone 15 Pro: 6.1-inch OLED display with 2556x1179 resolution, adaptive refresh rates up to 120Hz, HDR, True Tone, and wide color support. iPhone 15 Pro Max: 6.7-inch OLED display with 2796x1290 resolution, adaptive refresh rates up to 120Hz, HDR, True Tone, and wide color support.',
            'Camera': 'Pro camera system: Main: 48MP with 24mm focal length, ƒ/1.78 aperture, sensor-shift optical image stabilization, and support for super-high-resolution photos (24MP and 48MP). Ultra Wide: 12MP with 13mm focal length, ƒ/2.2 aperture, and 120° field of view. 2x Telephoto (enabled by quad-pixel sensor): 12MP with 48mm focal length, ƒ/1.78 aperture, and sensor-shift optical image stabilization. 3x Telephoto: 12MP with 77mm focal length, ƒ/2.8 aperture, and optical image stabilization. Offers 3x optical zoom in and 2x optical zoom out; 6x optical zoom range. Digital zoom up to 15x.',
            'Chip': 'Apple A17 Pro chip: New 6-core CPU with 2 performance and 4 efficiency cores. New 6-core GPU. 16-core Neural Engine.',
            'Battery and Charging': 'Supports 15W MagSafe Wireless Charging.',
            'Security': 'Facial Lock and PIN.'
        }
    },
    {
        'id': 3,
        'name': 'Apple Watch Series 9',
        'price': 41900,
        'description': 'Smarter, brighter, and mightier',
        'image': 'Apple Watch Series 9.jpeg',
        'specifications': {
            'Design': 'Available in Midnight, Starlight, Silver, Product Red, and Pink finishes. Ceramic Shield front and textured matte glass back.',
            'Sizes and Weight': '41mm: Height: 41mm, Width: 35mm, Depth: 10.7mm, Weight (aluminum, GPS): 31.9 grams, Weight (aluminum, GPS + Cellular): 32.1 grams, Weight (stainless steel): 42.3 grams (fits 130–200mm wrists). 45mm: Height: 45mm, Width: 38mm, Depth: 10.7mm, Weight (aluminum, GPS): 38.7 grams, Weight (aluminum, GPS + Cellular): 39.0 grams, Weight (stainless steel): 51.5 grams (fits 140–245mm wrists).',
            'Display': 'Always-On Retina LTPO OLED display with edge-to-edge design. Ion-X front glass (aluminum cases) and sapphire front crystal (stainless steel cases). Up to 2000 nits maximum brightness and 1 nit minimum brightness. 326 pixels per inch.',
            'Chip': 'S9 SiP with 64-bit dual-core processor and 4-core Neural Engine. 64GB storage capacity.',
            'Health Sensors': 'Electrical heart sensor (ECG). Third-generation optical heart sensor. Temperature sensing. Compass. Always-on altimeter. High-G accelerometer. High dynamic range gyroscope. Ambient light sensor.',
            'Battery Life': 'All-day battery life, up to 18 hours of normal use. Up to 36 hours in Low Power Mode. Built-in rechargeable lithium-ion battery. Fast-charge capable (up to 80% charge in about 45 minutes).',
            'Connectivity': 'Cellular (optional), Wi-Fi, Bluetooth, U2, NFC, GPS. Second-generation Ultra Wideband chip.'
        }
    },
    {
        'id': 4,
        'name': 'iPad',
        'price': 39900,
        'description': 'Loveable, drawable, and magical',
        'image': 'iPad.jpeg',
        'specifications': {
            'Design and Dimensions': 'Available in Silver and Space Gray finishes. Dimensions: 9.8 inches (250.6 mm) in height, 6.8 inches (174.1 mm) in width, and 0.29 inch (7.5 mm) in thickness. Weight: Wi-Fi models: 1.07 pounds (487 grams). Wi-Fi + Cellular models: 1.09 pounds (498 grams).',
            'Display': '10.2-inch Retina display with LED-backlit Multi-Touch technology. IPS technology with a resolution of 2160 by 1620 pixels at 264 pixels per inch (ppi). True Tone display for natural color representation. Brightness of 500 nits. Fingerprint-resistant oleophobic coating. Supports the Apple Pencil (1st generation).',
            'Chip': 'Powered by the A13 Bionic chip with a Neural Engine for efficient performance.',
            'Camera': 'Rear Camera: 8MP Wide camera with ƒ/2.4 aperture. Digital zoom up to 5x. Panorama mode (up to 43MP). HDR for photos. Auto image stabilization. Burst mode. Video recording in 1080p HD at 25 fps and 30 fps, and 720p HD at 30 fps. Slo-mo video support for 720p at 120 fps. Time-lapse video with stabilization. Video image stabilization. Cinematic video stabilization (1080p and 720p). Continuous autofocus video. Playback zoom. Video formats recorded: HEVC and H.264. Front Camera: 12MP Ultra Wide camera with a 122° field of view and ƒ/2.4 aperture. HDR for photos. Video recording in 1080p HD at 25 fps, 30 fps, or 60 fps. Time-lapse video with stabilization. Extended dynamic range for video up to 30 fps. Cinematic video stabilization (1080p and 720p). Lens correction. Retina Flash. Auto image stabilization. Burst mode.',
            'Audio and Calling': 'Stereo speakers. Dual microphones for calls, video recording, and audio recording. Supports FaceTime video and audio calling. Center Stage feature for dynamic video calls.',
            'Connectivity': 'Wi-Fi 5 (802.11ac) with 2x2 MIMO (speeds up to 866 Mbps). Bluetooth 4.2. Wi-Fi + Cellular models support Gigabit-class LTE (various bands) and eSIM.',
            'Sensors and Security': 'Touch ID for secure unlocking and Apple Pay. Three-axis gyro, accelerometer, barometer, and ambient light sensor.',
            'Battery': 'Non-removable Li-Ion battery with 8557 mAh capacity (32.4 Wh).'
        }
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
    else:
        sorted_products = products  # Default sorting by product ID

    return render_template('products.html', sorted_products=sorted_products)


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

@app.route('/product/<int:product_id>', methods=['GET'])
def display_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return jsonify({'message': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

