from base.models import Box, BoxService
from bs4 import BeautifulSoup
from base.modules.notifications import Notification


def handle_uploaded_box(f):
    #add validation
    #update already existing boxes
    n = Notification()
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
            try:
                host_name = host.hostname.get('name')
            except:
                host_name = None
            try:
                os_fam = host.osclass.get('osfamily')
            except:
                os_fam = None
            try:
                host_state = host.status.get('state')
            except:
                host_state = None
            #try:
            #    dupe = Box.objects.filter(ip=address)
            #except:
            #    dupe = None

            retrieved_box, created = Box.objects.update_or_create(ip=address, 
            defaults={'hostname':host_name, 'state':host_state, 'os':os_fam})
            if(created):
                #print("{} was created".format(retrieved_box))
                n.append_notification(retrieved_box, None, None, True, None)
                retrieved_box.new = True
                retrieved_box.save()
            else:
                if retrieved_box.updated is True:
                    n.append_notification(retrieved_box, None, True, None, None)
            #print(retrieved_box)
            #print(created)

            #CHANGE THIS
            #if dupe:
            #    for d in dupe:
            #        for b in d.boxservice_set.all():
            #            
            #        d.boxservice_set.all().delete()
            #        d.save()
            #    dupe.update(ip=address, hostname=host_name, state=host_state, os=os_fam, new=True)
            #else:
            #    b = Box(ip=address, hostname=host_name, state=host_state, os=os_fam, new=True)
            #    b.save()

            try:
                ports = host.find_all('port')
            except:
                ports = None
  
            if ports:
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
                            #get all bs for box?
                            #if d.boxservice_set.all().port == service_port:
                            #    print("DUPED SERVICE" + service_port)
                            #    continue
                            #else:
                            #    bs = BoxService (port=service_port, protocol=service_protocol, state=service_state, name=service_name, version=service_pv_combined, script=script_output, new=True, cBox=d)
                            #    bs.save()
                    new_service, service_created = BoxService.objects.update_or_create(port=service_port, protocol=service_protocol, defaults={'state':service_state, 'name':service_name, 'version':service_pv_combined, 'script':script_output, 'cBox':retrieved_box})
                    if(service_created):
                        #print("{} was created".format(new_service))
                        n.append_notification(retrieved_box, new_service, None, True, None)
                        new_service.new = True
                        new_service.save()
                    else:
                        if new_service.updated is not None:
                            n.append_notification(retrieved_box, new_service, True, None, new_service.updated)
                    #else:
                    #    bs = BoxService(port=service_port, protocol=service_protocol, state=service_state, name=service_name, version=service_pv_combined, script=script_output, new=True, cBox=retrieved_box)
                    #    bs.save()
    n.send_notification()
    return

    #b = Box(ip="192.168.5.140", comments="test box!")
    #b.save()