import socket

portc = 5000
portrs = 5001
portts = 5002

end = "endconnection"

def fileIn():
    DNS_output = []
    f = open("PROJI-HNS.txt", "r")
    for line in f:
        DNS_output.append(line.rstrip())
    return DNS_output


def Client(DNS_entries):
    print("DNS Entries from client are:", DNS_entries)
    print("Client started ...")
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_name = socket.gethostname()
        local_ip = (socket.gethostbyname(local_name))
        rs.connect((local_ip, portrs))
    except socket.error:
        print(socket.error)

    ts = None
    f = open("RESOLVED.txt", "w")
    for i in DNS_entries:
        rs.send(i.encode('utf-8'))
        read_data = rs.recv(100).decode('utf-8')
        splits = read_data.split()
        print(splits)

        if (splits[-1] == 'A'):
            print(" Recieved this output for", i, "from RS server: ", splits[0], splits[1], splits[2])
        else:
            print(" RS does not have the output for",i ,", connecting TS ....")
            try:
                if ts == None:
                    ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_name = splits[0]
                    remote_ip = socket.gethostbyname(remote_name)
                    ts.connect((remote_ip, portts))
            except socket.error:
                print(socket.error)
            ts.send(i.encode('utf-8'))
            read_data = ts.recv(100).decode('utf-8')
            if read_data != "Hostname - Error:HOST NOT FOUND":
                splits2 = read_data.split()
                print(splits2[0], splits2[1], splits2[2])
            else:
                print("Hostname - Error:HOST NOT FOUND.")
        f.write(read_data+"\n")

    ts.send(end.encode('utf-8'))
    rs.send(end.encode('utf-8'))
    ts.close()
    rs.close()

    exit()

if __name__ == '__main__':
    DNS_entries = fileIn()
    Client(DNS_entries)