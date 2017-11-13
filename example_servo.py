
#importamos la libreria de GPIO para usar los pines de la Raspi
import RPi.GPIO as GPIO
#importamos la libreria time para hacer retardos recordar que es en segundos
from time import sleep

#----------------Configuramos la raspberry, aqui esta con BCM es decir usando el numero del GPIO------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)#evito los mensajes de innecesarios warning


servo1 = 19 #servo de la puerta
servo2 = 13 #servo de la ventana #2

GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)


s1= GPIO.PWM(servo1,50)        #Ponemos el pin servo1 en modo PWM y enviamos 50 pulsos por segundo
s1.start(0)               #Enviamos un pulso del 7.5% para centrar el servo1
s2= GPIO.PWM(servo2,50)        #Ponemos el pin servo1 en modo PWM y enviamos 50 pulsos por segundo
s2.start(0) #7.5 cerrado



# Metodo que mueve los servos
def moveServomotors(servo,pulso):
    servo.ChangeDutyCycle(pulso)



statusServo1 = False
statusServo2 = False


try:
    while(True):
        if (statusServo1):
            print("Puerta Abierta")
            moveServomotors(s1, 3.2)  # abrir
        else:
            print("Puerta Cerrada")
            moveServomotors(s1, 7.5)  # cerrar

        if (statusServo2):
            print("Ventana2 Abierta")
            moveServomotors(s2, 3.2)  # abrir
        else:
            print("Ventana2 Cerrada")
            moveServomotors(s2, 7.5)  # cerrar

        sleep(1)

except KeyboardInterrupt:
    s1.stop()
    s2.stop()
    GPIO.cleanup()