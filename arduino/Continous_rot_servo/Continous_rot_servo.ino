//This code is to demonstrate the use of a continuous rotation servo motor with its different functions
//Refer to surtrtech.com to understand further

#include <Servo.h> //Servo library

Servo myservo;  //Servo name is myservo
  

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo signal pin on pin D6

}

void loop() {

  myservo.write(40); //Motor rotate inside
  delay(2000);
  myservo.write(90);
  delay(5000);
  myservo.write(180); //Motor rotate outside
  delay(4000);
  myservo.write(90);
  delay(5000);
  
      
}
