//.write(0) servo rotate CCW
//.write(180) servo rotate CW
//.write(90) servo stop rotation


#include <Servo.h>

Servo left, right;  // create servo object to control a servo
// twelve servo objects can be created on most boards

#define LEFT_STOP   90
#define RIGHT_STOP  90

int pos = 0;    // variable to store the servo position
char incomingByte = NULL;   // for incoming serial data

void setup() {
  Serial.begin(115200);
  left.attach(4);// attaches the servo on pin 4 to the servo object
  right.attach(5);
  fullstop();
}

void fullstop() {
  left.write(LEFT_STOP);
  right.write(RIGHT_STOP);
}

void loop() {

  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();


      Serial.print("received: ");
      Serial.println(incomingByte);// say what you got:
      if (incomingByte == 'F') {
        Serial.println(" sent F, Moving Forward");
        left.write(0);
        right.write(180);
      }
      else if (incomingByte == 'B') {
        Serial.println(" sent B, Moving Backward");
        left.write(180);
        right.write(0);
      }
      else if (incomingByte == 'R') {
        Serial.println(" sent R, Moving Backward");
        left.write(180);
        right.write(180);
      }
      else if (incomingByte == 'L') {
        Serial.println(" sent L, Moving Backward");
        left.write(0);
        right.write(0);
      }
      else if (incomingByte == 'S' ) {
        Serial.println(" sent S, Stopped Moving ");
        fullstop();
      }
      else {
        Serial.println(" Command not recognised");
      }




  }


}
