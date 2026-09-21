import os, time, threading, requests
from flask import Flask
app=Flask(__name__)
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
SEEN=set()
KEYWORDS=["trump","elon","musk","bezos","zuckerberg","biden","maga","taylor"]
def send(m):
 try: requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={m}",timeout=10)
 except: pass
def hunter():
 send("✅ RICH BOT LIVE 24/7\nHunting Trump/Elon/Bezos coins!")
 while True:
  try:
   for k in KEYWORDS:
    d=requests.get(f"https://api.dexscreener.com/latest/dex/search/?q={k}",timeout=15).json()
    for p in d.get('pairs',[])[:3]:
     pid=p.get('pairAddress')
     if pid in SEEN: continue
     fdv=p.get('fdv',0) or 0
     liq=p.get('liquidity',{}).get('usd',0) or 0
     if fdv<2000000 and liq>300:
      link=f"https://dexscreener.com/{p['chainId']}/{p['pairAddress']}"
      send(f"🚨 NEW RICH COIN!\n{p['baseToken']['name']} ({p['baseToken']['symbol']})\nFDV ${fdv:,.0f}\n{link}\nKeyword:{k}")
      SEEN.add(pid)
    time.sleep(2)
  except: pass
  time.sleep(15)
threading.Thread(target=hunter,daemon=True).start()
@app.route('/')
def home(): return "RICH BOT LIVE"
