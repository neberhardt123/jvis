import argparse
import sys
import os
import requests



if __name__ == '__main__':
    example = 'Examples:\n\n'
    example += "$ python3 nathanvis.py -i 'http://192.168.50.3' -p 8000"
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=example)
    sgroup = parser.add_argument_group("Main Arguments")
    sgroup.add_argument("-i", metavar="[IP]", dest='target_ip', default=False, type=str, help="IP of collab server", required=True)
    sgroup.add_argument("-p", metavar="[PORT]", dest='target_port', default=False, type=int, help="Port of collab server", required=True)
    sgroup.add_argument("-s", metavar="[VICTIM IP/HOST/SUBNET]", dest="victim_addr", default=False, type=str, help="Host name, IP or subnet of victim", required=True)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    try:
        os.remove('temp.xml')
    except:
        pass
    os.system("nmap -sV -oX temp.xml {}".format(args.victim_addr))
    try:
        with open('temp.xml', 'rb') as f:
            r = requests.post('{}:{}/upload/'.format(args.target_ip,args.target_port), files={'file': f})
        os.remove('temp.xml')
    except Exception as e:
        print(e)

