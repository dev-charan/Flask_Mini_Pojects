# 4. HEADERS EXAMPLE
# Headers are additional information sent with HTTP requests
# Common headers: Content-Type, Authorization, User-Agent, etc.

from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# HTML template with examples and JavaScript for AJAX requests
headers_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Headers Example</title>
    <script>
        function sendAjaxRequest() {
            fetch('/api/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Custom-Header': 'MyCustomValue',
                    'Authorization': 'Bearer fake-token-123'
                },
                body: JSON.stringify({message: 'Hello from JavaScript!'})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('ajax-result').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            });
        }
    </script>
</head>
<body>
    <h2>Headers Demo</h2>
    
    <h3>👆 Click to see your current headers:</h3>
    <p><a href="/headers">View Headers from Browser</a></p>
    
    <h3>🔧 Test Custom Headers with JavaScript:</h3>
    <button onclick="sendAjaxRequest()">Send AJAX Request with Custom Headers</button>
    <div id="ajax-result"></div>
    
    <h3>🧪 Test with curl commands:</h3>
    <p>Open terminal and try these commands:</p>
    <pre>
    curl -H "Content-Type: application/json" http://127.0.0.1:5000/headers
    curl -H "Authorization: Bearer my-token" http://127.0.0.1:5000/headers
    curl -H "X-Custom-Header: MyValue" http://127.0.0.1:5000/headers
    </pre>
    
    <h3>📱 Different User Agents:</h3>
    <p>Try these curl commands to simulate different devices:</p>
    <pre>
    curl -H "User-Agent: Mozilla/5.0 (iPhone)" http://127.0.0.1:5000/headers
    curl -H "User-Agent: MyBot/1.0" http://127.0.0.1:5000/headers
    </pre>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(headers_html)

@app.route('/headers')
def show_headers():
    # Get specific headers
    content_type = request.headers.get('Content-Type', 'Not specified')
    user_agent = request.headers.get('User-Agent', 'Not specified')
    authorization = request.headers.get('Authorization', 'Not provided')
    accept = request.headers.get('Accept', 'Not specified')
    
    # Get custom headers (usually start with X-)
    custom_header = request.headers.get('X-Custom-Header', 'Not provided')
    
    # Get all headers as dictionary
    all_headers = dict(request.headers)
    
    # Check for specific header patterns
    is_mobile = 'mobile' in user_agent.lower() or 'iphone' in user_agent.lower()
    is_api_request = content_type == 'application/json'
    has_auth = authorization != 'Not provided'
    
    result = f"""
    <h2>Request Headers Analysis</h2>
    
    <h3>🔍 Key Headers:</h3>
    <p><strong>Content-Type:</strong> {content_type}</p>
    <p><strong>User-Agent:</strong> {user_agent}</p>
    <p><strong>Authorization:</strong> {authorization}</p>
    <p><strong>Accept:</strong> {accept}</p>
    <p><strong>Custom Header:</strong> {custom_header}</p>
    
    <h3>📊 Analysis:</h3>
    <p><strong>Mobile Device:</strong> {'Yes' if is_mobile else 'No'}</p>
    <p><strong>API Request:</strong> {'Yes' if is_api_request else 'No'}</p>
    <p><strong>Has Authentication:</strong> {'Yes' if has_auth else 'No'}</p>
    
    <h3>📋 All Headers:</h3>
    <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; font-family: monospace;">
    """
    
    for header, value in all_headers.items():
        result += f"<strong>{header}:</strong> {value}<br>"
    
    result += """
    </div>
    
    <br>
    <a href="/">← Back to examples</a>
    """
    
    return result

@app.route('/api/data', methods=['POST'])
def api_endpoint():
    # This endpoint specifically looks for API-related headers
    content_type = request.headers.get('Content-Type')
    authorization = request.headers.get('Authorization')
    custom_header = request.headers.get('X-Custom-Header')
    
    # Check if request has proper API headers
    if content_type != 'application/json':
        return jsonify({
            'error': 'Content-Type must be application/json',
            'received': content_type
        }), 400
    
    if not authorization:
        return jsonify({
            'error': 'Authorization header required',
            'hint': 'Include Authorization: Bearer your-token'
        }), 401
    
    # Process the request
    data = request.get_json() if request.is_json else {}
    
    response = {
        'message': 'Success! Headers received correctly',
        'received_headers': {
            'Content-Type': content_type,
            'Authorization': authorization,
            'X-Custom-Header': custom_header
        },
        'received_data': data,
        'analysis': {
            'has_valid_content_type': content_type == 'application/json',
            'has_authorization': bool(authorization),
            'has_custom_header': bool(custom_header)
        }
    }
    
    return jsonify(response)

@app.route('/auth-required')
def auth_required():
    # Example of checking authorization header
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({'error': 'Authorization header required'}), 401
    
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization must be Bearer token'}), 401
    
    token = auth_header.split(' ')[1]
    
    # In real app, you'd validate the token
    if token != 'valid-token-123':
        return jsonify({'error': 'Invalid token'}), 401
    
    return jsonify({'message': 'Access granted!', 'token': token})

@app.route('/user-agent-test')
def user_agent_test():
    # Analyze user agent header
    user_agent = request.headers.get('User-Agent', '')
    
    # Simple user agent analysis
    analysis = {
        'raw_user_agent': user_agent,
        'is_mobile': any(keyword in user_agent.lower() for keyword in ['mobile', 'iphone', 'android']),
        'is_bot': any(keyword in user_agent.lower() for keyword in ['bot', 'crawler', 'spider']),
        'browser': 'Unknown'
    }
    
    # Simple browser detection
    if 'chrome' in user_agent.lower():
        analysis['browser'] = 'Chrome'
    elif 'firefox' in user_agent.lower():
        analysis['browser'] = 'Firefox'
    elif 'safari' in user_agent.lower():
        analysis['browser'] = 'Safari'
    elif 'edge' in user_agent.lower():
        analysis['browser'] = 'Edge'
    
    return jsonify(analysis)

if __name__ == '__main__':
    print("Visit: http://127.0.0.1:5000")
    print("Headers contain metadata about the request")
    print("Try the curl commands to see different headers!")
    app.run(debug=True)