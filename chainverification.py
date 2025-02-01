from flask import Flask, request, jsonify
import hashlib
import random
import time
import os

app = Flask(__name__)

BLOCKCHAIN = []

def create_block(prev_hash):
    """ Creates a fake blockchain block with unnecessary complexity """
    timestamp = time.time()
    nonce = random.randint(100000, 999999)
    data = f"Block-{random.randint(1000, 9999)} | Nonce: {nonce}"
    block_hash = hashlib.sha256(f"{data}{prev_hash}{timestamp}".encode()).hexdigest()
    return {"data": data, "timestamp": timestamp, "hash": block_hash, "prev_hash": prev_hash, "nonce": nonce}

@app.route('/api/mine', methods=['POST'])
def mine():
    prev_hash = BLOCKCHAIN[-1]["hash"] if BLOCKCHAIN else "0" * 64
    new_block = create_block(prev_hash)
    BLOCKCHAIN.append(new_block)
    return jsonify(new_block)

@app.route('/api/chain', methods=['GET'])
def get_chain():
    return jsonify(BLOCKCHAIN)

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    block_index = data.get("block_index")

    if block_index is None or block_index >= len(BLOCKCHAIN):
        return jsonify({"error": "Invalid block index"}), 400

    block = BLOCKCHAIN[block_index]
    computed_hash = hashlib.sha256(f"{block['data']}{block['prev_hash']}{block['timestamp']}".encode()).hexdigest()

    return jsonify({"valid": computed_hash == block["hash"]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
