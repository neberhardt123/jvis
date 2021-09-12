import argparse
import sys
import os
import requests
import time

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
    #initial_scan = "nmap -n -sn {} -oG - | awk '/Up$/{{print $2}}' > first.txt".format(args.victim_addr)
    initial_scan = "nmap -n -sn -PU -PY80,23,443,21,22,25,3389,110,445,139 -PS80,23,443,21,22,25,3389,110,445,139,143,53,135,3306,8080,1723,111,995,993,5900,1025,587,8888 {} -oG - | awk '/Up$/{{print $2}}' > hosts_simple.txt".format(args.victim_addr)
    initial_scan_v = "nmap -n -sn -PU -PS --top-ports 1000 {} -oG - | awk '/Up$/{{print $2}}' > hosts_detailed.txt".format(args.victim_addr)

    first_scan = "nmap -n -T5 -iL hosts_simple.txt -oX temp.xml {}".format(args.victim_addr)
    second_scan = "nmap -T4 -O --osscan-limit -iL hosts_detailed.txt -Pn -sSVC --top-ports 2000 -oX temp.xml {}".format(args.victim_addr)

    #fast host discovery

    try:
        os.remove('hosts_simple.txt')
    except:
        pass
    os.system(initial_scan)

    try:
        os.remove('temp.xml')
    except:
        pass
    os.system(first_scan)

    try:
        with open('temp.xml', 'rb') as f:
            r = requests.post('{}:{}/upload/'.format(args.target_ip,args.target_port), files={'file': f})
            f.close()
    except Exception as e:
        print(e)

    #slower host discovery
    
    try:
        os.remove('hosts_detailed.txt')
    except:
        pass
    os.system(initial_scan_v)

    #while True:
    try:
        os.remove('temp.xml')
    except:
        pass
    os.system(second_scan)
    try:
        with open('temp.xml', 'rb') as f:
            r = requests.post('{}:{}/upload/'.format(args.target_ip,args.target_port), files={'file': f})
            f.close()
    except Exception as e:
        print(e)
            
    #    time.sleep(10)

