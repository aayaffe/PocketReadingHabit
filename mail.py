import requests


def send_mailgun_msg(config, subject, text_msg, html_msg, image_path):
    return requests.post(
        "https://api.mailgun.net/v3/" + config.mailgun_domainname + "/messages",
        auth=("api", config.mailgun_apikey),
        files=[("inline", open(image_path,"rb"))],
        data={"from": config.fromaddr,
              "to": config.toaddrs,
              "subject": subject,
              "text": text_msg,
              "html": '<html>' + html_msg + '<br/><img src="cid:' + image_path + '"></html>'
              })
