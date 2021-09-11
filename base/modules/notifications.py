
class Notification:
    def __init__(self):
        self.message = ""
    def append_notification(self, host, port=None, updated = None, created = None, extra=None):
        if(updated):
            if host and port and extra:
                self.message += "Fields on port {} on host {} were updated:\n {}\n".format(port, host, extra)
            elif host and port:
                self.message += "Port {} on host {} was updated.\n".format(port, host)
            elif host:
                self.message += "{} was updated.\n".format(host)
            else:
                print("Nothing was updated")
        elif(created):
            if host and port:
                self.message += "Port {} on host {} was added.\n".format(port, host)
            elif host:
                self.message += "{} was added.\n".format(host)
            else:
                print("Nothing was created")

    def send_notification(self):
        print(self.message)
