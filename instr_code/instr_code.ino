#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include<math.h>
#include <WiFi.h> //Connect to WiFi NetworkTFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h


//not working at the moment, just copy and pasted some stuff in

MPU9255 imu; //imu object called, appropriately, imu
TFT_eSPI tft = TFT_eSPI();


int freq = 2000;
int channel = 0;
int resolution = 8;
const int sammpling_rate = 125;   //125 ms note sampling

const int BUTTON_PIN = 16;  //the bop button
const int BUTTON_PIN2 = 5;  //used to activate the game

uint32_t sample_timer;    //times the sampling

void  change_frequency(int note)  {
  switch(note)  {
    case 0:
      ledcWriteTone(channel,0);
      break;
    case 1:
      ledcWriteTone(channel,262); //Low c
      break;
    case 2:
      ledcWriteTone(channel,294); //Low d
      break;
    case 3:
      ledcWriteTone(channel,330); //Low d
      break;
    case 4:
      ledcWriteTone(channel,349); //Low d
      break;
    case 5:
      ledcWriteTone(channel,392); //Low d
      break;
    case 6:
      ledcWriteTone(channel,440); //Low d
      break;
    case 7:
      ledcWriteTone(channel,494); //Low d
      break;
  }
}



void setup() {

  Serial.begin(115200);
  pinMode(BUTTON_PIN,INPUT_PULLUP);
  pinMode(BUTTON_PIN2,INPUT_PULLUP);
  pinMode(27,OUTPUT);

  ledcSetup(channel, freq, resolution);
  ledcAttachPin(27, channel);
  ledcWrite(channel,10);

  sample_timer = millis();

}

void loop() {
  for (int freq = 250; freq < 1000; freq = freq + 1){

       Serial.println(freq);

       ledcWriteTone(channel, freq);
       delay(100);
    }
}



///INFRARED BELOW


#include <Wire.h>
#include <VL6180X.h>

VL6180X sensor;

void setup()
{
  Serial.begin(115200); //for debugging if needed.
  Wire.begin(21,22);
  Serial.println("this is starting up");

  sensor.init();
  sensor.configureDefault();

  // Reduce range max convergence time and ALS integration
  // time to 30 ms and 50 ms, respectively, to allow 10 Hz
  // operation (as suggested by Table 6 ("Interleaved mode
  // limits (10 Hz operation)") in the datasheet).
  sensor.writeReg(VL6180X::SYSRANGE__MAX_CONVERGENCE_TIME, 30);
  sensor.writeReg16Bit(VL6180X::SYSALS__INTEGRATION_PERIOD, 50);

  sensor.setTimeout(500);

   // stop continuous mode if already active
  sensor.stopContinuous();
  // in case stopContinuous() triggered a single-shot
  // measurement, wait for it to complete
  delay(300);
  // start interleaved continuous mode with period of 100 ms
  sensor.startInterleavedContinuous(100);
  sensor.setScaling(3);
  Serial.println("setup done");

}

void loop()
{
  Serial.print(sensor.readRangeContinuousMillimeters());    ///PRINTS THE mm DISTANCE READINGS FROM THE LASER
  Serial.println();
}
