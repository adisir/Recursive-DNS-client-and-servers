import socket

port = 5002
def fileIn():
    DNS_output = []
    host_name = ""
    f = open("PROJI-DNSTS.txt","r")
    for line in f:
        splits = line.split()
        if splits[2] == "NS":
            host_name = [splits[0], splits[1], splits[2]]
        else:
            DNS_output.append([splits[0],splits[1], splits[2]])
    return DNS_output,host_name

def getDNS(read_client, DNS_entries, host_name):
    for i in DNS_entries:
        if i[0] == read_client.strip():
            return i[0] + " " + i[1] + " " + i[2]
    return i[0] + " - Error:HOST NOT FOUND"

def Server(DNS_entries, host_name):
    print("DNS Entries on TS are:", DNS_entries, host_name)
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
        read_client = conn.recv(100).decode('utf-8')
        if (read_client == "endconnection"):
            s.close()
            exit()
        output = getDNS(read_client, DNS_entries, host_name)
        print("Sending to the client:" + output)
        conn.send(output.encode('utf-8'))

if __name__ == '__main__':
    DNS_entries, host_name = fileIn()
    Server(DNS_entries, host_name)
