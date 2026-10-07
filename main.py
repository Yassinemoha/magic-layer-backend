from http.server import BaseHTTPRequestHandler
import json
import cgi
from PIL import Image
from psd_tools import PSDImage
import io

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "online",
            "message": "Magic Layer Backend is running with Pillow and psd-tools!"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        # سنقوم هنا لاحقاً بإضافة منطق استقبال الصورة وتقسيمها
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "success",
            "message": "Image received successfully (Processing logic coming next)"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
