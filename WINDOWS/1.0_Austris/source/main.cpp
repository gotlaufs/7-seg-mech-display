#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "SerialPort.hpp"

using namespace std;
bool validate(string input);

//String for getting the output from arduino
char input[MAX_DATA_LENGTH];

/*Portname must contain these backslashes, and remember to
replace the following com port*/

//String for incoming data
char incomingData[MAX_DATA_LENGTH];

int main(int argc, char *argv[])
{
    if(argc != 3){
        cout << "Usage example: hpamssm.exe COM20 \"Hello World!\";" << endl;
        return -1;
    }
    string output = argv[2];
    for(int i = 0 ; i <= output.length(); i++){
        output[i] = toupper(output[i]);
    }
    if(output == ""){
        cout << "Please, enter text!" << endl;
        return -3;
    }
    char port_name[7 + strlen(argv[1])] = "\\\\.\\";
    strcat(port_name, argv[1]);
    SerialPort arduino(port_name);
    if (arduino.isConnected()){
        cout << "Connection Established!" << endl;
        cout << "Sending: " << output << endl;
    }else{
        cout << "PORT isn't connected!";
        return -2;
    }


    if(validate(output) != true){
        cout << "Wrong input!" << endl;
        return -4;
    }else{
        //Creating a c string
        char *c_string = new char[output.size() + 1];
        //copying the std::string to c string
        std::copy(output.begin(), output.end(), c_string);
        //Adding the delimiter
        c_string[output.size()] = '\n';
        //Writing string to arduino
        arduino.writeSerialPort(c_string, MAX_DATA_LENGTH);
        //Getting reply from arduino
        arduino.readSerialPort(input, MAX_DATA_LENGTH);
        //printing the output
        puts(input);
        //freeing c_string memory
        delete[] c_string;
    }
}

bool validate(string input){
    string allowed_characters;

    //65 - 90; 97 - 122; 48 - 57
    allowed_characters = allowed_characters + " ";
    for(int i = 48; i <= 57; i++){
        allowed_characters = allowed_characters + (char)i;
    }
    for(int i = 65; i <= 90; i++){
        allowed_characters = allowed_characters + (char)i;
    }
    for(int i = 97; i <= 122; i++){
        allowed_characters = allowed_characters + (char)i;
    }
    bool is_valid = false;
    for(int i = 0; i <= input.length(); i++){
        for(int n = 0; n <= allowed_characters.length(); n++){
            if(allowed_characters[n] == input[i]){
                is_valid = true;
            }
        }
        if(is_valid != true){
            return false;
        }else{
            is_valid = false;
        }
    }
    return true;
}
