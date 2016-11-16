import urllib3, argparse, socket, bs4
from netaddr import IPAddress
from modules import script


class ApacheServerStatus(script.Script):
    def __init__(self, host, proto="http", port=80, timeout=15, strict=True, retries=None, redirect=True,
                 assert_same_host=False, assert_hostname=None, assert_fingerprint=None, ssl_version=None):
        if "://" in host:
            host = host.split("://")[1].split("/")[0]
            
        socket.gethostbyname(host)

        self.request_cfg = {"timeout": timeout, "retries": retries, "redirect": redirect, "assert_same_host": assert_same_host}

        if proto.lower() == "https":
            self.connection = urllib3.HTTPSConnectionPool(host, port=port, timeout=timeout, retries=retries, ssl_version=ssl_version, assert_hostname=assert_hostname, assert_fingerprint=assert_fingerprint)
        else:
            self.connection = urllib3.HTTPConnectionPool(host, port=port, timeout=timeout, retries=retries, strict=strict)

        self.target = host
            

    def valid_address(self, address, family=socket.AF_INET):
        try:
            socket.inet_pton(family, address)
            return True
        except:
            if family == socket.AF_INET:
                self.valid_address(address, socket.AF_INET6)
            return False
        
    def run(self):
        try:
            response = self.connection.request("GET", "/server-status", **self.request_cfg)
                                                     
            soup = bs4.BeautifulSoup(response.data, "html.parser")
            if soup.title.text.lower() != "apache status" or response.status != 200: raise Exception("Target is not vulnerable ...")
            
            self.print("[i] " + soup.h1.text)
            self.print("    " + soup.address.text)
            info = [i.text for i in soup.findAll("dl")]
            for i in info:
                for i in i.split("\n"):
                    k, *v = i.split(":")
                    if v:
                        self.print("    {}:{}".format(self.colored(k), self.colored(":".join(v), dark=True)), dark=True)
                    else:
                        self.print("    " + self.colored(k))
            self.print("    " + soup.pre.text.replace("\n", "\n    "), dark=True)
            self.print("    {}\n".format(soup.p.text.replace("\n", "\n    ")), dark=True)
            self.print("\n")

            logs, logs_help = soup.findAll("table")
            filename = "{}-logs.csv".format(self.target)
            open(filename, "w").write("\n".join(", ".join(log.stripped_strings) for log in logs.findAll("tr")))
            self.print("    Server logs have been saved as CSV on file \"{}\".".format(filename))

            self.print("    Logs keys description:")
            self.print("        {}".format("\n        ".join(["{}: {}".format(*i.stripped_strings) for i in logs_help.findAll("tr")])), dark=True)
        except Exception as e:
            self.print("[!] " + str(e), "red", True)

parser = argparse.ArgumentParser("ApacheServerStatus", description="Apache /server-status page displays many information about your Apache server. This script is used to retrieve the information from that page and output it to your console ... NOTE: VerifiedHTTPSConnection uses one of assert_fingerprint, assert_hostname and host in this order to verify connections. If assert_hostname is False, no verification is done.")
parser.add_argument("host", type=str, help="Host used for this HTTP Connection (e.g. \"localhost\").")
parser.add_argument("-p", "--port", type=int, default=80, help="Port used for the HTTP Connection (Default is 80).")
parser.add_argument("-P", "--proto", type=str, default="http", help="If set as \"https\" a secure connection is going to be used, otherwise this argument is ignored.")
parser.add_argument("-r", "--retries", default=None, help="Configure the number of retries to allow before raising a \"MaxRetryError\" exception. Pass \"None\" to retry until you receive a response. Pass an integer number to retry connection errors that many times, but no other types of errors. Pass zero to never retry. If \"False\", then retries are disabled and any exception is raised immediately. Also, instead of raising a MaxRetryError on redirects, the redirect response will be returned.")
parser.add_argument("-R", "--redirect", type=bool, default=True, help="If True, automatically handle redirects (status codes 301, 302, 303, 307, 308). Each redirect counts as a retry. Disabling retries will disable redirect, too.")
parser.add_argument("-s", "--strict", type=bool, default=True, help="Causes BadStatusLine to be raised if the status line can't be parsed as a valid HTTP/1.0 or 1.1 status line.")
parser.add_argument("-S", "--ssl-version", type=int, default=True, help="Causes BadStatusLine to be raised if the status line can't be parsed as a valid HTTP/1.0 or 1.1 status line.")
parser.add_argument("-t", "--timeout", type=int, default=15, help="Socket timeout in seconds. This can be a float or integer, which sets the timeout for the HTTP requests.")
parser.add_argument("--assert-same-host", type=bool, default=False, help="If \"True\", will make sure that the host of the pool requests is consistent else will raise HostChangedError. When False, you can use the pool on an HTTP proxy and request foreign hosts.")
parser.add_argument("--assert-hostname", type=bool, default=None)
parser.add_argument("--assert-fingerprint", type=bool, default=None)

args = parser.parse_args()

if __name__ == "__main__":
    args = parser.parse_args()
    args = {arg: getattr(args, arg) for arg in dir(args) if arg[0] != "_"}
    try:
        script = ApacheServerStatus(**args)
        script.run()
    except Exception as e:
        print("[!] Failed to retrieve server-status page info from \"{}\":".format(args["host"]))
        print("    " + str(e))
