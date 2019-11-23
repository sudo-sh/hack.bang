/*This code is for the Beacon 
 * i.e these are the fixed reference.
 * BEACON
 * 
 * Check the setData function in DW1000.cpp file to 
 * append extra data to the MOBILE
 * 
 */
#include <SPI.h> 
#include "DW1000Ranging.h"
#include "DW1000Device.h" 


//typedef union {
// float floatingPoint;
// byte binary[4];
// unsigned long ulong;
//} binaryFloat;


//void printFloat(float v){
//  binaryFloat b;
//  b.floatingPoint = v;  
//  Serial.write(b.binary[0]);  
//  Serial.write(b.binary[1]);  
//  Serial.write(b.binary[2]);  
//  Serial.write(b.binary[3]);  
//}
//
//void printLong(unsigned long v){
//  binaryFloat b;
//  b.ulong = v; 
//  Serial.write(b.binary[0]);  
//  Serial.write(b.binary[1]);  
//  Serial.write(b.binary[2]);  
//  Serial.write(b.binary[3]);  
//}

void showDeviceInfo(){
    // DEBUG chip info and registers pretty printed
    char msg[256];
    DW1000.getPrintableDeviceIdentifier(msg);
    Serial.print("Device ID: "); Serial.println(msg);
    DW1000.getPrintableExtendedUniqueIdentifier(msg);
    Serial.print("Unique ID: "); Serial.println(msg);
    DW1000.getPrintableNetworkIdAndShortAddress(msg);
    Serial.print("Network ID & Device Address: "); Serial.println(msg);
    DW1000.getPrintableDeviceMode(msg); 
    Serial.print("Device mode: "); Serial.println(msg);
}
  
volatile int rangingFlag=0;
int set_count=1;
int _set_count=1;
void setup() {
  Serial.begin(115200);
  delay(1000);
  //init the configuration
  DW1000Ranging.initCommunication(5, 10); //Reset and CS pin  
  //showDeviceInfo(); 
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  //we start the module as a tag
 //DW1000Ranging.startAsTag("00:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//Beacon 1
//  DW1000Ranging.startAsTag("01:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//Beacon 2
 DW1000Ranging.startAsTag("02:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//Beacon 3
   
//Required Message from the Mobiles
}

void loop() { 
  if(rangingFlag==0)
  {
   //Serial.println("Stop Ranging##################################");
   
   //DO Nothing till now
  if(_set_count=1){
    //init the configuration
  //DW1000Ranging.initCommunication(5, 10); //Reset and CS pin  
  //showDeviceInfo(); 
  //define the sketch as anchor. It will be great to dynamically change the type of module
  //DW1000Ranging.attachNewRange(newRange);
  //we start the module as a tag
// DW1000Ranging.startAsTag("00:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_4);//Beacon 1
  //DW1000Ranging.startAsTag("01:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_4);//Beacon 2
 //DW1000Ranging.startAsTag("02:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_4);//Beacon 3
   //delay(200);
//Required Message from the Mobiles
  }
    //Serial.println("Idle Mode");
    DW1000.idle();
    set_count=1;
    DW1000Ranging.loop(1); 
    _set_count=0;
    
   
//Required Message from the Mobiles
  }
  if(rangingFlag==1)
  {
    _set_count=1;
    if(set_count==1){
    //Serial.println("Keep Ranging");
  //init the configuration
//  DW1000Ranging.initCommunication(5, 10); //Reset and CS pin  
  //showDeviceInfo(); 
  //define the sketch as anchor. It will be great to dynamically change the type of module
  //DW1000Ranging.attachNewRange(newRange);
  //we start the module as a tag
//  DW1000Ranging.startAsTag("00:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//Beacon 1
//  DW1000Ranging.startAsTag("01:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//Beacon 2
 //DW1000Ranging.startAsTag("02:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//Beacon 3
   //delay(200);
    }
    
    DW1000Ranging.loop(1);
    set_count=0; 
  }
}

float d1 = 0;
float d2 = 0;

void newRange(){ 
  
  float d = DW1000Ranging.getDistantDevice()->getRange();//The range obtained is in m.
  //float p = DW1000Ranging.getDistantDevice()->getRXPower();
  unsigned int a = DW1000Ranging.getDistantDevice()->getShortAddress();
  //Serial.println(a);
  if(d<0)
    d=-1*d;
  
  int range=int(d*1000);//Converts the range to cms.
  int temp_range=range;
  int temp_a=a;
  byte write_buff[11]={'-1'};
  int j=0;
  int i=0;
  int div_flag=1;
  int mul_times=4;
  for(i=0;i<5;i++)
  {
    div_flag=1;
    for(j=mul_times;j>0;j--)
    {
      div_flag=div_flag*10;
    }
    mul_times=mul_times-1;
    
    write_buff[i]=(temp_a/div_flag);
    temp_a=temp_a%div_flag;
    write_buff[5+i]=(temp_range/div_flag);
    temp_range=temp_range%div_flag;
    
    
  }
  write_buff[10]='\n';
  Serial.write(write_buff,11);

  
  //Check Whether the Buffer is assembeled Correctly.
//  Serial.println("Data");
//  for(i=0;i<10;i++)
//  {
//    Serial.print(int(write_buff[i]));Serial.print(",");
//  }
//  Serial.println();

  
  /*int idx = (a >> 8) - 49;
  if (idx == 0) d1 = d;
  if (idx == 1) d2 = d;
  Serial.print(d1);
  Serial.print("  ");
  Serial.println(d2);*/
  /*
  Serial.write(0x44);
  Serial.write(0xaa); 
  printLong(millis());
  Serial.write(a >> 8);
  Serial.write(a & 0xFF);
  printFloat(d);
  printFloat(p);  
  Serial.write(0x44);
  Serial.write(0xaa);  
  */
  
//  Serial.print("from: "); Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);  
// Serial.print("\t Range: "); Serial.print(DW1000Ranging.getDistantDevice()->getRange()); Serial.print(" m"); 
// Serial.print("\t RX power: "); Serial.print(DW1000Ranging.getDistantDevice()->getRXPower()); Serial.println(" dBm");
 /*
  * We need to create a packet here with the Mobile ID and the range we are getting.
  */
  
  
  /*dist = 0.9 * dist + 0.1 * d;
  power = 0.9* power + 0.1 * p;
  Serial.print("distance: ");
  Serial.print(dist);
  Serial.print(" m");
  Serial.print("  power: ");
  Serial.print(power);
  Serial.println(" dBm");*/
}




void serialEvent(){
  while(Serial.available())
    {
      unsigned char inChar=Serial.read();
      //Serial.println(inChar);

      if(inChar==83)//83-ASCII of S for Stop Ranging
        {
          //Stop Ranging
          rangingFlag=0;
        }

      if(inChar==82)//82-ASCII of R for Keep Ranging
        {
          //Start Ranging
          rangingFlag=1;
        }
    }
}


