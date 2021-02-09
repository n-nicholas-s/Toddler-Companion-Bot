import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import os




GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
pwm=GPIO.PWM(27,50)
pwm.start(0)

msg = None
check = 0

def SetAngle(angle):
    
    duty = angle/ 18 + 2
    GPIO.output(27, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(27,False)
    pwm.ChangeDutyCycle(0)

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code: {}".format(rc))
   
def on_disconnect(client, userdata, rc):
    print("[INFO] Connection has Disconnected")
    
def on_message(client, userdate, message):
    global msg, check
    
   
    msg = str(message.payload.decode("utf-8"))
    print(msg)
    if msg == "2" and check != 1:
        SetAngle(55)
        print('Projector down')
        check = 1

    elif msg == "8" and check != 0:
        SetAngle(150)
        print('Projector up')
        check = 0
        
    elif msg == "1":
        client.publish("Toddler/info","Exiting Projection Control Mode...")
        print("Exiting Projection Control Mode...")
        time.sleep(2)
        client.publish("Toddler/info","Loading...")
        print("Loading...")
        client.disconnect()
        GPIO.cleanup()
        pwm.stop()
        os.system("python3 Main-system.py")   


        

broker = "broker.hivemq.com"

port = 1883

client = mqtt.Client(clean_session = True)

client.on_connect = on_connect

client.on_disconnect = on_disconnect

client.on_message = on_message






def run():

    client.connect(broker, port)
    print("[INFO] Connecting to broker")
    client.subscribe("Toddler/move")
    client.publish("Toddler/info","Currently in Projection Control Mode...")
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()   
    except KeyboardInterrupt:
        pwm.stop()
        client.loop_stop()
        GPIO.cleanup()

    


