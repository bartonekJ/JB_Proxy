from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

def scrape_model(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}"}

        soup = BeautifulSoup(r.text, "html.parser")

        data = None

        # Try JSON from Next.js
        script = soup.find("script", id="__NEXT_DATA__")
        if script and script.string:
            try:
                data = json.loads(script.string)
            except:
                data = None

        # Try JSON from Rails store
        if not data:
            alt = soup.find("script", attrs={"data-js-react-on-rails-store": True})
            if alt and alt.string:
                try:
                    data = json.loads(alt.string)
                except:
                    data = None

        if not data:
            return {"error": "Model data not found"}

        # Normalize structure
        try:
            model = data["props"]["pageProps"]["model"]
        except:
            model = data.get("model", {})

        if not model:
            return {"error": "Model section missing"}

        title = model.get("title")
        
        stats = model.get("statistics", {})
        views = stats.get("views")
        downloads = stats.get("downloads")
        likes = stats.get("likes")

        sales = model.get("sales", {})
        price = sales.get("price")
        total = sales.get("total")

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
    return "Cults3D Non-Playwright Proxy Running!"
