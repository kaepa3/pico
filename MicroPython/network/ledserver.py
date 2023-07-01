import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import env


#
# Wi-Fiに接続する関数です
#
def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(env.Ssid, env.Password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


#
# WEBページを生成する関数です
#
def webpage(temperature, state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)


#
# クライアント(ブラウザ)からの接続に対応する関数です
#
def serve(connection):
    # Start a web server
    state = "OFF"
    pico_led.off()
    temperature = 0

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass

        if request == "/lighton?":
            pico_led.on()
            state = "ON"

        elif request == "/lightoff?":
            pico_led.off()
            state = "OFF"

        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()


#
# データをやり取りする口(ソケット)を
# 作成する関数です
#


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


#
# メインの処理部分です
#
try:
    # Wi-Fiに接続し、IPアドレスを取得します
    ip = connect()

    # IPアドレスを使って、データをやり取りするソケットを作ります
    connection = open_socket(ip)

    # ソケットを使って、クライアント(ブラウザ)からの接続を待ちます
    # (内部で無限ループ)
    serve(connection)

#
# プログラムが中断された場合は、この処理に飛び、
# デバイスをリセットします
#
except KeyboardInterrupt:
    machine.reset()
