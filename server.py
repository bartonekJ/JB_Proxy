from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def parse_model(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        html = requests.get(url, headers=headers, timeout=15).text
    except Exception as e:
        return {"error": f"Download failed: {e}"}

    soup = BeautifulSoup(html, "html.parser")

    stats = {
        "title": None,
        "price": None,
        "likes": None,
        "downloads": None,
        "views": None,
        "total": None
    }

    h1 = soup.find("h1")
    if h1:
        stats["title"] = h1.text.strip()

    price_el = soup.find("span", {"data-js": "price"})
    if price_el:
        stats["price"] = price_el.text.strip()

    likes_el = soup.find("span", {"title": "Likes"})
    if likes_el:
        stats["likes"] = likes_el.text.strip()

    downloads_el = soup.find("span", {"title": "Downloads"})
    if downloads_el:
        stats["downloads"] = downloads_el.text.strip()

    views_el = soup.find("span", {"title": "Views"})
    if views_el:
        stats["views"] = views_el.text.strip()

    total_el = soup.find("span", {"title": "Total earned"})
    if total_el:
        stats["total"] = total_el.text.strip()

    return stats

@app.route("/")
def home():
    return "Cults3D Proxy Running. Use /stats?url=...", 200

@app.route("/stats")
def stats():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing ?url="})
    return jsonify(parse_model(url))
