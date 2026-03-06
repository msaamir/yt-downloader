from flask import Flask, render_template, request, jsonify
import yt_dlp

# Yahan 'name' ki jagah 'name' hoga
app = Flask(name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [{"quality": f.get('format_note'), "url": f.get('url'), "ext": f.get('ext')} 
                       for f in info.get('formats', []) if f.get('vcodec') != 'none']
            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "formats": formats[:10] 
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Yahan bhi 'name' ki jagah 'name' aur 'main' ki jagah 'main' hoga
if name == "main":
    app.run(host='0.0.0.0', port=8080)
