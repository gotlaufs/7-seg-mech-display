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
  
  String input = "";
  //If any input is detected in arduino
  if(Serial.available() > 0){
    //read the whole string until '\n' delimiter is read
    input = Serial.readStringUntil('\n');
    //If input == "ON" then turn on the led 
    //and send a reply
    Serial.println("Ready! Typing!");
    Serial.end();
    delay(1000);
    char curr_ch = 0;
    char next_ch = 0;
    bool last_iter = false;
    for(int i = 0; i <= input.length(); i++){
      curr_ch = input[i];
      if(i != input.length()){
        next_ch = input[i + 1];
      }else{
        last_iter = true;
      }
      sayLetter(input[i]);
      delay(NORMAL_DELAY);
      if(last_iter != true){
        if(curr_ch == next_ch){
          sayLetter(0);
        }
      }
    }
    sayLetter(0);
    Serial.begin(BAUD);
  }
}


void sayLetter(char letter){
  int lett = (int)letter;
  switch(lett){
    case 32://(space)
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = DOWN; seg[5] = DOWN; seg[6] = DOWN;
      break;
    case 48://0
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;   
    case 49://1
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] =DOWN; seg[5] = DOWN; seg[6] = DOWN;
      break;   
    case 50://2
      seg[0] = UP; seg[1] = UP; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = DOWN; seg[6] = UP;
      break;   
    case 51://3
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = DOWN; seg[5] = DOWN; seg[6] = UP;
      break;  
    case 52://4
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = DOWN; seg[5] = UP; seg[6] = UP;
      break;   
    case 53://5
      seg[0] = UP; seg[1] = DOWN; seg[2] = UP; seg[3] = UP; seg[4] = DOWN; seg[5] = UP; seg[6] = UP;
      break;   
    case 54://6
      seg[0] = UP; seg[1] = DOWN; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;   
    case 55://7
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = DOWN; seg[5] = DOWN; seg[6] = DOWN;
      break;  
    case 56://8
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;  
    case 57://9
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = DOWN; seg[5] = UP; seg[6] = UP;
      break;   
    case 65://A
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;    
    case 66://B
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 67://C
      seg[0] = UP; seg[1] = DOWN; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 68://D
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 69://E
      seg[0] = UP; seg[1] = DOWN; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 70://F
      seg[0] = UP; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 71://G
      seg[0] = UP; seg[1] = DOWN; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 72://H
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 73://I
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 74://J
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = DOWN; seg[5] = DOWN; seg[6] = DOWN;
      break;
    case 75://K
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 76://L
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 77://M
      seg[0] = UP; seg[1] = DOWN; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = DOWN; seg[6] = DOWN;
      break;
    case 78://N
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = DOWN; seg[6] = UP;
      break;
    case 79://O
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 80://P
      seg[0] = UP; seg[1] = UP; seg[2] = DOWN; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 81://Q
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = DOWN; seg[5] = UP; seg[6] = UP;
      break;
    case 82://R
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = UP; seg[5] = DOWN; seg[6] = UP;
      break;
    case 83://S
      seg[0] = UP; seg[1] = DOWN; seg[2] = UP; seg[3] = UP; seg[4] = DOWN; seg[5] = UP; seg[6] = UP;
      break;
    case 84://t
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 85://U
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = DOWN;
      break;
    case 86://V
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = DOWN; seg[6] = DOWN;
      break;
    case 87://W
      seg[0] = DOWN; seg[1] = UP; seg[2] = DOWN; seg[3] = UP; seg[4] = DOWN; seg[5] = UP; seg[6] = DOWN;
      break;
    case 88://X
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = DOWN; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
    case 89://Y
      seg[0] = DOWN; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = DOWN; seg[5] = UP; seg[6] = UP;
      break;
    case 90://Z
      seg[0] = UP; seg[1] = UP; seg[2] = DOWN; seg[3] = UP; seg[4] = UP; seg[5] = DOWN; seg[6] = UP;
      break;
    case 0:
      seg[0] = DOWN; seg[1] = DOWN; seg[2] = DOWN; seg[3] = DOWN; seg[4] = DOWN; seg[5] = DOWN; seg[6] = DOWN;
      break;
      /*
    case 66://B
      seg[0] = UP; seg[1] = UP; seg[2] = UP; seg[3] = UP; seg[4] = UP; seg[5] = UP; seg[6] = UP;
      break;
      */
  }
  for(int i = 0; i <= 6; i++){
    digitalWrite((i+1) * 2 + seg[i], HIGH);
  }
  delay(NORMAL_DELAY);
  for(int i = 2; i <= 15; i++){
    digitalWrite(i,LOW);
  }
}
