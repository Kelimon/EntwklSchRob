#include <Arduino.h>
#include <Stepper.h> // Hinzufügen der Programmbibliothek

// Pins für die Linearmotoren
int Motor1a = 4;
int Motor1b = 5;
int Motor2a = 6;
int Motor2b = 7;

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino ready");
}

void loop() {
  if (Serial.available() > 0) {
    String move = Serial.readStringUntil('\n');
    Serial.print("Received move: ");
    Serial.println(move);
    // Hier würde normalerweise der Code für moveMotors() stehen, der die Motoren bewegt
    Serial.println("done");
  }
}
