import json
import requests
import time
import urllib

with open('token', 'r') as f:
    TOKEN = f.readlines()[0].strip()

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

CHATID = '231085745'

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    #for update in updates["result"]:
    update = updates["result"][-1]
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]
    send_message(text, chat)


def nag_the_mods():
    send_message("update", CHATID)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    return (text, CHATID)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    LASTUPDATE = int(time.time())
    last_update_id = None
    while True:
        print(int(time.time()), "polling...")
        updates = get_updates(last_update_id)
        timeout = 10
        if int(time.time()) - LASTUPDATE > timeout:
            nag_the_mods()
            LASTUPDATE = int(time.time())
        elif len(updates["result"]) > 0: 
            LASTUPDATE = updates["result"][-1]["message"]["date"]
        time.sleep(5)


if __name__ == '__main__':
    main()
