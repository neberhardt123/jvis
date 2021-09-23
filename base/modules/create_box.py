from base.models import Box, BoxService
from bs4 import BeautifulSoup
from base.modules.notifications import Notification


def handle_uploaded_box(f):
    #add validation
    #update already existing boxes
    #n = Notification()
    try:
        soup = BeautifulSoup(f, "xml")
    except Exception as e:
        print(e)
        return
    try:
        hosts= soup.find_all('host')
    except Exception as e:
        print(e)
        return
    if hosts:
        for host in hosts:
            try:
                address = host.address.get('addr')
            except:
                address = None
            #try:
            #    host_name = host.hostname.get('name')
            #except:
            #    host_name = None
            #try:
            #    os_fam = host.osclass.get('osfamily')
            #except:
            #    os_fam = None
            try:
                host_state = host.status.get('state')
            except:
                host_state = None

            retrieved_box, created = Box.objects.update_or_create(ip=address, 
            defaults={'state':host_state})
            if(created):
                #n.append_notification(retrieved_box, None, None, True, None)
                retrieved_box.new = True
                retrieved_box.save()
            #else:
                #if retrieved_box.updated is True:
                    #n.append_notification(retrieved_box, None, True, None, None)


            try:
                ports = host.find_all('port')
            except:
                ports = None
  
            if ports:
                #n.append_block()
                for p in ports:
                    try:
                        service_port = p.get('portid')
                    except:
                        service_port = None
                    try:
                        service_protocol = p.get('protocol')
                    except:
                        service_protocol = None
                    try:
                        service_state = p.state.get('state')
                    except:
                        service_state = None
                    try:
                        service_name = p.service.get('name')
                    except:
                        service_name = None
                    try:
                        service_version =  p.service.get('version')
                    except:
                        service_version = None
                    try:
                        service_product = p.service.get('product')
                    except:
                        service_product = None
                    try:
                        script_output = p.script.get('output')
                    except:
                        script_output = None

                    if(service_version is not None and service_product is not None):
                        service_pv_combined = service_version + service_product
                    else:
                        service_pv_combined = None
                    new_service, service_created = BoxService.objects.update_or_create(cBox=retrieved_box, port=service_port, protocol=service_protocol, defaults={'state':service_state, 'name':service_name, 'version':service_pv_combined, 'script':script_output})
                    if(service_created):
                        #n.append_notification(retrieved_box, new_service, None, True, None)
                        new_service.new = True
                        new_service.save()

        #n.append_block()
        #n.send_notification()
        Box.objects.all().update(new=False, updated=False)
        BoxService.objects.all().update(new=False, updated=None)
    return
