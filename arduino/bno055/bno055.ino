/*  The BNO055 can output the following sensor data:

    - Absolute Orientation (Euler Vector, 100Hz)
      Three axis orientation data based on a 360° sphere
    - Absolute Orientation (Quaterion, 100Hz)
      Four point quaternion output for more accurate data manipulation
    - Angular Velocity Vector (100Hz)
      Three axis of 'rotation speed' in rad/s
    - Acceleration Vector (100Hz)
      Three axis of acceleration (gravity + linear motion) in m/s^2
    - Magnetic Field Strength Vector (20Hz)
      Three axis of magnetic field sensing in micro Tesla (uT)
    - Linear Acceleration Vector (100Hz)
      Three axis of linear acceleration data (acceleration minus gravity) in m/s^2
    - Gravity Vector (100Hz)
      Three axis of gravitational acceleration (minus any movement) in m/s^2
    - Temperature (1Hz)
      Ambient temperature in degrees celsius
 */

#include <Wire.h>
#include "Adafruit_Sensor.h"
#include "Adafruit_BNO055.h"
#include "imumaths.h"
#include <EEPROM.h>

/* This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.

   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3-5V DC
   Connect GROUND to common ground

   History
   =======
   2015/MAR/03  - First release (KTOWN)
*/

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (200)

Adafruit_BNO055 bno = Adafruit_BNO055(55);

imu::Vector<3> euler;
imu::Vector<3> accel;
imu::Vector<3> mag;
imu::Vector<3> vel(0,0,0);
imu::Vector<3> pos(0,0,0);
int8_t temp;
unsigned long timestamp;
unsigned long nextOutputTime;
uint8_t sys, cgyro, caccel, cmag = 0;


typedef union {
 float floatingPoint;
 byte binary[4];
 unsigned long ulong;
} binaryFloat;


/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  //delay(500);
}

/**************************************************************************/
/*
    Display some basic info about the sensor status
*/
/**************************************************************************/
void displaySensorStatus(void)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  //delay(500);
}

/**************************************************************************/
/*
    Display the raw calibration offset and radius data
    */
/**************************************************************************/
void displaySensorOffsets(const adafruit_bno055_offsets_t &calibData)
{
    Serial.print("Accelerometer: ");
    Serial.print(calibData.accel_offset_x); Serial.print(" ");
    Serial.print(calibData.accel_offset_y); Serial.print(" ");
    Serial.print(calibData.accel_offset_z); Serial.print(" ");

    Serial.print("\nGyro: ");
    Serial.print(calibData.gyro_offset_x); Serial.print(" ");
    Serial.print(calibData.gyro_offset_y); Serial.print(" ");
    Serial.print(calibData.gyro_offset_z); Serial.print(" ");

    Serial.print("\nMag: ");
    Serial.print(calibData.mag_offset_x); Serial.print(" ");
    Serial.print(calibData.mag_offset_y); Serial.print(" ");
    Serial.print(calibData.mag_offset_z); Serial.print(" ");

    Serial.print("\nAccel Radius: ");
    Serial.print(calibData.accel_radius);

    Serial.print("\nMag Radius: ");
    Serial.print(calibData.mag_radius);
}

/**************************************************************************/
/*
    Display sensor calibration status
    */
/**************************************************************************/
void displayCalStatus(void)
{
    /* Get the four calibration values (0..3) */
    /* Any sensor data reporting 0 should be ignored, */
    /* 3 means 'fully calibrated" */
    uint8_t system, gyro, accel, mag;
    system = gyro = accel = mag = 0;
    bno.getCalibration(&system, &gyro, &accel, &mag);

    /* The data should be ignored until the system calibration is > 0 */
    Serial.print("\t");
    if (!system)
    {
        Serial.print("! ");
    }

    /* Display the individual values */
    Serial.print("Sys:");
    Serial.print(system, DEC);
    Serial.print(" G:");
    Serial.print(gyro, DEC);
    Serial.print(" A:");
    Serial.print(accel, DEC);
    Serial.print(" M:");
    Serial.print(mag, DEC);
}

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");

    /* Initialise the sensor */
    if (!bno.begin())
    {
        /* There was a problem detecting the BNO055 ... check your connections */
        Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
        while (1);
    }

    int eeAddress = 0;
    long bnoID;
    bool foundCalib = false;

    EEPROM.get(eeAddress, bnoID);

    adafruit_bno055_offsets_t calibrationData;
    sensor_t sensor;

    /*
    *  Look for the sensor's unique ID at the beginning oF EEPROM.
    *  This isn't foolproof, but it's better than nothing.
    */
    bno.getSensor(&sensor);
    if (bnoID != sensor.sensor_id)
    {
        Serial.println("\nNo Calibration Data for this sensor exists in EEPROM");
        delay(500);
    }
    else
    {
        Serial.println("\nFound Calibration for this sensor in EEPROM.");
        eeAddress += sizeof(long);
        EEPROM.get(eeAddress, calibrationData);

        displaySensorOffsets(calibrationData);

        Serial.println("\n\nRestoring Calibration data to the BNO055...");
        bno.setSensorOffsets(calibrationData);

        Serial.println("\n\nCalibration data loaded into BNO055");
        foundCalib = true;
    }

    //delay(1000);

    /* Display some basic information on this sensor */
    displaySensorDetails();

    /* Optional: Display current status */
    displaySensorStatus();

    bno.setExtCrystalUse(true);

    sensors_event_t event;
    bno.getEvent(&event);
    if (foundCalib){
        /*Serial.println("Move sensor slightly to calibrate magnetometers");
        while (!bno.isFullyCalibrated())
        {
            bno.getEvent(&event);
            delay(BNO055_SAMPLERATE_DELAY_MS);
        }*/
    }
    else
    {
        Serial.println("Please Calibrate Sensor: ");
        while (!bno.isFullyCalibrated())
        {
            bno.getEvent(&event);

            Serial.print("X: ");
            Serial.print(event.orientation.x, 4);
            Serial.print("\tY: ");
            Serial.print(event.orientation.y, 4);
            Serial.print("\tZ: ");
            Serial.print(event.orientation.z, 4);

            /* Optional: Display calibration status */
            displayCalStatus();

            /* New line for the next sample */
            Serial.println("");

            /* Wait the specified delay before requesting new data */
            delay(BNO055_SAMPLERATE_DELAY_MS);
        }
        
        Serial.println("\nFully calibrated!");
        Serial.println("--------------------------------");
        Serial.println("Calibration Results: ");
        adafruit_bno055_offsets_t newCalib;
        bno.getSensorOffsets(newCalib);
        displaySensorOffsets(newCalib);

        Serial.println("\n\nStoring calibration data to EEPROM...");

        eeAddress = 0;
        bno.getSensor(&sensor);
        bnoID = sensor.sensor_id;

        EEPROM.put(eeAddress, bnoID);

        eeAddress += sizeof(long);
        EEPROM.put(eeAddress, newCalib);
        Serial.println("Data stored to EEPROM.");

        Serial.println("\n--------------------------------\n");        
    }    
}


void printFloat(float v){
  binaryFloat b;
  b.floatingPoint = v;  
  Serial.write(b.binary[0]);  
  Serial.write(b.binary[1]);  
  Serial.write(b.binary[2]);  
  Serial.write(b.binary[3]);  
}

void printLong(unsigned long v){
  binaryFloat b;
  b.ulong = v; 
  Serial.write(b.binary[0]);  
  Serial.write(b.binary[1]);  
  Serial.write(b.binary[2]);  
  Serial.write(b.binary[3]);  
}

void printAsBinary(){
  Serial.write(0x55);    
  Serial.write(0xAA);   
  printLong(timestamp);     
  Serial.write(temp);  
  printFloat(euler.x());  
  printFloat(euler.y());
  printFloat(euler.z());    
  printFloat(accel.x());
  printFloat(accel.y());
  printFloat(accel.z());
  printFloat(mag.x());
  printFloat(mag.y());
  printFloat(mag.z());
  printFloat(vel.x());  
  printFloat(vel.y());  
  printFloat(vel.z());  
  printFloat(pos.x());  
  printFloat(pos.y());  
  printFloat(pos.z());  
  Serial.write(sys);
  Serial.write(cgyro);
  Serial.write(caccel);
  Serial.write(cmag);
  Serial.write(0x55);    
  Serial.write(0xAA);      
}

void printAsText(){
  Serial.print("Time: ");  
  Serial.print(timestamp);
  Serial.print(F("  "));
  
  /* Display the current temperature */
  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print(" C");
  Serial.print(F("  "));
   
  /*// Quaternion data
  imu::Quaternion quat = bno.getQuat();
  Serial.print("qW: ");
  Serial.print(quat.w(), 4);
  Serial.print(" qX: ");
  Serial.print(quat.y(), 4);
  Serial.print(" qY: ");
  Serial.print(quat.x(), 4);
  Serial.print(" qZ: ");
  Serial.print(quat.z(), 4);
  Serial.print("\t\t");
  */  

  /* The processing sketch expects data as roll, pitch, heading */
  Serial.print(F("Orient: "));
  Serial.print(euler.x());
  Serial.print(F(" "));
  Serial.print(euler.y());
  Serial.print(F(" "));
  Serial.print(euler.z());
  Serial.print(F("  "));

  Serial.print(F("Acc: "));
  Serial.print(accel.x());
  Serial.print(F(" "));
  Serial.print(accel.y());
  Serial.print(F(" "));
  Serial.print(accel.z());
  Serial.print(F("  "));  

  Serial.print(F("Mag: "));
  Serial.print(mag.x());
  Serial.print(F(" "));
  Serial.print(mag.y());
  Serial.print(F(" "));
  Serial.print(mag.z());
  Serial.print(F("  "));    

  /* Also send calibration data for each sensor. */
  Serial.print(F("Calib: "));
  Serial.print(sys, DEC);
  Serial.print(F(" "));
  Serial.print(cgyro, DEC);
  Serial.print(F(" "));
  Serial.print(caccel, DEC);
  Serial.print(F(" "));
  Serial.print(cmag, DEC);

  Serial.println();  
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  /* Get a new sensor event */
  //sensors_event_t event;
  //bno.getEvent(&event);

  /* Board layout:
         +----------+
         |         *| RST   PITCH  ROLL  HEADING
     ADR |*        *| SCL
     INT |*        *| SDA     ^            /->
     PS1 |*        *| GND     |            |
     PS0 |*        *| 3VO     Y    Z-->    \-X
         |         *| VIN
         +----------+
  */

  // Possible vector values can be:
  // - VECTOR_ACCELEROMETER - m/s^2
  // - VECTOR_MAGNETOMETER  - uT
  // - VECTOR_GYROSCOPE     - rad/s
  // - VECTOR_EULER         - degrees
  // - VECTOR_LINEARACCEL   - m/s^2
  // - VECTOR_GRAVITY       - m/s^2  

  timestamp = millis();
  accel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);          
  if (abs(accel.magnitude() < 0.3)) accel = imu::Vector<3>(0,0,0);    
  
  vel = vel * 0.99 + accel;     
  //if (abs(accel.magnitude() < 0.5)) accel = imu::Vector<3>(0,0,0);    
  //vel = vel + accel;
  //if (abs(vel.magnitude() < 0.5)) vel = imu::Vector<3>(0,0,0);    
  pos = pos + vel;
    
  if (timestamp >= nextOutputTime){
    nextOutputTime = timestamp + BNO055_SAMPLERATE_DELAY_MS;
    euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);    
    mag = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);    
    temp = bno.getTemp();  
    bno.getCalibration(&sys, &cgyro, &caccel, &cmag);  

    printAsBinary();
    //printAsText();
  }
  
  //delay(BNO055_SAMPLERATE_DELAY_MS);
}


