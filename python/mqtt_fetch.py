import paho.mqtt.client as mqtt
import mariadb, sys
import db


# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("EAAA/+/data",0)
    client.subscribe

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    database.write_to_db('measures', str(msg.payload))
    print(msg.topic+" "+str(msg.payload))

        



database = db.db('root', 'newpass', 'measurements', 'temperature')
#print(database.return_all())
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.43.181")
client.loop_forever()