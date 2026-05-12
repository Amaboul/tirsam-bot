from playwright.sync_api import sync_playwright
import requests
import re
import time
args=["--no-sandbox", "--disable-dev-shm-usage"]

# =========================
# TELEGRAM
# =========================

BOT_TOKEN = "8402009370:AAF5GoYOUz364qy-BIIZzx3IxB2GJeNr6Ts"
CHAT_ID = "7618363544"

# =========================
# PRIX CIBLE
# =========================

TARGET_MIN = 1400000
TARGET_MAX = 1900000

# =========================
# TELEGRAM FUNCTION
# =========================

def send_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

# =========================
# EXTRACTION PRIX
# =========================

def extract_price(text):

    match = re.search(r'(\d[\d\s]+)\s*DZD', text)

    if match:

        price = match.group(1)

        price = price.replace(" ", "")

        return int(price)

    return None

# =========================
# MAIN
# =========================

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    while True:

        print("\n🔄 Vérification du site...")

        page.goto("https://tirsam.com/camionnette/")

        page.wait_for_timeout(3000)

        content = page.content()

        # Vérifier présence camionnette
        if "Camionnette simple cabine" in content:

            print("🚐 Camionnette détectée")

            # Chercher tous les prix
            prices = re.findall(r'(\d[\d\s]+)\s*DZD', content)

            found_target = False

            for p_text in prices:

                price = int(p_text.replace(" ", ""))

                print("💰 Prix trouvé :", price)

                # Vérifier plage cible
                if TARGET_MIN <= price <= TARGET_MAX:

                    found_target = True

                    alert_message = (
                        f"🚨 PRIX CIBLE DÉTECTÉ !\n\n"
                        f"🚐 Camionnette simple cabine\n"
                        f"💰 Prix : {price:,} DZD"
                    )

                    print(alert_message)

                    send_alert(alert_message)

                    break

            if not found_target:

                print("⏳ Aucun prix cible pour le moment")

        else:

            print("❌ Camionnette non trouvée")

        # attendre avant prochain scan
        print("⏱ Nouvelle vérification dans 30 secondes...\n")

        time.sleep(30)