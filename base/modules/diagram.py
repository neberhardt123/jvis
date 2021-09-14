import csv
import json
import ipaddress
import numpy as np
from django.http import FileResponse
from base.models import Box, BoxService
from django.db.models import Q

def create_diagram():
    boxes = Box.objects.all()
    windows_boxes = Box.objects.filter(Q(os="Windows") | Q(os="windows"))
    linux_boxes = Box.objects.filter(Q(os="Linux") | Q(os="linux"))
    other_boxes = Box.objects.filter(~(Q(os="Windows") | Q(os="windows")) & ~(Q(os="Linux") | Q(os="linux")))
    #boxes = ['te','te','te']
    header = ['id', 'component', 'refs','fill', 'stroke', 'shape', 'type', 'image', 'width', 'height', 'font', 'fontSize', 'parent','identity']
    data = []
    #['1', 'Hello World', '#dae8fc', '#6c8ebf', 'rectangle'],
    #['2','Am I alive?','#fff2cc','#d6b656','rhombus','1']

    #index = 0



    for box in boxes:
        info_temp = None
        text_temp = None
        h = None
        if box.hostname:
            h = box.hostname
        else:
            h = box.ip
        info_temp = ["info{}".format(box.id), h,"box{}".format(box.id),"#60a917","","","swimlane","","220","80","#FFFFFF","14","","info{}".format(box.id)]
        msg = ""
        for bs in box.boxservice_set.all().filter(state="open"):
            msg += "Port " + str(bs.port) + " - " + (str(bs.name) or "") + "<br>"
        text_temp = ["text{}".format(box.id),msg,"","","","","text","","220","80","#000000","14","info{}".format(box.id),"text{}".format(box.id)]

    #
        data.append(info_temp)
        data.append(text_temp)

    for box in windows_boxes:
        #box_temp = None
        box_temp = ["box{}".format(box.id), "", "".format(box.id),"","","","image","img/lib/mscae/VirtualMachineWindows.svg", "90", "80","","","","box{}".format(box.id)]
        data.append(box_temp)
    
    for box in linux_boxes:
        box_temp = ["box{}".format(box.id), "", "".format(box.id),"","","","image","img/lib/mscae/VM_Linux.svg", "90", "80","","","","box{}".format(box.id)]
        data.append(box_temp)

    for box in other_boxes:
        box_temp = ["box{}".format(box.id), "", "".format(box.id),"","","","image","", "90", "80","","","","box{}".format(box.id)]
        data.append(box_temp)


    config = [  'label: %component%', 
                'style: shape=%shape%;fillColor=%fill%;strokeColor=%stroke%;fontSize=%fontSize%;fontColor=%font%;aspect=fixed;%type%;image=%image%;align=center;whiteSpace=wrap;html=1', 
                'namespace: csvimport-',
                'connect: {"from":"refs", "to":"id","style":"opacity=0","invert":true}',
                'width: @width',
                'parentstyle: swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#3f7de0;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;fontColor=#ffffff;aspect=fixed;fontSize=14;whiteSpace=wrap;html=1',
                'parent: parent',
                'identity: identity',
                'height: @height',
                'left:%left%'
                'padding: 15',
                'ignore: id, shape, fill, stroke, refs',
                'nodespacing: 40',
                'levelspacing: 20',
                'edgespacing: 40',
                'layout: horizontalflow']
    file_path = 'static/diagram.csv'
    with open(file_path, 'w', newline='') as f:
        for l in config:
            f.write("# {} \n".format(l))
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    f.close()
    response = FileResponse(open(file_path, 'rb'))
    return response

def create_topology():
    boxes = Box.objects.all()
    header = ['id', 'name', 'refs', 'cat', 'width', 'height', 'parent','identity']
    data = []
    attacker_parent = ["attacker_parent", "Attacker Network", "router", "","180","80","","attacker_parent"]
    attacker = ["attacker","VDI Infrastructure","","atkr","80","60","attacker_parent","attacker"]


    data.append(attacker_parent)
    data.append(attacker)
    nets = []
    for box in boxes:
        try:
            n = str(ipaddress.ip_network('{}{}'.format(box.ip,box.cidr), strict=False))
            nets.append(n)
        except:
            pass

    x = np.array(nets)
    unique = np.unique(x)

    for u in unique:
        subnet_parent = [u,"CHANGE ME{}{}".format("<br>",u),"","","180","500","",u]
        data.append(subnet_parent)

    
    for box,n in zip(boxes,nets):
        subnet_child = [box.ip,"{}{}{}".format(box.ip,"<br>",box.hostname),"","atkr","80","",n,box.ip]
        data.append(subnet_child)

    router_reference = "{}".format(','.join(unique))
    router = ["router","",router_reference,"rtr","122","80","","router"]
    data.append(router)
    #for u in unique:
        #net_parent = [u, "CHANGE ME{}{}".format("<br>",u),"",""]
    styles = {
        #"template": "shape=%shape%;fillColor=%fill%;strokeColor=%stroke%;fontSize=%fontSize%;fontColor=%font%;aspect=fixed;%type%;image=%image%;align=center;whiteSpace=wrap;html=1",
        "atkr": "fontColor=#232F3E;fillColor=#232F3E;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=image;image=https://cdn0.iconfinder.com/data/icons/cyber-security-solid-threat-protection/512/Hacker_anonymous-128.png;strokeColor=#232F3E;aspect=fixed;whiteSpace=wrap;",
        "rtr": "fontColor=#232F3E;fillColor=#232F3E;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=image;image=img/lib/clip_art/networking/Router_Icon_128x128.png;strokeColor=#232F3E;aspect=fixed;whiteSpace=wrap;"
    }
    config = [  'label: %name%',
                #'style: shape=%shape%;fillColor=%fill%;strokeColor=%stroke%;fontSize=%fontSize%;fontColor=%font%;aspect=fixed;%type%;image=%image%;align=center;whiteSpace=wrap;html=1',
                'parentstyle: swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=26;autoSize=1;fillColor=#3f7de0;horizontalStack=1;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;fontColor=#ffffff;fontSize=12;whiteSpace=wrap;html=1',
                'stylename: cat',
                'styles: {}'.format(json.dumps(styles)),
                'vars: -',
                'labelname: -',
                'labels: -',
                'identity: identity',
                'parent: parent',
                'namespace: csvimport-',
                #'connect: {"from": "manager", "to": "name", "invert": true, "label": "manages", "style": "curved=1;endArrow=blockThin;endFill=1;fontSize=11;"}'
                'connect:{"from": "refs", "to":"id", "style":"rounded=0;endArrow=classic;jumpStyle=sharp;strokeColor=#3f7de0"}',
                'left:',
                'top:',
                'width: @width',
                'height: auto',
                'padding: 15',
                'ignore: id, cat, fill, refs',
                'nodespacing: 40',
                'levelspacing: 100',
                'edgespacing: 40',
                'layout: verticalflow'
    ]
    file_path = 'static/topology.csv'
    with open(file_path, 'w', newline='') as f:
        for l in config:
            f.write("# {} \n".format(l))
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    f.close()

    response = FileResponse(open(file_path, 'rb'))
    return response