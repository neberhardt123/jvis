from base.models import Box, BoxService
from bs4 import BeautifulSoup

def handle_uploaded_box(f):
    
    #add validation
    #update already existing boxes
    try:
        soup = BeautifulSoup(f, "xml")
    except:
        return
    try:
        hosts= soup.find_all('host')
    except:
        return
    if hosts:
        for host in hosts:
            try:
                address = soup.find('address')['addr']
            except:
                address = "N/A"
            try:
                host_name = soup.find('hostname')['name']
            except:
                host_name = "N/A"
            try:
                os_fam = soup.find('osclass')['osfamily']
            except:
                os_fam = "N/A"
            try:
                host_state = host.status.get('state')
            except:
                host_state = "N/A"
            b = Box(ip=address, hostname=host_name, state=host_state, os=os_fam)
            b.save()
            ports = soup.find_all('port')
            services = soup.find_all('service')

            if ports:
                for p, s in zip(ports, services):
                    try:
                        service_port = p.get('portid')
                    except:
                        service_port = "N/A"
                    try:
                        service_protocol = p.get('protocol')
                    except:
                        service_protocol = "N/A"
                    try:
                        service_state = p.state.get('state')
                    except:
                        service_state = "N/A"
                    try:
                        service_name = s.get('name')
                    except:
                        service_name = "N/A"
                    try:
                        service_version =  s.get('version')
                    except:
                        service_version = "N/A"
                    try:
                        service_product = s.get('product')
                    except:
                        service_product = "N/A"
                    if(service_version is not None and service_product is not None):
                        service_pv_combined = service_version + service_product
                    else:
                        service_pv_combined = "N/A"
                    bs = BoxService(port=service_port, protocol=service_protocol, state=service_state, name=service_name, version=service_pv_combined, cBox=b)
                    bs.save()
    return

    #b = Box(ip="192.168.5.140", comments="test box!")
    #b.save()