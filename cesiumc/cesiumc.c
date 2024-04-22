#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MaxLineSize (uint64_t)2048


typedef unsigned long long uint64_t;

typedef enum {
        _cref,
        _extern,
        _func,
        _return,
        _if,
        _else,
        _for,
        _while,
        _break,
        _continue,
        _c,
        _asm,
        _i64,
        _i32,
        _i16,
        _i8,
        _u64,
        _u32,
        _u16,
        _u8,
        _f64,
        _f32,
        _typdef,
        _struct,
        _enum,
        _bool,
        _mut,
        _static,
        _register,
        _local,
        _volital,
        _inculde,
        _const,
        _macro,
        _class,
        _self,
        _scope
} kwt;

char keywords[37][256] = {
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
        "typdef",
        "struct",
        "enum",
        "bool",
        "mut",
        "static",
        "register",
        "local",
        "volital",
        "inculde",
        "const",
        "macro",
        "class",
        "self",
        "scope"
};

char seperator[] = {
    ' ',
    '\t',
    '(', 
    ';',
    '-',
    '+',
    '/',
    '=',
    '!',
    '~',
    '|',
    '%',
    '^',
    '&',
    '>',
    '<',
    '\'',
    '\"',
    ',',
    ':',
    '*'
};

char c = 'F';

char name_space[256][256];
uint64_t nsp = 0;

char gnamespaces[256][256];
char gfunctions[256][256];
char gvars[256][256];

typedef enum {
    open,
    close
} type_of_chns;

void chns(const char* ns, type_of_chns t) {
    if (t == open) {
        strcpy(name_space[++nsp], ns);
    }
    else if (t == close) {
        strcpy(name_space[nsp--], "");
    }
}


char* name2c(const char* sin, const char* namespace) {
    uint64_t sz = 0, p = 0;
    while (sin[p] != 0) sz++, p++;
    p = 0;
    while (namespace[p] != 0) sz++, p++;
    p++;//for _

    sz += sizeof("___CESIUM_") - 1;

    sz++;//for '\n'
    char* sout = (char*)malloc(sz);

    strcpy(sout, "___CESIUM_");
    strcat(sout, namespace);
    strcat(sout, "_");
    strcat(sout, sin);

    return sout;
}


int isseperator(const char cin) {
    for (int i = sizeof(seperator); !(i < 0); i--) {
        if (cin == seperator[i]) {
            return 1;
        }
    }
    return 0;
}



char* compile(const char* sin, kwt kw, char* sout) {
    return sout;
}

char* compile_part(const char* sin) {
    char* sout = (char*)malloc(MaxLineSize * 4);

    uint64_t p = 0;

    while ((sin[p] == ' ') || (sin[p] == ';') || (sin[p] == '\t')) p++;//clear white_spaces

    if ((sin[p] == '/') && (sin[p+1] == '/')) {//Comment
        sout[0] = 0;
        return sout;
    }
    if (sin[p] == '\n') {//empty
        sout[0] = 0;
        return sout;
    }


    //Inline C
    if ((c == 'F') && (sin[p] == 'c') && (sin[p+1] == '{') && (sin[p+2] == '\n')) {
        c = 'T';
        sout[0] = 0;
        return sout;
    }
    if (c == 'T') {
        uint64_t i = 0;
        if ((sin[p] == '}')&& (sin[p+1] == 'c')&& (sin[p+2] == '\n')) {
            c = 'F';
            sout[0] = 0;
            return sout;
        }
        else {
            strcpy(sout, sin+p);
            return sout;
        }
    }

    char part[256] = {0};
    uint64_t p2 = 0;
    while (isseperator(sin[p]) != 1) part[p2++] = sin[p++];


    for (int i = (sizeof(keywords) / 256); i != -1; i--) {
        if (strcmp(part, keywords[i]) == 0) {
            return compile(sin+p, (kwt)i, sout);
        }
    }

    //do call

    return sout;
}




char keywords_maped[37][256] = {

};



int main(int argc, const char** argv) {

    //In
    if (argv[1] == NULL) {
        printf("No file in!\n");
        return -1;
    }
    FILE* f = fopen(argv[1], "r");
    if (f == NULL) {
        printf("Bad file name!\n");
        return -1;
    }

    //out
    FILE* fout = fopen("./out.c", "w");
    if (fout == NULL) {
        printf("Could not open output ./out.c!\n");
        return -1;
    }
    fclose(fout);
    fout = fopen("./out.c", "a");
    if (fout == NULL) {
        printf("Could not open output ./out.c!\n");
        return -1;
    }

    //loop read and break on ; and \n
    char lin[MaxLineSize] = {0};
    uint64_t l = 1;
    while (1) {
        lin[MaxLineSize-1] = 0;//Nullify end of lin to make suer no overflow

        if (fgets(lin, MaxLineSize, f) == NULL) {
            break;
        }

        if (lin[MaxLineSize-1] != 0) {
            printf("Error! Line %llu is too long! MaxLineSize = %llu", l, MaxLineSize - 1);
            return 1;
        }

        //tokenize(lin);

        char* lout = compile_part(lin);
        fputs(lout, fout);
        free(lout);

    }

    //Verify file is right

    fclose(f);


    return 0;
}