import argparse
import sys
import os
import requests

#LOOP
#ADD LESS COMPLEX SCAN

if __name__ == '__main__':
    example = 'Examples:\n\n'
    example += "$ python3 nathanvis.py -i http://192.168.50.3 -p 8000 -s 192.168.50.0/24 "
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=example)
    sgroup = parser.add_argument_group("Main Arguments")
    sgroup.add_argument("-i", metavar="[IP]", dest='target_ip', default=False, type=str, help="IP of collab server", required=True)
    sgroup.add_argument("-p", metavar="[PORT]", dest='target_port', default=False, type=int, help="Port of collab server", required=True)
    sgroup.add_argument("-s", metavar="[VICTIM IP/HOST/SUBNET]", dest="victim_addr", default=False, type=str, help="Host name, IP or subnet of victim", required=True)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    initial_scan = "nmap -n -sn {} -oG - | awk '/Up$/{{print $2}}' > first.txt".format(args.victim_addr)
    first_scan = "nmap -T5 -oX temp.xml {}".format(args.victim_addr)
    second_scan = "nmap -T5 -O --osscan-limit -sV -sC -iL first.txt -oX temp.xml {}".format(args.victim_addr)
    try:
        os.remove('first.txt')
    except:
        pass
    os.system(initial_scan)
    for x in range(2):
        try:
            os.remove('temp.xml')
        except:
            pass
        if x == 0:
            os.system(first_scan)
        elif x == 1:
            os.system(second_scan)
        #os.system("nmap -v -T5 {} -p 21,22,23,25,110,139,443,445,3000,3389,8080 | grep Discovered | awk '{print $6}' > second.txt")
        #os.system("sort first.txt second.txt | uniq > initial.txt")
        #os.system("nmap -T5 -iL first.txt -oX temp.xml {}".format(args.victim_addr))
        #os.system("nmap -sV -oX temp.xml {}".format(args.victim_addr))
        try:
            with open('temp.xml', 'rb') as f:
                r = requests.post('{}:{}/upload/'.format(args.target_ip,args.target_port), files={'file': f})
        except Exception as e:
            print(e)
    try:
        os.remove('temp.xml')
    except:
        pass
