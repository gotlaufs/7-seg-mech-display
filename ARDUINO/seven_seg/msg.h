/*
 * Static strings
 *
 * Refer to:
 * https://playground.arduino.cc/Main/PROGMEM
 */

#ifndef _MSG_H
#define _MSH_H
#include <avr/pgmspace.h>

// Help message
const PROGMEM char MSG_HELP_0[] = "The seven segment display will ";
const PROGMEM char MSG_HELP_1[] = "display messages that are sent ";
const PROGMEM char MSG_HELP_2[] = "to it using the SAY command.\n";
const PROGMEM char MSG_HELP_3[] = " >> SAY <message> - display the";
const PROGMEM char MSG_HELP_4[] = " <message> letter by letter on ";
const PROGMEM char MSG_HELP_5[] = "the 7-segment display to the ";
const PROGMEM char MSG_HELP_6[] = "best of it's abilities.\n\n";
const PROGMEM char MSG_HELP_7[] = "There ar few commands available";
const PROGMEM char MSG_HELP_8[] = " to configure the message ";
const PROGMEM char MSG_HELP_9[] = "display behaviour:\n";
const PROGMEM char MSG_HELP_10[] = " >> LETTER_DELAY <ms> - how ";
const PROGMEM char MSG_HELP_11[] = "much time to wait (in ";
const PROGMEM char MSG_HELP_12[] = "milliseconds) between ";
const PROGMEM char MSG_HELP_13[] = "displaying each letter. ";
const PROGMEM char MSG_HELP_14[] = "Minimum 0.\n";
const PROGMEM char MSG_HELP_15[] = " >> WORD_DELAY <ms> - how much ";
const PROGMEM char MSG_HELP_16[] = "time to wait (in milliseconds) ";
const PROGMEM char MSG_HELP_17[] = "between individual words in a ";
const PROGMEM char MSG_HELP_18[] = "sentence. Minimum 0.\n";
const PROGMEM char MSG_HELP_19[] = " >> BLANK <ON;OFF> - enable or ";
const PROGMEM char MSG_HELP_20[] = "disable the blanking ";
const PROGMEM char MSG_HELP_21[] = "(whitespace) between displaying";
const PROGMEM char MSG_HELP_22[] = " each letter on the 7-seg ";
const PROGMEM char MSG_HELP_23[] = "indicator.\n\n";
const PROGMEM char MSG_HELP_24[] = "There are also few other ";
const PROGMEM char MSG_HELP_25[] = "commands:\n";
const PROGMEM char MSG_HELP_26[] = " >> HELP or just H - print this";
const PROGMEM char MSG_HELP_27[] = " message.\n";
const PROGMEM char MSG_HELP_28[] = " >> CONFIG - print out current ";
const PROGMEM char MSG_HELP_29[] = "configuration.\n";
const PROGMEM char MSG_HELP_31[] = " >> ABOUT - print out the intro";
const PROGMEM char MSG_HELP_32[] = " message.\n";
const PROGMEM char MSG_HELP_33[] = "Have fun!\n\n";

const char * const MSG_HELP_TABLE[] PROGMEM= {
	MSG_HELP_0,
	MSG_HELP_1,
	MSG_HELP_2,
	MSG_HELP_3,
	MSG_HELP_4,
	MSG_HELP_5,
	MSG_HELP_6,
	MSG_HELP_7,
	MSG_HELP_8,
	MSG_HELP_9,
	MSG_HELP_10,
	MSG_HELP_11,
	MSG_HELP_12,
	MSG_HELP_13,
	MSG_HELP_14,
	MSG_HELP_15,
	MSG_HELP_16,
	MSG_HELP_17,
	MSG_HELP_18,
	MSG_HELP_19,
	MSG_HELP_20,
	MSG_HELP_21,
	MSG_HELP_22,
	MSG_HELP_23,
	MSG_HELP_24,
	MSG_HELP_25,
	MSG_HELP_26,
	MSG_HELP_27,
	MSG_HELP_28,
	MSG_HELP_29,
	MSG_HELP_31,
	MSG_HELP_32,
	MSG_HELP_33
};

const int MSG_HELP_LEN = 33;

// About message
const PROGMEM char MSG_ABOUT_0[] = "_______________________________";
const PROGMEM char MSG_ABOUT_1[] = "_______________________________";
const PROGMEM char MSG_ABOUT_2[] = "    ____                       ";
const PROGMEM char MSG_ABOUT_3[] = "   /    /                      ";
const PROGMEM char MSG_ABOUT_4[] = "-------/--------__----__----__-";
const PROGMEM char MSG_ABOUT_5[] = "      /   ===  (_ ` /___) /   )";
const PROGMEM char MSG_ABOUT_6[] = "_____/________(__)_(___ _(___/_";
const PROGMEM char MSG_ABOUT_7[] = "                            /  ";
const PROGMEM char MSG_ABOUT_8[] = "                        (_ /   ";
const PROGMEM char MSG_ABOUT_9[] = "-------------------------------";
const PROGMEM char MSG_ABOUT_10[] = " A parrot seven segment display";
const PROGMEM char MSG_ABOUT_11[] = "";
const PROGMEM char MSG_ABOUT_12[] = "Type SAY <message> for action!";
const PROGMEM char MSG_ABOUT_13[] = "Or type HELP for more info.";
const PROGMEM char MSG_ABOUT_14[] = "\n";

const char * const MSG_ABOUT_TABLE[] PROGMEM= {
	MSG_ABOUT_0,
	MSG_ABOUT_1,
	MSG_ABOUT_2,
	MSG_ABOUT_3,
	MSG_ABOUT_4,
	MSG_ABOUT_5,
	MSG_ABOUT_6,
	MSG_ABOUT_7,
	MSG_ABOUT_8,
	MSG_ABOUT_9,
	MSG_ABOUT_10,
	MSG_ABOUT_11,
	MSG_ABOUT_12,
	MSG_ABOUT_13,
	MSG_ABOUT_14
};

const int MSG_ABOUT_LEN = 14;

#endif // _MSG_H