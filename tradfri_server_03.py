


# general imports
import os
import sys
import threading
import time
import uuid
import json


# Hack to allow relative import above top level package
folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(f"{folder}/.."))


#tradfri imports
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory, APIRequestProtocol
from pytradfri.device import Device
from pytradfri.error import PytradfriError
from pytradfri.resource import ApiResource
from pytradfri.util import load_json, save_json


class Tradfri_conn():

    def __init__(self, host):

        self.CONFIG_FILE    = "tradfri_standalone_psk.conf"
        self.conf           = load_json(self.CONFIG_FILE)

        self.HOST           = host
        self.IDENTITY       = self.conf[self.HOST].get("identity")
        self.PSK            = self.conf[self.HOST].get("key")

        self.api_factory    = APIFactory(host=self.HOST, psk_id=self.IDENTITY, psk=self.PSK)
        self.api            = self.api_factory.request

        self.gateway        = Gateway()

        devices_command     = self.gateway.get_devices()
        devices_commands    = self.api(devices_command)

        self.devices        = self.api(devices_commands)

        self.lights         = [dev for dev in self.devices if dev.has_light_control]




    # mehtods for lights

    def get_status(self, light_index):
        light = self.lights[light_index]
        try:
            return light.light_control.lights[0].state
        except pytradfri.error.RequestTimeout:
            return 408

    def get_dimmer_status(self, light_index):
        light = self.lights[light_index]

        try:
            return light.light_control.lights[0].dimmer
        except pytradfri.error.RequestTimeout:
            return 408

    def get_light_name(self, light_index):
        light = self.lights[light_index]

        try:
            return light.name

        except pytradfri.error.RequestTimeout:
            return 408

    # level must be between 0 and 254i
    def set_brightness(self,light_index, level):
        light = self.lights[light_index]
        dim_command = light.light_control.set_dimmer( level )

        try:
            self.api( dim_command )
            return 200

        except pytradfri.error.RequestTimeout:
            return 408


    def set_color_temp(self, light_index, hex_color):
        light = self.lights[light_index]
        color_command = light.light_control.set_color_temp(250)

        try:
           self.api( color_command )
        except pytradfri.error.RequestTimeout:
            return 408


    def set_hex_color(self, light_index, hex_color):
        light = self.lights[light_index]
        color_command = light.light_control.set_hex_color( hex_color )
        self.api( color_command )

if __name__ == '__main__':
    trad_conn = Tradfri_conn("192.168.222.104")

    i=0
    while i < len(trad_conn.lights):
        print(trad_conn.get_light_name(i))
        trad_conn.set_brightness(i, 254)
        trad_conn.set_hex_color(i, "e573455")
        i+=1

