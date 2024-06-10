int Index;
int Motor1a = 6;
int Motor1b = 7;
int Motor2a = 4;
int Motor2b = 5;
int enable = 13;
int puls = 12;
int Direction = 11;
int magneta = 20;
int magnetb = 21;




void setup() {
  // put your setup code here, to run once:
  pinMode(Motor1a, OUTPUT);
  pinMode(Motor1b, OUTPUT);
  pinMode(Motor2a, OUTPUT);
  pinMode(Motor2b, OUTPUT);

  pinMode(enable, OUTPUT); //Enable
  pinMode(puls, OUTPUT); //Puls
  pinMode(Direction, OUTPUT);
  pinMode(magneta, OUTPUT);
  pinMode(magnetb, OUTPUT);

  digitalWrite(magneta, LOW); //Motor 1 einfahren
  digitalWrite(magnetb, HIGH);

  digitalWrite(Motor1a, LOW); //Motor 1 einfahren
  digitalWrite(Motor1b, HIGH);
  digitalWrite(Motor2a, HIGH); //Motor 2 einfahren
  digitalWrite(Motor2b, LOW);
  delay(11000);
  digitalWrite(Motor1a, LOW); //Motor 1 stop
  digitalWrite(Motor1b, LOW);
  digitalWrite(Motor2a, LOW); //Motor 2 stop
  digitalWrite(Motor2b, LOW);


  digitalWrite(13,LOW);

  digitalWrite(11,HIGH);  //High = links, LOW = rechts

  for(Index = 0; Index < 2580; Index++)
  {
  digitalWrite(12,HIGH);
  delayMicroseconds(500);
  digitalWrite(12,LOW);
  delayMicroseconds(500);
  }

  digitalWrite(Motor2a, LOW); //Motor 2 ausfahren
  digitalWrite(Motor2b, HIGH);
  delay(2550);
  digitalWrite(Motor2a, LOW); //Motor 1 stop
  digitalWrite(Motor2b, LOW);

  digitalWrite(Motor1a, HIGH); //Motor 1 ausfahren
  digitalWrite(Motor1b, LOW);
  delay(5670);
  digitalWrite(Motor1a, LOW); //Motor 1 stop
  digitalWrite(Motor1b, LOW);

  



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
