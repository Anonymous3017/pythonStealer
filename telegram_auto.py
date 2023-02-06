import requests

def send_message_to_telegram_bot(token, chat_id, message):
    Turl =f"https://api.telegram.org/bot{token}/sendMessage"
    payload =  {"chat_id": chat_id, "text": message}
    response = requests.post(Turl, json=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")

#usage example
cid = "your_chat_id"
tok = "your_token_id"
send_message_to_telegram_bot(tok, cid, "Hello Bigsec community")