# Pico to Azure, Pico to Azure, can you hear me?
# Orrin Edenfield

import mip
import network
import machine
import time
import utime
from machine import Pin

# Global variables
ssid = "<REDACTED-WIFI-SSID>"
password = "<REDACTED-WIFI-PASSWORD>"
led = Pin("LED", Pin.OUT)
conversion_factor = 3.3 / (65535)

# Azure variables
hostname = '<REDACTED-AZURE-IOT-HUB-NAME>.azure-devices.net'
clientid = '<REDACTED-AZURE-IOT-HUB-DEVICE-ID>'
user_name = '<REDACTED-AZURE-IOT-HUB-NAME>.azure-devices.net/<REDACTED-AZURE-IOT-HUB-DEVICE-ID>'
passw = 'SharedAccessSignature sr=<REDACTED-AZURE-IOT-HUB-DEVICE-ID>.azure-devices.net%2Fdevices%2F<REDACTED-AZURE-IOT-HUB-DEVICE-ID>&sig=<REDACTED-SAS-TOKEN>'
topic_pub = b'devices/<REDACTED-AZURE-IOT-HUB-DEVICE-ID>/messages/events/'
#topic_msg = b'{"buttonpressed":"1"}'
port_no = 0
subscribe_topic = "devices/<REDACTED-AZURE-IOT-HUB-DEVICE-ID>/messages/devicebound/#"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
 
# Install UMQTT.simple
mip.install('umqtt.simple')
from umqtt.simple import MQTTClient

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
 

# Connect to MQTT
def mqtt_connect():

    certificate_path = "baltimore.cer"
    print('Loading Baltimore Certificate')
    with open(certificate_path, 'r') as f:
        cert = f.read()
    print('Obtained Baltimore Certificate')
    sslparams = {'cert':cert}
    
    client = MQTTClient(client_id=clientid, server=hostname, port=port_no, user=user_name, password=passw, keepalive=3600, ssl=True, ssl_params=sslparams)
    client.connect()
    print('Connected to IoT Hub MQTT Broker')
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def callback_handler(topic, message_receive):
    print("Received message")
    print(message_receive)
    if message_receive.strip() == b'led_on':
        led.value(1)
    else:
        led.value(0)

try:
    client = mqtt_connect()
    client.set_callback(callback_handler)
    client.subscribe(topic=subscribe_topic)
except OSError as e:
    reconnect()

while True:
    sensor_temp = machine.ADC(4)
    reading = sensor_temp.read_u16() * conversion_factor
    tempfloat = 27 - (reading - 0.706)/0.001721
    temperature = str(tempfloat)
    topic_msg = temperature
    client.publish(topic_pub, topic_msg)
    time.sleep(5)