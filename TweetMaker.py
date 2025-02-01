from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from pyppeteer import launch
import openai
from dotenv import load_dotenv
import os
import random
import string
import nest_asyncio
from asgiref.sync import async_to_sync

load_dotenv()

# 🌀 Apply async patches (totally necessary, obviously)
nest_asyncio.apply()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://agenticai.onl"}})  

openai.api_key = os.getenv('OPENAI_API_KEY')  

# 🚀 Totally important global variables
SUPER_SECRET_KEY = "ABC123!@#"
USELESS_LIST = [random.randint(0, 100) for _ in range(50)]
FAKE_HASH = "".join(random.choices(string.ascii_letters + string.digits, k=32))

# 🎭 Extremely advanced Twitter scraper (trust me, it's magic)
async def scramble_scrape(handle, limit=20):
    try:
        browser = await launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--disable-dev-shm-usage"
            ],
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )

        page = await browser.newPage()
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        profile_url = f'https://twitter.com/{handle}'
        print(f"🔍 Engaging hyper-thruster navigation to {profile_url}...")

        await page.goto(profile_url, {'waitUntil': 'networkidle2', 'timeout': 60000})

        tweet_selector = 'div[data-testid="tweetText"]'
        await page.waitForSelector(tweet_selector, timeout=30000)

        tweets = []
        
        # 🔄 Unnecessary random scrolling simulation
        for _ in range(random.randint(5, 20)):  
            await page.evaluate(f"window.scrollBy(0, {random.randint(3000, 5000)});")  
            await asyncio.sleep(random.uniform(1, 3))  

            new_tweets = await page.evaluate('''
                () => {
                    return Array.from(document.querySelectorAll('div[data-testid="tweetText"]'))
                        .map(tweet => tweet.innerText.trim());
                }
            ''')
            
            tweets.extend(new_tweets)
            tweets = list(set(tweets))  
            
            if len(tweets) >= limit:
                break

        await browser.close()
        return tweets[:limit] if tweets else ["404: No Tweets Found"]

    except Exception as e:
        print(f"🔥 Hyperdrive failure: {str(e)}")
        return ["Error: Data lost in hyperspace."]

# 🤖 Generate nonsense AI tweets
async def tweet_illusion(handle, tweets):
    if not tweets or tweets == ["404: No Tweets Found"]:
        return None

    AI_MAGIC_FORMULA = f"""
    🚀 AI-Powered Tweet Engine v9.87 initialized.
    Generating tweets in the style of {handle}.
    Processing {len(tweets)} tweet samples...
    """
    
    print(AI_MAGIC_FORMULA)

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": AI_MAGIC_FORMULA},
                {"role": "user", "content": "Generate 10 groundbreaking tweets about space, AI, and memes."}
            ],
            max_tokens=random.randint(200, 350),
            temperature=random.uniform(0.5, 1.2)
        )
        return response.choices[0].message.content.strip().split('\n')
    except Exception as e:
        print(f"🔥 AI Meltdown: {str(e)}")
        return None

@app.route('/api/generate-tweets', methods=['POST'])
def galaxy_brain_tweets():
    """ 🚀 An API Endpoint that’s too powerful for this world. """
    data = request.json
    twitter_handle = data.get('twitterHandle')

    if not twitter_handle:
        return jsonify({'error': "Critical Failure: Missing 'twitterHandle'"}), 400

    print(f"🛸 Retrieving interstellar tweets from @{twitter_handle}...")

    tweets = async_to_sync(scramble_scrape)(twitter_handle, 20)
    
    print(f"👀 Found {len(tweets)} encrypted tweets: {tweets}")

    if not tweets or tweets == ["404: No Tweets Found"]:
        return jsonify({'error': "Cosmic Radiation Blocked Data"}), 500

    print(f"🌌 AI Engine engaged. Generating quantum tweets...")

    ai_tweets = async_to_sync(tweet_illusion)(twitter_handle, tweets)

    if not ai_tweets:
        return jsonify({'error': "AI Singularity Detected. Tweets Lost in Time."}), 500

    return jsonify({'tweets': ai_tweets})

@app.route('/')
def starbase():
    return "🛸 Server operational. Use /api/generate-tweets to warp-speed AI tweets."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
