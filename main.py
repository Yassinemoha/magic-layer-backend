from http.server import BaseHTTPRequestHandler
import json
import cgi

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "online",
            "message": "Magic Layer Backend is ready for image processing!"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        # سنقوم هنا لاحقاً باستقبال الصورة وتقسيمها
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "success": True,
            "message": "Image received successfully. Layer splitting in progress..."
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
