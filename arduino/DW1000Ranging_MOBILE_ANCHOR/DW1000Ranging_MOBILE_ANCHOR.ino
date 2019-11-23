/*This Code is for the Mobile Soldiers
 * 
 * MOBILE
 * 
 * Check the loop function of the DW1000Ranging.cpp 
 * to recieve the data
 * 
 */




#include <SPI.h> 
#include "DW1000Ranging.h"
#include "DW1000Device.h"  

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
  
volatile long count=0;
volatile uint64_t _delay_count=0;
int start_delay=0;
void setup() {
  Serial.begin(115200);
  delay(1000);
  //init the configuration
  DW1000Ranging.initCommunication(5, 10); //Reset and CS pin  
 // showDeviceInfo(); 
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  //we start the module as an anchor 
 // DW1000Ranging.startAsAnchor("01:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//ID1 
    DW1000Ranging.startAsAnchor("02:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5); //ID2
   //DW1000Ranging.startAsAnchor("04:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5); //ID3
}

void loop() { 

//    if(start_delay)
//      _delay_count++;
//
//    if(count>5)
//  {
////        DW1000Ranging.initCommunication(5, 10); //Reset and CS pin  
////        DW1000Ranging.attachNewRange(newRange);
////      // DW1000Ranging.startAsAnchor("01:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_4);//ID1 
////        DW1000Ranging.startAsAnchor("02:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_4); //ID2
////       // DW1000Ranging.startAsAnchor("04:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_4); //ID3
////        delay(200);
//        count=0;
//        start_delay=1;
//       
//
//    }
////
//    
//
//    if(_delay_count>10000000)
//    {
//        count=0;
//        _delay_count=0;
//        start_delay=0;
//        DW1000.idle();
////        DW1000Ranging.initCommunication(5, 10); //Reset and CS pin  
////        DW1000Ranging.attachNewRange(newRange);
////       //DW1000Ranging.startAsAnchor("01:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);//ID1 
////        DW1000Ranging.startAsAnchor("02:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5); //ID2
////      //  DW1000Ranging.startAsAnchor("04:00:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY,DW1000.CHANNEL_5);
////        delay(200);
//    }
//        
    DW1000Ranging.loop();
  
 
}

void newRange(){  
  Serial.print("from: "); Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  Serial.print("\t Range: "); Serial.print(DW1000Ranging.getDistantDevice()->getRange()); Serial.print(" m"); 
  Serial.print("\t RX power: "); Serial.print(DW1000Ranging.getDistantDevice()->getRXPower()); Serial.println(" dBm");

  //Now We will wait for some time so that other mobiles can be ranged with the Beacon.

  //count=count+1;
}


