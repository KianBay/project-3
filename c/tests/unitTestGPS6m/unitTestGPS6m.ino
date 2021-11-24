
#include <SoftwareSerial.h>

SoftwareSerial ss(12, 14);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ss.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (ss.available() > 0) {
    byte gpsData = ss.read();
    Serial.write(gpsData);
  }
}
