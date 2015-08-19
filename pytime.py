# pytime.py
# Anthony Butler, 2015
#
import RPi.GPIO as GPIO
import time
from time import time, sleep
from datetime import datetime, timedelta

import pygame, sys, math
from pygame.locals import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# these are the GPIO pins used by the stepper motor control board
coil_A_1_pin = 17
coil_A_2_pin = 27
coil_B_1_pin = 18
coil_B_2_pin = 22
coil_C_1_pin = 23
coil_C_2_pin = 25
coil_D_1_pin = 24
coil_D_2_pin = 4

# set the GPIO pins as output using GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(coil_C_1_pin, GPIO.OUT)
GPIO.setup(coil_C_2_pin, GPIO.OUT)
GPIO.setup(coil_D_1_pin, GPIO.OUT)
GPIO.setup(coil_D_2_pin, GPIO.OUT)

# procedure to turn both motors at the same time - anticlockwise
def antiboth(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 1, 0, 1, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0, 0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 1, 0, 1, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1, 1, 0, 0, 1)
    time.sleep(delay)
    
# procedure to turn both motors at the same time - clockwise
def clockboth(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1,1,0,0,1)
    time.sleep(delay)
    setStep(0, 1, 0, 1,0,1,0,1)
    time.sleep(delay)
    setStep(0, 1, 1, 0,0,1,1,0)
    time.sleep(delay)
    setStep(1, 0, 1, 0,1,0,1,0)
    time.sleep(delay)

# procedure to turn LEFT motor only - anticlockwise
def antileft(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 1, 0,0,0,0,0)
    time.sleep(delay)
    setStep(0, 1, 1, 0,0,0,0,0)
    time.sleep(delay)
    setStep(0, 1, 0, 1,0,0,0,0)
    time.sleep(delay)
    setStep(1, 0, 0, 1,0,0,0,0)
    time.sleep(delay)

# procedure to turn LEFT motor only - clockwise
def clockleft(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1,0,0,0,0)
    time.sleep(delay)
    setStep(0, 1, 0, 1,0,0,0,0)
    time.sleep(delay)
    setStep(0, 1, 1, 0,0,0,0,0)
    time.sleep(delay)
    setStep(1, 0, 1, 0,0,0,0,0)
    time.sleep(delay)     

# procedure to turn RIGHT motor only - anticlockwise
def antirite(delay, steps):  
  for i in range(0, steps):
    setStep(0,0,0,0,1, 0, 1, 0)
    time.sleep(delay)
    setStep(0,0,0,0,0, 1, 1, 0)
    time.sleep(delay)
    setStep(0,0,0,0,0, 1, 0, 1)
    time.sleep(delay)
    setStep(0,0,0,0,1, 0, 0, 1)
    time.sleep(delay)

# procedure to turn RIGHT motor only - clockwise
def clockrite(delay, steps):  
  for i in range(0, steps):
    setStep(0,0,0,0,1, 0, 0, 1)
    time.sleep(delay)
    setStep(0,0,0,0,0, 1, 0, 1)
    time.sleep(delay)
    setStep(0,0,0,0,0, 1, 1, 0)
    time.sleep(delay)
    setStep(0,0,0,0,1, 0, 1, 0)
    time.sleep(delay)

# this procedure turns the GPIO pins on and off which activates the
# magnets in the stepper motors in the correct sequence
def setStep(w1, w2, w3, w4, w5, w6, w7, w8):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)
  GPIO.output(coil_C_1_pin, w5)
  GPIO.output(coil_C_2_pin, w6)
  GPIO.output(coil_D_1_pin, w7)
  GPIO.output(coil_D_2_pin, w8) 

# procedure to set the hands to the current system time
def sethands(ihour, imins):
  # check if the time is beyond midday
  if ihour > 12:
    ihour = ihour - 12

  fhour=float(ihour)
  fmins = float(imins)

  # reset all step variables
  hsteps = 0 # hour steps
  msteps = 0 # minute steps

  # left motor = hours
  hfrac = float((30 * fhour) / 360)
  hsteps = int(hfrac * 512)

  # right motor = minutes
  mfrac = float((6 * fmins) / 360)
  msteps = int(mfrac * 512)

  # move the hands to the time
  clockleft(int(delay) / 1000.0, int(hsteps))
  clockrite(int(delay) / 1000.0, int(msteps))
# end of sethands

# procedure to reset the hands back to 12:00 when told to exit the program
def unsethands(ihour, imins):
  if ihour > 12:
    ihour = ihour - 12

  fhour=float(ihour)
  fmins = float(imins)

  # reset all step variables
  hsteps = 0 # hour steps
  msteps = 0 # minute steps

  # left motor = hours
  hfrac = float((30 * fhour) / 360)
  hsteps = int(hfrac * 512)

  # right motor = minutes
  mfrac = float((6 * fmins) / 360)
  msteps = int(mfrac * 512)

  # move the hands to the time
  antileft(int(delay) / 1000.0, int(hsteps))
  antirite(int(delay) / 1000.0, int(msteps))
# end of unsethands

# see if the use rhas pressed a key to quit  
def processInput():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

# clean up and stop the program
def terminate():
  # return the hands to the zero positions
  print("Rewinding Time!")
  phour = str(datetime.now().strftime('%H'))
  pmins = str(datetime.now().strftime('%M'))

  jhour = int(phour)
  jmins = int(pmins)

  unsethands(jhour, jmins)
  
  pygame.quit
  sys.exit()

# delay between stepper motor activations
delay = 3
# define the pygame window size
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

#main program loop
def main():

  # create the pygame window
  global surface
  pygame.init()
  
  surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption('Raspberry Pi Time')

  get the current time from the system as hours and minutes as STRING data
  phour = str(datetime.now().strftime('%H'))
  pmins = str(datetime.now().strftime('%M'))
  # make them INTEGERS
  jhour = int(phour)
  jmins = int(pmins)
  # set the hands
  sethands(jhour, jmins)
  # wait a while
  delay = 50

  # main code loop
  while True:
    # get the time
    thour = str(datetime.now().strftime('%H'))
    tmins = str(datetime.now().strftime('%M'))

    ihour = int(thour)
    imins = int(tmins)

    # has the time changed yet?
    if (ihour != jhour) or (imins != jmins):
      sethands(ihour - jhour, imins - jmins)
      # update the stored time for the next check
      jhour = ihour
      jmins = imins

    # pause for a second
    sleep(1)
    # check if the user wants to quit
    processInput()
    
if __name__ == '__main__':
  main()
