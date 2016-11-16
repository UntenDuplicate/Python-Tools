import os, sys
try:
    import colorama, termcolor
    colorama.init(autoreset=True)
except Exception as e:
    termcolor = colorama = None



class Script(object):
    def __init__(self):
        self.location = os.path.dirname(os.path.realpath(__file__))

    def colored(self, text, color="green", dark=False):
        try:
            if not termcolor: raise Exception("")
            return termcolor.colored(text, color, attrs=["dark"] if dark else [])
        except Exception as e:
            return text

    def print(self, text, color="green", dark=False):
        for line in str(text).split("\n"):
            string = ""
            first_word = line.split(" ")[0]
            if first_word and first_word[0] == "[" and first_word[-1] == "]":
                string = "{}{}".format(self.colored(first_word, color), self.colored(line[len(first_word):], color, dark))
            else:
                if "\x1b[" in line:
                    string = line
                else:
                    string = self.colored(line, color, dark)
            sys.stdout.write(string + "\n")

    def read_file(self, filename, mode="r"):
        try:
            file = open(filename, mode)
            content = chunk = file.read(0xFFF)
            while chunk:
                chunk = file.read(0xFFF)
                content += chunk
                
            return content
        except Exception as e:
            return ""
