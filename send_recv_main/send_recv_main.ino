#include <SoftwareSerial.h>
#define setPin 6

SoftwareSerial mySerial(10,11); //RX, TX

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
    
  pinMode(6, OUTPUT);
  digitalWrite(setPin, LOW);
  delay(100);
  
  mySerial.write("AT+A001");
  delay(100);
  mySerial.write("AT+C001");
  delay(100);
  mySerial.write("AT+B9600");
  delay(100);
  mySerial.write("AT+FU3");
  delay(100);
  
  digitalWrite(setPin, HIGH);
}

void loop() {
  
  
  if(Serial.available() > 0){//Read from serial monitor and send over HC-12
    String input = Serial.readString();
    mySerial.println(input); 
//    Serial.println("Me: "+input); 
    //Serial.println(input);  
    //mySerial.println(input); 

   
  }
 
  if(mySerial.available() > 1){//Read from HC-12 and send to serial monitor
    String input = mySerial.readString();
    Serial.println(input);
    //Serial.println(input);  
       

  }
  
}
