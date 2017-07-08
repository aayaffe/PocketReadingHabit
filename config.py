import json
from os import path
from collections import namedtuple

configs_file = path.expanduser('~/pocket_reminder_config')

# Copied from https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
# Magic here: 
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class Config:
    def __init__(self):
        self.toaddrs = ''
        self.fromaddr = ''
        self.pocket_consumer_key = ''
        self.mailgun_domainname = ''
        self.mailgun_apikey = ''
        self.localhost_port = 4567

def __get_config():
    global configs_file
    
    if path.isfile(configs_file) == False:
        return None

    with open(configs_file, "r") as f:
        raw_config = f.read()
        return json2obj(raw_config)

def __write_config(conf):
    global configs_file

    with open(configs_file, "w+") as f:
        f.write(json.dumps(conf.__dict__))
        f.flush()

def __ask_user_for_config():
    global configs_file
    print ("Missing configuration at - ", configs_file)
    print ("Will now ask you for the minimal configurations needed to start")

    print ("You will need a pocket consumer key, you can get one at:")
    print ("'https://getpocket.com/developer/docs/authentication'")

    config = Config()
    config.pocket_consumer_key = input ("Enter your pocket consumer key: ")
    config.toaddrs = input ("Enter the recipient mail address: ")
    print ("This program works with 'http://wwww.mailgun.com'")
    config.mailgun_domainname = input("Enter your mailgun domain name: ")
    config.mailgun_apikey = input("Enter your mailgun apikey: ")
    
    mail_sender = input("Enter the name of the mail sender: ")
    config.fromaddr = mail_sender + " <" + "pocketreminder@" + config.mailgun_domainname + '>'

    print ("This program will bind to  '0.0.0.0:'", config.localhost_port, " you can change the port in the config file: ", configs_file)
    return config

def load_config():
    config = __get_config()

    if config == None:
        config = __ask_user_for_config()
        __write_config(config)

    print ("Running with the following config - ", config)
    return config