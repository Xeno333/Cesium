import sys
import re
import os

#Line count
lc = 0
cflag = False
#asmflag = False
c_block_nest_num = 0
arrayc = 0


#vars and func and structs
declared = {}
cref = []

#output
file = "#define cesium_main main\n"



list_of_lines = []

try:
	incp = sys.argv[3]
except:
	incp = ""

def get_source(f):
	lout = []

	fin = open(f, "r")
	input = fin.read()
	fin.close()

	list_of_lines1 = input.split("\n")

	#get list of lines from file
	for line in list_of_lines1:
		if line.lstrip() == "\n" or line.lstrip() == "":
			continue
		lout.append(line.strip())

	return lout


list_of_lines = get_source(sys.argv[1])


ces_type = {
	"i64":"long long int",
	"i32":"int",
	"i16":"short int",
	"i8":"signed char",
	"u64":"unsigned long long int",
	"u32":"unsigned ing",
	"u16":"unsigned short int",
	"u8":"unsigned char",
	"f64":"double",
	"f32":"float",
	"typedef":"typedef",
	"struct":"struct",
	"enum":"enum",
	"bool":"bool",
	"*":"*",
}

keyword = {
	"if":1,
	"else":1,
	"while":1,
	"break":0,
	"continue":0,
	"extern":0,
	"return":0
}

decs = [
	"i64",
	"i32",
	"i16",
	"i8",
	"u64",
	"u32",
	"u16",
	"u8",
	"f64",
	"f32",
	"typedef",
	"struct",
	"enum",
	"bool",
	"mut",
	"static",
	"register",
	"volital"
]

quals = [
	"mut",
	"static",
	"register",
	"volital"
]


def is_dec(s):
	if s in decs:
		return True
	return False

def is_qual(s):
	if s in quals:
		return True
	return False


def make_cesium_ref_from_src_ref(strin):
	if strin in cref:
		return strin
	return "cesium_" + strin



def do_block(s):
	global arrayc
	string = False
	out = ""
	number = False

	pi = -1
	skip = 0
	for part in s:
		pi += 1

		#array
		if part == "}" and arrayc > 0:
			arrayc -= 1
		if part == "{":
			arrayc += 1

		#skip
		if not skip == 0:
			skip -= 1
			continue


		#string
		if (part == "\"" or part == "\'") and string == False:
			string = True
			out += part
			continue
		elif (part == "\"" or part == "\'") and string == True:
			string = False
			out += part
			continue
		if string == True:
			out += part
			continue

		#number

		if part in ["=", ",", "{", "}", "[", "]", "*", " ", "\t", "(", ")", "+", "-", "|", "&", "^", "~", "!", ">", "<", "?"]:
			number = False
			out += part
			continue

		#print(s)

		if part.isdigit():
			number = True

		if number == True:
			out += part
			continue

		#cast
		if part == ":":
			ol = ["("]
			for part in s[pi+1:]:
				skip += 1
				if part.isspace() == True:
					continue
				if part in ["=", ",", "{", "}", "[", "]", "*", "(", ")", "+", "-", "|", "&", "^", "~", "!", ">", "<", "?"]:
					skip -= 1
					break
				if not part in ces_type:
					print("Error tried to cast to invalid type at line ", lc, "!")
					exit()
				ol.append(ces_type[part])

			
			l1 = re.split("([^a-zA-Z0-9_ \t])", out)
			p = len(l1)
			bd = 0
			string1 = False

			while True:
				p -= 1

				if (part == "\"" or part == "\'") and string1 == False:
					string1 = True
					continue

				if (part == "\"" or part == "\'") and string1 == True:
					string1 = False
					continue

				if string1 == True:
					continue

				if l1[p] in [")", "}", "]"]:
					bd += 1
					continue
				
				if l1[p] in ["(", "{", "["]:
					bd -= 1
					if bd < 0:
						break
					continue

				if not bd == 0:
					continue

				if p == -1:
					break
				
				if l1[p] in ["=", ",", "{", "}", "[", "]", "*", "(", ")", "+", "-", "|", "&", "^", "~", "!", ">", "<", "?"]:
					break


			ol.append(")")
			l1.insert(p+1, "".join(ol))

			out = "".join(l1)

			continue



		else:
			if make_cesium_ref_from_src_ref(part) in declared:
				out += make_cesium_ref_from_src_ref(part)
				continue
			elif part in keyword:
				out += part
				continue

			#do func



	return out



c_block = False
c_block_e = False

def strip_comment(line):
	done = []

	global c_block
	global c_block_e

	#string
	string = False

	#size
	s = 0

	#Pointer to next part
	p = 0

	for part in line:
		p += 1

		if part == "'" and not line[p-2] == "\\":
			string = not string
		elif part == "\"" and not line[p-2] == "\\":
			string = not string

		#check for end of statment
		if c_block_e == True:
			c_block_e = False
			continue

		#hanndel comments
		if part == "/" and line[p] == "/" and string == False:
			break
		elif part == "/" and line[p] == "*" and string == False:
			c_block = True
			continue
		elif part == "*" and line[p] == "/" and string == False:
			c_block = False
			c_block_e = True
			continue

		if c_block == False:
			done.append(part)
			s += 1

	return done, s









def compile_line(line):
	
	if line == "...":
		return "..."

	global cflag, arrayc

	if line == "c{":
		cflag = True
		return ""
	
	if line == "}c":
		cflag = False
		return ""

	if cflag == True:
		output = line + "\n"
		return output

	output = ""

	parts = re.split("([^a-zA-Z0-9_])", line)
	parts = list(filter(None, parts))
	parts, s = strip_comment(parts)

	if s == 0:
		return ""


	if parts[0] in keyword:
		arrayc -= keyword[parts[0]]
		output += do_block(parts)
		return output

	if parts[0] == "import":
		global list_of_lines
		im = ""

		i = 1
		for part in parts[i:]:
			i += 1
			if part.isspace() == True:
				continue
			i -= 1
			break

		for part in parts[i:]:
			im += part
		
		if incp == "":
			im = os.path.dirname(os.path.abspath(__file__)) + "/lib/" + im

		list_of_lines = list_of_lines[:lc] + get_source(im) + list_of_lines[lc:]

		return output

	if parts[0] == "func":
		p = ""
		i = 0
		for part in parts:
			i += 1
			if part == "(":
				break

		c = 1
		v = i
		for part in parts[i:]:
			v += 1
			if part == ")":
				c -= 1
			if part == "(":
				c += 1
				continue
			if c == 0:
				for part in parts[v:]:
					if part == "{":
						break
					p += part
				break
		#type
		if (do_block(list(filter(None, re.split("([^a-zA-Z0-9_])", p.strip()))))).replace(')', '').replace('(', '') == "":
			output += "void"
		output += (do_block(list(filter(None, re.split("([^a-zA-Z0-9_])", p.strip()))))).replace(')', '').replace('(', '') + " "

		p = 0
		for part in parts[1:]:
			p += 1
			if part.isspace() == False:
				val = {
					"type":"func",
				}
				declared[make_cesium_ref_from_src_ref(part)] = val

				output += make_cesium_ref_from_src_ref(parts[p]) + "("
				v = []
				bc = 0
				for part in parts[p+1:]:
					if part == "(":
						bc += 1
						continue

					if part == ")":
						bc -= 1
						continue

					if bc == 0:
						output += compile_line("".join(v).strip()) 
						v = []
						break
					
					if bc == 1 and part == ",":
						output += compile_line("".join(v)) + ","
						v = []
						continue

					v.append(part)

				if parts[len(parts)-1] == "{":
					output += compile_line("".join(v)) + ") {"
				else:
					output += compile_line("".join(v)) + ")"

				break
		return output

	#cref
	elif parts[0] == "cref":
		parts2 = []
		i = -1


		for part in parts:
			i += 1
			if part == "cref":
				continue
			if part.isspace() == True:
				continue
			break
		
		while i < len(parts):
			parts2.append(parts[i])
			i += 1
		
		parts = parts2


		if parts[0] == "func":
			p = ""
			i = 0
			for part in parts:
				i += 1
				if part == "(":
					break

			c = 1
			v = i
			for part in parts[i:]:
				v += 1
				if part == ")":
					c -= 1
				if part == "(":
					c += 1
					continue
				if c == 0:
					for part in parts[v:]:
						if part == "{":
							break
						p += part
					break
			#type
			output += (do_block(list(filter(None, re.split("([^a-zA-Z0-9_])", p.strip()))))).strip("()") + " "

			p = 0
			for part in parts[1:]:
				p += 1
				if part.isspace() == False:
					val = {
						"type":"func",
					}
					cref.append(part)
					declared[make_cesium_ref_from_src_ref(part)] = val

					output += make_cesium_ref_from_src_ref(parts[p]) + "("
					v = []
					bc = 0
					for part in parts[p+1:]:
						if part == "(":
							bc += 1
							continue

						if part == ")":
							bc -= 1
							continue

						if bc == 0:
							output += compile_line("".join(v).strip()) 
							v = []
							break
						
						if bc == 1 and part == ",":
							output += compile_line("".join(v)) + ","
							v = []
							continue

						v.append(part)

					if parts[len(parts)-1] == "{":
						output += compile_line("".join(v)) + ") {"
					else:
						output += compile_line("".join(v)) + ")"
					break
			return ""
		
		elif is_dec(parts[0]) == True:
			i = 0
			quals = []
			q = False
			for part in parts:
				if part.isspace() == True:
					continue
				if is_qual(part) == True:
					q = True
					quals.append(part)
				else:
					break
				i += 1

			if q == True:
				i += 1

			for part in parts:
				if part.isspace() == False:
					break
				i += 1


			val = {
				"type":parts[i],
				"qual":quals
			}

			val["posttype"] = ""
			j = i
			while j < len(parts):
				j += 1
				if j >= len(parts):
					break
				if parts[j].isspace():
					continue
				if parts[j] == "*":
					val["posttype"] = parts[j]
					i += 1
					break


			while True:
				i += 1
				if is_dec(parts[i]) == True:
					continue
				if parts[i].isspace() == True:
					continue
				break

			j = i
			something = ""
			while True:
				j += 1
				if j >= len(parts):
					break
				if parts[j].isspace() == True:
					continue
				if parts[j] == "=":
					break
				if parts[j] == ";":
					break
				something += parts[j]


			val["something"] = something

			cref.append(parts[i])

			#if not make_cesium_ref_from_src_ref(parts[i]) in declared:
			declared[make_cesium_ref_from_src_ref(parts[i])] = val
			#else:
			#	print("Error on line ", lc, ": <", line, "> Declares var that exists! Note: Line number refrences line breaks via \\n and via ;")
			#	exit()
			
			return ""


	#declear
	elif is_dec(parts[0]) == True:
		i = 0
		quals = []
		q = False
		for part in parts:
			if part.isspace() == True:
				continue
			if is_qual(part) == True:
				q = True
				quals.append(part)
			else:
				break
			i += 1

		if q == True:
			i += 1

		for part in parts:
			if part.isspace() == False:
				break
			i += 1


		val = {
			"type":parts[i],
			"qual":quals
		}

		val["posttype"] = ""
		j = i
		while j < len(parts):
			j += 1
			if j >= len(parts):
				break
			if parts[j].isspace():
				continue
			if parts[j] == "*":
				val["posttype"] = parts[j]
				i += 1
				break


		while True:
			i += 1
			if is_dec(parts[i]) == True:
				continue
			if parts[i].isspace() == True:
				continue
			break


		j = i
		something = ""
		while True:
			j += 1
			if j >= len(parts):
				break
			if parts[j].isspace() == True:
				continue
			if parts[j] == "=":
				break
			if parts[j] == ";":
				break
			something += parts[j]


		val["something"] = something

		#if not make_cesium_ref_from_src_ref(parts[i]) in declared:
		declared[make_cesium_ref_from_src_ref(parts[i])] = val
		#else:
		#	print("Error on line ", lc, ": <", line, "> Declares var that exists! Note: Line number refrences line breaks via \\n and via ;")
		#	exit()


		#compile to C

		mut = False

		if "mut" in val["qual"]:
			mut = True

		if not mut == True:
			output += "const "

		for q in val["qual"]:
			if q == "mut":
				continue
			output += q + " "

		output += ces_type[val["type"]] + val["posttype"] + " "

		output += make_cesium_ref_from_src_ref(parts[i]) + val["something"] + " "


		i = -1
		for part in parts:
			i += 1
			if part == "=":
				p = []
				for part in parts[i:]:
					p.append(part)
				output += do_block(p)
				break


		return output

	elif parts[0] == "func":
		print("Func not supported")


	else:
		output += do_block(parts)
		return output

	return ""



while True:
	if lc == len(list_of_lines):
		break

	line = list_of_lines[lc]
	lc += 1
	
	done = compile_line(line)

	if done == "":
		continue
	if arrayc == 0:
		file += done + ";\n"
		continue
	else:
		file += done + "\n"

print(file)


fout = open(sys.argv[2], "w")
fout.write(file)
fout.close() 