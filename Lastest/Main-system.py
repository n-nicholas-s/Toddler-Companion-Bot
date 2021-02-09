import paho.mqtt.client as mqtt
import os
import time


msg = 0






def on_message(client, userdata, message):
    global x
    msg = str(message.payload.decode("utf-8"))
    if msg != "":
        print("received message: ", msg)
        action = str(message.payload.decode("utf-8"))
    
        if action == "a":
            mode = "Entering Manual Mode..."
            information(mode)
            os.system("python3 Manual.py")
        
        elif action == "b":
            mode = "Entering Object Tracking Mode..."
            information(mode)
#             os.system("python3 Object-tracking-test.py")
            os.system("python3 Object-tracking-test1.py")
            
        elif action == "c":
            mode = "Entering Voice Recognition Mode..."
            information(mode)
    #         os.system("python3 Voice-recognition.py")  
            
        elif action == "d":
            mode = "Entering Facial Recognition Mode..."
            information(mode)
    #         os.system("python3 Face-recognition.py")
#             os.system("python3 Facial-recognition.py")
            os.system("python3 Facial-recognition1.py")
             
        elif action == "e":
            mode = "Entering Emotion Recognition Mode..."
            information(mode)
            os.system("python3 Emotion-recognition.py")
     
        elif action == "f":
            mode = "Entering Video Projection Mode..."
            information(mode)
    #         os.system("python3 Video-projection.py ")
            os.system("python3 Projection-control.py ")
    
            
        elif action == "g":
            mode = "Entering Autonomous Mode..."
            information(mode)
    #         os.system("python3 Autonomous.py")
    
def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code: {}".format(rc))
    
   
def on_disconnect(client, userdata, rc):
    print("[INFO] Connection has Disconnected")
    


def temperature():
    status, data = temp.read_temperature()
    print(status)
    print(data)
    


def information(info):
    client.publish("Toddler/info", info)                   #Doesn't display on phone text
    print(info)
    client.disconnect()
    time.sleep(2)

      
broker = "broker.hivemq.com"
# broker = "broker.emqx.io"

port = 1883

client = mqtt.Client(clean_session=True)

client.on_connect = on_connect

client.on_disconnect = on_disconnect

client.on_message = on_message



def run():

    client.connect(broker, port)
    print("[INFO] Connecting to broker")
    client.subscribe("Toddler/action")
    client.publish("Toddler/info","Please pick the choice of Action...")
    client.publish("Toddler/action"," ")
    client.loop_forever()
    


    

    

if __name__ == '__main__':
    run()




