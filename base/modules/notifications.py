import os
import json
import requests
import datetime

class Notification:
    def __init__(self):
        self.message = ""
        self.webhookurl = "https://discordapp.com/api/webhooks/886055588755292191/sbTYIAqg0pyJ0GLXrhr50g3OhsDO8EMjBDX7K8IojXg7IvxZKorIKLk8CbjAEZeE-zFX"

    #TODOOOO
    def parse_ini():
        print("blaahahahahah")

    def append_notification(self, host, port=None, updated = None, created = None, extra=None):
        if(updated):
            if host and port and extra:
                self.message += "Fields on port {} on host {} were updated:\n {}\n".format(port, host, extra)
            elif host and port:
                self.message += "Port {} on host {} was updated.\n".format(port, host)
            elif host:
                self.message += "Box **{}** was updated ({}).\n".format(host, datetime.datetime.utcnow())
            else:
                print("Nothing was updated")
        elif(created):
            if host and port:
                self.message += "Port {} on host {} was added.\n".format(port, host)
            elif host:
                self.message += "Box **{}** was added ({}).\n".format(host, datetime.datetime.utcnow())
            else:
                print("Nothing was created")
    
    def append_line(self):
        self.message += "<===============================================================>\n"

    def append_block(self):
        self.message += "```"

    def send_notification(self):
        payload = {
            'username': 'CPTC Notification',
            'content': self.message
        }
        r = requests.post(self.webhookurl, json=payload)
