#include<string.h>
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
const int trigPin = 34;
const int echoPin = 19;

long duration;
int distance;
 
void setup(){
    Serial.begin(9600); //initialize serial!
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT_PULLDOWN);
}
    
void loop(){
  // Clears the trigPin
    // digitalWrite(trigPin, LOW);
    
    // // Sets the trigPin on HIGH state for 10 micro seconds
    // digitalWrite(trigPin, HIGH);
    
    // digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = digitalRead(echoPin);
    
    Serial.print(duration);
    // Calculating the distance
    distance= duration*0.034/2;
    // Prints the distance on the Serial Monitor
    // Serial.print("Distance: ");
    // Serial.println(distance);
}