from base.models import Box
from bs4 import BeautifulSoup

def handle_uploaded_box(f):
    
    #add validation
    try:
        #with open(f, 'r') as file:
        #    data = file.read
                
        soup = BeautifulSoup(f, "xml")
        hosts= soup.find_all('host')
        for host in hosts:
            address = soup.find('address')['addr']
            host_name = soup.find('hostname')['name']
            b = Box(ip=address, hostname=host_name)
            b.save()
    except Exception as e:
        print(e)
        return

    #b = Box(ip="192.168.5.140", comments="test box!")
    #b.save()