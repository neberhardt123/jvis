import csv
from django.http import FileResponse
from base.models import Box, BoxService

def create_diagram():
    #boxes = Box.objects.all()
    boxes = ['te','te','te']
    header = ['id', 'component', 'refs','fill', 'stroke', 'shape', 'type', 'image', 'width', 'height', 'font', 'fontSize', 'parent','identity']
    data = []
    #['1', 'Hello World', '#dae8fc', '#6c8ebf', 'rectangle'],
    #['2','Am I alive?','#fff2cc','#d6b656','rhombus','1']

    index = 0
    for box in boxes:
        #linux = img/lib/mscae/VM_Linux.svg
        box_temp = ["box{}".format(index), "", "info{}".format(index),"","","","image","img/lib/mscae/VirtualMachineWindows.svg", "90", "80","","","","box{}".format(index)]
        info_temp = ["info{}".format(index), "Windows Host","","#60a917","","","swimlane","","220","80","#FFFFFF","14","","info{}".format(index)]
        text_temp = ["text{}".format(index),"testetset","","","","","text","","auto","auto","","","info{}".format(index),"text{}".format(index)]
        index += 1
        data.append(box_temp)
        data.append(info_temp)
    config = [  'label: %component%', 
                'style: shape=%shape%;fillColor=%fill%;strokeColor=%stroke%;fontSize=%fontSize%;fontColor=%font%;aspect=fixed;align=center;%type%;image=%image%', 
                'namespace: csvimport-',
                'connect: {"from":"refs", "to":"id", "style":"opacity=0"}',
                'width: @width',
                'parentstyle: swimlane;whiteSpace=wrap;html=1;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;',
                'parent: %parent%',
                'identity: %identity%',
                'height: @height',
                'padding: 15',
                'ignore: id, shape, fill, stroke, refs',
                'nodespacing: 40',
                'levelspacing: 100',
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

