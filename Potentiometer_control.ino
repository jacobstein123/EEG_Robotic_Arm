#include <Servo.h> 

Servo myservo0; // create servo object to control a servo 
Servo myservo1;  
Servo myservo2;
Servo myservo3;
Servo myservo4;
Servo myservo5;

Servo servo_list[] = {myservo0, myservo1, myservo2, myservo3,myservo5}; //make a list of all the servos
 
/*int potpin = 0;  // analog pin used to connect the potentiometer
int val1;    // variable to read the value from the analog pin 
int val2;
int oldVal1 = val1;
int oldVal2 = val2;
int potpin2 = 1; */

 
void setup() 
{ 
  myservo1.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(10);
  myservo3.attach(11);
  myservo4.attach(6);
  myservo0.attach(5);
  myservo5.attach(3);
  Serial.begin(9600);
} 
 
void loop() 
{ 
  for (int i = 0; i <5; i++) 
  {
    int initial_value = analogRead(i); //gets the resistance value of the potentiometer from 0 to 1023
    int value = map(initial_value, 0, 1023, 0, 179); //maps the resistance value to a range of 0 to 179 to be used by a servo
    Serial.println(value);
    servo_list[i].write(value); //sets the appropriate servo to move to a certain number of degrees
    if (i == 3) //servos 3 and 4 need to be controlled by the same potentiometer
    {
       myservo4.write(179-value);
    }
  }
} 
