#! /usr/bin/python3
#
# Draws matches for the gifting game 'secret santa'
# and notifies all participants by mail
#
# Expects as input a json file in the current working
# directory of the following form:
# {
#      "sender"  : "...",
#      "subject" : "...",
#      "message" : ["...", "...", ...]
#      "santas"  : {
#          "Aaron" : "aaron_mail",
#          "Bryce" : "bryce_mail"
#      }
# }
#
# To send the mails a prompt asks for username
# and password as login for the smtp server. The
# server name is constructed from the email domain.
# 
# Disclaimer: This script was written to suit my
#   needs, to be useful some alterations might
#   be necessary.

import sys
import json
import random as elf
import getpass as gp
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr

with open('santas.json', 'r') as f:
    config = json.load(f)
    message = "\n".join(config["message"])
    santas  = config["santas"]

imps = list(santas.keys())

elf.seed()
for _ in range(100):
    elf.shuffle(imps)

# draw a match for each santa
secret_santa = dict()
for santa, mail in santas.items():
    imp = elf.choice(imps)
    while imp == santa:
        imp = elf.choice(imps)

    secret_santa[santa] = imp
    imps.remove(imp)
    elf.shuffle(imps)

# prompt for username and check for correct format
user = input('Username: ')
if '@' in parseaddr(user)[1]:
    server = user.split('@')[1]
else:
    sys.exit('Not a valid email address, try again!')

# prompt for the password
pwd  = gp.getpass()

# send a mail to each participant
for santa, imp in secret_santa.items():
    msg = MIMEText(message.format(santa, imp))
    msg['Subject'] = config["subject"]
    msg['From']    = config["sender"]
    msg['To']      = santas[santa]

    s = smtplib.SMTP(server, 587)
    s.starttls()
    s.login(user, pwd)
    s.send_message(msg)
    s.quit()
