import RPi.GPIO as GPIO
import serial
import time

#Assigning pin numbers to LEDs
LED_PIN_1 = 1
LED_PIN_2 = 17

#Assigning Pin numbers to sonar sensors
Sonar_TRIG1 = 16
Sonar_ECHO1 = 18

# Raspberry Pi setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
GPIO.setup(Sonar_TRIG1, GPIO.OUT)
GPIO.setup(Sonar_ECHO1, GPIO.IN)
GPIO.output(Sonar_TRIG1, False)

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK  = 16
MISO = 20
MOSI = 26
CS   = 21
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

class DataUsage:
    #function to read Voltage from the LEDs
    def read_voltage():
        adc_value = mcp.read_adc(0)
        voltage = (adc_value / 1023.0) * 3.3
        return voltage
    
    #Function to read Current from the LEDs
    def read_current(mcp, voltage, channel=0):
        adc_value = mcp.read_adc(channel)
        V_out = (adc_value / 1023.0) * 5.0
        sensitivity = 100.0e-3
        current = (V_out - 2.5) / sensitivity
        current = current / 100
        return current

    #functions to turn LEDs On and off
    def turn_on_led():
        GPIO.output(12, GPIO.HIGH)
        
    def turn_off_led():
        print("hi")
        GPIO.output(12, GPIO.LOW)

    #Checking if a person is in a room or not
    def is_object_in_front(Sonar_TRIG1):
        time.sleep(2)
        GPIO.output(Sonar_TRIG1, True)
        pulse_start = time.time()
        time.sleep(0.00001)
        GPIO.output(Sonar_TRIG1, False)
        pulse_end = time.time()
        
        pulse_start = 0
        pulse_end = 0
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150 / 2
        distance = round(distance, 2)
        
        return distance

#main function
#storing data in variables and printing to screen

while True:
    voltage_1 = DataUsage.read_voltage()
    print("Voltage: ", voltage_1)

    current_1 = DataUsage.read_current(mcp, voltage_1)
    print("Current: ", current_1)
    
    resistance_1 = voltage_1 / current_1
    print("resistance: ", resistance_1)

    wattage_1 = voltage_1 * current_1
    print("wattage: ", wattage_1)
    
    distance = DataUsage.is_object_in_front(Sonar_TRIG1)
    print("total distance is", distance, "cm.")
    
    if distance > 200:
        DataUsage.turn_on_led()
    else:
        DataUsage.turn_off_led()
    
    
    
