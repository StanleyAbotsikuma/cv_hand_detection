#include <WebSocketsClient_Generic.h>


#include <Arduino.h>
#include <ArduinoWebsockets.h>

WebSocketsClient webSocket;

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
  
#include <Hash.h>

ESP8266WiFiMulti WiFiMulti;


#define USE_SERIAL Serial1


//***************//
#include <ArduinoJson.h>
StaticJsonDocument<256> doc;

int Motor1A = 14;
int Motor1B =2;
int Motor2A = 12;
int Motor2B = 13;

String loadData;

//*******************//



void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {

  switch(type) {
    case WStype_DISCONNECTED:
      Serial.printf("[WSc] Disconnected!\n");
      break;
    case WStype_CONNECTED: {
      Serial.printf("[WSc] Connected to url: %s\n", payload);

      // send message to server when Connected
      //webSocket.sendTXT("Connected");
    }
      break;
    case WStype_TEXT:
//      Serial.printf("[WSc] get text: %s\n", payload);

      // send message to server
      // webSocket.sendTXT("message here");
      //**********//
      getPayloadFunction(payload);
      //*********************//
      break;
    case WStype_BIN:
      Serial.printf("[WSc] get binary length: %u\n", length);
      hexdump(payload, length);

      // send data to server
      // webSocket.sendBIN(payload, length);
      break;
        case WStype_PING:
            // pong will be send automatically
            Serial.printf("[WSc] get ping\n");
            break;
        case WStype_PONG:
            // answer to a ping we send
            Serial.printf("[WSc] get pong\n");
            break;
    }

}

void setup() {
  //**********************//
    pinMode(Motor1A, OUTPUT);
  pinMode(Motor1B, OUTPUT);
  pinMode(Motor2A, OUTPUT);
  pinMode(Motor2B, OUTPUT);
//***************************//
  // Serial.begin(115200);
   Serial.begin(115200);

  //Serial.setDebugOutput(true);
  Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  for(uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] BOOT WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }


  WiFiMulti.addAP("Trevillion", "trevillion.mifi.c");

  //WiFi.disconnect();
  while(WiFiMulti.run() != WL_CONNECTED) {
    delay(100);
  }

  // server address, port and URL
  webSocket.begin("192.168.1.163", 4041, "/");

  // event handler
  webSocket.onEvent(webSocketEvent);

  // use HTTP Basic Authorization this is optional remove if not needed
 // webSocket.setAuthorization("user", "Password");

  // try ever 5000 again if connection has failed
  webSocket.setReconnectInterval(5000);
  
  // start heartbeat (optional)
  // ping server every 15000 ms
  // expect pong from server within 3000 ms
  // consider connection disconnected if pong is not received 2 times
  webSocket.enableHeartbeat(15000, 3000, 2);

}

void loop() {

  webSocket.loop();
}



//***********************************//


void connectedPayLoadFunction(uint8_t * payload) {
  String payload1 = (char * )payload;
  Serial.println(payload1);
}


void getPayloadFunction(uint8_t * payload) {

  loadData  = (char * )payload;
// Serial.println(loadData);
  DeserializationError err = deserializeJson(doc, loadData);
  if (err)
  {
    Serial.println(err.c_str());
    return;
  }
// Serial.printf((char * ) doc);

  String r_type = doc["type"];
//  Serial.printf(r_type);
  if ( r_type == "board")
  { 
    String r_data = doc["data"];
    if ( r_data  == "forward")
    {
      forward();
       Serial.println("forward");


    }

    if ( r_data  == "stop")
    {
      to_stop();
       Serial.println("stop");


    }
    if ( r_data  == "left")
    {
      left();
Serial.println("left");
    }

     if ( r_data  == "right")
    {
      right();
Serial.println("right");
    }

      if ( r_data  == "back")
    {
      back();
Serial.println("back");
    }



  }

 



}






void forward()
{
   digitalWrite(Motor1A, LOW);
  digitalWrite(Motor2A, LOW);

  digitalWrite(Motor1B, HIGH);
  digitalWrite(Motor2B, HIGH);
}

void back()
{


  digitalWrite(Motor1B, LOW);
  digitalWrite(Motor2B, LOW);

  digitalWrite(Motor1A, HIGH);
  digitalWrite(Motor2A, HIGH);
}

void to_stop()
{
  digitalWrite(Motor1A, HIGH);
  digitalWrite(Motor2A, HIGH);

  digitalWrite(Motor1B, HIGH);
  digitalWrite(Motor2B, HIGH);
}

void right()
{
  digitalWrite(Motor1B, LOW);
  digitalWrite(Motor2A, LOW);

  digitalWrite(Motor1A, HIGH);
  digitalWrite(Motor2B, HIGH);
}

void left()
{
  digitalWrite(Motor1B, HIGH);
  digitalWrite(Motor2A, HIGH);

  digitalWrite(Motor1A, LOW);
  digitalWrite(Motor2B, LOW);
}

//*********************************//
