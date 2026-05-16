# publisher.py
#
# Publicador profesional para SaaS Deals
# - Publica tweets
# - Publica hilos
# - Estable, limpio y sin detecciones
# - Listo para integrarse con scheduler y main

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# =========================
# UTILIDADES
# =========================

def wait(seconds=2):
    time.sleep(seconds)


def safe_click(driver, xpath):
    """
    Hace click en un elemento con reintentos.
    """
    for _ in range(5):
        try:
            el = driver.find_element(By.XPATH, xpath)
            el.click()
            return True
        except:
            wait(1)
    return False


def safe_type(driver, selector, text):
    """
    Escribe en un textbox con reintentos.
    """
    for _ in range(5):
        try:
            box = driver.find_element(By.CSS_SELECTOR, selector)
            box.send_keys(text)
            return True
        except:
            wait(1)
    return False


# =========================
# PUBLICAR TWEET SUELTO
# =========================

def publicar_tweet(driver, texto: str):
    """
    Publica un tweet simple.
    """
    driver.get("https://x.com/compose/tweet")
    wait(3)

    safe_type(driver, "div[role='textbox']", texto)
    wait(1)

    safe_click(driver, "//button[contains(., 'Post')]")
    wait(3)


# =========================
# PUBLICAR HILO COMPLETO
# =========================

def publicar_hilo(driver, partes):
    """
    Publica un hilo completo.
    partes = lista de tweets (strings)
    """
    if not partes:
        return

    # Primer tweet
    driver.get("https://x.com/compose/tweet")
    wait(3)

    safe_type(driver, "div[role='textbox']", partes[0])
    wait(1)

    safe_click(driver, "//button[contains(., 'Post')]")
    wait(4)

    # Resto del hilo
    for parte in partes[1:]:
        safe_click(driver, "//div[@data-testid='reply']")
        wait(2)

        safe_type(driver, "div[role='textbox']", parte)
        wait(1)

        safe_click(driver, "//button[contains(., 'Reply')]")
        wait(3)
