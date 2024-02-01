int Motor1a = 4;
int Motor1b = 5;
int Motor2a = 6;
int Motor2b = 7;


void setup() {
  // put your setup code here, to run once:
  pinMode(Motor1a, OUTPUT);
  pinMode(Motor1b, OUTPUT);
  pinMode(Motor2a, OUTPUT);
  pinMode(Motor2b, OUTPUT);
  
  digitalWrite(Motor2a, HIGH); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  digitalWrite(Motor1a, LOW); //Motor 1 einfahren
  digitalWrite(Motor1b, HIGH);
  delay(12000);
  digitalWrite(Motor2a, LOW); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  digitalWrite(Motor1a, LOW); //Motor 1 einfahren
  digitalWrite(Motor1b, LOW);



  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  delay(6000);
  digitalWrite(Motor1a, LOW); //Motor ausschalten
  digitalWrite(Motor1b, LOW);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  Kopier Vorlage -----------------------------------------------------------------------------------------
  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  
  digitalWrite(Motor1a, LOW); //Motor 1 einfahren
  digitalWrite(Motor1b, HIGH);
  
  digitalWrite(Motor2a, HIGH); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  
  digitalWrite(Motor2a, LOW); //Motor 2 ausfahren
  digitalWrite(Motor2b, HIGH);
  -----------------------------------------------------------------------------------------------------------
  */

  digitalWrite(Motor1a, LOW);  //Motor 1 einfahren
  digitalWrite(Motor1b, HIGH);
  delay(3000);
  digitalWrite(Motor2a, LOW); //Motor 2 ausfahren
  digitalWrite(Motor2b, HIGH);
  delay(4000);
  digitalWrite(Motor1a, LOW); //Motor 1 aussschalten
  digitalWrite(Motor1b, LOW);
  delay(7000);
  digitalWrite(Motor2a, LOW); //Motor 2 aussschalten
  digitalWrite(Motor2b, LOW);
  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  delay(7000);
  digitalWrite(Motor1a, LOW); //Motor 1 aussschalten
  digitalWrite(Motor1b, LOW);
  delay(1000);
  //------------------------------------------------------------ Alle schritte rückwärts:
  digitalWrite(Motor1a, LOW);  //Motor 1 einfahren
  digitalWrite(Motor1b, HIGH);
  delay(7000);
  digitalWrite(Motor1a, LOW); //Motor 1 aussschalten
  digitalWrite(Motor1b, LOW);
  digitalWrite(Motor2a, HIGH); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  delay(7000);
  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  delay(4000);
  digitalWrite(Motor2a, LOW); //Motor 2 aussschalten
  digitalWrite(Motor2b, LOW);
  delay(1000);
  digitalWrite(Motor1a, LOW); //Motor 1 aussschalten
  digitalWrite(Motor1b, LOW);
  delay(1000);
}
