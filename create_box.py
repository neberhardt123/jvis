from base.models import Box, BoxService
from bs4 import BeautifulSoup

def handle_uploaded_box(f):
    
    #add validation
    b = None
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
                address = host.address.get('addr')
            except:
                address = "N/A"
            try:
                host_name = host.hostname.get('name')
            except:
                host_name = "N/A"
            try:
                os_fam = host.osclass.get('osfamily')
            except:
                os_fam = "N/A"
            try:
                host_state = host.status.get('state')
            except:
                host_state = "N/A"
            try:
                dupe = Box.objects.filter(ip=address)
            except:
                dupe = None

            if dupe:
                dupe.update(ip=address, hostname=host_name, state=host_state, os=os_fam, new=True)
                for d in dupe:
                    d.boxservice_set.all().delete()
                    d.save()
            else:
                b = Box(ip=address, hostname=host_name, state=host_state, os=os_fam, new=True)
                b.save()
            try:
                ports = host.find_all('port')
            except:
                ports = None
  
            if ports:
                for p in ports:
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
                        service_name = p.service.get('name')
                    except:
                        service_name = "N/A"
                    try:
                        service_version =  p.service.get('version')
                    except:
                        service_version = "N/A"
                    try:
                        service_product = p.service.get('product')
                    except:
                        service_product = "N/A"
                    try:
                        script_output = p.script.get('output')
                    except:
                        script_output = "N/A"

                    if(service_version is not None and service_product is not None):
                        service_pv_combined = service_version + service_product
                    else:
                        service_pv_combined = "N/A"
                    if dupe:
                        for d in dupe:
                            #get all bs for box?
                            bs = BoxService (port=service_port, protocol=service_protocol, state=service_state, name=service_name, version=service_pv_combined, script=script_output, new=True, cBox=d)
                            bs.save()
                    else:
                        bs = BoxService(port=service_port, protocol=service_protocol, state=service_state, name=service_name, version=service_pv_combined, script=script_output, new=True, cBox=b)
                        bs.save()
    return

    #b = Box(ip="192.168.5.140", comments="test box!")
    #b.save()