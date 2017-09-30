from pocket import Pocket
import random
import os
from http.server import *
import webbrowser

import history
import mail
import config

access_token_file = os.path.expanduser('~/pocket_reminder_access_token')
history_file = os.path.expanduser('~/pocket_reminder_history')


def get_user_permission_for_pocket():
    print("Preparing to get authenticated with pocket, may take a few seconds")
    server_address = ('0.0.0.0', config.localhost_port)
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    redirect_uri = 'http://localhost:' + str(config.localhost_port)
    request_token = Pocket.get_request_token(consumer_key=config.pocket_consumer_key, redirect_uri=redirect_uri)
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)

    print("Opening the browser to handle user input ", redirect_uri)
    webbrowser.open_new_tab(auth_url)

    print("Waiting for authentication")
    httpd.handle_request()

    user_credentials = Pocket.get_credentials(consumer_key=config.pocket_consumer_key, code=request_token)

    print("Pocket authenticated! credentials = ", user_credentials)
    return user_credentials['access_token']


def existing_token():
    global access_token_file

    if os.path.isfile(access_token_file) == False:
        return ''

    with open(access_token_file, 'r') as f:
        return f.read()


def save_token(token):
    global access_token_file
    with open(access_token_file, 'w+') as f:
        f.write(token)


def login_to_pocket():
    access_token = existing_token()
    if access_token == '':
        print("User access token does not exist, need to get user permission")
        access_token = get_user_permission_for_pocket()
        save_token(access_token)

    try:
        pocket_instance = Pocket(config.pocket_consumer_key, access_token)
        pocket_instance.get(count=1)
    except:
        print("User revoked his permissions from pocket, asking again")
        access_token = get_user_permission_for_pocket()
        save_token(access_token)

    return Pocket(config.pocket_consumer_key, access_token)


config = config.load_config()

pocket_instance = login_to_pocket()

art_list = pocket_instance.get(state='unread')[0]['list']

list_length = len(art_list)
print('Number of items in Pocket list is: ' + str(list_length))
rand_key = random.choice(list(art_list.keys()))
rand_article = art_list[rand_key]
title = rand_article['resolved_title']
if len(title)==0 or title.isspace():
    title = rand_article['given_title']
if len(title)==0 or title.isspace():
    title = rand_article['resolved_url']
word_count = rand_article['word_count']
id = rand_article['item_id']
url = "https://getpocket.com/a/read/" + id
delete_url = "https://getpocket.com/v3/send?actions=%5B%7B%22action%22%3A%22delete%22%2C%22item_id%22%3A" + id + "%7D%5D&access_token=" + existing_token() + "&consumer_key=" + config.pocket_consumer_key
print(title)
print(word_count)
print(url)
minutes = int(word_count) // 178
print("Read time (min): " + str(minutes))

history.write_amount(history_file, list_length)
imp_path = history.get_graph(history_file)

subject = "Here is what you need to read today"
txtmsg = "With only " + str(list_length) + \
         " items left in your pocket read list, here is what I offer you to read today\n" + title + \
         "\nwhich will take you " + str(minutes) + " minutes to read.\n" + url

htmlmsg = "With only <B>" + str(list_length) + \
          '</B> items left in your pocket read list, here is what I offer you to read today: <br/> <B> <a href="' + \
          url + '">' + title + '</a>' + \
          "</B><br/>which will take you " + str(minutes) + ' minutes to read. \n Not interesting?? <a href="' + delete_url + '">DELETE</a>'

response = mail.send_mailgun_msg(config, subject, txtmsg, htmlmsg, imp_path)
print(response)
