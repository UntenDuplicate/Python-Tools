import argparse, socket

class Whois:
    def __init__(self, server="whois.arin.net", port=43):
        self.server = server
        self.port = port
        
    def query(self, query):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        sock.send("{}\r\n".format(query).encode())
        
        data = chunk = sock.recv(0xFFF)
        while chunk:
            chunk = sock.recv(0xFFF)
            data += chunk

        return data.decode()



if __name__ == "__main__":
    parser = argparse.ArgumentParser("Whois", "Retrieves whois information for IPv4 and IPv6 hosts, and outputs it to your console ...")
    parser.add_argument("query", type=str, help="Query to be sent to the whois server.")
    parser.add_argument("-s", "--server", default="whois.arin.net", type=str, help="Server which to send the query (defaults to \"whois.arin.net\").")
    parser.add_argument("-p", "--port", default=43, type=int, help="Port of the server which to send the query (defaults to 43).")

    args = parser.parse_args()

    whois = Whois(args.server, args.port)
    print(whois.query(args.query))
