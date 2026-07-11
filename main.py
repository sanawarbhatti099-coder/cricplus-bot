import requests
from bs4 import BeautifulSoup
import time
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# فائر بیس کی معلومات
FIREBASE_URL = "https://chatting-app-d69d6-default-rtdb.firebaseio.com"
DATABASE_SECRET = "XKIogJS4N6mCFTyHlqoyZNYxbA22hKRs8lDvqtCJ"

CRICBUZZ_URL = "https://m.cricbuzz.com/cricket-match/live-scores"
UPDATE_URL = f"{FIREBASE_URL}/cricket.json?auth={DATABASE_SECRET}"

def fetch_and_update():
    while True:
        try:
            response = requests.get(CRICBUZZ_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            score_element = soup.find(class_="cb-lv-scrs-col")
            
            if score_element:
                live_score = score_element.text.strip()
            else:
                live_score = "No Live Match"
                
            print("Updating Firebase with:", live_score)
            data = {"score1": live_score}
            requests.put(UPDATE_URL, json=data)
            
        except Exception as e:
            print("Error occurred:", e)
        time.sleep(15)

# رینڈر کی فری سروس کے لیے ایک فرضی ویب سرور
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Running Perfectly!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), MyServer)
    server.serve_forever()

if __name__ == "__main__":
    # اسکور اپڈیٹ کرنے والے لوپ کو بیک گراؤنڈ میں چلانا
    threading.Thread(target=fetch_and_update, daemon=True).start()
    # ویب سرور آن کرنا تاکہ رینڈر خوش رہے
    run_web_server()
      
