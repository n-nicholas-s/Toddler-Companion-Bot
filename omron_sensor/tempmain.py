
import grove_d6t
import pigpio
import time

d6t = grove_d6t.GroveD6t()
status = ("[..INITIATING SENSOR..]")

temp = 36.5 #fever temperature

while True:
        try:
                tpn, tptat = d6t.readData()
                if tpn == None:
                        continue
                
                print(tpn, status ,end = '                   \r')
                time.sleep(1.0)
                
                
                chk = len([i for i in tpn if i >= temp])
                
                if (chk > 0):
                
                    status = ("[FEVER DETECTED!]")
                    
                else:
                
                    status = ("[Normal]")
                       
                        
        except IOError:
                print("IOError")
