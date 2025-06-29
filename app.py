from flask import Flask, Response
import requests
import re

app = Flask(__name__)

@app.route("/playlist.m3u")
def playlist():
    url = "https://www.myvideo.ge/tv/kolkheti89"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Find iframe src
    iframe_match = re.search(r'<iframe[^>]+src="([^"]+)"', html)
    if not iframe_match:
        return "Stream iframe not found", 404

    iframe_url = iframe_match.group(1)
    if not iframe_url.startswith("http"):
        iframe_url = "https:" + iframe_url

    iframe_response = requests.get(iframe_url, headers=headers)
    iframe_html = iframe_response.text

    # Find .m3u8 token URL
    stream_match = re.search(r'https://[^"]+\.m3u8\?token=[^"]+', iframe_html)
    if not stream_match:
        return "Stream URL not found", 404

    stream_url = stream_match.group(0)
    m3u = f"""#EXTM3U
#EXTINF:-1,კოლხეთი 89
{stream_url}
"""
    return Response(m3u, mimetype="application/x-mpegURL")
