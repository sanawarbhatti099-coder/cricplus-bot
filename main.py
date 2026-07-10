import requests
from bs4 import BeautifulSoup
import time

# 1. فائر بیس کی معلومات (لنک میں نے سیٹ کر دیا ہے)
FIREBASE_URL = "https://chatting-app-d69de-default-rtdb.firebaseio.com"
DATABASE_SECRET = "XKIogJS4N6mCFTyHlqoyZNYxbA22hKRs8lDvqtCJ"

# کرکنز کا لائیو میچوں والا لنک
CRICBUZZ_URL = "https://m.cricbuzz.com/cricket-match/live-scores"
# فائر بیس کو اپڈیٹ کرنے کا فائنل لنک
UPDATE_URL = f"{FIREBASE_URL}/cricket.json?auth={DATABASE_SECRET}"

def fetch_and_update():
    try:
        response = requests.get(CRICBUZZ_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # اسکور والا ڈبہ ڈھونڈنا
        score_element = soup.find(class_="cb-lv-scrs-col")
        
        if score_element:
            live_score = score_element.text.strip()
        else:
            live_score = "No Live Match"
            
        print("Updating Firebase with:", live_score)
        
        # ڈائریکٹ فائر بیس کو لائیو ڈیٹا بھیجنا
        data = {"score1": live_score}
        requests.put(UPDATE_URL, json=data)
        
    except Exception as e:
        print("Error occurred:", e)

# یہ لوپ بغیر رکے ہر 15 سیکنڈ بعد خود بخود چلتا رہے گا
while True:
    fetch_and_update()
    time.sleep(15)
  
