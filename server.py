from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def scrape_model(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")

            # Title
            title = page.locator("h1").inner_text()

            # Stats
            likes = page.locator('[title="Likes"]').inner_text()
            downloads = page.locator('[title="Downloads"]').inner_text()
            views = page.locator('[title="Views"]').inner_text()

            # Price
            price = page.locator('[data-js="price"]').inner_text()

            # Total earned
            total = page.locator('[title="Total earned"]').inner_text()

            browser.close()

            return {
                "title": title,
                "price": price,
                "likes": likes,
                "downloads": downloads,
                "views": views,
                "total": total
            }

        except Exception as e:
            browser.close()
            return {"error": str(e)}

@app.route("/stats")
def stats():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing ?url=xxx"})
    return jsonify(scrape_model(url))

@app.route("/")
def home():
    return "Cults3D Playwright Proxy Running!"
