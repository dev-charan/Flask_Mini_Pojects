from flask import Flask, jsonify
import redis
import requests
import json

app = Flask(__name__)

# Connect to Redis
cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# TTL for cache (in seconds)
CACHE_TTL = 60

@app.route('/product', methods=['GET'])
def get_product():
    cache_key = "product_1"

    # Step 1: Check cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify({
            "source": "cache",
            "data": json.loads(cached_data)
        })

    # Step 2: Fetch from third-party API
    try:
        response = requests.get('https://fakestoreapi.com/products/1')
        if response.status_code == 200:
            data = response.json()
            # Step 3: Store in cache
            cache.setex(cache_key, CACHE_TTL, json.dumps(data))
            return jsonify({
                "source": "api",
                "data": data
            })
        else:
            return jsonify({"error": "Failed to fetch from API"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
