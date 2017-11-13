# importamos la libreria de pyrebase previamente instalada por consola
import pyrebase
# importamos la libreria de GPIO para usar los pines de la Raspi
import RPi.GPIO as GPIO
# importamos la libreria time para hacer retardos recordar que es en segundos
from time import sleep
from lcd_i2c_mod import *
import time
from datetime import datetime

import os



#----------------Configuramos la raspberry, aqui esta con BCM es decir usando el numero del GPIO------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)#evito los mensajes de innecesarios warning



#------------------------------iniciamos variables que necesitamos en el sistema---------------------------------------

config = {
  "apiKey": "AIzaSyBwmhqTzDC7QlpPRr63tazjhsBsTuner3U",
  "authDomain": "gofy-c1730.firebaseapp.com",
  "databaseURL": "https://gofy-c1730.firebaseio.com",
  "storageBucket": "gofy-c1730.appspot.com"
}
#inicializamos el sdk de Firebase
firebase = pyrebase.initialize_app(config)

#hvariable que contiene la referencia(raiz url) de la base datos en firebase
db = firebase.database()

#identificador del producto GoFY
idProduct = "-Kw24TH46pgvGBWBr8lQ"
#pines de la respberry que vamos a usar
pinIR1 = 20 #sensor ventana #1
pinIR2 = 21 #sensor ventana #2
pinIR3 = 16 #sensor de la puerta #3
pinPIR1 = 12 #sensor de la sala
pinAlarm = 10
pinLed1 = 4
servo1 = 19 #servo de la puerta
servo2 = 13 #servo de la ventana #2
servo3 = 6  #servo de la ventana #1
pulsador1 = 17 #Boton para activar la pregunta
pulsador2 = 22 #Boton del NO
pulsador3 = 27 #Boton del SI
lecturaIR1 = False
lecturaIR2 = False
lecturaIR3 = False
lecturaPIR = False
lecturaPulsador1 = False
lecturaPulsador2 = False
lecturaPulsador3 = False
isModeScan = False
showSecurityQuestions = False
actualSecurityQuestions = 1
numAnswers = 0
correctAnswers = 0
sendLicenseReport = True



##Date time formatting
dateString = '%d/%m/%Y %H:%M:%S'


#------------------------------------pines de entreda que tiene el sistema---------------------------------------------
#GPIO.setup(pulsador3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(pinIR1, GPIO.IN)#pin de lectura para el sensor IR (Para la ventana #1)
GPIO.setup(pinIR2, GPIO.IN)#pin de lectura para el sensor IR (Para la ventana #2)
GPIO.setup(pinIR3, GPIO.IN)#pin de lectura para el sensor IR (Para la puerta principal de la casa)
GPIO.setup(pinPIR1, GPIO.IN)#pin de lectura para el sensor PIR (Para detectar objectos dentro de la casa)
GPIO.setup(pulsador1, GPIO.IN)#pin de lectura para el pulsador 1(Simula un boton para pedir acceso a la casa por medio de las preguntas de seguridad)
GPIO.setup(pulsador2, GPIO.IN)#pin de lectura para el pulsador 2(Boton para responder las preguntas de seguirdad SI - NO)
GPIO.setup(pulsador3, GPIO.IN)#pin de lectura para el pulsador 3(Boton para responder las preguntas de seguirdad SI - NO)


#----------------------------------pines de salida que tiene el sistema------------------------------------------------

GPIO.setup(pinLed1, GPIO.OUT)#pin de salida para el led que indica cuando la casa esta en modo escaneo de sensores
GPIO.setup(pinAlarm, GPIO.OUT)#pin de salida para la alarma
GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)




s1= GPIO.PWM(servo1,50)        #Ponemos el pin servo1 en modo PWM y enviamos 50 pulsos por segundo
#s1.start(7.5)               #Enviamos un pulso del 7.5% para centrar el servo1
s2= GPIO.PWM(servo2,50)        #Ponemos el pin servo1 en modo PWM y enviamos 50 pulsos por segundo
#s2.start(7.5) #7.5 cerrado
lcd_init()



#--------------------------metodos necesarios para el buen funcionamiento del sistema----------------------------------




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
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))





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



# Escribe mensajes en la LCD
def writeMSMLCD(mensaje,linea):
    print("Se escribio el mensaje '"+mensaje+"' en la LCD")

    if(linea == 1):
        clear_lcd(0)
    lcd_string(mensaje, linea)


# Este metodo se encarga de escuchar a los sensores de la casa
def listenerSensor():

    messageLog = ""

    #---------------------------Sensores de la ventana---------------------
    if (lecturaIR1 == False):
        # la alarma encendida solo por 4 segundos
        db.child("active-systems").child(idProduct).child("system-information").child("alarm").set(True)
        messageLog = "El sensor #1 de la ventana detecto movimiento"
        print("Se detecto movimiento en la ventana #1")

        if (isModeScan == True):
            # se envia a firebase
            db.child("report-scan-sensors").child(idProduct).push().set("DM")
            print("Se escaneo con exito el sensor de la  ventana #1")


    if (lecturaIR2 == False):
        # la alarma encendida solo por 4 segundos
        db.child("active-systems").child(idProduct).child("system-information").child("alarm").set(True)
        messageLog = "El sensor #2 de la ventana detecto movimiento"
        print("Se detecto movimiento en la ventana #2")

        if (isModeScan == True):
            # se envia a firebase
            db.child("report-scan-sensors").child(idProduct).push().set("DM")
            print("Se escaneo con exito el sensor de la  ventana #2")


    if (lecturaIR3 == False):
        # la alarma encendida solo por 4 segundos
        db.child("active-systems").child(idProduct).child("system-information").child("alarm").set(True)
        messageLog = "El sensor #3 de la ventana detecto movimiento"
        print("Se detecto movimiento en la ventana #3")

        if (isModeScan == True):
            # se envia a firebase
            db.child("report-scan-sensors").child(idProduct).push().set("DM")
            print("Se escaneo con exito el sensor de la  ventana #3")


    # Sensores de la puesta
    if (lecturaPIR == True):
        # la alarma encendida solo por 4 segundos
        db.child("active-systems").child(idProduct).child("system-information").child("alarm").set(True)
        messageLog = "El sensor #4 de la sala, detecto movimiento"
        print("Se detecto movimiento en la sala")


    if(messageLog):
        eventLog = {"date": "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(date.day),
                    "log": messageLog}
        db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)




# Metodo que mueve los servos
def moveServomotors(servo,pulso):
    servo.ChangeDutyCycle(pulso)



##--------------------------------------------------MAIN--------------------------------------------------------


writeMSMLCD("GoFY",1)
writeMSMLCD("Seguridad",2)


try:

    # mientras el codigo se este ejecutando
    # mientras no se suspenda el codigo
    while True:
        date = datetime.now()
        if db.child("active-systems").child(idProduct).child("system-information").child("activeSystem").get().val():

            if(db.child("list-of-product-licenses").child(idProduct).get().val()):



                #Informacion del sistema

                # CPU INFO
                CPU_temp = getCPUtemperature()
                CPU_usage = getCPUuse()
                #firebase.make_put_request("/PI/CPU", "/temperature", CPU_temp)

                db.child("active-systems").child(idProduct).child("system-information").child("valueCPUTemp").set(CPU_temp)

                db.child("active-systems").child(idProduct).child("system-information").child("valueCPU").set(CPU_usage)


                # RAM INFO
                RAM_stats = getRAMinfo()
                RAM_total = round(int(RAM_stats[0]) / 1000, 1)
                RAM_used = round(int(RAM_stats[1]) / 1000, 1)
                RAM_free = round(int(RAM_stats[2]) / 1000, 1)
                #firebase.make_put_request("/PI/RAM", "/free", str(RAM_free) + "")
                #firebase.make_put_request("/PI/RAM", "/used", str(RAM_used) + "")
                #firebase.make_put_request("/PI/RAM", "/total", str(RAM_total) + "")

                db.child("active-systems").child(idProduct).child("system-information").child("valueRAM").set(RAM_used)

                # DISK INFO
                DISK_stats = getDiskSpace()
                DISK_total = DISK_stats[0]
                DISK_free = DISK_stats[1]
                DISK_perc = DISK_stats[3]
                #DISK_used = float(DISK_total[:-1]) - float(DISK_free[:-1])
                #firebase.make_put_request("/PI/DISK", "/total", str(DISK_total[:-1]))
                #firebase.make_put_request("/PI/DISK", "/free", str(DISK_free[:-1]))
                #firebase.make_put_request("/PI/DISK", "/used", str(DISK_used))
                #firebase.make_put_request("/PI/DISK", "/percentage", str(DISK_perc))
                #db.child("active-systems").child(idProduct).child("system-information").child("valueDisk").set(DISK_used)





                # lectura del dato <askPermission> en firebase
                typeAccess = db.child("active-systems").child(idProduct).child("system-information").child("permissionResponse")\
                    .child("typeAccess").get()

                response =  db.child("active-systems").child(idProduct).child("system-information").child("permissionResponse")\
                    .child("response").get().val()

                idUser = db.child("active-systems").child(idProduct).child("system-information").child(
                    "permissionResponse") \
                    .child("idUser").get().val()

                # lectura del dato en el nodo <askPermission> en firebase
                lockSystem = db.child("active-systems").child(idProduct).child("system-information").child("lockSystem").get().val()


                if(lockSystem == True):
                    writeMSMLCD('Sistema Bloqueado',1)
                else:
                    lecturaPulsador1 = GPIO.input(pulsador1)

                    if(lecturaPulsador1 == GPIO.HIGH):
                        readyAnswer1 = False
                        readyAnswer2 = False
                        readyAnswer3 = False
                        showSecurityQuestions = True
                        print("Boton #1 pulsado")
                        eventLog = {"date": "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(date.day),
                                    "log": "Se solicito permiso para ingresar a la casa por medio de las preguntas de seguridad"}
                        db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)

                    while (True):

                        print("Responde las preguntas")
                        lecturaPulsador2 = GPIO.input(pulsador2)

                        lecturaPulsador3 = GPIO.input(pulsador3)

                        writeMSMLCD('Mantener precionado', 1)
                        writeMSMLCD('el boton', 2)
                        sleep(2)

                        answer = db.child("active-systems").child(idProduct).child("list-safety-questions").child(
                            "question" + str(actualSecurityQuestions)).get().val()

                        # Escribimos en la LCD la pregunta #1
                        writeMSMLCD(answer, 1)

                        if (readyAnswer1 == False):
                            sleep(2)
                            if (lecturaPulsador2 == GPIO.HIGH):
                                correctAnswers += 1
                                actualSecurityQuestions += 1
                                readyAnswer1 = True
                            elif (lecturaPulsador3 == GPIO.HIGH):
                                actualSecurityQuestions += 1
                                readyAnswer1 = True

                        elif (readyAnswer2 == False):
                            sleep(2)
                            if (lecturaPulsador2 == GPIO.HIGH):
                                correctAnswers += 1
                                actualSecurityQuestions += 1
                                readyAnswer2 = True
                            elif (lecturaPulsador3 == GPIO.HIGH):
                                actualSecurityQuestions += 1
                                readyAnswer2 = True

                        if (readyAnswer3 == False):
                            sleep(2)
                            if (lecturaPulsador2 == GPIO.HIGH):
                                correctAnswers += 1
                                actualSecurityQuestions += 1
                                readyAnswer3 = True
                            elif (lecturaPulsador3 == GPIO.HIGH):
                                actualSecurityQuestions += 1
                                readyAnswer3 = True

                        if (readyAnswer1 and readyAnswer2 and readyAnswer3):
                            showSecurityQuestions = False
                            writeMSMLCD('El sistema', 1)
                            writeMSMLCD('esta validando...', 2)
                            sleep(1)
                            if (correctAnswers == 3):
                                eventLog = {
                                    "date": "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(
                                        date.day),
                                    "log": "Se ingreso a la casa por medio de las preguntas de seguirdad"}
                                db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)
                                writeMSMLCD('Bienvenido', 1)
                                writeMSMLCD('a tu casa', 2)
                            else:
                                # "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(date.day)
                                eventLog = {
                                    "date": "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(date.day),
                                    "log": "Se bloqueo el sistema, preguntas de seguridad incorrectas"}
                                db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)
                                writeMSMLCD('Tu sistema se bloqueo totalmente por seguridad', 1)
                                db.child("active-systems").child(idProduct).child("system-information").child(
                                    "lockSystem").set(True)
                            break
                            # permissions['typeAccess']

                    #validos los permisos que le estan pidiendo a la rasberry
                    if (typeAccess == "scan-sensors"):
                            eventLog = {"date": "Fecha:"+str(date.year)+"-"+str(date.month)+"-"+str(date.day),
                                        "log":"Se solicito permiso para hacer un escaneo del sistema"}

                            db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)

                            db.child("active-systems").child(idProduct).child("system-information").child(
                                "permissionResponse").update({'typeAccess': "n"})

                            if(isModeScan == True):
                                db.child("active-systems").child(idProduct).child("system-information").child(
                                    "modeScan").set(False)
                            else:
                                db.child("active-systems").child(idProduct).child("system-information").child(
                                    "modeScan").set(True)

                    elif(typeAccess == "access-house"):
                        writeMSMLCD("Validando acceso...",1)
                        eventLog = {"date": "Fecha:" + str(date.year) + "-" + str(date.month) + "-" + str(date.day),
                                    "log": "Se solicito permiso para entrar a la casa"}
                        db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)
                        db.child("active-systems").child(idProduct).child("system-information").child(
                            "permissionResponse").update({'typeAccess': "busy"})


                        if(db.child("active-systems").child(idProduct).child("users").child(idUser)
                                   .child("status").get().val()==0):
                            writeMSMLCD("Validando el acceso...", 1)
                            sleep(1)
                            response = {"date": "Fecha:" + str(date.year) + "-" + str(date.month) + "-" + str(date.day),
                                        "typeAccess": typeAccess,
                                        "response":"0"}
                            #db.child("active-systems").child(idProduct).child("users").child(idUser)\
                                #.child("permissionResponse").set(response)
                            writeMSMLCD("No tienes permiso", 1)
                            writeMSMLCD("de ningun tipo",2)
                            break
                        else:

                            response = {"date": "Fecha:" + str(date.year) + "-" + str(date.month) + "-" + str(date.day),
                                        "typeAccess": typeAccess,
                                        "response": "1"}
                            db.child("active-systems").child(idProduct).child("users").child(idUser) \
                                .child("permissionResponse").set(response)
                            writeMSMLCD("Ingrese",1)
                            writeMSMLCD("su código",2)
                            sleep(2)
                            codeAccess = db.child("active-systems").child(idProduct).child("users").child(
                                idUser).child("inputCode").get().val()
                            for i in range (1,20):
                                inputCode = db.child("active-systems").child(idProduct).child("users").child(idUser).child("inputCode").get().val()
                                print("Leyendo el código de acceso")
                                if(codeAccess == inputCode):
                                    db.child("active-systems").child(idProduct).child("users").child(
                                        idUser).child("inputCode").set(".")
                                    # Enviamos un pulso del 4.5% para girar los servos hacia la izquierda
                                    moveServomotors(s1,3.2)#abrir
                                    writeMSMLCD("Bienvenido",1)
                                    writeMSMLCD(db.child("active-systems").child(idProduct).child("users").child(idUser).child("name").get().val(), 2)
                                    checkIn = {"timestamp": "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(
                                        date.day),
                                                "idUser": idUser}
                                    db.child("active-systems").child(idProduct).child("users-registration").push(checkIn)
                                    break
                                sleep(1)







                # lectura del dato <alarm> en firebase
                alarm = db.child("active-systems").child(idProduct).child("system-information").child("alarm").get().val()


                if (alarm == True):
                    if(isModeScan == True):
                        # se enciende la alarma en la casa
                        GPIO.output(pinAlarm, GPIO.HIGH)
                        # la alarma encendida solo por 4 segundos
                        db.child("active-systems").child(idProduct).child("system-information").child("alarm").set(False)
                        sleep(4)
                        GPIO.output(pinAlarm,GPIO.LOW)
                    else:
                        # se enciende la alarma en la casa
                        GPIO.output(pinAlarm, GPIO.HIGH)
                else:
                    GPIO.output(pinAlarm, GPIO.LOW)


                # lectura del dato de firebase
                isModeScan = db.child("active-systems").child(idProduct).child("system-information").child("modeScan").get().val()


                #leemos la lectura digital del pi del IR(de la ventana #1)
                lecturaIR1 = GPIO.input(pinIR1)
                # leemos la lectura digital del pi del IR(de la ventana #2)
                lecturaIR2 = GPIO.input(pinIR2)
                # leemos la lectura digital del pi del IR(de la ventana #3)
                lecturaIR3 = GPIO.input(pinIR3)

                lecturaPIR = GPIO.input(pinPIR1)



                # Enviamos un pulso del 4.5% para girar los servos hacia la izquierda
                #moveServomotors(4.5)

                # Enviamos un pulso del 10.5% para girar los servos hacia la derecha
                #moveServomotors(10.5)

                # Enviamos un pulso del 7.5% para centrar los servos de nuevo
                #moveServomotors(7.5)


                #Cerrar ventana #1
                ##moveServomotors(10.5)
                ##moveServomotors(10.5)

                listenerSensor()




            else:
                writeMSMLCD('Este producto no esta licenciado',1)
                writeMSMLCD('esta licenciado', 2)
                print("Este producto no esta licenciado")
                if(sendLicenseReport):
                    sendLicenseReport = False
                    eventLog = {"date": "Fecha: " + str(date.year) + " - " + str(date.month) + " - " + str(date.day),
                                "description": "El producto con identificado con ID-->"+idProduct+
                                               " no esta licenciado o no se ha registrado todavia"}
                    db.child("active-systems").child(idProduct).child("event-logs").push(eventLog)

        else:
            writeMSMLCD('Sistema', 1)
            writeMSMLCD('Desactivado', 2)



        # es como un delay pero en segundos, es 2 segundos
        sleep(1)
except KeyboardInterrupt:
    s1.stop()
    GPIO.cleanup()
    clear_lcd(0)
#except Exception as e:
    #print(e)
