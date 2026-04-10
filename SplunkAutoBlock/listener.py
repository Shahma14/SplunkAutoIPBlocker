
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import logging

# Log file setup
logging.basicConfig(
    filename=r"C:\SplunkAutoBlock\listener.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class SplunkHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            raw = self.rfile.read(length)
            data = json.loads(raw)

            logging.info(f"Received payload: {data}")

            # Extract IP from Splunk webhook payload
            result = data.get('result', {})
            ip = (result.get('src_ip') or result.get('Source_Network_Address') or '').strip()

            if not ip:
                logging.warning("No src_ip found in payload")
                self.send_response(400)
                self.end_headers()
                return

            logging.info(f"Blocking IP: {ip}")

            # Run PowerShell block script
            subprocess.run([
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-File", r"C:\SplunkAutoBlock\block_ip.ps1",
                "-ip", ip
            ])

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        except Exception as e:
            logging.error(f"Error: {e}")
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress default console logs

print("Listener started on port 8888...")
HTTPServer(('0.0.0.0', 8888), SplunkHandler).serve_forever()