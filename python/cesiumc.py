import sys

fin = open(sys.argv[1], "r")
input = fin.read()
fin.close()


cflag = False
asmflag = False
c_block_nest_num = 0

output = ""
list_of_lines1 = input.split("\n")
list_of_lines = []

for line in list_of_lines1:
    list_of_lines.append(line.lstrip())


def compile_line(line):
    global cflag
    global asmflag
    global c_block_nest_num
    if cflag == True:
        if line == "}":
            c_block_nest_num -= 1
        if line == "{":
            c_block_nest_num += 1
        if c_block_nest_num == 0:
            cflag = False
        output += line + "\n"
        return
    return


for line in list_of_lines:
    compile_line(line)




fout = open(sys.argv[2], "w")
fout.write(output)
fout.close() 