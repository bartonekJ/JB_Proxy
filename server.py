from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def scrape_model(url):
    try:
        # Fetch HTML
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}"}

        soup = BeautifulSoup(r.text, "html.parser")

        # Extract the Next.js JSON block
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            return {"error": "NEXT_DATA not found"}

        data = json.loads(script.string)

        # Navigate the structure
        model = data["props"]["pageProps"]["model"]

        title = model.get("title", None)

        stats = model.get("statistics", {})
        views = stats.get("views", None)
        downloads = stats.get("downloads", None)
        likes = stats.get("likes", None)

        sales = stats.get("sales", {})
        price = sales.get("price", None)
        total = sales.get("total", None)

        return {
            "title": title,
            "views": views,
            "downloads": downloads,
            "likes": likes,
            "price": price,
            "total": total
        }

    except Exception as e:
        return {"error": str(e)}

@app.route("/stats")
def stats():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing ?url=xxx"})
    return jsonify(scrape_model(url))

@app.route("/")
def home():
    return "Cults3D Lightweight Proxy Running!"
