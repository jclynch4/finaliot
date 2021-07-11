import RPi.GPIO as GPIO
import time
import datetime
import sqlite3
import smtplib

con = sqlite3.connect('../db.sqlite3')
cur = con.cursor()

LIGHT_PIN = 16
previous_state = 'off'

def readSensor():

    GPIO.setmode(GPIO.BCM)
    SENSOR_PIN = 23
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    print(GPIO.input(SENSOR_PIN))
    return GPIO.input(SENSOR_PIN)

def getCurrentMode():
    cur.execute('SELECT * FROM myapp_mode')
    data = cur.fetchone()
    return data[1]

def getCurrentState():
    cur.execute('SELECT * FROM myapp_state')
    data = cur.fetchone()
    return data[1]

def setCurrentState(val):
    query = 'UPDATE myapp_state set name = "'+val+'"'
    cur.execute(query)
    con.commit()

def lightOn(PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, True)

def lightOff(PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, False)

def manualMode():
    global previous_state
    currentState = getCurrentState()
    if currentState == 'on':
        print('manual on')
        lightOn(LIGHT_PIN)
        if currentState != previous_state:
            sendemail('light turned on')
    elif currentState == 'off':
        lightOff(LIGHT_PIN)
        print('manual off')
        if currentState != previous_state:
            sendemail('light turned off')
    previous_state = currentState


def autoMode():
    global previous_state
    light_level = readSensor()
    currentState = getCurrentState()
    if light_level == 1:
        lightOn(LIGHT_PIN)
        print('auto on')
        setCurrentState('on')
        if currentState != previous_state:
            sendemail('light turned on')
    elif light_level == 0:
        lightOff(LIGHT_PIN)
        print('auto off')
        setCurrentState('off')
        if currentState != previous_state:
            sendemail('light turned off')
    print(previous_state, currentState)
    previous_state = currentState

def runController():
    currentMode = getCurrentMode()
    if currentMode == 'auto':
        autoMode()
    elif currentMode == 'manual':
        manualMode()

    return True

def sendemail(message):
    from_email = 'jacob.c.lynch@gmail.com'
    rec_list = 'jclynch4@asu.edu'
    cc_list = []
    subject = 'Hello'
    username = 'jacob.c.lynch@gmail.com'
    password = 'Itisnotthis1!'
    server = 'smtp.gmail.com:587'
	
    header = 'From: %s \n' % from_email
    header += 'To: %s \n' % ','.join(rec_list)
    header += 'CC: %s \n' % ','.join(cc_list)
    header = 'Subject: %s \n \n' % subject
    message = header+message
    server = smtplib.SMTP(server)
    server.starttls()
    server.login(username,password)
    problems = server.sendmail(from_email, rec_list, message)
    server.quit()
    time.sleep(1)

while True:
    runController()
    time.sleep(5)

