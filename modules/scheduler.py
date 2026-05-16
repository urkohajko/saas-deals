# scheduler.py
#
# Scheduler profesional para SaaS Deals
# - Controla horarios
# - Llama a generators
# - Llama al publisher
# - Mantiene rotación inteligente
# - Pensado para integrarse con main.py

from datetime import datetime, timedelta
from generator_tweets import generar_tweet
from generator_threads import generar_hilo
from publisher import publicar_tweet, publicar_hilo


# =========================
# CONFIG
# =========================

TWEET_INTERVAL = 3 * 3600      # 3 horas
THREAD_INTERVAL = 6 * 3600     # 6 horas
CTA_INTERVAL = 24 * 3600       # 24 horas


# =========================
# SCHEDULER
# =========================

class Scheduler:
    def __init__(self):
        self.last_tweet = datetime.now() - timedelta(seconds=TWEET_INTERVAL)
        self.last_thread = datetime.now() - timedelta(seconds=THREAD_INTERVAL)
        self.last_cta = datetime.now() - timedelta(seconds=CTA_INTERVAL)
        self.cycle = 0

    def should_post_tweet(self):
        return (datetime.now() - self.last_tweet).total_seconds() >= TWEET_INTERVAL

    def should_post_thread(self):
        return (datetime.now() - self.last_thread).total_seconds() >= THREAD_INTERVAL

    def should_post_cta(self):
        return (datetime.now() - self.last_cta).total_seconds() >= CTA_INTERVAL

    def post_tweet(self, driver):
        texto = generar_tweet(self.cycle)
        publicar_tweet(driver, texto)
        self.last_tweet = datetime.now()
        self.cycle += 1

    def post_thread(self, driver):
        partes = generar_hilo()
        publicar_hilo(driver, partes)
        self.last_thread = datetime.now()

    def post_cta(self, driver):
        cta = "Daily SaaS tools & exclusive deals. Follow @SaaSDealsHQ."
        publicar_tweet(driver, cta)
        self.last_cta = datetime.now()
