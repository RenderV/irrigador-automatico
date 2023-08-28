#define BLYNK_TEMPLATE_ID           ""
#define BLYNK_DEVICE_NAME           ""
#define BLYNK_AUTH_TOKEN            ""
#define pot 33
#define led 32
#define BLYNK_PRINT Serial

// BIBLIOTECAS
#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "";
char pass[] = "";

typedef struct Config{
  bool automatic;
  double time_limit;
  int threshold;
} Config;

typedef struct Status{
  bool dry_soil;
  bool pump_activated;
  double pinValue;
  double umidadePercentual;
  double last_activation;
} Status;

Config config = {.automatic = false, .time_limit = 2, .threshold = 20};
Status status = {.dry_soil = false, .pump_activated = false, .umidadePercentual = 100, .last_activation = 0};
BlynkTimer timer;

BLYNK_WRITE(V0)
{
  int value = param.asInt();
  Blynk.virtualWrite(V1, value);
  if(value == 0){
    value = false;
  } else {
    value = true;
  }
  config.automatic = value;

}

BLYNK_WRITE(V5) {
   String inp = param.asStr();
   Serial.println("User input:"+inp);
}

BLYNK_WRITE(V6)
{
  int value = param.asInt();
  if(value){
    Blynk.virtualWrite(V5, "[!] Sinal para ativação de bomba recebido.\n");  
    Blynk.virtualWrite(V5, ">"+bombaON()+"\n");
    Blynk.virtualWrite(V6, 0);
  }
}

BLYNK_CONNECTED()
{
  Blynk.setProperty(V3, "offImageUrl", "https://static-image.nyc3.cdn.digitaloceanspaces.com/general/fte/congratulations.png");
  Blynk.setProperty(V3, "onImageUrl",  "https://static-image.nyc3.cdn.digitaloceanspaces.com/general/fte/congratulations_pressed.png");
  Blynk.setProperty(V3, "url", "https://docs.blynk.io/en/getting-started/what-do-i-need-to-blynk/how-quickstart-device-was-made");
}

void regHumidity()
{
  Blynk.virtualWrite(V2, millis() / 1000);
  Blynk.virtualWrite(V4, status.umidadePercentual);
  if(status.umidadePercentual < config.threshold)
    status.dry_soil = true;
  else
    status.dry_soil = false;
  if(config.automatic && status.dry_soil){
    Blynk.virtualWrite(V5, "[!] Umidade é de menos que " + String(config.threshold) + ". Tentando ligar a bomba...\n");
    Blynk.virtualWrite(V5, bombaON());
  }
}

String bombaON()
{
  if(status.pump_activated){
    return ">> Bomba já está ativada.\n";
  }
  double time_diff = millis() - status.last_activation;
  if(time_diff < 1e4){
    return ">>Última ativação ocorreu em menos de 10 segundos (" + String(time_diff) + "ms)\n";
  }
  digitalWrite(led, HIGH);
  status.last_activation = millis();
  status.pump_activated = true;
  timer.setTimeout(4e3, []()->void {Blynk.virtualWrite(V5, bombaOFF());});
  return ">>Bomba ativada.\n\n";
}

String bombaOFF(){
  digitalWrite(led, LOW);
  status.pump_activated = false;
  return ">>Bomba desativada.\n";
}


void setup()
{
  Serial.begin(115200);
  pinMode(pot, INPUT);
  pinMode(led, OUTPUT);

  Blynk.begin(auth, ssid, pass);

  timer.setInterval(2000L, regHumidity);

}

void loop()
{
 
  umidadeValor = analogRead(sensor);
  umidadePercentual = map(umidadeValor, Seco, Umido, 0, 100);
  status.pinValue = analogRead(pot);
  status.umidadePercentual = map(status.pinValue, 2700, 1050, 0, 100);
  Blynk.run();
  timer.run();
}
