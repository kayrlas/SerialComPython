// Copyright 2019 Kayrlas (https://github.com/kayrlas)

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("9600 bps, readString() timeout: 1000ms");
  Serial.println("Ready");
}

void loop()
{
  // put your main code here, to run repeatedly:
  String message;
  static int loop_num = 0;

  if (Serial.available() > 0)
  {
    message = Serial.readString();

    Serial.print("Recieved: ");
    Serial.println(message);
  }

  if (loop_num > 9) {
    Serial.println("pending");
    loop_num = 0;
  }
  loop_num++;
  delay(1000);
}
