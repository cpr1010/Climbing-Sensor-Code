#include <M5StickCPlus.h>
#include "Adafruit_VL53L0X.h"
#include "WiFi.h"


Adafruit_VL53L0X lox = Adafruit_VL53L0X();

float dist;
float dist2;
float dist3;
float dist4;
float dist5;


float accX, accY, accZ;
float pitch, roll, yaw;
float sumVec;

int fallCounter = 00;

const char* ssid = "ColesIphone";
const char* password = "Romeo0813";

const uint16_t port = 9999;
const char* host = "172.20.10.3";

String distStr = String ("/");
String sumVecStr = String("/");



void setup() {
  M5.begin();
  M5.IMU.Init();
  M5.Lcd.setTextSize(2);
  M5.Lcd.setRotation(1);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() == WL_CONNECTED) {
      delay(500);
      
  }

  while (! Serial) {
    delay(1);
  }

  Serial.println("Adafruit VL53L0X test.");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power
  Serial.println(F("VL53L0X API Continuous Ranging example\n\n"));

  // start continuous ranging
  lox.startRangeContinuous();
}
void loop() {

  
  M5.IMU.SetAccelFsr(M5.IMU.AFS_4G);
  M5.IMU.getAccelData(&accX, &accY, &accZ);
  M5.IMU.getAhrsData(&pitch, &roll, &yaw);

  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("NOOOOO");
  }
  

  sumVec = sqrt((accX*accX) + (accY*accY) + (accZ*accZ));
  sumVecStr = String(sumVec) + ",";
  


  M5.update();
  if (M5.BtnA.isPressed()){
    client.stop();
    M5.Lcd.fillScreen(BLACK);
    
  }

 
dist = lox.readRange(); 
distStr = String (dist) + ",";








client.print(distStr);
client.print(sumVecStr);

delay(10);
}
