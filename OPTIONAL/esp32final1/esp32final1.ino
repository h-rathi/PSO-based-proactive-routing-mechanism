#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>

String baseURL = "http://INSERT_IP_HERE:8081/insertTemperature"; // Placeholder for IP address

void setup() {
  Serial.begin(9600);
  WiFi.disconnect();
  delay(2000);
  Serial.print("Start Connection");
  WiFi.begin("H Rathi", "");
  while (!(WiFi.status() == WL_CONNECTED)) {
    delay(200);
    Serial.print("..");
  }
  Serial.println("connected");
 // Get the IP address of the gateway (router)
  IPAddress gatewayIP = WiFi.gatewayIP();
  String routerIP = gatewayIP.toString();
  // Replace the placeholder with the actual IP address in the base URL string
  baseURL.replace("INSERT_IP_HERE", esp32IP);

}

void loop() {

  String data = Serial.readStringUntil('\n');
  Serial.println(data);
  float voltage = data.substring(0, 4).toFloat();
  Serial.println(voltage);
  float current = data.substring(4, 9).toFloat();
  Serial.println(current);
  float power = data.substring(9, 14).toFloat();
  Serial.println(power);
  float battery_charge_level = data.substring(14).toFloat();
  Serial.println(battery_charge_level);
  sendData(voltage,current, power, battery_charge_level);
  delay(1000);
  
}

void sendData(float voltage, float current, float power, float battery_charge_level) {
  WiFiClient client;
  HTTPClient http;
  String newUrl = baseURL + "/" + String(voltage) + "/" + String(current) + "/" + String(power) + "/" + String(battery_charge_level);
  Serial.println(newUrl);
  http.begin(client, newUrl);
  int responsecode = http.GET();
  String responseData = http.getString();
  Serial.println(responseData);
  http.end();
}
