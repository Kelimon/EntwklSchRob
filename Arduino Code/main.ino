#include <Arduino.h>
#include <Stepper.h> // Hinzufügen der Programmbibliothek

// Pins für die Linearmotoren
int Motor1a = 4;
int Motor1b = 5;
int Motor2a = 6;
int Motor2b = 7;

// Schritte pro Umdrehung für den Schrittmotor
const int stepsPerRevolution = 2048;

// Initialisiere den Schrittmotor
Stepper myStepper(stepsPerRevolution, 3, 5, 4, 6);

// Definiere die Ausgangsposition
struct Durations {
  int durationLinMotor1;
  int durationLinMotor2;
  int stepsStepperMotor;
};

Durations homePosition = {0, 0, 0};

Durations chessFieldDurations[8][8] = {
  {{0, 0, 0}, {10, 0, 100}, {20, 0, 200}, {30, 0, 300}, {40, 0, 400}, {50, 0, 500}, {60, 0, 600}, {70, 0, 700}}, // Row 1 (1)
  {{0, 10, 100}, {10, 10, 200}, {20, 10, 300}, {30, 10, 400}, {40, 10, 500}, {50, 10, 600}, {60, 10, 700}, {70, 10, 800}}, // Row 2 (2)
  {{0, 20, 200}, {10, 20, 300}, {20, 20, 400}, {30, 20, 500}, {40, 20, 600}, {50, 20, 700}, {60, 20, 800}, {70, 20, 900}}, // Row 3 (3)
  {{0, 30, 300}, {10, 30, 400}, {20, 30, 500}, {30, 30, 600}, {40, 30, 700}, {50, 30, 800}, {60, 30, 900}, {70, 30, 1000}}, // Row 4 (4)
  {{0, 40, 400}, {10, 40, 500}, {20, 40, 600}, {30, 40, 700}, {40, 40, 800}, {50, 40, 900}, {60, 40, 1000}, {70, 40, 1100}}, // Row 5 (5)
  {{0, 50, 500}, {10, 50, 600}, {20, 50, 700}, {30, 50, 800}, {40, 50, 900}, {50, 50, 1000}, {60, 50, 1100}, {70, 50, 1200}}, // Row 6 (6)
  {{0, 60, 600}, {10, 60, 700}, {20, 60, 800}, {30, 60, 900}, {40, 60, 1000}, {50, 60, 1100}, {60, 60, 1200}, {70, 60, 1300}}, // Row 7 (7)
  {{0, 70, 700}, {10, 70, 800}, {20, 70, 900}, {30, 70, 1000}, {40, 70, 1100}, {50, 70, 1200}, {60, 70, 1300}, {70, 70, 1400}}  // Row 8 (8)
};

int columnToIndex(char column) {
  return column - 'a';
}

void moveLinearMotor(int motorA, int motorB, int duration, bool forward) {
  if (forward) {
    digitalWrite(motorA, HIGH);
    digitalWrite(motorB, LOW);
  } else {
    digitalWrite(motorA, LOW);
    digitalWrite(motorB, HIGH);
  }
  delay(duration);
  digitalWrite(motorA, LOW);
  digitalWrite(motorB, LOW);
}

void moveMotorsToPosition(Durations pos) {
  // Bewege den Schrittmotor
  myStepper.step(pos.stepsStepperMotor);

  // Bewege Linearmotoren
  moveLinearMotor(Motor1a, Motor1b, pos.durationLinMotor1, true);
  moveLinearMotor(Motor2a, Motor2b, pos.durationLinMotor2, true);

}

void moveMotors(String move) {
  char startCol = move.charAt(1);
  int startRow = move.charAt(2) - '0' - 1;  // Reihenindex 0-basiert
  char endCol = move.charAt(3);
  int endRow = move.charAt(4) - '0' - 1;    // Reihenindex 0-basiert

  Durations startPos = chessFieldDurations[startRow][columnToIndex(startCol)];
  Durations endPos = chessFieldDurations[endRow][columnToIndex(endCol)];

  // Bewege die Motoren zu den Startpositionen und dann zu den Endpositionen
  moveMotorsToPosition(startPos);
  //elektromagnet an
  moveMotorsToPosition(endPos);
  //elektromagnet aus
  
  // Nach dem Zug zur Ausgangsposition zurückkehren
  moveMotorsToPosition(homePosition);

  Serial.println("Move completed: " + move);
  
}

void setup() {
  Serial.begin(9600);

  pinMode(Motor1a, OUTPUT);
  pinMode(Motor1b, OUTPUT);
  pinMode(Motor2a, OUTPUT);
  pinMode(Motor2b, OUTPUT);

  myStepper.setSpeed(3); // Set the speed of the stepper motor

  Serial.println("Arduino ready");
}

void loop() {
  if (Serial.available() > 0) {
    String move = Serial.readStringUntil('\n');
    Serial.print("Received move: ");
    Serial.println(move);
    moveMotors(move);
    Serial.println("done");
  }
}
