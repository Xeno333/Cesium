#include <stdio.h>

char* rawcode;
unsigned long long pointer = 0;

void out_line(char* s) {
    printf("%s", s);
}

void do_var() {
}


typedef struct {
    int a;
    int b;
    void (*print)(void* o);
} obj;

void print(void* i) {
    obj* o = (obj*)i;
        printf("%d, %d\n", o -> a, o -> b);
}

obj obj_init_o1() {
    obj o;
    o.a = 0;
    o.b = 1;
    o.print = &print;
    return o;
}



int main(int argc, char** args) {
    rawcode = "func main() : i64 {\nreturn 0\n}";
    obj o = obj_init_o1();
    o.print(&o);
    return 0;
}