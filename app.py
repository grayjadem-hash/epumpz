from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html
import random

DESTINATIONS = [
    {
        "name": "Amalfi Coast, Italy",
        "tags": ["romantic", "sunny", "coastal", "photogenic", "pasta", "beach", "photography"],
        "foods": [
            "Seafood linguine at a cliffside trattoria",
            "Handmade gnocchi with tomato-basil sauce",
            "Lemon pasta and tiramisu by the sea",
        ],
        "activities": [
            "Golden-hour beach date in Positano",
            "Couples photo walk through colorful streets",
            "Boat day to hidden coves with friends",
            "Sunset picnic with candid photography prompts",
        ],
    },
    {
        "name": "Bali, Indonesia",
        "tags": ["tropical", "wholesome", "creative", "relaxing", "beach", "friends", "photography"],
        "foods": [
            "Fresh seafood pasta at Jimbaran Beach",
            "Italian fusion dinner in Canggu",
            "Healthy brunch and coffee date by the coast",
        ],
        "activities": [
            "Beach day with girlfriends",
            "Waterfall photography adventure",
            "Sunrise walk and beachfront brunch",
            "Spa + gratitude journaling night",
        ],
    },
    {
        "name": "Lisbon + Cascais, Portugal",
        "tags": ["charming", "coastal", "playful", "warm", "friends", "bubbly", "photography"],
        "foods": [
            "Creamy truffle pasta in Alfama",
            "Ocean-view seafood risotto in Cascais",
            "Pastel de nata café hopping",
        ],
        "activities": [
            "Vintage tram photo challenge",
            "Cascais beach date and sunset boardwalk stroll",
            "Polaroid scavenger hunt with friends",
            "Rooftop dinner with live music",
        ],
    },
]


def score_destination(profile_text: str, interests: str, travel_style: str, destination: dict) -> int:
    content = f"{profile_text} {interests} {travel_style}".lower()
    score = 0
    for tag in destination["tags"]:
        if tag in content:
            score += 3
    if "beach" in content:
        score += 2
    if "pasta" in content:
        score += 2
    if "photography" in content or "photos" in content:
        score += 2
    return score


def build_result(profile_text: str, interests: str, style: str, days: int):
    ranked = sorted(DESTINATIONS, key=lambda d: score_destination(profile_text, interests, style, d), reverse=True)
    best = ranked[0]
    backup = ranked[1]
    itinerary = []
    for day in range(1, days + 1):
        itinerary.append((day, random.choice(best["activities"]), random.choice(best["foods"])))
    return best, backup, itinerary


def render_page(content: str) -> str:
    return f"""
<!doctype html>
<html>
<head>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Sweet Escape Planner</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #fff8f5; margin: 0; padding: 16px; }}
    .card {{ max-width: 680px; margin: 0 auto; background: white; border-radius: 16px; padding: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }}
    h1 {{ margin-top: 0; }}
    textarea, input, select {{ width: 100%; margin: 8px 0 12px; padding: 10px; border-radius: 10px; border: 1px solid #ddd; font-size: 16px; box-sizing: border-box; }}
    button {{ width: 100%; background: #ff5f8f; color: white; border: 0; padding: 12px; border-radius: 12px; font-size: 16px; font-weight: bold; }}
    .result {{ background: #fff3f8; border-radius: 12px; padding: 12px; margin-top: 14px; }}
    ul {{ margin-top: 6px; }}
    .hint {{ color: #444; font-size: 14px; }}
  </style>
</head>
<body>
  <div class=\"card\">
    <h1>🌴 Sweet Escape Planner</h1>
    <p class=\"hint\">Mobile-friendly vacation planner based on personality + interests.</p>
    <form method=\"POST\">
      <label>Describe her personality</label>
      <textarea name=\"personality\" rows=\"4\" placeholder=\"Sweet, bubbly, loves wholesome beach dates and quality time with friends\"></textarea>

      <label>Interests (comma-separated)</label>
      <input name=\"interests\" placeholder=\"beach dates, pasta, photography, girls trips\" />

      <label>Travel style</label>
      <select name=\"style\">
        <option>Balanced</option>
        <option>Romantic</option>
        <option>Social & fun</option>
        <option>Relaxing</option>
      </select>

      <label>Trip length (days)</label>
      <input type=\"number\" min=\"3\" max=\"10\" value=\"5\" name=\"days\" />

      <button type=\"submit\">✨ Generate Vacation Plan</button>
    </form>
    {content}
  </div>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send_html(self, body: str):
        payload = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        self._send_html(render_page(""))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        data = parse_qs(self.rfile.read(length).decode("utf-8"))

        personality = data.get("personality", [""])[0].strip()
        interests = data.get("interests", [""])[0].strip()
        style = data.get("style", ["Balanced"])[0]
        days_raw = data.get("days", ["5"])[0]

        try:
            days = max(3, min(10, int(days_raw)))
        except ValueError:
            days = 5

        if not personality:
            content = "<div class='result'>Please enter a personality description for better matching.</div>"
            self._send_html(render_page(content))
            return

        best, backup, itinerary = build_result(personality, interests, style, days)

        itinerary_items = "".join(
            f"<li><b>Day {day}:</b> {html.escape(activity)}<br/><i>Meal:</i> {html.escape(meal)}</li>"
            for day, activity, meal in itinerary
        )
        foods = "".join(f"<li>{html.escape(item)}</li>" for item in best["foods"])
        acts = "".join(f"<li>{html.escape(item)}</li>" for item in best["activities"])

        content = f"""
        <div class='result'>
          <h3>Top match: {html.escape(best['name'])}</h3>
          <b>🍝 Where to eat</b>
          <ul>{foods}</ul>
          <b>📸 Activities she'll love</b>
          <ul>{acts}</ul>
          <b>🗓️ Itinerary preview</b>
          <ul>{itinerary_items}</ul>
          <p><b>Backup option:</b> {html.escape(backup['name'])}</p>
        </div>
        """
        self._send_html(render_page(content))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8501), Handler)
    print("Running on http://0.0.0.0:8501")
    server.serve_forever()
