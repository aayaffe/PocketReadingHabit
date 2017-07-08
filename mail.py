import requests

def send_mailgun_msg(config, subject, msg):
    return requests.post(
        "https://api.mailgun.net/v3/"+config.mailgun_domainname+"/messages",
        auth=("api", config.mailgun_apikey),
        data={"from": config.fromaddr,
              "to": config.toaddrs,
              "subject": subject,
              "text": msg})
