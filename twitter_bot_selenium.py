from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # ============================
        # CONFIGURACIÓN CHROME LINUX
        # ============================
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        # Anti‑detección
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # ============================
        # DRIVER LINUX (RENDER)
        # ============================
        self.driver = webdriver.Chrome(
            service=Service("/usr/bin/chromedriver"),
            options=options
        )

        # ============================
        # ANTI‑DETECCIÓN JAVASCRIPT
        # ============================
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            }
        )

    # ============================
    # LOGIN
    # ============================
    def login(self):
        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(5)

        user_input = self.driver.find_element(By.NAME, "text")
        user_input.send_keys(self.username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(3)

        pass_input = self.driver.find_element(By.NAME, "password")
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.ENTER)
        time.sleep(5)

    # ============================
    # PUBLICAR TWEET
    # ============================
    def post_tweet(self, text):
        self.driver.get("https://twitter.com/compose/tweet")
        time.sleep(5)

        box = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='Texto del Tweet']")
        box.send_keys(text)
        time.sleep(1)

        tweet_button = self.driver.find_element(By.XPATH, "//span[text()='Publicar']")
        tweet_button.click()

        time.sleep(5)
