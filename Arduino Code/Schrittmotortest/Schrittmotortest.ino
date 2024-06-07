int Index;

void setup()
{
pinMode(13, OUTPUT); //Enable
pinMode(12, OUTPUT); //Puls
pinMode(11, OUTPUT); //Direction

digitalWrite(13,LOW);

digitalWrite(11,HIGH);

for(Index = 0; Index < 1800; Index++)
{
digitalWrite(12,HIGH);
delayMicroseconds(500);
digitalWrite(12,LOW);
delayMicroseconds(500);
}




}

void loop()
{

}