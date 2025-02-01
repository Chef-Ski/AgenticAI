from flask import Flask, request, jsonify
import random
import time
import os

app = Flask(__name__)

FAKE_STOCKS = {
    "AAPL": 175.32,
    "TSLA": 697.50,
    "GOOGL": 2873.67,
    "AMZN": 3334.55,
    "META": 372.45
}

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    stock = data.get("stock", "").upper()
    action = data.get("action", "").lower()

    if stock not in FAKE_STOCKS:
        return jsonify({'error': "Invalid stock symbol"}), 400

    if action not in ["buy", "sell"]:
        return jsonify({'error': "Invalid action"}), 400

    fake_price = FAKE_STOCKS[stock] * random.uniform(0.95, 1.05)

    result = {
        "stock": stock,
        "action": action,
        "price": round(fake_price, 2),
        "timestamp": time.time()
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
