#include <iostream>
#include <string>
#include <list>
#include <fstream>

using namespace std;


list<string> lines;

void name2c() {
    
}



int main(int argc, const char** argv) {
    if (argv[1] == NULL) {
        cout << "Bad file name!" << endl;
        return 1;
    }
    ifstream file(argv[1]);
    if (!file.is_open()) {
        cout << "Bad file name!" << endl;
        return 1;
    }

    //loop read and break on ; and \n
    /*while (true) {

    }*/

    file.close();


    return 0;
}
