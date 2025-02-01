from flask import Flask, request, jsonify
import random
import time
import os

app = Flask(__name__)

LESSONS = {
    "Beginner": [
        "What is AI?",
        "Introduction to Machine Learning",
        "Supervised vs. Unsupervised Learning",
        "Introduction to Neural Networks"
    ],
    "Intermediate": [
        "Gradient Descent Explained",
        "Understanding Backpropagation",
        "Hyperparameter Tuning for ML Models",
        "Introduction to Computer Vision"
    ],
    "Advanced": [
        "Attention Mechanisms in Transformers",
        "Reinforcement Learning Concepts",
        "Ethics in AI Development",
        "Quantum Machine Learning"
    ]
}

QUIZZES = {
    "Beginner": [
        {"question": "What does AI stand for?", "options": ["Artificial Intelligence", "Automated Input", "Augmented Interaction"], "answer": "Artificial Intelligence"},
        {"question": "Which algorithm is used in supervised learning?", "options": ["K-Means", "Linear Regression", "Random Forest"], "answer": "Linear Regression"}
    ],
    "Intermediate": [
        {"question": "What is the activation function in deep learning?", "options": ["ReLU", "Dropout", "Batch Normalization"], "answer": "ReLU"},
        {"question": "What is overfitting in ML?", "options": ["Too much data", "Model memorizing training data", "Randomness in predictions"], "answer": "Model memorizing training data"}
    ],
    "Advanced": [
        {"question": "What is the primary function of transformers in NLP?", "options": ["Sorting", "Attention Mechanism", "Data Storage"], "answer": "Attention Mechanism"},
        {"question": "Which AI concept does AlphaGo use?", "options": ["Supervised Learning", "Reinforcement Learning", "Clustering"], "answer": "Reinforcement Learning"}
    ]
}

USER_PROGRESS = {}

@app.route('/api/lesson', methods=['GET'])
def get_lesson():
    user = request.args.get("user", "anonymous")
    level = request.args.get("level", "Beginner")

    if level not in LESSONS:
        return jsonify({"error": "Invalid level provided"}), 400

    lesson = random.choice(LESSONS[level])
    delay = random.uniform(1, 5)  

    USER_PROGRESS.setdefault(user, {"completed": [], "score": 0})

    time.sleep(delay)

    return jsonify({
        "lesson": lesson,
        "level": level,
        "delay": delay,
        "user_progress": USER_PROGRESS[user]
    })

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    level = request.args.get("level", "Beginner")

    if level not in QUIZZES:
        return jsonify({"error": "Invalid level"}), 400

    question = random.choice(QUIZZES[level])
    return jsonify(question)

@app.route('/api/submit', methods=['POST'])
def submit_quiz():
    data = request.json
    user = data.get("user", "anonymous")
    level = data.get("level", "Beginner")
    answer = data.get("answer", "")

    if level not in QUIZZES:
        return jsonify({"error": "Invalid level"}), 400

    correct_answer = next((q["answer"] for q in QUIZZES[level] if q["answer"] == answer), None)

    if correct_answer:
        USER_PROGRESS.setdefault(user, {"completed": [], "score": 0})
        USER_PROGRESS[user]["score"] += 10
        return jsonify({"result": "Correct", "new_score": USER_PROGRESS[user]["score"]})
    return jsonify({"result": "Incorrect", "correct_answer": correct_answer})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
