from LCD1602 import LCD
from machine import Pin
import utime
import math
import _thread

roomOccu_sensor = Pin(26,Pin.IN)        #PIR SENSOR PLACED IN PIN 26
buzzer = Pin(11, Pin.OUT)				#BUZZER PLACED IN PIN 11
led1 = Pin(15,Pin.OUT)                  #LED PLACED IN PIN 15

thermistor = machine.ADC (27)
conversion_factor = 3.3 / 65535
photocell = machine.ADC(26)


def roomOccupancy_detected(pin):
    for i in range(10):             #Loops 10 times when motion is detected
        #The following line 14 tests if the motion sensor is on:
        print(roomOccu_sensor.value())
        buzzer.toggle()             #Toggles the buzzer to indicate room occupancy
        led1.toggle()				 #Toggles the LED  when motion is detected in the room
        utime.sleep(3)			     #Toggles the LED every 3 seconds
        
roomOccu_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=roomOccupancy_detected)        #Triggers the PIR Sensor to switch on when it detects motion

_thread.start_new_thread(roomOccupancy_detected, ())

lcd = LCD()

while True:
    #led1.toggle()
    #utime.sleep(3)
    v = thermistor.read_u16() * conversion_factor        #Converts to temperature readings
    light_level = photocell.read_u16()       #The light level the photoresistor monitors
    Rt = 10 * v / (3.3 - v)
    tempK = 1 / (1 / (273.15 + 25) + math.log(Rt / 10) / 3950)
    tempC = tempK - 273.15 - 40
    print("Temperature:", round(tempC, 1), "C", "Light_Level: " , light_level)      #Displays temperature and Light level readings
    utime.sleep(2)
    
    temperature = "Temp: " + '{:.2f}'.format(tempC)+ " C"
    light = "\nLight: " + str(light_level)
    lcd.message(temperature)      #Displays temperature readings on LCD
    lcd.message(light)
    utime.sleep(5)
    if roomOccu_sensor.value() == 1:
        lcd.message("\nOccupied")
    else:
        lcd.message("Unoccupied")
    lcd.clear()                  #Clear LCD screen after 2 seconds
    
