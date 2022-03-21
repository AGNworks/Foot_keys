byte escape1  = 8;
byte shift2 = 9;
byte space3 = 4; 



void setup() {
pinMode(escape1, INPUT_PULLUP);
pinMode(shift2, INPUT_PULLUP);
pinMode(space3, INPUT_PULLUP);

Serial.begin(115200);
}

void loop() {
 if (digitalRead(escape1) == LOW){
  delay(10);
  if (digitalRead(escape1) == LOW){
    Serial.print("1");
    delay(200);
  }
 }

 if (digitalRead(shift2) == LOW){
  delay(10);
  if (digitalRead(shift2) == LOW){
    Serial.print("2");
    delay(200);
  }
 }

 if (digitalRead(space3) == LOW){
  delay(10);
  if (digitalRead(space3) == LOW){
    Serial.print("3");
    delay(200);
  }
 }
}
