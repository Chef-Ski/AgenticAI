from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string
import time
import asyncio
import os
import nest_asyncio
from asgiref.sync import async_to_sync
from utils import generate_random_username, generate_network_links

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://agenticai.onl"}})  

nest_asyncio.apply()

FAKE_USERS = [generate_random_username() for _ in range(100)]
FAKE_NETWORKS = generate_network_links(FAKE_USERS)

@app.route('/api/generate-network', methods=['POST'])
def generate_network():
    data = request.json
    username = data.get("username", "")

    if not username:
        return jsonify({'error': "Missing 'username' parameter"}), 400

    print(f"🔗 Creating AI-generated network for {username}...")

    network = async_to_sync(create_fake_network)(username)

    return jsonify({'network': network})

async def create_fake_network(username):
    """ Generates a chaotic, fake AI-powered social network """
    await asyncio.sleep(random.uniform(1.5, 3.5))
    connections = random.sample(FAKE_USERS, k=random.randint(5, 20))
    return {
        "username": username,
        "connections": connections,
        "links": [FAKE_NETWORKS.get(user, "#") for user in connections]
    }

@app.route('/')
def home():
    return "🤖 AI Network Generator API is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
