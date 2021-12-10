#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>;

//REMEMBER TO UPDATE THESE
//BASED ON THE NETWORK WE'LL BE USING
const char* ssid = "Hackerman";
const char* password = "123456789";
const char* mqtt_server = "192.168.43.181";

//PROJECT 3 - our defines, setup of 2 sensors(DHT, LDR)
//DHT - pin 14, LDR - A0(ADC on ESP)
//variables to store
#define DHTPIN 14     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value
int LDR_Pin = A0;
int ldrValue = 0;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;


//setup_wifi function, passing ssid&password, creating WiFi connection
//if it fails, waits 0.5 secs, tries it again
//display IP address on the serial console
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//basic callback function - imported from example
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
//payload[0] = "b" && payload[1] 
}

//reconnect function - if we are not able to get connection to MQTT broker, try again
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic5");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

//Function just to get humidity, temp and light value
void getValues(){
    hum = dht.readHumidity();
    temp= dht.readTemperature();
    ldrValue = analogRead(LDR_Pin);
}

//WIFI setup + DHT, LDR setup
void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  dht.begin();
  pinMode(LDR_Pin, INPUT);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

//every 4,5 sec, send a new message
//Call and get sensor values, put them in the msg[] and publish them into a certain topic
//DHT22 has sampling rate of 0.5Hz, so grabbing information once every two seconds
  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    getValues();
//based on the MAC address, we'll publish data to one of our topics
//On serial console ex.: "Publish message: T23.4 H34.2 L491"
    if(WiFi.BSSIDstr() == "BE:FB:E4:4A:6A:10"){
      snprintf (msg, MSG_BUFFER_SIZE, "%T%.1f H%.1f L%d", temp, hum, ldrValue);
      Serial.print("Publish message: ");
      Serial.println(msg);
      client.publish("EAAA/BE:FB:E4:4A:6A:10/data", msg);
      delay(10000);
    }
    if(WiFi.BSSIDstr() == "BE:FB:E4:4B:6A:10"){
      snprintf (msg, MSG_BUFFER_SIZE, "%T%.1f H%.1f L%d", temp, hum, ldrValue);
      Serial.print("Publish message: ");
      Serial.println(msg);
      client.publish("EAAA/BE:FB:E4:4B:6A:10/data", msg);
      delay(10000);
    }
    if(WiFi.BSSIDstr() == "04:8C:9A:2E:46:77"){
      snprintf (msg, MSG_BUFFER_SIZE, "%T%.1f H%.1f L%d", temp, hum, ldrValue);
      Serial.print("Publish message: ");
      Serial.println(msg);
      client.publish("EAAA/04:8C:9A:2E:46:77/data", msg);
      delay(10000);
    }
  }
}
