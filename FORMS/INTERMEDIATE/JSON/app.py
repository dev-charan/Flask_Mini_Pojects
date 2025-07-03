# 5. JSON DATA EXAMPLE
# This handles JSON data sent in API requests (common in modern web apps)

from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# HTML template with JavaScript for sending JSON requests
json_html = """
<!DOCTYPE html>
<html>
<head>
    <title>JSON Data Example</title>
    <style>
        .example { background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .result { background: #e8f5e8; padding: 10px; margin: 10px 0; border-radius: 5px; }
        button { padding: 10px 15px; margin: 5px; cursor: pointer; }
        textarea { width: 100%; height: 100px; }
    </style>
    <script>
        function sendSimpleJSON() {
            const data = {
                name: "John Doe",
                age: 30,
                email: "john@example.com"
            };
            
            sendJSON('/api/user', data, 'simple-result');
        }
        
        function sendComplexJSON() {
            const data = {
                user: {
                    name: "Alice Smith",
                    age: 25,
                    preferences: {
                        theme: "dark",
                        notifications: true
                    }
                },
                products: [
                    { id: 1, name: "Laptop", price: 999 },
                    { id: 2, name: "Mouse", price: 29 }
                ],
                metadata: {
                    timestamp: new Date().toISOString(),
                    source: "web"
                }
            };
            
            sendJSON('/api/complex', data, 'complex-result');
        }
        
        function sendCustomJSON() {
            const textarea = document.getElementById('custom-json');
            try {
                const data = JSON.parse(textarea.value);
                sendJSON('/api/custom', data, 'custom-result');
            } catch (e) {
                document.getElementById('custom-result').innerHTML = 
                    '<div style="color: red;">Invalid JSON: ' + e.message + '</div>';
            }
        }
        
        function sendJSON(url, data, resultId) {
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                document.getElementById(resultId).innerHTML = 
                    '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
            })
            .catch(error => {
                document.getElementById(resultId).innerHTML = 
                    '<div style="color: red;">Error: ' + error.message + '</div>';
            });
        }
    </script>
</head>
<body>
    <h2>JSON Data Demo</h2>
    
    <div class="example">
        <h3>📦 Simple JSON Example:</h3>
        <p>Send a simple user object:</p>
        <button onclick="sendSimpleJSON()">Send Simple JSON</button>
        <div id="simple-result" class="result"></div>
    </div>
    
    <div class="example">
        <h3>🔧 Complex JSON Example:</h3>
        <p>Send nested objects and arrays:</p>
        <button onclick="sendComplexJSON()">Send Complex JSON</button>
        <div id="complex-result" class="result"></div>
    </div>
    
    <div class="example">
        <h3>✏️ Custom JSON Example:</h3>
        <p>Write your own JSON and send it:</p>
        <textarea id="custom-json" placeholder='{"message": "Hello World", "number": 42}'></textarea>
        <br>
        <button onclick="sendCustomJSON()">Send Custom JSON</button>
        <div id="custom-result" class="result"></div>
    </div>
    
    <div class="example">
        <h3>🔧 Test with curl:</h3>
        <p>Try these commands in terminal:</p>
        <pre>
curl -X POST http://127.0.0.1:5000/api/user \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "age": 25, "email": "test@example.com"}'

curl -X POST http://127.0.0.1:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"products": [{"name": "Book", "price": 15}]}'
        </pre>
    </div>
    
    <h3>📋 Available API Endpoints:</h3>
    <ul>
        <li><code>POST /api/user</code> - User data</li>
        <li><code>POST /api/complex</code> - Complex nested data</li>
        <li><code>POST /api/custom</code> - Any JSON data</li>
        <li><code>POST /api/products</code> - Product list</li>
        <li><code>GET /api/info</code> - Request information</li>
    </ul>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(json_html)

@app.route('/api/user', methods=['POST'])
def handle_user():
    # Check if request contains JSON
    if not request.is_json:
        return jsonify({
            'error': 'Content-Type must be application/json',
            'received': request.headers.get('Content-Type', 'Not specified')
        }), 400
    
    # Get JSON data
    user_data = request.get_json()
    
    # Validate required fields
    if not user_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    required_fields = ['name', 'age', 'email']
    missing_fields = [field for field in required_fields if field not in user_data]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing': missing_fields,
            'required': required_fields
        }), 400
    
    # Process the user data
    response = {
        'message': 'User created successfully!',
        'user': {
            'name': user_data['name'],
            'age': user_data['age'],
            'email': user_data['email'],
            'id': 12345  # Fake ID
        },
        'received_data': user_data,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

@app.route('/api/complex', methods=['POST'])
def handle_complex():
    """Handle complex nested JSON data"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    complex_data = request.get_json()
    
    if not complex_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    # Process the complex data
    response = {
        'message': 'Complex data processed successfully!',
        'analysis': {
            'total_keys': len(complex_data.keys()),
            'has_user': 'user' in complex_data,
            'has_products': 'products' in complex_data,
            'has_metadata': 'metadata' in complex_data
        },
        'processed_data': complex_data,
        'server_timestamp': datetime.now().isoformat()
    }
    
    # Add specific processing for known structures
    if 'user' in complex_data:
        user = complex_data['user']
        response['user_info'] = {
            'name': user.get('name', 'Unknown'),
            'age_group': 'adult' if user.get('age', 0) >= 18 else 'minor',
            'has_preferences': 'preferences' in user
        }
    
    if 'products' in complex_data:
        products = complex_data['products']
        if isinstance(products, list):
            response['product_summary'] = {
                'count': len(products),
                'total_value': sum(p.get('price', 0) for p in products),
                'product_names': [p.get('name', 'Unknown') for p in products]
            }
    
    return jsonify(response)

@app.route('/api/custom', methods=['POST'])
def handle_custom():
    """Handle any custom JSON data"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    custom_data = request.get_json()
    
    if not custom_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    # Analyze the custom data
    def analyze_json(data, path="root"):
        """Recursively analyze JSON structure"""
        if isinstance(data, dict):
            return {
                'type': 'object',
                'keys': list(data.keys()),
                'key_count': len(data),
                'nested_analysis': {k: analyze_json(v, f"{path}.{k}") for k, v in data.items()}
            }
        elif isinstance(data, list):
            return {
                'type': 'array',
                'length': len(data),
                'item_types': [type(item).__name__ for item in data],
                'sample_items': data[:3] if len(data) > 3 else data
            }
        else:
            return {
                'type': type(data).__name__,
                'value': data
            }
    
    analysis = analyze_json(custom_data)
    
    response = {
        'message': 'Custom JSON processed successfully!',
        'received_data': custom_data,
        'structure_analysis': analysis,
        'data_size': len(str(custom_data)),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

@app.route('/api/products', methods=['POST'])
def handle_products():
    """Handle product data specifically"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    product_data = request.get_json()
    
    if not product_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    if 'products' not in product_data:
        return jsonify({'error': 'Expected "products" key in JSON'}), 400
    
    products = product_data['products']
    
    if not isinstance(products, list):
        return jsonify({'error': 'Products must be an array'}), 400
    
    # Process products
    processed_products = []
    total_value = 0
    
    for i, product in enumerate(products):
        if not isinstance(product, dict):
            return jsonify({'error': f'Product at index {i} must be an object'}), 400
        
        name = product.get('name', f'Product {i+1}')
        price = product.get('price', 0)
        
        try:
            price = float(price)
        except (ValueError, TypeError):
            price = 0
        
        processed_product = {
            'id': product.get('id', i+1),
            'name': name,
            'price': price,
            'category': product.get('category', 'Uncategorized'),
            'in_stock': product.get('in_stock', True)
        }
        
        processed_products.append(processed_product)
        total_value += price
    
    response = {
        'message': f'Successfully processed {len(processed_products)} products',
        'products': processed_products,
        'summary': {
            'total_products': len(processed_products),
            'total_value': round(total_value, 2),
            'average_price': round(total_value / len(processed_products), 2) if processed_products else 0,
            'categories': list(set(p['category'] for p in processed_products))
        },
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

@app.route('/api/info', methods=['GET'])
def request_info():
    """Get information about the current request"""
    info = {
        'method': request.method,
        'url': request.url,
        'base_url': request.base_url,
        'headers': dict(request.headers),
        'remote_addr': request.remote_addr,
        'user_agent': request.user_agent.string,
        'timestamp': datetime.now().isoformat(),
        'available_endpoints': [
            {'method': 'GET', 'path': '/', 'description': 'Main demo page'},
            {'method': 'POST', 'path': '/api/user', 'description': 'Handle user data'},
            {'method': 'POST', 'path': '/api/complex', 'description': 'Handle complex nested data'},
            {'method': 'POST', 'path': '/api/custom', 'description': 'Handle any custom JSON'},
            {'method': 'POST', 'path': '/api/products', 'description': 'Handle product data'},
            {'method': 'GET', 'path': '/api/info', 'description': 'Get request information'}
        ]
    }
    
    return jsonify(info)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': 'The request was invalid',
        'timestamp': datetime.now().isoformat()
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            'GET /',
            'POST /api/user',
            'POST /api/complex',
            'POST /api/custom',
            'POST /api/products',
            'GET /api/info'
        ],
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Flask JSON API Demo...")
    print("📱 Open your browser to: http://127.0.0.1:5000")
    print("🔧 API endpoints available:")
    print("   POST /api/user - User data")
    print("   POST /api/complex - Complex nested data")
    print("   POST /api/custom - Any JSON data")
    print("   POST /api/products - Product data")
    print("   GET /api/info - Request information")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='127.0.0.1', port=5000)