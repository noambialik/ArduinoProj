//HC-12 messenger send/receive
//autor Tom Heylen tomtomheylen.com
 
#include <SoftwareSerial.h>
 
SoftwareSerial mySerial(10,11); //RX, TX
String NAME = "Tomer";
 
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}
 
void loop() {
 
 
  if(Serial.available() > 0){//Read from serial monitor and send over HC-12
    String input = Serial.readString();
    String full = NAME + ": " + input;
    String encoded = NAME + ":" + input;
    for(int i=0; i < full.length(); i++){
      encoded[i] += full.length();
    }
    mySerial.println(encoded); 
    Serial.println(full); 
 
  }
 
  if(mySerial.available() > 1){//Read from HC-12 and send to serial monitor
    String input = mySerial.readString();
    String decoded = input;
    for(int i=0; i < input.length(); i++){
      decoded[i] -= input.length();
    }
    Serial.println("input: "+input);
    Serial.println("decoded: "+decoded);
   
  }
 
}
