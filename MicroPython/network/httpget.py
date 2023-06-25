import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine


#
# Wi-Fiに接続する関数です
#


def connect(ssid, password):
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    return ip


if __name__ == "__main__":
    ssid = "ssid"
    password = "pass"
    ip = connect(ssid, password)
    print("connect{ip}")
