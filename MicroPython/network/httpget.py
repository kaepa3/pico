import network
from time import sleep
from picozero import pico_temp_sensor, pico_led
import urequests
import env


#
# Wi-Fiに接続する関数です
#
class Network:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def Connect(self):
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        while not wlan.isconnected():
            print("Waiting for connection...")
            sleep(1)
        ip = wlan.ifconfig()[0]
        return ip

    def Access(self, url):
        print("start!!!")
        try:
            return True, urequests.get(url)
        except OSError:
            return False, ""


if __name__ == "__main__":
    nw = Network(env.Ssid, env.Password)
    ip = nw.Connect()
    print(f"connect{ip}")
    url = "http://zip.cgis.biz/xml/zip.php?zn=1030000"

    for num in range(10):
        rst = nw.Access(url)
        if rst[0]:
            print(rst[1].text)
            break

        sleep(0.5)
