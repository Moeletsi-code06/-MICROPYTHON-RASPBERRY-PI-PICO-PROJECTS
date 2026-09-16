from LCD1602 import LCD          #imports LCD Library
from machine import Pin,PWM      #imports Pin library and the PWM library to emnable control of things such as LED brightness, motor speed and  servo motors.
import utime                     #imports to time libary to make use of time methods.


button1 = Pin(14,Pin.IN,Pin.PULL_DOWN)   #Assigns the GP14 pin to the first button's variable.
button2 = Pin(13,Pin.IN,Pin.PULL_DOWN)   #Assigns the GP13 pin to the second button's variable.
button3 = Pin(12,Pin.IN,Pin.PULL_DOWN)   #Assigns the GP12 pin to the third button's variable.
buzzer =  Pin(20,Pin.OUT)                #Assigns the GP20 pin to the alert buzzer
led1 = Pin(10,Pin.OUT)                   #Assigns the GP10 pin to led1(RED LED)
led2 = Pin(15,Pin.OUT)                   #Assigns the GP15 pin to led2(GREEN LED)
servo = PWM(Pin(16))                     #Assigning the GP16 pin to a variable
lcd = LCD()                              #function to allow the use of lcd methods

servo.freq(50)
 
locked = 4915 			#the locked state the servo will be in 
unlocked = 8192 		#the unlocked state the servo will be in
servo.duty_u16(locked) 	#setting the servo to always begin in the locked state


#dictionary list to store log entries
accessLog = {
            "LOG NO.": [], 		#[list for  the current logs]
            "BINARY CODE": [], 	#[list for the currently entered binary access codes]
            "USER TYPE": [], 	#[list for the current user types]
            "RESULT": [], 		#[list for the current access results]
            "ACCESS COUNT": [], #[list for the access count]
            "Time" : []   		#list for the different access times
            }

#FUNCTION DEFINITIONS FOR RETRIEVAL OF THE ACCESS CODE,DENIAL OF UNAUTHORIZED ACCESS,SERVO ACCESS INDICATOR,LOGS AND MAINTENACE INDICATOR.
def access_code():
    access = str(button1.value()) + str(button2.value()) + str(button3.value())    #Converts binary input into a string
    utime.sleep(0.1)                                                               #Provides the button states time to not create duplicate entries
    return access                                                                  #returns the complete 3-bit binary access code

def unauthorized():
    for i in range(50):
            buzzer.toggle()              #Toggles the buzzer to indicate room occupancy
            led1.toggle()				 #Toggles the LED  when motion is detected in the room
            utime.sleep(0.1)             #Time delay method to allow the green led to blink every 0.1 seconds
            
            
def authorized():
    for i in range(10):             #For loop to allow the access granted green led to go on for 1 second(10 x 0.1)
        led2.toggle()               #Green LED switches on 
        utime.sleep(0.1)            #Time delay method to allow the green led to blink every 0.1 seconds
   
def servo_access():
    servo.duty_u16(unlocked)   #Moves the servo into a unlocked state
    utime.sleep(2)             #Time delay of 2 seconds before it changes states
    servo.duty_u16(locked)     #Moves the servo into a locked state 
    
#Following function appends the formatted log entry data to the created log_book
def logging_function():                                #Appending log entries stored in the dictionary list to a text file.
    access = -1                                        #Appends the last entry made in the dictionary list of log entries
    with open("accessLogs.txt","a") as file:           #Appends to the access lof text file the formatted log entries
        file.write(f"{accessLog["LOG NO."][access]}{accessLog["BINARY CODE"][access]:>14}{accessLog['USER TYPE'][access]:>20}{accessLog["RESULT"][access]:>16}{accessLog["ACCESS COUNT"][access]:>15}{accessLog["Time"][access]:>12}\n")
    
    
def maintenance_threshold(success):                          #Maintenance alert function
    global successful_access             
    successful_access = success                                         
    threshold= 5                                            #Threshold of 5 successful entries 
    if successful_access == threshold:                      #If the number of successful entries is equal to the threshold the following executes:
        lcd.clear()                                         #Clears the lcd screen
        lcd.message("MAINTENANCE")                          #Displays Maintenance required on the LCD 
        lcd.message("\nREQUIRED")
        for i in range(30):                                 #Triggers the buzzer and led for a duration of 3 seconds
            buzzer.toggle()
            led1.toggle()
            utime.sleep(1)                                  #buzzer and led trigger for 1 second each
        

            
authorised_codes = ["101","110","010", "001"]                               #Authorised access code list
user_type = ["General Staff", "Academic Staff","Student", "Maintenance"]    #Authorized users of the system list



log_num = 0                     #log number counter intializer variable set to 0
successful_access = 0 		    #Initialized counter to track how many successful accesses.
#access_entries = 0             #Initialized counter to track how many entries in the system
appending_completed = False     #Initializes while loop blocker for logging function

while True: 
    accessC = access_code()          		 #Receives the access code from the function access_code():
    current_time = utime.localtime()         #sets the current computer time with the utime library
    standard_format= "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])    #formats the current time of the device to be in standard time format.
    access_Time = standard_format  # sets the formatted access time in the access_time variable that will be looping to display different time values.
    
    
    #.append() method is used to add log entries in the log book
    if accessC in authorised_codes:       #Condition that checks the access_code received earlier is within the authorized access code list
        result = "Granted"
        position = authorised_codes.index(accessC)
        user = user_type[position]
        successful_access += 1 #Counts how many successful accesses in each loop.
        log_num = log_num + 1      #Counter for the log number in the log entries
        accessLog["LOG NO."].append(log_num)   #appends the log entry number into the access log text file
        
        
        lcd.clear()  
        lcd.message("ACCESS GRANTED")    			#Displays access granted on the LCD screen
        accessLog["BINARY CODE"].append(accessC)
        accessLog["USER TYPE"].append(user)
        accessLog["RESULT"].append(result)
        accessLog["Time"].append(access_Time)
        access_count = accessLog["BINARY CODE"].count(accessC)    #Makes use of the .count method to count how many times the entered code is present in the dictionary list storing binary access codes
        if access_count >= 1:                                     #Evaluates if the count is 1 or greater than 1 and appends the current count 
            accessLog["ACCESS COUNT"].append(access_count)      
        else:                                                     #If the current count is 0 it appends 1
            accessLog["ACCESS COUNT"].append(1)
        appending_completed = True					#acknowlegeds the appending of access log data is true
        if appending_completed == True:				#condition set to keep the logging function from iterating duplicate entries
            logging_function()  					#Calls the function that logs the access entry data
        authorized()    							#Calls the authorized function to display the access was granted on the hardware.
        servo_access()
        maintenance_threshold(successful_access)   	#Function to check if maintenance threshold is reached
        
    #The code "111" is an unauthorized access code therefore the function unauthorized() will be called to display access denied on the hardware.           
    elif accessC == "111":
        #access_entries +=1
        lcd.clear()
        log_num = log_num + 1      #Counter for the log number in the log entries
        accessLog["LOG NO."].append(log_num)   #appends the log entry number
        lcd.message("ACCESS DENIED")
        accessLog["BINARY CODE"].append(accessC)
        accessLog["USER TYPE"].append("UNAUTHORIZED USER")
        accessLog["RESULT"].append("DENIED")
        accessLog["Time"].append(access_Time)
        accessLog["ACCESS COUNT"].append(1)
        appending_completed = True              #acknowledges the appending of access log data is true
        if appending_completed == True:
            logging_function()  				#Calls the function that logs the access entry data
        unauthorized()  						#Calls the unauthorized access function.
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        