import requests, argparse, socket, json
from modules import script

class Tracker(script.Script):
    def __init__(self):
        self.globe = ["            ,,,,,,            ",
                      "        o#'9MMHb':'-,o,       ",
                      "     .oH\":HH$' \"' ' -*R&o,    ",
                      "    dMMM*\"\"'`'      .oM\"HM?.  ",
                      "  ,MMM'          \"HLbd< ?&H\  ",
                      " .:MH .\"\          ` MM  MM&b ",
                      ". \"*H    -        &MMMMMMMMMH:",
                      ".    dboo        MMMMMMMMMMMM.",
                      ".   dMMMMMMb      *MMMMMMMMMP.",
                      ".    MMMMMMMP        *MMMMMP .",
                      "     `#MMMMM           MM6P , ",
                      " '    `MMMP\"           HM*`,  ",
                      "  '    :MM             .- ,   ",
                      "   '.   `#?..  .       ..'    ",
                      "      -.   .         .-       ",
                      "        ''-.oo,oo.-''         "]

    def track(self, host: str):
        try:
            socket.gethostbyname(host)
            resp = json.loads(requests.get("http://ip-api.com/json/" + host).text)

            info = [" Tracking Results ".center(35, "-"),
                    "{} {}".format("IP Address".rjust(18), resp["query"]),
                    "{} {}".format("Country".rjust(18), resp["country"], resp["countryCode"]),
                    "{} {}".format("Region".rjust(18), resp["regionName"], resp["region"]),
                    "{} {}".format("City".rjust(18), resp["city"]),
                    "{} {}".format("ZipCode".rjust(18), resp["zip"]),
                    "{} {}".format("Time Zone".rjust(18), resp["timezone"]),
                    "{} {}".format("Organization".rjust(18), resp["org"]),
                    "{} {}".format("ISP".rjust(18), resp["isp"]),
                    "{} {}".format("Latitude".rjust(18), resp["lat"]),
                    "{} {}".format("Longitude".rjust(18), resp["lon"]),
                    "{}{}".format(" " * 9, resp["as"])]
                
            for line in self.globe:
                index = self.globe.index(line)
                
                try:
                    if index in [2, 13]:
                        self.print("     {}  {}".format(line, info[index-2]))
                    elif index > 2 and index < 13:
                        self.print("     {}  {}".format(self.colored(line), self.colored(info[index-2], dark=True)))
                    else:
                        self.print(" " * 5 + line)
                except Exception as e:
                    self.print(" " * 5 + line)
        except Exception as e:
            self.print("[!] Failed to track \"{}\":".format(host), "red")
            self.print("    " + str(e), "red", True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("PyTracker", description="Basic host location tracker using the JSON API provided by ip-api.com ...")
    parser.add_argument("host", type=str, help="Target hostname or IP Address to be tracked ...")

    args = parser.parse_args()

    tracker = Tracker()
    tracker.track(args.host)
