// Written by Jake Schwarz

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>
#include <string.h>
#include <ctype.h>
#include <iostream>
#include <string>

using namespace std;

void recurse_directories(const char* directory);
void parse_args(int argc, char* argv[]);
void determine_type(char* type_name);
void determine_size(char* sizespec);
void check_file(const char* filename, const char* directory);
void check_first(const char* filename);
bool check_conditions(const char* filename, string final, int ftype, int fsize_blocks, int fsize_chars);

int debug = 0;
char* name = NULL;
int type = -1;
int lessthan = -1;
int greaterthan = -1;
int equal_var = -1;
int lessthan_c = -1;
int greaterthan_c = -1;
int equal_c = -1;


int main(int argc, char *argv[])
{

    if (argc < 2) {
        fprintf(stderr, "No directory provided\n");
        fprintf(stderr, "Usage: ./find directory [filters]\n");
        exit(-1);
    }

    parse_args(argc, argv);
    check_first(argv[1]);
    recurse_directories(argv[1]);

    exit(0);
}

void recurse_directories(const char* directory){
    DIR *dp;
    struct dirent *dirp;

    // if (debug == 1)
    //     cout << "Opening: " << directory << endl;
    
    if ((dp = opendir(directory)) == NULL) {
        perror(directory);
        exit(-1);
    }

    while ((dirp = readdir(dp)) != NULL){
        const char* filename = dirp->d_name;

        // if (debug)
        //     printf("Checking file: %s\n", filename);

        if (strcmp(filename, "..") != 0 && strcmp(filename, ".") != 0){
            check_file(filename, directory);
        }    
    }    
            
    if (closedir(dp) == -1)
        perror("closedir");
}

void parse_args(int argc, char *argv[]){
    for(int i = 2; i < argc; i++){
        int j = i;
        
        if (debug)
            cout << "Arg " << i << ": " << argv[i] << endl;
        
        if (strcmp(argv[i], "-d") == 0)
            debug = 1;
        else if (strcmp(argv[i], "-name") == 0) {
            if(i + 1 < argc && argv[++j][0] != '-'){
                name = strdup(argv[++i]);
                // ++i;
                if (debug)
                    cout << "Name: " << name << endl; 
            }
            else{
                fprintf(stderr, "Not a valid name.\n");
                exit(-1);
            }
        }
        else if (strcmp(argv[i], "-type") == 0) {
            if(i + 1 < argc && argv[++j][0] != '-'){
                determine_type(strdup(argv[++i]));
                // ++i;
            }
            else{
                fprintf(stderr, "Not a valid type.\n");
                exit(-1);
            }
        }
        else if (strcmp(argv[i], "-size") == 0){
            if(i + 1 < argc){
                determine_size(strdup(argv[++i]));
                // ++i;
            }
            else{
                fprintf(stderr, "Not a valid size.\n");
                exit(-1);
            }
        }
        else{
            fprintf(stderr, "Not a valid filter.\n");
            exit(-1);
        }
    }
}

void determine_type(char* type_name){
    switch (type_name[0])
    {
    case 'f':
        type = S_IFREG;
        if (debug)
            cout << "Type: " << type << endl;
        break;

    case 'd':
        type = S_IFDIR;
        if (debug)
            cout << "Type: " << type << endl;
        break;

    case 'l':
        type = S_IFLNK;
        if (debug)
            cout << "Type: " << type << endl;
        break;

    case 'b':
        type = S_IFBLK;
        if (debug)
            cout << "Type: " << type << endl;
        break;

    case 'c':
        type = S_IFCHR;
        if (debug)
            cout << "Type: " << type << endl;
        break; 
    
    default:
        fprintf(stderr, "Not a valid type\n");
        exit(-1);
    }
}

void determine_size(char* sizespec){
    if (sizespec[0] == '+' && sizespec[strlen(sizespec)-1] == 'c'){
        sizespec++;
        sizespec[strlen(sizespec)-1] = 0;
        greaterthan_c = atoi(sizespec++);
        if (debug)
            cout << "Greater than char: " << greaterthan_c << endl;
    }
    else if (sizespec[0] == '+'){
        sizespec++;
        greaterthan = atoi(sizespec++);
        if (debug)
            cout << "Greater than: " << greaterthan << endl;
    }
    else if (sizespec[0] == '-' && sizespec[strlen(sizespec)-1] == 'c'){
        sizespec++;
        sizespec[strlen(sizespec)-1] = 0;
        lessthan_c = atoi(sizespec);
        if (debug)
            cout << "Less than char: " << lessthan_c << endl;
    }
    else if (sizespec[0] == '-'){
        sizespec++;
        lessthan = atoi(sizespec++);
        if (debug)
            cout << "Less than: " << lessthan << endl;
    }
    else if (isdigit(sizespec[0]) && sizespec[strlen(sizespec)-1] == 'c'){
        sizespec[strlen(sizespec)-1] = 0;
        equal_c = atoi(sizespec);
        if (debug)
            cout << "Equal char: " << equal_c << endl;
    }
    else if (isdigit(sizespec[0])){
        equal_var = atoi(sizespec++);
        if (debug)
            cout << "Equal: " << equal_var << endl;
    }
    else{
        fprintf(stderr, "Not a valid size.\n");
        exit(-1);
    }
    
}

void check_file(const char* filename, const char* directory){
        struct stat statbuf;
        string strfilename(filename);
        string strdirectory(directory);
        string final = strdirectory + "/" + strfilename;

        int ret = lstat(final.c_str(),&statbuf);

        if (ret != 0) {
            perror(filename);
            return;
        }

        int ftype = statbuf.st_mode & S_IFMT;
        int fsize_blocks = statbuf.st_blocks;
        int fsize_chars = statbuf.st_size;

        if(check_conditions(filename, final, ftype, fsize_blocks, fsize_chars))
            cout << final << endl;

        if (ftype == S_IFDIR && strcmp(filename, ".") != 0){
            recurse_directories(final.c_str());
        }
}

void check_first(const char* filename){
        struct stat statbuf;
        string strfilename(filename);
        string final = strfilename;

        int ret = lstat(final.c_str(),&statbuf);

        if (ret != 0) {
            perror(filename);
            return;
        }

        int ftype = statbuf.st_mode & S_IFMT;
        int fsize_blocks = statbuf.st_blocks;
        int fsize_chars = statbuf.st_size;

        if(check_conditions(filename, final, ftype, fsize_blocks, fsize_chars))
            cout << final << endl;
}

bool check_conditions(const char* filename, string final, int ftype, int fsize_blocks, int fsize_chars){
    if (type != -1 && type != ftype)
        return false;
    if (name != NULL && strcmp(name, filename) != 0)
        return false;
    if (greaterthan != -1 && fsize_blocks <= greaterthan)
        return false;
    if (greaterthan_c != -1 && fsize_chars <= greaterthan_c)
        return false;
    if (lessthan != -1 && fsize_blocks >= lessthan)
        return false;
    if (lessthan_c != -1 && fsize_chars >= lessthan_c)
        return false;
    if (equal_var != -1 && fsize_blocks != equal_var)
        return false;
    if (equal_c != -1 && fsize_chars != equal_c)
        return false;
    else
        return true;
}