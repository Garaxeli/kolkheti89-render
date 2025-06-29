from flask import Flask, Response, request
import requests
import re

app = Flask(__name__)

@app.route("/playlist.m3u")
def playlist():
    url = "https://www.myvideo.ge/tv/kolkheti89"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    html = r.text

    match = re.search(r'https://.*?\.m3u8\?token=[^"]+', html)
    if not match:
        return "Stream URL not found", 404

    stream_url = match.group(0)
    playlist_content = f"""#EXTM3U
#EXTINF:-1,კოლხეთი 89
{stream_url}
"""
    return Response(playlist_content, mimetype="application/x-mpegURL")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)