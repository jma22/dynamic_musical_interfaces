#include <string.h>
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>
#include <Wire.h>
#include <VL6180X.h>
#include <math.h>
#include <WiFi.h> //Connect to WiFi NetworkTFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

VL6180X sensor;
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

//For use outside of lab:
char network[] = "6s08";
char password[] = "iesc6s08";
//For use in lab:
//char network[] = "6s08";  //SSID for 6.08 Lab
//char password[] = "iesc6s08"; //Password for 6.08 Lab

//Global Wifi Client variable:
WiFiClient globalclient;
int clientstate=0;

char notes[500];
char instrument[20]="Theremin";

const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host

const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response

const int freq = 2000;
const int channel = 0;
const int resolution = 8;
const int sammpling_rate = 125;   //125 ms note sampling

uint32_t sampling_timer;
uint32_t post_timer;

int distance; //distance will be used to record how far the hand is from the theremin
int note_num;

//
long duration;


void unblocked_http_request(char* host, char* request, char* response, uint16_t response_size, uint16_t response_timeout, uint8_t serial){
  if (globalclient.connect(host, 80)){
    if (serial) Serial.print(request);//Can do one-line if statements in C without curly braces
    globalclient.print(request);
    globalclient.stop();
    memset(response, 0, response_size); //Null out (0 is the value of the null terminator '\0') entire buffer
  } else {
    if (serial) Serial.println("connection failed :/");
    if (serial) Serial.println("wait 0.5 sec...");
    globalclient.stop();
  }
}

void  change_frequency(int note)  {
  switch(note)  {
    case 0:
      ledcWriteTone(channel,0);
      break;
    case 1:
      ledcWriteTone(channel,262*2); //Low c
      break;
    case 2:
      ledcWriteTone(channel,294*2); //Low d
      break;
    case 3:
      ledcWriteTone(channel,330*2); //Low d
      break;
    case 4:
      ledcWriteTone(channel,349*2); //Low d
      break;
    case 5:
      ledcWriteTone(channel,392*2); //Low d
      break;
    case 6:
      ledcWriteTone(channel,440*2); //Low d
      break;
    case 7:
      ledcWriteTone(channel,494*2); //Low d
      break;
  }
}

void setup(){
    Serial.begin(115200); //for debugging if needed.
    Wire.begin(21,22);
    sensor.init();
    sensor.configureDefault();

    sensor.writeReg(VL6180X::SYSRANGE__MAX_CONVERGENCE_TIME, 30);
    sensor.writeReg16Bit(VL6180X::SYSALS__INTEGRATION_PERIOD, 50);
    sensor.setTimeout(500);

    sensor.stopContinuous();
    delay(300);
    // start interleaved continuous mode with period of 100 ms
    sensor.startInterleavedContinuous(100);
    sensor.setScaling(3);

    tft.init();  //init screen
    tft.setRotation(2); //adjust rotation
    tft.setTextSize(1); //default font size
    tft.fillScreen(TFT_BLACK); //fill background
    tft.setTextColor(TFT_GREEN, TFT_BLACK); //set color of font to green foreground, black background
    delay(100); //wait a bit (100 ms)

    ledcSetup(channel, freq, resolution);
    ledcAttachPin(26, channel);   //buzzer needs to be on pin 26
    ledcWrite(channel,10);
    ledcWriteTone(channel,0); //automatically writes a rest into the instrument on startup


    WiFi.begin(network,password); //attempt to connect to wifi
    uint8_t count = 0; //count used for Wifi check times
    Serial.print("Attempting to connect to ");
    Serial.println(network);
    while (WiFi.status() != WL_CONNECTED && count<12) {
      delay(500);
      Serial.print(".");
      count++;
    }
    delay(2000);
    if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
      Serial.println("CONNECTED!");
      Serial.println(WiFi.localIP().toString() + " (" + WiFi.macAddress() + ") (" + WiFi.SSID() + ")");
      delay(500);
    } else { //if we failed to connect just Try again.
      Serial.println("Failed to Connect :/  Going to restart");
      Serial.println(WiFi.status());
      ESP.restart(); // restart the ESP (proper way)
    }
    sampling_timer = millis();
    post_timer = millis();

    Serial.println("setup done");
    digitalWrite(trigPIN,LOW);
}

void loop() {
  distance = sensor.readRangeContinuousMillimeters();
  Serial.println(distance);
  if (millis() - sampling_timer > sammpling_rate) {
    note_num = 7 - distance/100;   //returns int from 0 to 7
    //Serial.println(note_num);

    if ((millis()-sampling_timer)>125){
      if (note_num == 7){
        strcat(notes,"7 ");
      } else if (note_num == 6){
        strcat(notes,"6 ");
      } else if (note_num == 5){
        strcat(notes,"5 ");
      } else if (note_num == 4){
        strcat(notes,"4 ");
      } else if (note_num == 3){
        strcat(notes,"3 ");
      } else if (note_num == 2){
        strcat(notes,"2 ");
      } else if (note_num == 1){
        strcat(notes,"1 ");
      } else {
        strcat(notes,"0 ");
      }
    change_frequency(note_num);
    sampling_timer = millis();
    }
  }
  //
  if ((millis()-post_timer)>10000){
    Serial.println("POST");
    //POST:
    char body[4000]; //for body;
    sprintf(body,"instrument=%s&notes=%s",instrument,notes);//generate body, posting to User, 1 step
    int body_len = strlen(body); //calculate body length (for header reporting)
    sprintf(request_buffer,"POST http://608dev.net/sandbox/sc/kvfrans/dynamic_musical_interfaces/music_database.py HTTP/1.1\r\n");
    strcat(request_buffer,"Host: 608dev.net\r\n");
    strcat(request_buffer,"Content-Type: application/x-www-form-urlencoded\r\n");
    sprintf(request_buffer+strlen(request_buffer),"Content-Length: %d\r\n", body_len); //append string formatted to end of request buffer
    strcat(request_buffer,"\r\n"); //new line from header to body
    strcat(request_buffer,body); //body
    strcat(request_buffer,"\r\n"); //header
    Serial.println(request_buffer);
    unblocked_http_request("608dev.net", request_buffer, response_buffer, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT,true);
    memset(notes,0,500);
    post_timer=millis();
  }
}
