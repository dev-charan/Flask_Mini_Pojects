# 3. REQUEST INFORMATION EXAMPLE
# This shows various information about the incoming HTTP request

from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template with different types of links
info_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Request Information Example</title>
</head>
<body>
    <h2>Request Information Demo</h2>
    <p>Visit these pages to see different request information:</p>
    
    <ul>
        <li><a href="/info">Basic request info</a></li>
        <li><a href="/info/user/123">URL with path parameter</a></li>
        <li><a href="/info?name=john&age=25">URL with query parameters</a></li>
        <li><a href="/about">About page</a></li>
        <li><a href="/contact">Contact page</a></li>
    </ul>
    
    <h3>Forms to test different methods:</h3>
    <form method="GET" action="/info">
        <input type="text" name="search" placeholder="Search term">
        <button type="submit">GET Request</button>
    </form>
    
    <form method="POST" action="/info">
        <input type="text" name="username" placeholder="Username">
        <button type="submit">POST Request</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(info_html)

@app.route('/info')
@app.route('/info/<path:extra_path>')  # This catches any extra path
def show_request_info(extra_path=None):
    # Get basic request information
    method = request.method                    # GET, POST, PUT, DELETE, etc.
    full_url = request.url                     # Complete URL
    base_url = request.base_url                # URL without query parameters
    path = request.path                        # Just the path part
    url_root = request.url_root                # The root URL
    
    # Client information
    user_agent = request.user_agent.string     # Browser information
    client_ip = request.remote_addr            # Client's IP address
    referrer = request.referrer                # Previous page (if any)
    
    # Server information
    host = request.host                        # Server host
    scheme = request.scheme                    # http or https
    
    # Function/endpoint information
    endpoint = request.endpoint                # The function name handling this request
    
    result = f"""
    <h2>Request Information</h2>
    
    <h3>🌐 URL Information:</h3>
    <p><strong>Full URL:</strong> {full_url}</p>
    <p><strong>Base URL:</strong> {base_url}</p>
    <p><strong>Path:</strong> {path}</p>
    <p><strong>URL Root:</strong> {url_root}</p>
    <p><strong>Host:</strong> {host}</p>
    <p><strong>Scheme:</strong> {scheme}</p>
    {f"<p><strong>Extra Path:</strong> {extra_path}</p>" if extra_path else ""}
    
    <h3>📡 Request Details:</h3>
    <p><strong>HTTP Method:</strong> {method}</p>
    <p><strong>Endpoint:</strong> {endpoint}</p>
    
    <h3>🖥️ Client Information:</h3>
    <p><strong>User Agent:</strong> {user_agent}</p>
    <p><strong>Client IP:</strong> {client_ip}</p>
    <p><strong>Referrer:</strong> {referrer if referrer else 'None (direct visit)'}</p>
    
    <h3>🔍 Query Parameters:</h3>
    <p><strong>Query String:</strong> {request.query_string.decode() if request.query_string else 'None'}</p>
    <p><strong>Args:</strong> {dict(request.args) if request.args else 'None'}</p>
    
    <h3>📝 Form Data (if POST):</h3>
    <p><strong>Form Data:</strong> {dict(request.form) if request.form else 'None'}</p>
    
    <br>
    <a href="/">← Back to examples</a>
    """
    
    return result

@app.route('/about')
def about():
    return f"""
    <h2>About Page</h2>
    <p>This is the about page.</p>
    <p>You came from: <strong>{request.referrer if request.referrer else 'Direct visit'}</strong></p>
    <p>Your browser: <strong>{request.user_agent.browser}</strong></p>
    <p>Your platform: <strong>{request.user_agent.platform}</strong></p>
    <br>
    <a href="/">← Back to home</a>
    """

@app.route('/contact')
def contact():
    return f"""
    <h2>Contact Page</h2>
    <p>Request method: <strong>{request.method}</strong></p>
    <p>Current path: <strong>{request.path}</strong></p>
    <p>Full URL: <strong>{request.url}</strong></p>
    <br>
    <a href="/">← Back to home</a>
    """

# Route that accepts different HTTP methods
@app.route('/methods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_methods():
    return f"""
    <h2>HTTP Methods Test</h2>
    <p>Current method: <strong>{request.method}</strong></p>
    <p>This endpoint accepts: GET, POST, PUT, DELETE</p>
    <p>Try using tools like Postman or curl to test different methods:</p>
    <ul>
        <li>curl -X GET http://127.0.0.1:5000/methods</li>
        <li>curl -X POST http://127.0.0.1:5000/methods</li>
        <li>curl -X PUT http://127.0.0.1:5000/methods</li>
        <li>curl -X DELETE http://127.0.0.1:5000/methods</li>
    </ul>
    <br>
    <a href="/">← Back to home</a>
    """

if __name__ == '__main__':
    print("Visit: http://127.0.0.1:5000")
    print("Explore different pages to see how request information changes")
    app.run(debug=True)