# 2. URL PARAMETERS (Query String) EXAMPLE
# This handles data passed in the URL after the ? symbol
# Example: /search?q=python&page=2&category=programming

from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template with links that contain URL parameters
home_html = """
<!DOCTYPE html>
<html>
<head>
    <title>URL Parameters Example</title>
</head>
<body>
    <h2>URL Parameters Demo</h2>
    <p>Click these links to see URL parameters in action:</p>
    
    <h3>Search Examples:</h3>
    <ul>
        <li><a href="/search?q=python">Search for "python"</a></li>
        <li><a href="/search?q=flask&page=2">Search for "flask" on page 2</a></li>
        <li><a href="/search?q=web development&page=3&category=programming">Complex search</a></li>
        <li><a href="/search">Search with no parameters</a></li>
    </ul>
    
    <h3>Product Examples:</h3>
    <ul>
        <li><a href="/products?category=electronics&min_price=100&max_price=500">Electronics $100-500</a></li>
        <li><a href="/products?category=books&sort=price&order=asc">Books sorted by price</a></li>
    </ul>
    
    <h3>Manual URL Test:</h3>
    <p>Try typing in your browser: <code>http://127.0.0.1:5000/search?q=YOUR_SEARCH&page=5</code></p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_html)

@app.route('/search')
def search():
    # Get URL parameters (query string)
    query = request.args.get('q', '')                    # Get 'q' parameter, default to empty string
    page = request.args.get('page', 1, type=int)         # Get 'page' parameter, convert to int, default 1
    category = request.args.get('category', 'all')       # Get 'category' parameter, default 'all'
    
    # Get all URL parameters as dictionary
    all_params = request.args.to_dict()
    
    # Build result
    result = f"""
    <h2>Search Results</h2>
    <p><strong>Search Query:</strong> '{query}' (empty if not provided)</p>
    <p><strong>Page Number:</strong> {page}</p>
    <p><strong>Category:</strong> {category}</p>
    <p><strong>All URL Parameters:</strong> {all_params}</p>
    
    <h3>URL Breakdown:</h3>
    <p><strong>Full URL:</strong> {request.url}</p>
    <p><strong>Base URL:</strong> {request.base_url}</p>
    <p><strong>Query String:</strong> {request.query_string.decode()}</p>
    
    <br>
    <a href="/">← Back to examples</a>
    """
    
    return result

@app.route('/products')
def products():
    # Multiple parameters for filtering/sorting
    category = request.args.get('category', 'all')
    min_price = request.args.get('min_price', 0, type=int)
    max_price = request.args.get('max_price', 999999, type=int)
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')
    
    # Get multiple values for same parameter (like tags)
    tags = request.args.getlist('tags')  # For URLs like: ?tags=new&tags=sale&tags=popular
    
    result = f"""
    <h2>Product Filter</h2>
    <p><strong>Category:</strong> {category}</p>
    <p><strong>Price Range:</strong> ${min_price} - ${max_price}</p>
    <p><strong>Sort By:</strong> {sort_by} ({order})</p>
    <p><strong>Tags:</strong> {tags if tags else 'None'}</p>
    
    <h3>Try these URLs:</h3>
    <ul>
        <li><code>/products?category=electronics&min_price=50&max_price=200</code></li>
        <li><code>/products?tags=new&tags=sale&tags=featured</code></li>
        <li><code>/products?sort=price&order=desc</code></li>
    </ul>
    
    <br>
    <a href="/">← Back to examples</a>
    """
    
    return result

if __name__ == '__main__':
    print("Visit: http://127.0.0.1:5000")
    print("Click the links to see how URL parameters work")
    print("URL parameters come after the ? in the URL")
    app.run(debug=True)