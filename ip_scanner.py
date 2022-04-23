import random
import subprocess

unchecked_ip_list = []
valid_ip_list = []

def make_octet():

    octet = str(random.randint(0,255))
    return(octet)

def make_ip():

    ip = ''

    for i in range(4):
        octet = make_octet()
        if i == 0:
            ip = ip + octet
        else:
            ip = ip + '.' + octet     
    return(ip)

## change the number below to adjust number of IPs generated
def make_unchecked_iplist():  
    for i in range(250):
        ip = make_ip()
        unchecked_ip_list.append(ip)
    print(unchecked_ip_list)

## optional function for adding a random port
def make_ip_and_port():

    port = str(random.randint(1,65535))
    ip = make_ip()
    full_ip = ip + ':' + port
    return(full_ip)

def verifier(ip):

    global valid_ip_list

    output = subprocess.Popen(f"ping {ip}", shell=True, stdout=subprocess.PIPE)
    msg_content = ''
    i = 0

    for line in output.stdout:
        #print(line)
        l = line.decode(encoding="utf-8", errors="ignore")
        msg_content += l

        ## runs the ping for 3 lines, this could posisbly be decreased to 2
        i += 1
        if i > 2:
            break

    ## quick check for the ping, I believe this only works for macOS and Linux
    if ("timeout" in msg_content) == True:
        return(False)
    elif ("timeout" in msg_content) == False:
        print(f"{ip} is valid.")
        return(True)
    else:
        pass
    

def main():

    make_unchecked_iplist()

    for ip in unchecked_ip_list:
        print(f"Verifying {ip}")
        ver = verifier(ip)

        if ver == True:
            print(f"Adding {ip} to valid_ip_list.")
            valid_ip_list.append(ip)
        else:
            print("IP is offline or invalid.")

    print(valid_ip_list)

    with open('valid_IPs.txt', 'a') as f:
        for i in valid_ip_list:
            f.write(i + '\n')

if __name__ == "__main__":
    main()
