#include <Servo.h>

Servo baseServo;
Servo gripperServo;

void setup() {
  Serial.begin(9600);
  baseServo.attach(9);      // Base servo on pin 9
  gripperServo.attach(10);  // Gripper servo on pin 10

  baseServo.write(90);      // Start at center
  gripperServo.write(0);    // Gripper open
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    if (command == "LEFT") {
      baseServo.write(45);  // Rotate base left
    } else if (command == "RIGHT") {
      baseServo.write(135); // Rotate base right
    } else if (command == "GRAB") {
      gripperServo.write(45);  // Close gripper
      delay(1000);
      gripperServo.write(0);   // Open gripper again (reset)
    }
  }
}

