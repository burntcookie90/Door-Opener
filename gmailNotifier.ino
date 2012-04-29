#include <Servo.h>

int outPin = 12; // Output connected to digital pin 2
int mail = LOW; // Is there new mail?
int val; // Value read from the serial port
int count;
Servo motor;

void setup()
{

  Serial.begin(9600);
  Serial.flush();
  motor.attach(outPin);
  count = 0;
}

void loop()
{
  // Read from serial port
  if (Serial.available())
  {
    val = Serial.read();
    Serial.println(val);
    if (val == 'M') mail = HIGH;
    else if (val == 'N') mail = LOW;
  }

  // Set the angle of the servo
  if(mail)
    motor.write(40);
  // count++;
  else
    motor.write(129);

  //if(count%2==1)
  // motor.write(175);
  // else
  //  motor.write(118);
}



