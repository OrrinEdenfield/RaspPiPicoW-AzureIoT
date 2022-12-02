# RaspPiPicoW-AzureIoT

Example MicroPython code to be added.

### Note: Please do read through the excellent article by Pete Gallagher, [Connecting a Raspberry Pi Pico W to Microsoft Azure IoT Hub using MicroPython and MQTT](https://www.petecodes.co.uk/connecting-a-raspberry-pi-pico-w-to-microsoft-azure-iot-hub-using-micropython-and-mqtt/). Some topics covered there include setting up the Azure IoT Hub, Device, creation of the SAS token, and the certificate used for authentication. I've made some modifications/additions to Pete's code to suit my needs.

Additional resources I found useful:
  - [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
  - [MicroPython documentation](https://docs.micropython.org/en/latest/index.html)
  - [Temperature Gauge documentation at AdaFruit](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/temperature-gauge)


Overview of what this code does:
  - Uses Pico W's built-in capabilities:  WiFi & temperature sensor
  - Takes temperature reading
  - Sends MQTT message with temperature reading to Azure IoT Hub

Steps in the process:
  1. Connects to Wifi.
  1. Installs UMQTT library in MicroPython.
  1. Reads temperature from onboard sensor in the CPU.
  1. Calculates the temperature in Celsius.
  1. Sends the temperature in a message to Azure IoT Hub.
  1. Waits 5 seconds before getting another temperature reading and sending to IoT Hub.

Thank you.