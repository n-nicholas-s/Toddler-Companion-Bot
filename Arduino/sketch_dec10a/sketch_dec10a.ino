#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

char incomingByte = NULL;

void setup()
{
  Serial.begin(115200);
  //Set initial speed of the motor & stop
  motor3.setSpeed(200);
  motor4.setSpeed(200);
  motor2.setSpeed(200);
  motor1.setSpeed(200);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor1.run(RELEASE);
}

void loop()
{
  if (Serial.available() >  0) {
    incomingByte = Serial.read();

    if (incomingByte == 'F') {
      //Moving Forward

      motor3.run(FORWARD);
      motor4.run(FORWARD);
      motor2.run(FORWARD);
      motor1.run(FORWARD);
    }
    else if (incomingByte == 'B') {
      //Moving Backward
      motor3.run(BACKWARD);
      motor4.run(BACKWARD);
      motor2.run(BACKWARD);
      motor1.run(BACKWARD);
    }
    else if (incomingByte == 'R') {
      //Moving Right
      motor3.run(BACKWARD);
      motor4.run(BACKWARD);
      motor2.run(BACKWARD);
      motor1.run(BACKWARD);
    }
    else if (incomingByte == 'L') {
      //Moving left
    }
    else if (incomingByte == 'S' ) {
      //Stopped Moving
      motor3.run(RELEASE);
      motor4.run(RELEASE);
      motor2.run(RELEASE);
      motor1.run(RELEASE);

    }
    else if (incomingByte == 'M' ) {
    }
    else {
      Serial.println(" Command not recognised");
    }

  }

}
