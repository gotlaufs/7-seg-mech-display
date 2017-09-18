//Default baud speed for communication
#define BAUD          9600
#define NORMAL_DELAY  300

#define UP            0;
#define DOWN          1;

int seg[7] = {0, 0, 0, 0, 0, 0, 0};
void setup(){
  Serial.begin(BAUD);
  for(int i = 0; i <= 15; i++){
    pinMode(i, OUTPUT);
  }
  
}

void loop(){
  
  String input;
  //If any input is detected in arduino
  if(Serial.available() > 0){
    //read the whole string until '\n' delimiter is read
    input = Serial.readStringUntil('\n');
    //If input == "ON" then turn on the led 
    //and send a reply
    if (input.equals("SAY")){
      sayLetter('F');
      delay(NORMAL_DELAY);
      sayLetter('U');
      delay(NORMAL_DELAY);
      sayLetter('C');
      delay(NORMAL_DELAY);
      sayLetter('K');
      delay(NORMAL_DELAY);
      sayLetter(0);
      Serial.println("ok");
    }
  }
}


void sayLetter(char letter){
  int lett = (int)letter;
  switch(lett){
    case 65://A
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 67://C
      seg[0] = UP; seg[1] = DOWN; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 70://F
      seg[0] = UP; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 75://K
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 85://U
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 0:
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = DOWN; seg[5] = DOWN; seg[6] = DOWN;
      break;
    
  }
  for(int i = 0; i <= 6; i++){
    digitalWrite((i+1) * 2 + seg[i], HIGH);
  }
  delay(NORMAL_DELAY);
  for(int i = 2; i <= 15; i++){
    digitalWrite(i,LOW);
  }
}
