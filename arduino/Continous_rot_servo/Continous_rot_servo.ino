//This code is to demonstrate the use of a continuous rotation servo motor with its different functions
//Refer to surtrtech.com to understand further

#include <Servo.h> //Servo library

Servo myservo;  //Servo name is myservo
  

void setup() {
  Serial.begin(9600);
  myservo.attach(3);  // attaches the servo signal pin on pin D6

}

void loop() {

  myservo.write(40); //Motor rotate inside
  delay(1300);
  myservo.write(90); //Motor break
  delay(5000);
  myservo.write(180); //Motor rotate outside
  delay(1300); 
  myservo.write(90); //Motor breal
  delay(5000); 
  /*
  myservo.write(90);
  delay(2000);
  myservo.write(280); //Motor rotate outside
  delay(1500);
  myservo.write(190);
  delay(5000);
  */
  
      
}
