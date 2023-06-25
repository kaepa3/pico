import network
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import urequests
import ujson


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


def access(url):
    print("start!!!")
    try:
        json_data = urequests.get(url)
        print("dating!!!")
        print(type(json_data))
        print(json_data.text)

    except OSError:
        return False
    return True


if __name__ == "__main__":
    # ssid = ""
    # password = ""
    ip = connect(ssid, password)
    print(f"connect{ip}")
    url = "http://zip.cgis.biz/xml/zip.php?zn=1030000"

    for num in range(10):
        if access(url):
            break
        sleep(0.5)
