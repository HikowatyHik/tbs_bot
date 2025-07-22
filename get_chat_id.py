import requests

TOKEN = "7638664258:AAFLufYyPenu3NuSRKpPvzPX_1KHzCiUxV0"  # Twój poprawiony token

def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    data = response.json()
    
    if not data['ok']:
        print("Błąd w API:", data)
        return
    
    results = data.get('result')
    if not results:
        print("Brak nowych wiadomości. Wyślij coś do bota w Telegramie i spróbuj ponownie.")
        return
    
    chat_id = results[0]['message']['chat']['id']
    print("Twój chat_id to:", chat_id)

if __name__ == "__main__":
    get_chat_id()
