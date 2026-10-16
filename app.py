from flask import Flask, request, jsonify, Response, send_from_directory
import yt_dlp, requests

app = Flask(__name__)

def get_info(url):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        return ydl.extract_info(url, download=False)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/get", methods=["POST"])
def get():
    url = (request.json or {}).get("url", "")
    if "instagram.com" not in url:
        return jsonify(error="Valid Instagram link daalo"), 400
    try:
        info = get_info(url)
        return jsonify(video=info["url"], title=info.get("title", "reel"),
                       thumb=info.get("thumbnail"))
    except Exception:
        return jsonify(error="Video nahi mila (private ya blocked)"), 400

@app.route("/api/dl")
def dl():
    url = request.args.get("url", "")
    if "instagram.com" not in url:
        return "bad url", 400
    info = get_info(url)
    r = requests.get(info["url"], stream=True, timeout=30)
    return Response(r.iter_content(65536), content_type="video/mp4",
        headers={"Content-Disposition": 'attachment; filename="reel.mp4"'})
