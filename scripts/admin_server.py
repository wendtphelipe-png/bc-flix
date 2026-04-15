import http.server
import socketserver
import json
import os

PORT = 8000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'database.json')

class AdminHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        # Serve the config CMS page directly on the root
        if self.path == '/' or self.path == '/config':
            self.path = '/templates/config-checkin.html'
            return super().do_GET()
            
        # REST API endpoint to fetch database.json
        elif self.path == '/api/db':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode('utf-8'))
            return
            
        return super().do_GET()

    def do_POST(self):
        # REST API endpoint to save database.json
        if self.path == '/api/db':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Validates payload format
                parsed_data = json.loads(post_data.decode('utf-8'))
                
                # Writes changes securely over the exact file system reference
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(parsed_data, f, indent=2, ensure_ascii=False)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
            return
            
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    # Allows address reuse so restarts are fast
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AdminHandler) as httpd:
        print("*" * 50)
        print(f"✅ SERVIDOR ADMINISTRATIVO BC INICIADO")
        print(f"👉 Acesse o CMS em: http://localhost:{PORT}")
        print("💡 Para parar o servidor, pressione: 'Ctrl + C' no terminal.")
        print("*" * 50)
        httpd.serve_forever()
