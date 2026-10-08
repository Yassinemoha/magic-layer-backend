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
            
            data = json.loads(post_data.decode('utf-8'))
            img_data = base64.b64decode(data["image"].split(",")[1])
            image = Image.open(io.BytesIO(img_data))
            width, height = image.size
            
            # محاكاة تقسيم الصورة إلى طبقتين (مثال: النصف العلوي والسفلي، أو قص الطبقات)
            # سنقوم هنا بتقسيم الصورة إلى جزأين كنموذج أولي للطبقات
            half_height = height // 2
            
            layer1 = image.crop((0, 0, width, half_height))
            layer2 = image.crop((0, half_height, width, height))
            
            # تحويل الطبقات إلى Base64 لإرسالها للواجهة الأمامية
            def image_to_base64(img):
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')

            layer1_base64 = image_to_base64(layer1)
            layer2_base64 = image_to_base64(layer2)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                "width": width,
                "height": height,
                "layers": [
                    {"name": "الطبقة العليا (Layer 1)", "data": layer1_base64},
                    {"name": "الطبقة السفلى (Layer 2)", "data": layer2_base64}
                ],
                "message": "تم تقسيم الصورة إلى طبقات بنجاح!"
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = {"error": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
