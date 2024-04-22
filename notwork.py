import sys

fin = open(sys.argv[1], "r")
file = fin.read()
fin.close()


output = ""

#C_section = False
#ASM_section = False


#class parsed_token:
#    type = ""#INITI"LIZE TO EITHER "C" OR "CESIUNM" or "ASM"
#    cont = ""
#    def __init__(self, type, cont):
#        self.type = type
#        self.cont = cont

class parsed_token_line:
    parsed_token = {}
    index = 0
    def add_token(self, token):
        self.parsed_token[self.index] = token
        self.index += 1

split_chars = {
    ",",
    ".",
    ":",
    "[",
    "]",
    "{",
    "}",
    "(",
    ")",
    "\"",
    "'",
    " ",
    "\t",
    "\n",
    "\r",
    "~",
    "!",
    "<",
    ">",
    "=",
    ";",
    "?",
    "@",
    "\\",
    "/",
    "+",
    "-",
    "$",
    "%",
    "^",
    "&",
    "*",
    "|",
    "%",
    "^",
    "`",
    "#"
}

def break_up(str_i):
    split_str_o = {}
    p = 0
    for char in str_i:
        #if char == " ":
        #    p += 1
        #    continue
        if char in split_chars:
            if not p == 0:
                try:
                    if not split_str_o[p] == "":
                        p += 1
                except:
                    p = p
            split_str_o[p] = char
            p += 1
            split_str_o[p] = ""
        else:
            try:
                if not split_str_o[p] == "":
                    split_str_o[p] += char
                else:
                    split_str_o[p] = char
            except:
                split_str_o[p] = char
                
    return split_str_o


#def parse_part(part):
#    print(parsed_token("CESIUM", part).type)
#    if C_section == True:
#        return parsed_token("C", part)
#    if ASM_section == True:
#        return parsed_token("ASM", part)

#    return parsed_token("CESIUM", part)


def parse_line(line):
    paresed_line = parsed_token_line()
    parts = break_up(line)

    for part in parts:
        #paresed_line.add_token(parse_part(parts[part]))
        paresed_line.add_token(parts[part])

    return paresed_line
    


def parse(input):
    lineso = input.split("\n")
    lines = {}
    p = 0
    for x in lineso:
        if x:
            lines[p] = x
            p += 1

    parsed_lines = {}
    #for line in lines:
    #    parsed_lines[line] = parse_line(lines[line])
    #    print(parsed_lines[0].parsed_token)
    parsed_lines[0] = parse_line(lines[0])
    parsed_lines[1] = parse_line(lines[1])
    print(parsed_lines[0].parsed_token)
    return parsed_lines



def to_C(parsed_lines):
    global output
    for line in parsed_lines: 
        for part in parsed_lines[line].parsed_token:
            output += parsed_lines[line].parsed_token[part] + "\n"
    return 0



to_C(parse(file))

#print(output)


fout = open(sys.argv[2], "w")
fout.write(output)
fout.close() 