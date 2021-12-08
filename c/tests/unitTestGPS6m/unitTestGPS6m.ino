
#include <SoftwareSerial.h>

SoftwareSerial ss(4, 3);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  ss.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (ss.available() > 0) {
    byte gpsData = ss.read();
    Serial.write(gpsData);
  }
}
