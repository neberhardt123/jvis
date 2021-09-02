from base.models import Box, BoxService
from bs4 import BeautifulSoup

def handle_uploaded_box(f):
    
    #add validation

    soup = BeautifulSoup(f, "xml")
    hosts= soup.find_all('host')
    for host in hosts:
        try:
            address = soup.find('address')['addr']
            host_name = soup.find('hostname')['name']
            host_state = host.status.get('state')
            b = Box(ip=address, hostname=host_name, state=host_state)
            b.save()
            ports = soup.find_all('port')
            services = soup.find_all('service')
        except Exception as e:
            print(e)

        for p, s in zip(ports, services):
            try:
                service_port = p.get('portid')
                service_protocol = p.get('protocol')
                service_state = p.state.get('state')
                service_name = s.get('name')
                service_version = s.get('version')
                host_os = s.get('ostype')
                bs = BoxService(port=service_port, protocol=service_protocol, state=service_state, name=service_name, version=service_version, os=host_os, cBox=b)
                bs.save()
            except Exception as e:
                print(e)
    return

    #b = Box(ip="192.168.5.140", comments="test box!")
    #b.save()