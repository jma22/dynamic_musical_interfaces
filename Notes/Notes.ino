#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

//For use outside of lab:
char network[] = "MIT";
char password[] = "";
//For use in lab:
//char network[] = "6s08";  //SSID for 6.08 Lab
//char password[] = "iesc6s08"; //Password for 6.08 Lab

//Global Wifi Client variable:
WiFiClient globalclient;
int clientstate=0;

//Variables for holding notes:
char notes[500];
char instrument[20]="Drums";

//Buttons:
const uint8_t PIN_1 = 16; //button 1
const uint8_t PIN_2 = 5; //button 2
const uint8_t PIN_3 = 19; //button 3
//Ultrasonic Sensors:
//echo
const uint8_t echoPIN = 26;
//trig
const uint8_t trigPIN = 27;

//
long duration;
int distance;
bool strum;
//
uint32_t durationtimer;
const uint16_t dtime=10;

//Buttons for playing (left to right):
uint8_t b1;
uint8_t b2;
uint8_t b3;

//Timers for recording and posting
uint32_t rtimer;
uint32_t ptimer;
const uint8_t recording=125;
const uint8_t posting=10000;

uint32_t primary_timer = 0;
uint32_t posting_timer = 0;

//Some constants and some resources:
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host

const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response

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

void setup() {
  Serial.begin(115200);
  tft.init();  //init screen
  tft.setRotation(2); //adjust rotation
  tft.setTextSize(1); //default font size
  tft.fillScreen(TFT_BLACK); //fill background
  tft.setTextColor(TFT_GREEN, TFT_BLACK); //set color of font to green foreground, black background
  delay(100); //wait a bit (100 ms)
  pinMode(PIN_1,INPUT_PULLUP);
  pinMode(PIN_2,INPUT_PULLUP);
  pinMode(PIN_3,INPUT_PULLUP);
  pinMode(trigPIN,OUTPUT);
  pinMode(echoPIN,INPUT);
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
  rtimer=millis();
  ptimer=millis();
  digitalWrite(trigPIN,LOW);
}

void loop() {
  b1=digitalRead(PIN_1);
  b2=digitalRead(PIN_2);
  b3=digitalRead(PIN_3);
  //Strumming:
  durationtimer=millis();
  digitalWrite(trigPIN,HIGH);
  while (millis()-durationtimer < dtime);
  digitalWrite(trigPIN,LOW);
  duration=pulseIn(echoPIN,HIGH);
  distance=duration*.034/2;
  Serial.println("Distance: ");
  Serial.println(distance);
  if (distance>3 && distance<11){
    strum=true;
    strcat(notes,"0 ");
  } 
  //Notes:
  if ((millis()-rtimer)>125 && strum){
    if (!b1 && !b2 && !b3){
      strcat(notes,"7 ");
    } else if (!b1 && !b3){
      strcat(notes,"6 ");
    } else if (!b2 && !b3){
      strcat(notes,"5 ");
    } else if (!b1 && !b2){
      strcat(notes,"4 ");
    } else if (!b3){
      strcat(notes,"3 ");
    } else if (!b2){
      strcat(notes,"2 ");
    } else if (!b1){
      strcat(notes,"1 ");
    } else {
      strcat(notes,"0 ");
      strum=false;
    }
    rtimer=millis();
  }
  if ((millis()-ptimer)>10000){
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
    ptimer=millis();
  }
}
