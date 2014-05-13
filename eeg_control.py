#-------------------------------------------------------------------------------
# Name:        eeg_control
# Purpose:     Controls a robotic arm by detecting blinks and attention levels
#              by using the Neurosky MindWave EEG headband.
# Author:      Jacob Stein
# Created:     7/30/2013
# Copyright:   (c) Jacob 2013
#-------------------------------------------------------------------------------

#TODO: make a way so instead of detecting when it first hits 150 or -150, ir waits until it reaches the peak by waiting until it starts going down/up.

from NeuroPy import NeuroPy
import time
import serial
#import sys
#import pygame
#from pygame.locals import *

object1=NeuroPy("COM4") #If port not given 57600 is automatically assumed
#Serial = serial.Serial(2,9600) #On port 4 at 9600 baud
#Serial.close()

'''def attention_callback(attention_value):
    "this function will be called everytime NeuroPy has a new value for attention"
    print "Value of attention is",attention_value
    #do other stuff (fire a rocket), based on the obtained value of attention_value
    #do some more stuff
    return None'''

#set call back:
#object1.setCallBack("attention",attention_callback)


#call start method
#values = []
#average = 0
object1.start() #initializes the MindWave headset
start_time = 0
i = 0
blinked = False
last_blink_time = 0
double_blink = False
triple_blink = False
quadruple_blink = False
quintuple_blink = False
degrees = False
shouldMove = 1
code_message_sent = False
servos = ['BASE','BOTTOM BARS','MIDDLE BARS','TOP BARS','GRIPPER']
current_servo = 0
code = [] #the binary code that will be determined based on single and double blinks

#pygame setup:
'''pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 500,500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font('arial.ttf',50)'''

try:
    while True:
        '''for event in pygame.event.get(): #pygame event loop checks for things like mouse clicks
            if event.type == QUIT:
                pygame.quit()
                sys.exit()'''
        value = object1.rawValue #gets the raw brain activity level
       # print value
        if value > 100: #if the raw level gets above 200, which indicates a spike, start the clock
            start_time = time.clock()
        if start_time:
            if value <  -100: #if the spike in brain activity is over
                total_time = time.clock() - start_time #how long the spike was
                start_time = 0
                if 0.010 < total_time < 0.05: #if the spike was a certain length
                    print "BLINKED: %i. %fms, %i"%(i,total_time,value)
                    if last_blink_time and time.clock() - last_blink_time < .4: #if the blink occured right after the previous blink
                        #print "double blink"
                        if quadruple_blink:
                            quintuple_blink = True
                        elif triple_blink:
                            quadruple_blink = True
                        elif double_blink:
                            triple_blink = True
                        else:
                            double_blink = True
                    last_blink_time = time.clock() #reset the clock
                    #if double_blink and time.clock() - last_blink_time > 0.001:
                        #triple_blink = True
                    i+=1
                    blinked = True
        if blinked and time.clock()-last_blink_time > .41: #if a certain amount of time has passed since the last blink
            if quintuple_blink:
                code = []
                print "Code erased     | %s  |Code: %s"%(servos[current_servo],''.join(code))
            elif quadruple_blink:
                code = []
                current_servo = (current_servo-1) % 5
                print "Quadruple Blink | %s  |Code: %s"%(servos[current_servo],''.join(code))

            elif triple_blink:
                code = []
                current_servo = (current_servo+1) % 5
                print "Triple Blink    | %s  |Code: %s"%(servos[current_servo],''.join(code))

            elif double_blink:
                if len(code) < 8:
                    code.append('1')
                print "Double Blink    | %s  |Code: %s"%(servos[current_servo],''.join(code))

            else:
                if len(code) < 8:
                    code.append('0')
                print "Single Blink    | %s  |Code: %s"%(servos[current_servo],''.join(code))
            if blinked and len(code) == 8:
                print int(''.join(code),base=2)
                #Serial.write('%i,%i,%i'%(current_servo,int(''.join(code),base=2),shouldMove))
            double_blink = blinked = triple_blink= quadruple_blink = quintuple_blink = False
        if object1.attention > 50 and shouldMove == False and len(code) == 8:
            shouldMove = 1
            #Serial.write('%i,%i,%i'%(current_servo,int(''.join(code),base=2),1))
            print 'HDJGHJKGF'
        if object1.attention <= 50 and shouldMove == True and len(code) == 8:
            shouldMove = 0
            #Serial.write('%i,%i,%i'%(current_servo,int(''.join(code),base=2),shouldMove))
except:
    Serial.close()

#10110100


