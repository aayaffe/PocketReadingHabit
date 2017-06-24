import requests
import smtplib
import config


def send_smtp_msg(fromaddr, toaddrs, subject, msg):
    print(msg)

    server = smtplib.SMTP(config.smtp_server)
    server.ehlo()
    server.starttls()
    server.login(config.smtp_username, config.smtp_password)
    payload = "\r\n".join([
        "From: " + fromaddr,
        "To: " + toaddrs,
        "Subject: " + subject,
        "",
        msg
    ])
    server.sendmail(fromaddr, toaddrs, payload)
    server.quit()


def send_mailgun_msg(fromaddr,toaddrs, subject, msg):
    return requests.post(
        "https://api.mailgun.net/v3/"+config.mailgun_domainname+"/messages",
        auth=("api", config.mailgun_apikey),
        data={"from": fromaddr,
              "to": toaddrs,
              "subject": subject,
              "text": msg})
