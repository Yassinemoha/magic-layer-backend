from http.server import BaseHTTPRequestHandler
import json
import cgi
from PIL import Image
from psd_tools import PSDImage, PSDBuilder
from psd_tools.psd.image_data import Channels
import io

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "online",
            "message": "Magic Layer Backend is fully ready for image processing!"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        try:
            # تحليل البيانات القادمة من الطلب (Multipart Form Data)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )

            if "image" not in form:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No image uploaded"}).encode('utf-8'))
                return

            # استقبال ملف الصورة
            image_item = form["image"]
            image_data = image_item.file.read()
            
            # فتح الصورة باستخدام Pillow
            img = Image.open(io.BytesIO(image_data)).convert("RGBA")
            width, height = img.size

            # تجربة تقسيم بسيطة: تقسيم الصورة إلى طبقتين أو معالجتها كطبقة أساسية
            # (سنقوم بتطوير خوارزمية الذكاء الاصطناعي/القص لاحقاً، حالياً سننشئ ملف PSD بـ طبقتين افتراضيتين للتجربة)
            
            # حفظ النتائج أو إرسال استجابة نجاح مؤقتة للتأكد من عمل الباك اند
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "Image processed successfully!",
                "width": width,
                "height": height
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        return
