import pyrebase
# importamos la libreria de GPIO para usar los pines de la Raspi
import RPi.GPIO as GPIO
# importamos la libreria time para hacer retardos recordar que es en segundos
from time import sleep
from lcd_i2c_mod import *
from push_notification_client import FCMPushClient
import time
from datetime import datetime
import json

import os

# ----------------Configuramos la raspberry, aqui esta con BCM es decir usando el numero del GPIO------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # evito los mensajes de innecesarios warning

# ------------------------------iniciamos variables que necesitamos en el sistema---------------------------------------

config = {
    "apiKey": "AIzaSyBwmhqTzDC7QlpPRr63tazjhsBsTuner3U",
    "authDomain": "gofy-c1730.firebaseapp.com",
    "databaseURL": "https://gofy-c1730.firebaseio.com",
    "storageBucket": "gofy-c1730.appspot.com"
}

fcmPush = FCMPushClient(
    "AAAA2gZ1JVo:APA91bH8g40cMDpoXycUtw5islbcXjG3MPUZVm2QEODwCpN6A-mb-zfHWfP7ADJApsgw2QMP-bLMs6Jeq1cMapBv9-uUf4vRa5IQ4KuPqZCVX5lGUYo-5ysYySOoIvmhpkonNN4ArH7L"
    , "https://fcm.googleapis.com/fcm/send")

notification = {"", ""}

# inicializamos el sdk de Firebase
firebase = pyrebase.initialize_app(config)

# hvariable que contiene la referencia(raiz url) de la base datos en firebase
db = firebase.database()

# identificador del producto GoFY
idProduct = "-Kw24TH46pgvGBWBr8lQ"


# --------------------------metodos necesarios para el buen funcionamiento del sistema----------------------------------




# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])


# Return % of CPU used by user as a character string
def getCPUuse():
    return (str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))


# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])


# Metodo que mueve los servos
def moveServomotors(pinServo, pulso):
    servo = GPIO.PWM(pinServo, 50)  # Ponemos el pin servo1 en modo PWM y enviamos 50 pulsos por segundo
    servo.start(0)
    sleep(0.5)
    servo.ChangeDutyCycle(pulso)
    sleep(0.5)
    servo.stop()


def getTimestamp():
    return "14 de Nov 2017 - Hora: " + str(date.hour) + ":" + str(date.minute)  # +":"+str(date.second)

#http://python-para-impacientes.blogspot.com.co/2016/12/threading-programacion-con-hilos-i.html

def sendPushNotication(body, message, tokensDevices):
    dataNotification = {
        "body": body,
        "title": "☆ GoFY ☆",
        "bigContent": message,
        "summaryText": body,
        "idNotification": 80,
        "content_available": True,
        "priority": "high"}

    #registration_id = "ev4T56UkvMU:APA91bGnFXivWkg_QhO4KudC5uXD9v7K24OertgdtH57TDTH-eoIIYzHeZsTBQv1cZjccKC1zMFThS-kHQojcJYg36WTa-8qE5Lv0FmlDFv170t4HN5RIlkh4_HUsLLWo7wIuEbluBam"
    for i in range(len(tokensDevices)):
        fcmPush.send_single(tokensDevices[i], notification, dataNotification)
    print("Notificacion enviada")


def stream_handler(permissionResponse):
    jsonToPython = json.loads(permissionResponse["data"])
    print(jsonToPython['typeAccess']) # put
    #print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    #print(message["data"])


##--------------------------------------------------MAIN--------------------------------------------------------

my_stream = db.child("active-systems").child(idProduct).child("system-information").child("permissionResponse").stream(stream_handler)

try:

    # mientras el codigo se este ejecutando
    # mientras no se suspenda el codigo
    while True:
        date = datetime.now()
        # lectura del dato de firebase

        # lectura del dato <askPermission> en firebase
        permissionResponse = db.child("active-systems").child(idProduct).child("system-information").child("permissionResponse").get()

        #print(permissionResponse["idUser"])

        tokensDevices = []
        # len(tokensDevices)
        for tokenDevice in db.child("active-systems").child(idProduct).child("tokens-users").get().each():
            tokensDevices.append(tokenDevice.val())
        #sendPushNotication("Alerta","Se ha detectado un intruso en la casa",tokensDevices)
        sleep(1)
        break
except KeyboardInterrupt:
    my_stream.close()
    GPIO.cleanup()
    clear_lcd(0)
# except Exception as e:
# print(e)
