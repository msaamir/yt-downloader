from flask import Flask, render_template, request, jsonify
import yt_dlp

# Flask ko start karne ke liye sahi syntax
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL link zaroori hai"}), 400
        
    try:
        # YouTube se data nikaalne ki settings
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Download links taiyaar karna
            formats = []
            for f in info.get('formats', []):
                # Sirf wo links lena jisme video aur audio dono ho
                if f.get('vcodec') != 'none' and f.get('url'):
                    formats.append({
                        "quality": f.get('format_note', 'HD'),
                        "url": f.get('url'),
                        "ext": f.get('ext', 'mp4')
                    })

            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "formats": formats[:10] # Top 10 links dikhana
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Server ko sahi port par chalane ke liye
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
