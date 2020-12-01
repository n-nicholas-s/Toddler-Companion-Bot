#include <Servo.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>


Adafruit_MMA8451 mma = Adafruit_MMA8451();

Servo left, right;  // create servo object to control a servo
// twelve servo objects can be created on most boards

#define LEFT_STOP   90
#define RIGHT_STOP  90

char incomingByte = NULL;   // for incoming serial data

void setup() {
  Serial.begin(115200);
  left.attach(4);// attaches the servo on pin 4 to the servo object
  right.attach(5);
  fullstop();

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");

  mma.setRange(MMA8451_RANGE_2_G);

  Serial.print("Range = "); Serial.print(2 << mma.getRange());
  Serial.println("G");

}

void fullstop() {
  left.write(LEFT_STOP);
  right.write(RIGHT_STOP);
}

void receive() {
  // send data only when you receive data:

  // read the incoming byte:
  incomingByte = Serial.read();

  if (incomingByte == 'F') {
    //Moving Forward
    left.write(0);
    right.write(180);
  }
  else if (incomingByte == 'B') {
    //Moving Backward
    left.write(180);
    right.write(0);
  }
  else if (incomingByte == 'R') {
    //Moving Right
    left.write(180);
    right.write(180);
  }
  else if (incomingByte == 'L') {
    //Moving left
    left.write(0);
    right.write(0);
  }
  else if (incomingByte == 'S' ) {
    //Stopped Moving
    fullstop();
  }
  else if (incomingByte == 'M' ){
    transmit();
  }
  else {
    Serial.println(" Command not recognised");
  }
}


void transmit() {
  // Read the 'raw' data in 14-bit counts
  mma.read();
  //  Serial.print("X:\t"); Serial.print(mma.x);
  //  Serial.print("\tY:\t"); Serial.print(mma.y);
  //  Serial.print("\tZ:\t"); Serial.print(mma.z);
  //  Serial.println();

  /* Get a new sensor event */
  sensors_event_t event;
  mma.getEvent(&event);

  /* Display the results (acceleration is measured in m/s^2) */
  //  Serial.print("X: \t"); Serial.print(event.acceleration.x); Serial.print("\t");
  //  Serial.print("Y: \t"); Serial.print(event.acceleration.y); Serial.print("\t");
  //  Serial.print("Z: \t"); Serial.print(event.acceleration.z); Serial.print("\t");
  //  Serial.println("m/s^2 ");
  //
  /* Get the orientation of the sensor */
  uint8_t o = mma.getOrientation();

  switch (o) {
    case MMA8451_PL_PUF:
      Serial.write("Portrait Up Front");
      break;
    case MMA8451_PL_PUB:
      Serial.write("Portrait Up Back");
      break;
    case MMA8451_PL_PDF:
      Serial.write("Portrait Down Front");
      break;
    case MMA8451_PL_PDB:
      Serial.write("Portrait Down Back");
      break;
    case MMA8451_PL_LRF:
      Serial.write("Landscape Right Front");
      break;
    case MMA8451_PL_LRB:
      Serial.write("Landscape Right Back");
      break;
    case MMA8451_PL_LLF:
      Serial.write("Landscape Left Front");
      break;
    case MMA8451_PL_LLB:
      Serial.write("Landscape Left Back");
      break;
  }
  Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() >  0) {
    receive();
  }
}
