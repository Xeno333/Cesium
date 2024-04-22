#define cesium_main main
#include <stdio.h>
;
long long int ci = 1;
;
void cesium_print_num(const long long int cesium_i ) {;
printf("%lli", cesium_i);
};
long long int cesium_add(const long long int cesium_i1 ,const long long int cesium_i2 ) {;
return cesium_i1 + cesium_i2;
};
long long int cesium_main() {;
const unsigned char cesium_array[3] = {0, 0, 0};
const unsigned char cesium_str[] = "Hello";
printf("%s", cesium_str);
const long long int cesium_a[123] = {1,
2,
3
};
const long long int cesium_i = ci;
long long int cesium_r = cesium_add(cesium_i, 50);
const int cesium_r32 =(int) (((long long int)cesium_r ) + cesium_r) ;
if (cesium_r == 100) {;
return 0;
};
return 1;
};
