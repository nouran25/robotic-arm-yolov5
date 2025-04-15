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

    if (command == "SORT_1") {
      baseServo.write(45);  // Move base to position for sorting Category 1
      delay(1000);           // Wait for arm movement
      gripperServo.write(45);  // Grab object
      delay(1000);
      gripperServo.write(0);   // Release object
      baseServo.write(90);  // Reset base position
    } else if (command == "SORT_2") {
      baseServo.write(135); // Move base to position for sorting Category 2
      delay(1000);
      gripperServo.write(45);  // Grab object
      delay(1000);
      gripperServo.write(0);   // Release object
      baseServo.write(90);  // Reset base position
    }
  }
}
