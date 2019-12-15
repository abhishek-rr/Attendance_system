#include <SPI.h>
#include <MFRC522.h>
#include <Ethernet.h>
//#include <Servo.h>
#define SS_PIN 5
#define RST_PIN 9
#define LDR_2 6
#define LDR_1 7
//#define LED_G 4 //define green LED pin
//#define LED_R 5 //define red LED
//#define BUZZER 2 //buzzer pin
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.
//Servo myServo; //define servo name
//int a=0;
//int b=0;
String arr="";
String CLASS_CONST="7";
static double time1,time2;
int flag=0;

// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)
char server[] = "https://attendence-system-akshay-chhajed.c9users.io";  // name address for Google (using DNS)

// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(192, 168, 31,35);
IPAddress myDns(202,177,240,252);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;

// Variables to measure the speed
unsigned long beginMicros, endMicros;
unsigned long byteCount = 0;
bool printWebData = true;  // set to false for better speed measurement

//var[0]="";
void setup()
{
 
 Serial.begin(9600); // Initiate a serial communication
    Serial.println("something random");
 SPI.begin(); // Initiate SPI bus
  pinMode(LDR_1, INPUT);
  pinMode(LDR_2, INPUT);
  Serial.println("Initialize Ethernet with DHCP:");
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
        delay(1); // do nothing, no point running without Ethernet hardware
      }
    }
    if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
    }
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip, myDns);
  } else {
    Serial.print("  DHCP assigned IP ");
    Serial.println(Ethernet.localIP());
  }
  // give the Ethernet shield a second to initialize:+
  delay(1000);
  Serial.print("connecting to ");
  Serial.print(server);
  Serial.println("...");
  
  mfrc522.PCD_Init(); // Init SPI bus
}

void loop()
{
  if(digitalRead(LDR_1))
  {int b=0;
    time1=0;
    time2=0;
   //   a=1;
      flag=0;
        Serial.println(time1);
        while(arr=="")
        {
         // Serial.println("in while before read function");
          read_rfids();
         // Serial.println(arr);
        //  Serial.println("in while after read function");
          
         }
      
      time1=millis();
      Serial.println(time1);
//      b=digitalRead(LDR_2);
      while(b==0)
      {
        b=digitalRead(LDR_2);
        time2=millis();
        if(time2-time1>=20000)
        {
          flag=1;
           Serial.println("time is out!");
          break;
        }
      }
      Serial.println();
      if(arr!="" && flag==0)
      {        //post
          String data="class="+CLASS_CONST+arr;
          Serial.println("in if block");
          String URL= "/att/temporarysave/";
          fun_post(URL,data);
          arr="";
      }
      
  }
  else if(digitalRead(LDR_2))
  {
     int b=0;
    time1=0;
    time2=0;
   //   a=1;
      flag=0;
        Serial.println(time1);
        while(arr=="")
        {
         // Serial.println("in while before read function");
          read_rfids();
         // Serial.println(arr);
        //  Serial.println("in while after read function");
          
         }
      
      time1=millis();
      Serial.println(time1);
//      b=digitalRead(LDR_1);
      while(b==0)
      {
        b=digitalRead(LDR_1);
        time2=millis();
        if(time2-time1>=20000)
        {
          flag=1;
           Serial.println("time is out!");
          break;
        }
      }
      Serial.println();
       if(arr!="" && flag==0)
      {        //post
          String data="class="+CLASS_CONST+arr;
           Serial.println("in if block");
          String URL= "/att/apply/";
          fun_post(URL,data);  
          arr="";
      }
  }
delay(2000);
}//

void read_rfids()
{
// Prepare key - all keys are set to FFFFFFFFFFFFh at chip delivery from the factory.
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;

  //some variables we need
  byte block;
  byte len;
  MFRC522::StatusCode status;

  //-------------------------------------------

  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  Serial.println(F("**Card Detected:**"));

  //-------------------------------------------

  mfrc522.PICC_DumpDetailsToSerial(&(mfrc522.uid)); //dump some details about the card
  Serial.print("UID tag :");
   String content= "";
   byte letter;
   for (byte i = 0; i < mfrc522.uid.size; i++)
   {
   Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
   Serial.print(mfrc522.uid.uidByte[i], HEX);
   content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
   content.concat(String(mfrc522.uid.uidByte[i], HEX));
   }
   
  //mfrc522.PICC_DumpToSerial(&(mfrc522.uid));      //uncomment this to see all blocks in hex

  //-------------------------------------------

  Serial.print(F("Name: "));

  byte buffer1[18];

  block = 4;
  len = 18;

  //------------------------------------------- GET FIRST NAME
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522.uid)); //line 834 of MFRC522.cpp file
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  status = mfrc522.MIFARE_Read(block, buffer1, &len);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  //PRINT FIRST NAME
  for (uint8_t i = 0; i < 16; i++)
  {
    if (buffer1[i] != 32)
    {
      Serial.write(buffer1[i]);
    }
  }

  //---------------------------------------- GET LAST NAME

  byte buffer2[18];
  block = 1;

  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 1, &key, &(mfrc522.uid)); //line 834
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  status = mfrc522.MIFARE_Read(block, buffer2, &len);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  //PRINT LAST NAME
  for (uint8_t i = 0; i < 16; i++) {
    Serial.write(buffer2[i] );
  }
  Serial.println("OHHHHHHHHHHHH");
  Serial.println(buffer2[0]);


  //----------------------------------------

  Serial.println(F("\n**End Reading**\n"));

  delay(1000); //change value if you want to read cards faster

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  // MFRC522::MIFARE_Key key;
 // for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;


  ////////////////////////////
  block = 1;
  //block reading done
   Serial.print("Message : ");
   content.toUpperCase();
   arr="&RFID='"+content+"'&FLAG="+(buffer2[0]-48);
  Serial.println(arr);
}

void fun_post(String URL, String data)
{
  

  // if you get a connection, report back via serial:
  if (client.connect(server,8080)) {
    Serial.print("connected to ");
    Serial.println(client.remoteIP());
    // Make a HTTP request:
    //data="Class=1&teacher=2&student=13";
    String post_req="POST "+URL+"  HTTP/1.1";
    client.println(post_req);
    client.println("Host: attendence-system-akshay-chhajed.c9users.io");
    client.println("Content-Type: application/x-www-form-urlencoded");
    //client.println("Connection: close");
    client.print("Content-Length: ");
    client.println(data.length());
    client.println();
    client.print(data);
    client.println();  
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
  beginMicros = micros();


   // if there are incoming bytes available
  // from the server, read them and print them:
  int len = client.available();
  if (len > 0) {
    byte buffer[80];
    if (len > 80) len = 80;
    client.read(buffer, len);
    if (printWebData) {
      Serial.write(buffer, len); // show in the serial monitor (slows some boards)
    }
    byteCount = byteCount + len;
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    endMicros = micros();
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    Serial.print("Received ");
    Serial.print(byteCount);
    Serial.print(" bytes in "); 
    float seconds = (float)(endMicros - beginMicros) / 1000000.0;
    Serial.print(seconds, 4);
    float rate = (float)byteCount / seconds / 1000.0;
    Serial.print(", rate = ");
    Serial.print(rate);
    Serial.print(" kbytes/second");
    Serial.println();
}
}
