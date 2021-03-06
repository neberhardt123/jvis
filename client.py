import argparse
import sys
import os
import requests
import time
from pwn import *
#LOOP
#ADD LESS COMPLEX SCAN

class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'


def main():

    banner = """
 ===========================
     ___     _____ ____  
    | \ \   / /_ _/ ___| 
 _  | |\ \ / / | |\___ \ 
| |_| | \ V /  | | ___) |
 \___/   \_/  |___|____/ 

 ===========================\n
    """
    print(Color.BLUE + banner + Color.END)
    example = 'Examples:\n\n'
    example += "$ python3 client.py -i 192.168.50.3 -p 8000 -s 192.168.50.0/24 "
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=example)
    sgroup = parser.add_argument_group("Main Arguments")
    sgroup.add_argument("-i", metavar="[IP]", dest='target_ip', default=False, type=str, help="IP of collaboration server", required=True)
    sgroup.add_argument("-p", metavar="[PORT]", dest='target_port', default=8000, type=int, help="Port of collab server", required=False)
    sgroup.add_argument("-s", metavar="[VICTIM IP/HOST/SUBNET]", dest="victim_addr", default=False, type=str, help="Host name, IP or subnet of victim", required=True)
    sgroup.add_argument("-n", action='store_false', dest="loop_f", help="Only run scan once")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    target_server = "http://{}:{}".format(args.target_ip,args.target_port)

    initial_scan = "nmap -n -sn -PS80,23,443,21,22,25,3389,110,445,139,143,53,135,3306,8080,1723,111,995,993,5900,1025,587,8888 {} -oG - | awk '/Up$/{{print $2}}' > hosts_simple.txt".format(args.victim_addr)
    initial_scan_v = "nmap -n -sn -PS --top-ports 1000 {} -oG - | awk '/Up$/{{print $2}}' > hosts_detailed.txt".format(args.victim_addr)

    first_scan = "nmap -n -T5 -iL hosts_simple.txt -oX temp1.xml {} > firstscan.txt".format(args.victim_addr)
    second_scan = "nmap -T4 -iL hosts_detailed.txt -Pn -sSVC --top-ports 2000 -oX temp2.xml {} > secondscan.txt".format(args.victim_addr)

    p2 = log.progress("Connecting to JVIS server")
    try:
        request = requests.get(target_server, timeout=5)
    except (requests.ConnectionError, requests.Timeout) as exception:
        p2.failure(Color.RED + "???" + Color.END)
        print(Color.RED + "\nCould not connect to " + target_server + "\n")
        exit(1)
    p2.success(Color.GREEN + "???" + Color.END)

    #fast host discovery
    p1 = log.progress("Obtaining host list")
    #p1.status("test" + Color.END)
    try:
        os.remove('hosts_simple.txt')
    except:
        pass
    try:
        os.system(initial_scan)
    except:
        p1.failure(Color.RED + "???" + Color.END)
        print(Color.RED + "\nScan on " + args.victim_addr + " failed\n")
        exit(1)

    filesize = os.path.getsize("hosts_simple.txt")
    if filesize == 0:
        p1.success(Color.YELLOW + "No hosts detected" + Color.END)
    else: 
        p1.success(Color.GREEN + "???" + Color.END)



    try:
        os.remove('temp1.xml')
    except:
        pass

    try:
        os.remove('firstscan.txt')
    except:
        pass



    p3 = log.progress("Performing light-weight scan on " + args.victim_addr)
    try:
        os.system(first_scan)
    except:
        p3.failure(Color.RED + "???" + Color.END)
        print(Color.RED + "\nScan on " + args.victim_addr + " failed\n")
        exit(1)

    try:
        l = open("firstscan.txt","r").read()
        print(l)
    except:
        p3.failure(Color.RED + "???" + Color.END)
        print(Color.RED + "\nFailed to read scan\n")
        exit(1)

    p3.success(Color.GREEN + "???" + Color.END)



    p4 = log.progress("Uploading results to jVis server")
    try:
        with open('temp1.xml', 'rb') as f:
            r = requests.post('{}/upload/'.format(target_server), files={'file': f})
            f.close()
    except:
        p4.failure(Color.RED + "???" + Color.END)
        print(Color.RED + "\nCould not send results to " + target_server + "\n")
        exit(1)

    p4.success(Color.GREEN + "???" + Color.END)

    #slower host discovery

    if args.loop_f is False:
        print(Color.BLUE + "Running scan once" + Color.END)
        p5 = log.progress("Running heavy-weight scan")
        print("\n")
        try:
            os.remove('hosts_detailed.txt')
        except:
            pass

        os.system(initial_scan_v)

        try:
            os.remove('temp2.xml')
        except:
            pass
        
        try:
            os.remove('secondscan.txt')
        except:
            pass

        try:
            os.system(second_scan)
        except:
            p5.failure(Color.RED + "???" + Color.END)
            print(Color.RED + "\nScan on " + args.victim_addr + " failed\n")
            exit(1)


        try:
            l = open("secondscan.txt","r").read()
            print(l)
        except:
            p5.failure(Color.RED + "???" + Color.END)
            print(Color.RED + "\nFailed to read scan\n")
            exit(1)

        p5.success(Color.GREEN + "???" + Color.END)


        p6 = log.progress("Uploading results to jVis server")
        try:
            with open('temp2.xml', 'rb') as f:
                r = requests.post('{}/upload/'.format(target_server), files={'file': f})
                f.close()
        except:
            p6.failure(Color.RED + "???" + Color.END)
            print(Color.RED + "\nCould not send results to " + target_server + "\n")
            exit(1)
        p6.success(Color.GREEN + "???" + Color.END)

    else:
        print(Color.BLUE + "Running scan till the end of time" + Color.END)
        while True:
            p5 = log.progress("Running heavy-weight scan")
            print("\n")
            try:
                os.remove('hosts_detailed.txt')
            except:
                pass

            os.system(initial_scan_v)

            try:
                os.remove('temp2.xml')
            except:
                pass
            
            try:
                os.remove('secondscan.txt')
            except:
                pass

            try:
                os.system(second_scan)
            except:
                p5.failure(Color.RED + "???" + Color.END)
                print(Color.RED + "\nScan on " + args.victim_addr + " failed\n")
                exit(1)


            try:
                l = open("secondscan.txt","r").read()
                print(l)
            except:
                p5.failure(Color.RED + "???" + Color.END)
                print(Color.RED + "\nFailed to read scan\n")
                exit(1)

            p5.success(Color.GREEN + "???" + Color.END)


            p6 = log.progress("Uploading results to jVis server")
            try:
                with open('temp2.xml', 'rb') as f:
                    r = requests.post('{}/upload/'.format(target_server), files={'file': f})
                    f.close()
            except:
                p6.failure(Color.RED + "???" + Color.END)
                print(Color.RED + "\nCould not send results to " + target_server + "\n")
                exit(1)
            p6.success(Color.GREEN + "???" + Color.END)
            time.sleep(10)
            #end while loop here
   

if __name__ == '__main__':
    main()