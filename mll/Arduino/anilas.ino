#include <Servo.h>
Servo myservo;  // create servo object to control a servo
               // a maximum of eight servo objects can be created
int pos = 0;    // variable to store the servo position
int i = -1;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
}

void loop() {
  i = Serial.read();
  if (i > -1) {
    myservo.write(i);
  }
}
