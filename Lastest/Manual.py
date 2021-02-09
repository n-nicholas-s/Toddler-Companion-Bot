import paho.mqtt.client as mqtt
import os
import time
import Sensor

prev = 0
x = 0

def motorMovement (movement): 
    global prev
    
    if prev == movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(1))
    elif prev != movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(0))

    prev = movement

def on_message(client, userdata, message):
    global x
    client.publish("Toddler/info","Currently in Manual Mode...")
    print("received message: ", str(message.payload.decode("utf-8")))
    x = int(message.payload.decode("utf-8"))
    motorMovement(x)
    
def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code: {}".format(rc))
   
def on_disconnect(client, userdata, rc):
   print("[INFO] Connection has Disconnected")
    

broker = "broker.hivemq.com"

client = mqtt.Client(clean_session=True)

client.connect(broker, 1883)
print("[INFO] Connecting to broker")

client.on_connect = on_connect

client.on_disconnect = on_disconnect

client.on_message = on_message

client.subscribe("Toddler/move")

client.publish("Toddler/info","Currently in Manual Mode...")

client.loop_start()










def main():
    global x

    while x != 1:
            sensor1, sensor2, sensor3, sensor4, ax, ay, az, o= Sensor.read_proximity_sensor()
            if float(ax) > 7.5 or float(ax) < -7.5 or float(ay) >7.5 or float(ay) < -7.5:
                x=0
                os.system("python3 motorplate-test.py " + str(x) + " " + str(1))
                client.publish("Toddler/info","Robot Lifted Off the Ground")
                time.sleep(2)
                client.publish("Toddler/info","Please place the Robot on the ground")
            else:
                os.system("python3 motorplate-test.py " + str(x) + " " + str(1))


if __name__ == '__main__':
    main()
    if x == True:
        client.loop_stop()
        client.publish("Toddler/info", "Exiting Manual Mode...")
        print("Exiting Manual Mode...")
        time.sleep(2)
        client.publish("Toddler/info","Loading...")
        client.disconnect()
        os.system("python3 Main-system.py") 
                 



