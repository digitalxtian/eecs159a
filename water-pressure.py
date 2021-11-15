#!/usr/bin/env python


import time, datetime
import pigpio

intervalTime  = 15  # in seconds
triggerMin    = 50  # limit in pulse counts - adjust to detect small leaks

SMTPserver    = 'smtp.gmail.com'
waterFlow     = 0
flowGpio      = 4

text_subtype = 'plain'

pi = pigpio.pi()

pi.set_mode(flowGpio, pigpio.INPUT)
pi.set_pull_up_down(flowGpio, pigpio.PUD_DOWN)

flowCallback = pi.callback(flowGpio, pigpio.FALLING_EDGE)

old_count   = 0
triggerTime = datetime.datetime.today() - datetime.timedelta(weeks=1)  

while True:

   time.sleep(intervalTime)

   count = flowCallback.tally()
   waterFlow = count - old_count
   #print("counted {} pulses".format(waterFlow))
   yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
   if ( (waterFlow > triggerMin) & (triggerTime < yesterday) ):

   old_count = count

pi.stop()

