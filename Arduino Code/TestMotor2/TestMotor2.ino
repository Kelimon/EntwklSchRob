int Motor1a = 6;
int Motor1b = 7;
int Motor2a = 4;
int Motor2b = 5;
int motorvornea =18;
int motorvorneb = 19;
int magneta = 21;
int magnetb = 20;


void setup() {
  // put your setup code here, to run once:
  pinMode(Motor1a, OUTPUT);
  pinMode(Motor1b, OUTPUT);
  pinMode(Motor2a, OUTPUT);
  pinMode(Motor2b, OUTPUT);

  digitalWrite(Motor1a, LOW); //Motor 1 einfahren
  digitalWrite(Motor1b, HIGH);
  digitalWrite(Motor2a, HIGH); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  delay(11000);
  digitalWrite(Motor1a, LOW); //Motor 1 stop
  digitalWrite(Motor1b, LOW);
  digitalWrite(Motor2a, LOW); //Motor 2 stop
  digitalWrite(Motor2b, LOW);




  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  delay(6200);
  digitalWrite(Motor1a, LOW); //Motor 1 stop
  digitalWrite(Motor1b, LOW);

  digitalWrite(Motor2a, LOW); //Motor 2 ausfahren
  digitalWrite(Motor2b, HIGH);
  delay(600);
  digitalWrite(Motor2a, LOW); //Motor 1 stop
  digitalWrite(Motor2b, LOW);



  digitalWrite(magnetb, HIGH); //Magnet an
  digitalWrite(magneta, LOW);
  delay(2000);



}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  Kopier Vorlage -----------------------------------------------------------------------------------------
  digitalWrite(Motor2a, HIGH); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  digitalWrite(Motor2a, LOW); //Motor 2 ausfahren
  digitalWrite(Motor2b, HIGH);
  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  digitalWrite(Motor1a, HIGH); //Motor 1 einfahren
  digitalWrite(Motor1b, LOW);

  -----------------------------------------------------------------------------------------------------------
  */


}
