#define cesium_main main
#include<stdio.h>
;
unsigned char* cesium_fget(const unsigned char* cesium_fn ,signed char* cesium_block ,const unsigned long long int cesium_size ) {;
const unsigned long long int cesium_f = ((unsigned long long int)fopen(cesium_fn, "rb") );
fread(cesium_block, 1, cesium_size, cesium_f);
fclose(cesium_f);
return cesium_block;
};
long long int cesium_fsize(const unsigned char* cesium_fb );
int cesium_main() {;
printf("Hello from cesium!\n");
return 0;
};
