#include <Arduino.h>
#include <hp_BH1750.h>

// Matthew L Bringle
// Sensor Controller for "PowerPlant" Project
// MUST BE A MEGA2560 or similiar




//SENSORS:
/*
Capacitive Soil Moisture Sensor V2.0
  A0
  returns percentage moisture
  
Adafruit BH1750 LUX sensor
  SDA/SCL
  returns a value in "lux" units (illuminance)

Thermoresistors (3)
  1 - low level - A1
  2 - mid level - A2
  3 - exposed air - A3

Voltage Probes
  1 A4
  2 A5
  3 A6
  4 A7
  5 A8
  6 A9
  
*/

//LUX sensor object
hp_BH1750 BH1750;    

// Provided from CSMSV2.0 Design Page
const int dry = 595; 
const int wet = 239;
int MoistureSensorVal;
int HumidityVal;

//thermoristors:
int Vo;
float R1 = 10000;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

void resetArduino() {
  asm volatile ("  jmp 0");
}

float thermo(int pinDef) {
  Vo = analogRead(pinDef);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;
  T = (T * 9.0)/ 5.0 + 32.0; 
  return T;  
}

void setup() {
  Serial.begin(115200);

  // init the sensor with address pin connetcted to ground
  bool avail = BH1750.begin(BH1750_TO_GROUND);

  if (!avail) {
    Serial.println("No BH1750 sensor found!");
    while (true) {};                                        
  }
}

void moisture() {
  MoistureSensorVal = analogRead(A0);
  HumidityVal = map(MoistureSensorVal, wet, dry, 100, 0);
  Serial.print(HumidityVal);
}
void lux() {
  BH1750.start();   //starts a measurement
  float lux=BH1750.getLux();  //  waits until a conversion finished
  Serial.print(lux); 
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readString();
    
    if (input.startsWith("sensors")) {

      //MOISTURE:
      moisture();
      Serial.print(" ");

      //LUX - ILLUMINOSITY
      lux();
      Serial.print(" ");

      //TEMPERATURE PROBES (LOW->HIGH)
      Serial.print(thermo(A1));
      Serial.print(" ");
      Serial.print(thermo(A2));
      Serial.print(" ");
      Serial.print(thermo(A3));
      
      Serial.print(" ");

      //Serial.print(analogRead(A4 * 5.0 /1024.0)); first voltage sensor is always grounded for Ref
      Serial.print(0); 
      Serial.print(" ");
      Serial.print(analogRead(A5) * 5.0 /1024.0);
      Serial.print(" ");
      Serial.print(analogRead(A6) * 5.0 /1024.0);
      Serial.print(" ");
      Serial.print(analogRead(A7) * 5.0 /1024.0);
      Serial.print(" ");
      Serial.print(analogRead(A8) * 5.0 /1024.0);
      Serial.print(" ");
      Serial.print(analogRead(A9) * 5.0 /1024.0);
      Serial.print(" ");

      Serial.println("");
    }
    
    else if (input.startsWith("reset")) {
      resetArduino();
    }

    else if (input.startsWith("thermo")) {
      Serial.print(thermo(A1));
      Serial.print(" ");
      Serial.print(thermo(A2));
      Serial.print(" ");
      Serial.print(thermo(A3));
      Serial.println("");
    }

    else if (input.startsWith("lux")) {
      lux();
      Serial.println("");
    }
    

    
  }
}
