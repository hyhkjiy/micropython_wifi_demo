# coding=utf-8
import json
import time

import machine
import network

from microWebSrv import MicroWebSrv
from config import ConfigFile


def wifi_connected(wifi, timeout=15):
    while not wifi.isconnected():
        if timeout <= 0:
            return False
        timeout -= 0.5
        time.sleep(0.5)
    return True


def network_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    ssid = ConfigFile.get('wifi').get('ssid')
    if ssid:
        sta_if.connect(ssid, ConfigFile.get('wifi').get('pwd'))

    if not wifi_connected(sta_if):
        ap = network.WLAN(network.AP_IF)  # create access-point interface
        ap.active(True)  # activate the interface
        ap.config(essid='micropython_ap')  # set the ESSID of the access point

        @MicroWebSrv.route('/aps', 'GET')
        def scan_ap(http_client, http_response):
            sta_if.active(True)
            ap_list = sta_if.scan()
            http_response.WriteResponseJSONOk([ap[0] for ap in ap_list])

        @MicroWebSrv.route('/connect', 'POST')
        def connect(http_client, http_response):
            params = json.loads(http_client.ReadRequestContent())
            ssid = params.get('ssid')
            if not ssid:
                http_response.WriteResponseJSONOk({
                    'Success': False,
                    'Message': 'ssid不能为空！'
                })
                return
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            sta_if.connect(ssid, params.get('pwd'))  # Connect to an AP
            if wifi_connected(sta_if):
                print('connect success!')
                wifi_config = ConfigFile.get('wifi', {})
                wifi_config['ssid'] = ssid
                wifi_config['pwd'] = params.get('pwd')
                ConfigFile.set('wifi', wifi_config)
                machine.reset()
            http_response.WriteResponseJSONOk({
                'Success': False,
                'Message': '连接失败！'
            })

        srv = MicroWebSrv(webPath='/src/templates/')
        srv.MaxWebSocketRecvLen = 256
        srv.WebSocketThreaded = False
        srv.Start()
