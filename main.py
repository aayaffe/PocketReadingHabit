from pocket import Pocket
import random
from time import sleep
from selenium import webdriver
import mail
import config


def auth_pocket():
    redirect_uri = "http://www.google.co.il"
    request_token = Pocket.get_request_token(consumer_key=config.pocket_consumer_key, redirect_uri=redirect_uri)
    # URL to redirect user to, to authorize your app
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
    driver = webdriver.Chrome()
    driver.get(auth_url)
    text_area = driver.find_element_by_id('feed_id')
    text_area.send_keys(config.pocket_username)
    text_area = driver.find_element_by_id('login_password')
    text_area.send_keys(config.pocket_password)
    python_link = driver.find_elements_by_xpath("//input[@type='submit' and @value='Authorize']")[0]
    python_link.click()
    sleep(5)
    if "google" in driver.current_url:
        driver.close()
    return request_token


request_token = auth_pocket()

user_credentials = Pocket.get_credentials(consumer_key=config.pocket_consumer_key, code=request_token)
access_token = user_credentials['access_token']

pocket_instance = Pocket(config.pocket_consumer_key, access_token)

art_list = pocket_instance.get(state='unread')[0]['list']

list_length = len(art_list)
print('Number of items in Pocket list is: ' + str(list_length))
rand_key = random.choice(list(art_list.keys()))
rand_article = art_list[rand_key]
title = rand_article['resolved_title']
word_count = rand_article['word_count']
id = rand_article['item_id']
url = "https://getpocket.com/a/read/" + id
print (title)
print(word_count)
print(url)
minutes = int(word_count)//178
print("Read time (min): " + str(minutes))


subject = "Here is what you need to read today"
msg = "With only " + str(list_length) + \
      " items left in your pocket read list, here is what I offer you to read today\n" + title +\
      "\nwhich will take you " + str(minutes) + " minutes to read.\n" + url

mail.send_mailgun_msg(config.fromaddr, config.toaddrs, subject, msg)
# mail.send_smtp_msg(config.fromaddr, config.toaddrs, subject, msg)
