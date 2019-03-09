import socket

port = 5001
def fileIn():
    dns_output = []
    host_name = ""
    f = open("PROJI-DNSRS.txt","r")
    for line in f:
        splits = line.split()
        if splits[2] == "NS":
            host_name = [splits[0], splits[1], splits[2]]
        else:
            dns_output.append([splits[0],splits[1], splits[2]])
    return dns_output,host_name


def getDNS(input_client, dns_entries, host_name):
    for i in dns_entries:
        if i[0] == input_client.strip():
            return i[0] + " " + i[1] + " " + i[2]
    return host_name[0] + " " + host_name[1] + " " + host_name[2]


def Server(dns_entries, host_name):
    print("DNS Entries on RS are:", dns_entries, host_name)
    print("Waiting for client(s)...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print(socket.error)
    s.bind(('', port))
    s.listen(1)
    local_name = socket.gethostname()
    local_ip = (socket.gethostbyname(local_name))
    conn, client_ip = s.accept()

    print("The local name is: ", local_name)
    print("The local IP is: ", local_ip)
    print("The client IP address is: ", client_ip)

    while True:
        input_client = conn.recv(100).decode('utf-8')
        if (input_client == "endconnection"):
            s.close()
            exit()
        output = getDNS(input_client, dns_entries, host_name)
        conn.send(output.encode('utf-8'))
        print("Sending to the client:" + output)



dns_entries, host_name = fileIn()
Server(dns_entries, host_name)