from base.models import Box


def run():
    b = Box(ip="192.168.5.140", comments="test box!")
    b.save()