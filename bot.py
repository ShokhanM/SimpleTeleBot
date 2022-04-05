import requests
import misc
from yobit import get_btc
from time import sleep
# import json


token = misc.token

# https://api.telegram.org/bot1733945567:AAEi6UHC9rNeeUDTRe0tSf4RGLSvvhBUgo4/sendmessage?chat_id=741096445&text=hi

URL = 'https://api.telegram.org/bot' + token + '/'

global last_update_id
last_update_id = 0



def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():

    # answer only for new messages
    # get update_id, every update
    # write for new var, then compare with update_id last element
    # in list result

    data = get_updates()

    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id

    if last_update_id != current_update_id:
        last_update_id = current_update_id

        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {'chat_id': chat_id,
                   'text': message_text}
        return message
    return None


def send_message(chat_id, text='Wait second, please...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def main():
    # d = get_updates()

    while True:
        answer = get_message()

        if answer != None:
            chat_id = answer['chat_id']
            text = answer['text']

            if text == '/btc':
                send_message(chat_id, get_btc())
        else:
            continue

        sleep(2)


if __name__ == '__main__':
    main()
