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
    loc = msg.topic.split('/')[1]
    database.write_to_db('measurements', str(msg.payload), loc)
    #print(msg.topic+" "+str(msg.payload))

        


#Connect to the database with credentials, db name and table to use.
database = db.db('root', 'newpass', 'project3', 'measurements')
#print(database.return_all())
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.43.181")
client.loop_forever()