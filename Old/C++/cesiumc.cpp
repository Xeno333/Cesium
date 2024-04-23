#include <iostream>
#include <string>
#include <map>
#include <list>

using namespace std;


typedef enum {
    func = 0,
    var = 1,
    obj = 2,
    INV = 3//In valid
} def_type;


typedef enum {
    code = 0,
    nl = 1,
    keyword = 2,
    sp_char = 3
} entry_type;

typedef struct {
    string line;
    entry_type type;
} entry;



list<entry> partslist;

map<string, def_type> crefs;
map<string, def_type> defs;


int make_ref(string str, def_type type) {
    map<string, def_type>::iterator it = defs.find(str);
    if(it != defs.end())  {
        return 0xff;
    }
    defs.insert({str, type});
    return 0;
}



class keyword {
    public:
        #define NUM_OF_KEYWORDS 37
        string keywords[NUM_OF_KEYWORDS] = {
            "cref", 
            "extern", 
            "func",
            "return",
            "if",
            "else",
            "for",
            "while",
            "break",
            "continue",
            "c",
            "asm",

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
            "local",
            "volital",

            "include",
            "const",
            "macro",

            "class",
            "self",
            "scope"
        };
        bool is_keyword(string str) {
            int p = -1;
            while (p++ != NUM_OF_KEYWORDS) {
                if (keywords[p] == str) {
                    return true;
                }
            }
            return false;
        }
};

string Cesium2C(string str) {
    return "cesium_" + str;
}



int parse_code(char* sin) {
    int p = 0;
    for (;sin[p] != 0; p++) {
        if (sin[p] == '\n') {
            partslist.push_back((entry){"", nl});
            continue;
        }
        //add line
    }
    for (const auto &part : partslist) {
        std::cout << "Line: " << part.line << ", Type: " << part.type << std::endl;
    }
    return 0;
}



int main(int argc, char** args) {

    char* code = (char*)"func main() : i64 {\n//example arrayu8 array[3] = {0, 0, 0}\n//exapmle number\ni64 i = 50\n// get return type\nmut i64 r = add(i, 50)\n//cast to other\ni32 r32 = r : i32\n//check logic\nif (r == 100) {\nreturn 0\n}\nreturn 1\n}\n";

    cout << parse_code(code) << endl;

    return 0;
}