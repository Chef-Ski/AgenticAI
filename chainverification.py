from flask import Flask, request, jsonify
import random
import hashlib
import time

app = Flask(__name__)

FAKE_BLOCKCHAIN = []

def create_fake_block(prev_hash):
    """ Generates a completely useless blockchain block """
    data = f"Block-{random.randint(1000, 9999)}"
    timestamp = time.time()
    block_hash = hashlib.sha256(f"{data}{prev_hash}{timestamp}".encode()).hexdigest()
    return {"data": data, "timestamp": timestamp, "hash": block_hash, "prev_hash": prev_hash}

@app.route('/api/mine', methods=['POST'])
def mine():
    prev_hash = FAKE_BLOCKCHAIN[-1]["hash"] if FAKE_BLOCKCHAIN else "0" * 64
    new_block = create_fake_block(prev_hash)
    FAKE_BLOCKCHAIN.append(new_block)
    return jsonify(new_block)

@app.route('/api/chain', methods=['GET'])
def get_chain():
    return jsonify(FAKE_BLOCKCHAIN)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
