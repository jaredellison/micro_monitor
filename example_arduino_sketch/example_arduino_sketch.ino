int inByte = 0;         // incoming serial byte

int i = 0;

void setup() {
  // start serial port at 9600 bps and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  establishContact();  // send a byte to establish contact until receiver responds
}

void loop() {
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    if (inByte == 10) {
      Serial.println();
    }
    else {
      // Check if inByte is in the lowercase range
      if (inByte >= 97 && inByte <= 122) {
        inByte = inByte - 32;
      }
      Serial.write(inByte);
      i++;
    }
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println("Waiting for a byte..");   // send an initial string
    delay(300);
  }
}
