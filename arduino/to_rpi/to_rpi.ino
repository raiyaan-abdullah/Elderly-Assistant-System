//motorPins
const int motorPin1 = 2,motorPin2 = 3;        //right motor
const int motorPin3 = 6,motorPin4 = 7;       //left motor

int motorspeed = 100;
int rotationspeed = 70;
int leftspeed,rightspeed;

void setup() {
  //initialize motor pins
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT); 
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int data2;
    Serial.print("You sent me before: ");
    Serial.println(data);

    if (data=="fo") {
      leftspeed, rightspeed = motorspeed;
      motor(leftspeed,rightspeed);
      delay(1000);
    } 
    
      else if (data.substring(0,2)=="le") {
        plannedACRotate();
        delay(500);


    } 
      else if (data.substring(0,2)=="ri") {
        plannedCRotate();
        delay(500);
    } 
    
     else if (data=="br") {
      brake();
    } 

  }
}



void motor(int left, int right)
{
  
  if(right>0)
  {
  analogWrite(motorPin1,right);
  analogWrite(motorPin2,0);
  }
  else
  {
    analogWrite(motorPin1,0);
    analogWrite(motorPin2,-right);
  }

  if(left>0)
  {
  analogWrite(motorPin3,left);
  analogWrite(motorPin4,0);
  }
  else
  {
   analogWrite(motorPin3,0);
   analogWrite(motorPin4,-left); 
  }

 }



void brake(void)
{
  analogWrite(motorPin1, 0);
  analogWrite(motorPin2, 0);
  analogWrite(motorPin3, 0);
  analogWrite(motorPin4, 0);
}

void plannedACRotate()
{
  analogWrite(motorPin1,rotationspeed);
  analogWrite(motorPin2, 0);
  analogWrite(motorPin3, 0);
  analogWrite(motorPin4,rotationspeed);

}

void plannedCRotate()
{
  analogWrite(motorPin1,0);
  analogWrite(motorPin2, rotationspeed);
  analogWrite(motorPin3, rotationspeed);
  analogWrite(motorPin4,0);

}
