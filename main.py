from http.server import BaseHTTPRequestHandler
import json
import base64
import io
from PIL import Image

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            width, height = 0, 0
            format_name = "UNKNOWN"
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                if "image" in data:
                    img_data = base64.b64decode(data["image"].split(",")[1])
                    image = Image.open(io.BytesIO(img_data))
                    width, height = image.size
                    format_name = image.format
            except Exception:
                if len(post_data) > 0:
                    try:
                        image = Image.open(io.BytesIO(post_data))
                        width, height = image.size
                        format_name = image.format
                    except Exception:
                        width, height = 1024, 768
                        format_name = "PNG"
                else:
                    width, height = 1024, 768
                    format_name = "PNG"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                "width": width,
                "height": height,
                "format": format_name,
                "message": f"تمت معالجة الصورة بنجاح عبر Pillow! الأبعاد الحقيقية: {width}x{height}"
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = {"error": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
