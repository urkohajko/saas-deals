import os
import time
import threading
from flask import Flask
from twitter_bot_selenium import TwitterBot

app = Flask(__name__)

@app.route("/")
def home():
    return "SaaS Deals Bot Running"

def run_bot():
    user = os.getenv("TW_USER")
    password = os.getenv("TW_PASS")

    bot = TwitterBot(user, password)
    bot.login()

    while True:
        try:
            bot.post_tweet("Automated SaaS Deals tweet.")
        except Exception as e:
            print("Error posting tweet:", e)
            try:
                bot.driver.quit()
            except:
                pass

            time.sleep(5)
            bot = TwitterBot(user, password)
            bot.login()

        time.sleep(3600)

if __name__ == "__main__":
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
