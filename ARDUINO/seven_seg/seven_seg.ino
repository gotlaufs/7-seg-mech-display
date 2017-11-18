/* asasc
*/
#include <string.h>
#include <ctype.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#include "alphabet.h"
#include "msg.h"

#define DEBUG

#define SEG_DRIVE_TIME 200 // How long apply current to each segment (ms)
// Order is important. Segments:
// G F E D C B A
const char SEG_UP[7] = {7, 3, 6, 8, 5, 4, 2};
const char SEG_DOWN[7] = {A0, 10, 12, A1, 13, 11, 9};

boolean ECHO = false;	// Echo back Serial characters is using standard terminal
boolean BLANK = true;	// Blank between letters
int LETTER_DELAY = 500;	// Delay between letters in milliseconds
int WORD_DELAY = 1000;	// Dealy between words in the text to say

// '1' in bit means segmet is UP
// Organized in 0x0gfe'dcba
uint8_t CURRENT_SEG_STATE;

char string_buffer[32];
int i;

String in_string = "";

// Helpers
void sayString(String text);
void sayLetter(char letter);
void printHelp(void);
void printAbout(void);
void printConfig(void);

#ifdef DEBUG
void printSegmentChar(char letter);
#endif

void setup(void){
	Serial.begin(9600);
	printAbout();

	// Pin setup:
	for (i=0; i<7; i++){
		pinMode(SEG_UP[i], OUTPUT);
		pinMode(SEG_DOWN[i], OUTPUT);
	}

	// Initialize the display to known state
	CURRENT_SEG_STATE = 0x7F;
	sayLetter(' ');
}

void loop(void){
	char in_byte = 0;
	int space_index = 0;
	String command = "";
	int working_int = 0;
	if (Serial.available() > 0){
		in_byte = Serial.read();

		// Sanitary checks, because we support only standard ASCII table
		if (!((in_byte > 127) || (in_byte < 0))){
			in_string += in_byte;
		}
		else{
			in_byte = 0;
		}

		if (ECHO == true){
			Serial.print(in_byte);
		}

		if (in_byte == '\n'){
			// Time to decode the in_string
			// Remove last character (newline)
			in_string = in_string.substring(0, in_string.length()-1);

			space_index = in_string.indexOf(' ');
			if (space_index > 0){
				// Split between command and the rest
				command = in_string.substring(0, space_index);
				in_string = in_string.substring(space_index + 1);
			}
			else{
				command = in_string;
				in_string = "";
			}

			// Decode command
			if (command.equalsIgnoreCase("SAY")){
				sayString(in_string);
			}
			else if (command.equalsIgnoreCase("HELP")){
				printHelp();
			}
			else if (command.equalsIgnoreCase("H")){
				printHelp();
			}
			else if(command.equalsIgnoreCase("WORD_DELAY")){
				working_int = in_string.toInt();
				if (working_int < 200){
					Serial.print("ERROR: Incorrect length for WORD_DELAY: <");
					Serial.print(in_string);
					Serial.println(">.");
					Serial.println("Supported values are integers >200");
				}
				else{
					WORD_DELAY = working_int;
					Serial.println("OK");
				}
			}
			else if(command.equalsIgnoreCase("LETTER_DELAY")){
				working_int = in_string.toInt();
				if (working_int < 200){
					Serial.print("ERROR: Incorrect length for LETTER_DELAY: <");
					Serial.print(in_string);
					Serial.println(">.");
					Serial.println("Supported values are integers >200");
				}
				else{
					LETTER_DELAY = working_int;
					Serial.println("OK");
				}
			}
			else if(command.equalsIgnoreCase("BLANK")){
				in_string.toUpperCase();
				if(in_string.startsWith("ON")){
					BLANK = true;
					Serial.println("OK");
				}
				else if(in_string.startsWith("OFF")){
					BLANK = false;
					Serial.println("OK");
				}
				else{
					Serial.print("ERROR: Incorrect parameter for BLANK: <");
					Serial.print(in_string);
					Serial.println(">.");
					Serial.println("Supported values are: ON, OFF");
				}
			}
			else if(command.equalsIgnoreCase("ECHO")){
				in_string.toUpperCase();
				if(in_string.startsWith("ON")){
					ECHO = true;
					Serial.println("OK");
				}
				else if(in_string.startsWith("OFF")){
					ECHO = false;
					Serial.println("OK");
				}
				else{
					Serial.print("ERROR: Incorrect parameter for ECHO: <");
					Serial.print(in_string);
					Serial.println(">.");
					Serial.println("Supported values are: ON, OFF");
				}
			}
			else if(command.equalsIgnoreCase("CONFIG")){
				printConfig();
			}
			else if(command.equalsIgnoreCase("ABOUT")){
				printAbout();
			}
			else{
				Serial.print("Unknown command: <");
				Serial.print(command);
				Serial.println(">");
				printHelp();
			}

			in_string = "";
		}
	}
}

void printHelp(void){
	for (i=0; i<MSG_HELP_LEN; i++){
		strcpy_P(string_buffer, (char*)pgm_read_word(&(MSG_HELP_TABLE[i])));
		Serial.print(string_buffer);
	}
}

void printAbout(void){
	for (i=0; i<MSG_ABOUT_LEN; i++){
		strcpy_P(string_buffer, (char*)pgm_read_word(&(MSG_ABOUT_TABLE[i])));
		Serial.println(string_buffer);
	}
}

void printConfig(void){
	Serial.println("Current configuration values:");
	Serial.print(" >> LETTER_DELAY = ");
	Serial.print(LETTER_DELAY);
	Serial.println(" ms");
	Serial.print(" >> WORD_DELAY = ");
	Serial.print(LETTER_DELAY);
	Serial.println(" ms");
	Serial.print(" >> ECHO = ");
	Serial.println(ECHO);
	Serial.print(" >> BLANK = ");
	Serial.println(ECHO);
	Serial.println();
}

void sayString(String text){
	Serial.print("Displaying data - observe..  ");

	for (i=0; i<text.length(); i++){
		sayLetter(text[i]);

		if(BLANK == true){
			sayLetter(' ');
		}
		if(text[i] == ' '){
			// Word ended - use word delay
			delay(WORD_DELAY);
		}
		else{
			// Just in between character delay
			delay(LETTER_DELAY);
		}
	}

	// Blank when done
	sayLetter(' ');

	Serial.println("DONE!");
}

void sayLetter(char letter){
	// This will drive only those segments that need to be driven.
	uint8_t working_char;
	uint8_t bitmask, this_bit;
	uint8_t drive_up[7], drive_down[7];
	int j;

	//working_char = pgm_read_word_near(ascii_lookup[text[i]]);
	working_char = ascii_lookup[letter];

	#ifdef DEBUG
	printSegmentChar(working_char);
	#endif

	bitmask = working_char ^ CURRENT_SEG_STATE;

	// Calculate drive signals
	for (j=0; j<7; j++){
		this_bit = 0x01 << j;
		if(bitmask & this_bit){
			// Current and segment to-display differ
			// Need to drive it
			if (working_char & this_bit){
				// Positive means need to go UP
				drive_up[j] = 1;
				drive_down[j] = 0;
			}
			else{
				drive_up[j] = 0;
				drive_down[j] = 1;
			}
		}
		else{
			drive_up[j] = 0;
			drive_down[j] = 0;
		}
	}

	// Do the actual driving
	for (j=0; j<7; j++){
		digitalWrite(SEG_UP[j], drive_up[j]);
		digitalWrite(SEG_DOWN[j], drive_down[j]);
	}

	delay(SEG_DRIVE_TIME);

	for (j=0; j<7; j++){
		digitalWrite(SEG_UP[j], 0);
		digitalWrite(SEG_DOWN[j], 0);
	}	

	CURRENT_SEG_STATE = working_char;
}

#ifdef DEBUG
void printSegmentChar(char letter){
	/*

	####  // 0
	#  #  // 4
	####  // 8
	#  #  // 12
	####  // 16

	*/
	char buffer[20] = {' '};
	int j;

	// Initialize buffer array
	for(j=0; j<20; j++){
		buffer[j] = ' ';
	}

	if(letter & (0x01 << 0)){
		// Segment A
		buffer[0] = '#';
		buffer[1] = '#';
		buffer[2] = '#';
		buffer[3] = '#';
	}
	if(letter & (0x01 << 1)){
		// Segment B
		buffer[3] = '#';
		buffer[7] = '#';
		buffer[11] = '#';
	}
	if(letter & (0x01 << 2)){
		// Segment C
		buffer[11] = '#';
		buffer[15] = '#';
		buffer[19] = '#';
	}
	if(letter & (0x01 << 3)){
		// Segment D
		buffer[16] = '#';
		buffer[17] = '#';
		buffer[18] = '#';
		buffer[19] = '#';
	}
	if(letter & (0x01 << 4)){
		// Segment E
		buffer[8] = '#';
		buffer[12] = '#';
		buffer[16] = '#';
	}
	if(letter & (0x01 << 5)){
		// Segment F
		buffer[0] = '#';
		buffer[4] = '#';
		buffer[8] = '#';
	}
	if(letter & (0x01 << 6)){
		// Segment G
		buffer[8] = '#';
		buffer[9] = '#';
		buffer[10] = '#';
		buffer[11] = '#';
	}

	// Print out the buffer
	for(j=0; j<20; j++){
		if(!(j%4)){
			// Every 4th line
			Serial.println();
		}
		Serial.print(buffer[j]);
	}
}
#endif
