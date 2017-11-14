/*
 * Alphabet lookup table
 *
 * 0x[0][h][g][f][e][d][c][b][a]
 * A '1' bit means segment is UP (green)
 * All bits up thus are 0x7F
 */
#ifndef _ALPHABET_H_
#define _ALPHABET_H_

#include <stdint.h>
#include <avr/pgmspace.h>
const uint8_t ascii_lookup[128] = 
	{
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,		// 0
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,		// 8
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,		// 16
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,		// 24
		0x00,	// Space				// 32
		      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 	// 33
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,		// 40
		0x3F,	// 0					// 48
		0x06,	// 1
		0x5B,	// 2
		0x4F,	// 3
		0x66,	// 4
		0x6D,	// 5
		0x7D,	// 6
		0x07,	// 7
		0x7F,	// 8					// 56
		0x6F,	// 9
		            0x00, 0x00, 0x00, 0x00, 0x00, 0x00,		// 58
		0x00,							// 64
		0x77, // A
		0x7C, // B
		0x39, // C
		0x5E, // D
		0x79, // E
		0x71, // F
		0x5F, // G +
		0x37, // H 					// 72
		0x06, // I
		0x38, // J
		0x33, // K
		0x0E, // L
		0x54, // M
		0x15, // N
		0x3E, // O
		0x67, // P 					// 80
		0x73, // Q
		0x05, // R
		0x5B, // S
		0x0F, // T
		0x3E, // U
		0x1C, // V
		0x2A, // W
		0x37, // X						// 88
		0x3B, // Y
		0x6D, // Z
		            0x00, 0x00, 0x00, 0x00, 0x00,		// 91
		0x00,							// 96
		0x77, // a
		0x7C, // b
		0x39, // c
		0x5E, // d
		0x79, // e
		0x71, // f
		0x5F, // g
		0x37, // h 					// 104
		0x06, // i
		0x38, // j
		0x33, // k
		0x0E, // l
		0x54, // m
		0x15, // n
		0x3E, // o
		0x67, // p 					// 112
		0x73, // q
		0x05, // r
		0x5B, // s
		0x0F, // t
		0x3E, // u
		0x1C, // v
		0x2A, // w
		0x37, // x 					// 120
		0x3B, // y
		0x6D, // z
		            0x00, 0x00, 0x00, 0x00, 0x00			// 123
	};

#endif // _ALPHABET_H_
