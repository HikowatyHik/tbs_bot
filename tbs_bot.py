import requests
from bs4 import BeautifulSoup
import os
import re

# === TWOJE DANE ===
BOTS = [
    {"token": "8049749392:AAEVf-c06Xnib9TtV2TaULRXuwUvmVN2OQY", "chat_id": "7138406243"},
    {"token": "7638664258:AAFLufYyPenu3NuSRKpPvzPX_1KHzCiUxV0", "chat_id": "6206540245"}
]

def send_telegram_message(text):
    for bot in BOTS:
        url = f"https://api.telegram.org/bot{bot['token']}/sendMessage"
        payload = {
            "chat_id": bot["chat_id"],
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Błąd wysyłania wiadomości do {bot['chat_id']}: {response.text}")
        else:
            print(f"Wysłano wiadomość do {bot['chat_id']}")

URL = "https://www.tbs-wroclaw.com.pl/mieszkania-na-wynajem"
OFFERS_FILE = "offers.txt"

def get_offers():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    offers = []
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)
        href = link['href']

        if re.search(r"\bul\.|\bul ", text, re.I) and href.endswith(".html"):
            if not href.startswith("http"):
                href = "https://www.tbs-wroclaw.com.pl/" + href.lstrip("/")
            offers.append(f"{text} | {href}")

    print(f"Znaleziono {len(offers)} ofert:")
    for o in offers:
        print(o)

    return offers

def load_saved_offers():
    if not os.path.exists(OFFERS_FILE):
        return []
    with open(OFFERS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_offers(offers):
    with open(OFFERS_FILE, "w", encoding="utf-8") as f:
        for offer in offers:
            f.write(offer + "\n")

def main():
    print("Pobieram oferty...")
    current_offers = get_offers()
    saved_offers = load_saved_offers()

    new_offers = [offer for offer in current_offers if offer not in saved_offers]

    if new_offers:
        print(f"Znaleziono {len(new_offers)} nowych ofert!")

        # Podziel na części max 20 ofert, aby nie było błędu 400
        chunk_size = 20
        for i in range(0, len(new_offers), chunk_size):
            chunk = new_offers[i:i+chunk_size]
            message = "Nowe oferty mieszkań TBS Wrocław:\n\n" + "\n".join(chunk)
            send_telegram_message(message)

        save_offers(current_offers)
    else:
        print("Brak nowych ofert.")
        send_telegram_message("Brak nowych ofert.")

if __name__ == "__main__":
    main()
