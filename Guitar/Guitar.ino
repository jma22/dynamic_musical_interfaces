#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include<math.h>
#include <WiFi.h> //Connect to WiFi NetworkTFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

//For use outside of lab:
char network[] = "MIT";
char password[] = "";
//For use in lab:
//char network[] = "6s08";  //SSID for 6.08 Lab
//char password[] = "iesc6s08"; //Password for 6.08 Lab

//Global Wifi Client variable:
WiFiClient globalclient;

//Variables for holding notes:
char notes[500];
char instrument[20]="guitar";

//Used for tabulating current amount of notes before they are posted
int totalnotes = 0;

//Buttons:
const uint8_t PIN_1 = 26; //button 1
const uint8_t PIN_2 = 27; //button 2
const uint8_t PIN_3 = 14; //button 3
const uint8_t PIN_4 = 13; //button 4
const uint8_t PIN_5 = 25; //button 5
//Ultrasonic Sensor:
//echo 
const uint8_t echoPIN = 19;
//trig
const uint8_t trigPIN = 21;

//Ultrasonic Sensor related variables for calculating distance
long duration;
int distance;
bool strum;
uint32_t durationtimer;
const uint16_t dtime=10;

//Buttons for playing (left to right):
uint8_t b1;
uint8_t b2;
uint8_t b3;
uint8_t b4;
uint8_t b5;

//Timers for recording and posting
uint32_t rtimer;
uint32_t ptimer;

//Variables for change_frequency
int freq = 2000;
int channel = 0;
int resolution = 8;

//Default last note is a rest
char lastnote[3] = "0 ";

//Some constants and some resources:
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host

const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response

void unblocked_http_request(char* host, char* request, char* response, uint16_t response_size, uint16_t response_timeout, uint8_t serial){
  if (globalclient.connect(host, 80)){
    //As long as Wificlient is connected, POST happens, and the function is finished
    if (serial) Serial.print(request);
    globalclient.print(request);
    globalclient.stop();
    memset(response, 0, response_size); //Null out (0 is the value of the null terminator '\0') entire buffer
  } else {
    //If not connected, POST does not happen
    if (serial) Serial.println("connection failed :/");
    if (serial) Serial.println("wait 0.5 sec...");
    globalclient.stop();
  }
}

//Will play the tone associated with the note given to it using its frequency
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
      ledcWriteTone(channel,330); //Low e
      break;
    case 4:
      ledcWriteTone(channel,349); //Low f
      break;
    case 5:
      ledcWriteTone(channel,392); //Low g
      break;
    case 6:
      ledcWriteTone(channel,440); //Low a
      break;
    case 7:
      ledcWriteTone(channel,494); //Low b
      break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(100); //wait a bit (100 ms)
  //Pin setup
  pinMode(PIN_1,INPUT_PULLUP);
  pinMode(PIN_2,INPUT_PULLUP);
  pinMode(PIN_3,INPUT_PULLUP);
  pinMode(PIN_4,INPUT_PULLUP);
  pinMode(PIN_5,INPUT_PULLUP);
  pinMode(trigPIN,OUTPUT);
  pinMode(echoPIN,INPUT);
  //Speaker playing notes setup
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(16, channel);   //buzzer needs to be on pin
  ledcWrite(channel,10);
  //Initial Wifi connection
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
  //Start timers for recording and posting
  rtimer=millis();
  ptimer=millis();
  //Initially sets trigPIN to low for distance measuring
  digitalWrite(trigPIN,LOW);
}

void loop() {
  //Get button values for note playing
  b1=digitalRead(PIN_1);
  b2=digitalRead(PIN_2);
  b3=digitalRead(PIN_3);
  b4=digitalRead(PIN_4);
  b5=digitalRead(PIN_5);
  int note_num;
  if ((millis()-rtimer)>=125){
    //Strumming:
    durationtimer=millis();
    //generates ultrasound
    digitalWrite(trigPIN,HIGH);
    while (millis()-durationtimer < dtime);
    //stops it after 10 microseconds
    digitalWrite(trigPIN,LOW);
    //Gets time that it traveled
    duration=pulseIn(echoPIN,HIGH);
    //Distance conversion to cm
    distance=duration*.034/2;
    Serial.println("Distance: ");
    Serial.println(distance);
    //If the distance sensor detects an object within a certain distance, it registers it as a strum
    if (distance>3 && distance<11){
      strum=true;
    }
    //Notes (only checked if a strum occured):
    if(strum) {
      if (!b4 && !b5){
        strcat(notes,"7 ");
        strcpy(lastnote, "7 ");
        note_num = 7;
      } else if (!b1 && !b2){
        strcat(notes,"6 ");
        strcpy(lastnote, "6 ");
        note_num = 6;
      } else if (!b5){
        strcat(notes,"5 ");
        strcpy(lastnote, "5 ");
        note_num = 5;
      } else if (!b4){
        strcat(notes,"4 ");
        strcpy(lastnote, "4 ");
        note_num = 4;
      } else if (!b3){
        strcat(notes,"3 ");
        strcpy(lastnote, "3 ");
        note_num = 3;
      } else if (!b2){
        strcat(notes,"2 ");
        strcpy(lastnote, "2 ");
        note_num = 2;
      } else if (!b1){
        strcat(notes,"1 ");
        strcpy(lastnote, "1 ");
        note_num = 1;
      } else {
        strcat(notes,"0 ");
        strcpy(lastnote, "0 ");
        strum=false;
        note_num = 0;
      }
    } else {
      strcat(notes,"0 ");
      strcpy(lastnote, "0 ");
      note_num = 0;
    }
    totalnotes += 1;
    rtimer=millis();
    change_frequency(note_num); //changes the note
  }
  if ((millis()-ptimer)>1000){
    Serial.println("POST");
    //to ensure we always get 8 notes
    int extra;
    extra=8-totalnotes;
    for (int x=0; x<extra; x++){
      strcat(notes,lastnote);
    }
    totalnotes = 0;
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
