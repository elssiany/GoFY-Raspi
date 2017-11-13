
import time
from datetime import datetime
# importamos la libreria de GPIO para usar los pines de la Raspi
import RPi.GPIO as GPIO
# importamos la libreria time para hacer retardos recordar que es en segundos
from time import sleep


#----------------Configuramos la raspberry, aqui esta con BCM es decir usando el numero del GPIO------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)#evito los mensajes de innecesarios warning



pulsador1 = 17 #Boton para activar la pregunta
pulsador2 = 22 #Boton del NO
pulsador3 = 27 #Boton del SI

lecturaPulsador1 = False
lecturaPulsador2 = False
lecturaPulsador3 = False


GPIO.setup(pulsador1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#pin de lectura para el pulsador 1(Simula un boton para pedir acceso a la casa por medio de las preguntas de seguridad)
GPIO.setup(pulsador2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#pin de lectura para el pulsador 2(Boton para responder las preguntas de seguirdad SI - NO)
GPIO.setup(pulsador3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#pin de lectura para el pulsador 3(Boton para responder las preguntas de seguirdad SI - NO)


try:

    # mientras el codigo se este ejecutando
    # mientras no se suspenda el codigo
    while True:

        date = datetime.now()
        print("Time in mili...")
        print(date.timestamp() * 1000)

        lecturaPulsador1 = GPIO.input(pulsador1)
        lecturaPulsador2 = GPIO.input(pulsador2)
        lecturaPulsador3 = GPIO.input(pulsador3)

        if (lecturaPulsador1 == GPIO.HIGH):
            print("Pulsador #1")

        if (lecturaPulsador2 == GPIO.HIGH):
            print("Pulsador #2")

        if (lecturaPulsador3 == GPIO.HIGH):
            print("Pulsador #3")


        sleep(2)

except KeyboardInterrupt:
    print("excefkjjkjkgtr")