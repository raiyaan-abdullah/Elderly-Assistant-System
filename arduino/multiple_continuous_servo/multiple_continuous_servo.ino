/*
  Physical Pixel

  An example of using the Arduino board to receive data from the computer. In
  this case, the Arduino boards turns on an LED when it receives the character
  'H', and turns off the LED when it receives the character 'L'.

  The data can be sent from the Arduino Serial Monitor, or another program like
  Processing (see code below), Flash (via a serial-net proxy), PD, or Max/MSP.

  The circuit:
  - LED connected from digital pin 13 to ground

  created 2006
  by David A. Mellis
  modified 30 Aug 2011
  by Tom Igoe and Scott Fitzgerald

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/PhysicalPixel
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver medicine_drawer = Adafruit_PWMServoDriver();




int pos = 0; 


int incomingByte;      // a variable to read incoming serial data into
int servo_forward = 600;
int servo_brake = 90;
int servo_backward = 150;

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  medicine_drawer.begin();
  medicine_drawer.setPWMFreq(60);

}

void loop() {
  
  // see if there's incoming serial data:
  /*
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    // if it's a capital H (ASCII 72), turn on the LED:
    if (incomingByte == '0') {
      run_drawer(0);
    }
    // if it's an L (ASCII 76) turn off the LED:
    if (incomingByte == '1') {
      run_drawer(1);
    }
     if (incomingByte == '2') {
      run_drawer(2);
    }
  }
  */
  run_drawer(4);
  
}

void run_drawer(int drawer_no) {


  medicine_drawer.setPWM(drawer_no, 0, servo_forward); 
  delay(1300);
  
  medicine_drawer.setPWM(drawer_no, 0, servo_brake); 
  delay(4000);
  
  medicine_drawer.setPWM(drawer_no, 0, servo_backward); 
  delay(1300);   
  medicine_drawer.setPWM(drawer_no, 0, servo_brake); 
  delay(2000);
 
   
}