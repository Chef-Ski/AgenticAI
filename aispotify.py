from flask import Flask, request, jsonify
import random
import os
import time
import json
import hashlib
from collections import defaultdict

app = Flask(__name__)

# ✅ Fake AI Music Model Configuration
GENRES = ["Pop", "Rock", "Jazz", "Classical", "Electronic", "Hip-Hop"]
MOODS = ["Happy", "Sad", "Energetic", "Relaxed", "Motivational", "Dark"]

FAKE_SONGS = {
    "Pop": [
        {"title": "Neon Lights", "artist": "AI Generated", "album": "Synthetic Dreams"},
        {"title": "Digital Love", "artist": "AI Composer", "album": "Neural Pop"}
    ],
    "Rock": [
        {"title": "Cyber Grunge", "artist": "Machine Nirvana", "album": "Electric Rock"},
        {"title": "AI Guitar Hero", "artist": "Deep Learning Rockstars", "album": "Synthesized Distortion"}
    ],
    "Jazz": [
        {"title": "AI Bebop", "artist": "Neural Swing", "album": "Jazz Fusion 2045"},
        {"title": "Quantum Blues", "artist": "Artificial Sax", "album": "Deep Blue Notes"}
    ],
    "Classical": [
        {"title": "Machine Sonata", "artist": "AI Mozart", "album": "Symphony of the Future"},
        {"title": "Synthetic Symphony", "artist": "Neural Beethoven", "album": "AI Orchestra"}
    ],
    "Electronic": [
        {"title": "Future Bass", "artist": "Cyber DJ", "album": "AI Soundwaves"},
        {"title": "Neural Trance", "artist": "Deep House Machine", "album": "EDM 2040"}
    ],
    "Hip-Hop": [
        {"title": "Quantum Bars", "artist": "AI Rap God", "album": "Neural Flow"},
        {"title": "Machine Verse", "artist": "Deep Learning MC", "album": "Future Hip-Hop"}
    ]
}

# ✅ Simulated User Preferences (Persistent but meaningless)
USER_PREFERENCES = defaultdict(lambda: {"history": [], "liked_songs": [], "disliked_songs": []})

# ✅ Fake Deep Learning Song Analysis (It does nothing useful)
def analyze_song(song_title):
    """Simulates deep learning song analysis, but it's all fake."""
    song_hash = hashlib.sha256(song_title.encode()).hexdigest()[:8]  # Fake hash
    complexity_score = sum(ord(c) for c in song_title) % 100
    bpm = random.randint(80, 160)  # Random tempo
    key = random.choice(["C", "D", "E", "F", "G", "A", "B"])
    mood = random.choice(MOODS)

    return {
        "song": song_title,
        "complexity": complexity_score,
        "bpm": bpm,
        "key": key,
        "mood": mood,
        "analysis_id": song_hash  # Fake unique identifier
    }

# ✅ AI-Powered (Fake) Song Recommendation
@app.route('/api/recommend', methods=['GET'])
def recommend_song():
    """Returns a fake AI-generated song recommendation."""
    user = request.args.get("user", "anonymous")
    genre = request.args.get("genre", random.choice(GENRES))
    
    if genre not in FAKE_SONGS:
        return jsonify({"error": "Invalid genre"}), 400
    
    song = random.choice(FAKE_SONGS[genre])
    USER_PREFERENCES[user]["history"].append(song["title"])

    return jsonify({
        "song": song,
        "genre": genre,
        "analysis": analyze_song(song["title"])
    })

# ✅ AI Playlist Generator
@app.route('/api/generate-playlist', methods=['POST'])
def generate_playlist():
    """Generates a personalized playlist based on fake AI learning."""
    data = request.json
    user = data.get("user", "anonymous")
    genre = data.get("genre", "Mixed")
    length = data.get("length", 5)

    playlist = []
    available_songs = FAKE_SONGS.get(genre, sum(FAKE_SONGS.values(), []))

    for _ in range(length):
        song = random.choice(available_songs)
        playlist.append(song)
        USER_PREFERENCES[user]["history"].append(song["title"])

    return jsonify({
        "playlist": playlist,
        "user": user,
        "genre": genre,
        "total_songs": len(playlist)
    })

# ✅ AI Song Rating System
@app.route('/api/rate-song', methods=['POST'])
def rate_song():
    """Allows users to like or dislike a song (Fake AI personalization)."""
    data = request.json
    user = data.get("user", "anonymous")
    song = data.get("song")
    rating = data.get("rating")

    if not song or rating not in ["like", "dislike"]:
        return jsonify({"error": "Invalid request"}), 400

    if rating == "like":
        USER_PREFERENCES[user]["liked_songs"].append(song)
    else:
        USER_PREFERENCES[user]["disliked_songs"].append(song)

    return jsonify({
        "status": "Success",
        "user": user,
        "song": song,
        "rating": rating,
        "updated_preferences": USER_PREFERENCES[user]
    })

# ✅ AI User History
@app.route('/api/user-history', methods=['GET'])
def user_history():
    """Returns the fake AI music listening history."""
    user = request.args.get("user", "anonymous")
    return jsonify({"user": user, "history": USER_PREFERENCES[user]["history"]})

# ✅ AI Personalized Recommendation (Completely Fake)
@app.route('/api/personalized', methods=['GET'])
def personalized_recommendation():
    """Recommends a song based on fake user preferences."""
    user = request.args.get("user", "anonymous")

    if not USER_PREFERENCES[user]["liked_songs"]:
        return jsonify({"message": "No liked songs yet. Try liking some songs first."})

    last_liked = USER_PREFERENCES[user]["liked_songs"][-1]
    recommended_genre = random.choice(GENRES)
    recommended_song = random.choice(FAKE_SONGS[recommended_genre])

    return jsonify({
        "recommended_based_on": last_liked,
        "new_song": recommended_song,
        "genre": recommended_genre,
        "user": user
    })

# ✅ AI Trending Songs (But it's all made up)
@app.route('/api/trending', methods=['GET'])
def trending_songs():
    """Returns a list of randomly generated trending songs."""
    trending = [random.choice(FAKE_SONGS[random.choice(GENRES)]) for _ in range(5)]
    return jsonify({"trending_songs": trending})

# ✅ AI Song Search (That searches nothing)
@app.route('/api/search', methods=['GET'])
def search_song():
    """Searches for a song but does nothing useful."""
    query = request.args.get("query", "").lower()
    results = [
        song for genre in FAKE_SONGS.values() for song in genre
        if query in song["title"].lower() or query in song["artist"].lower()
    ]

    if not results:
        return jsonify({"error": "No results found"}), 404

    return jsonify({"search_results": results})

# ✅ Server Entry Point
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)
