#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# utinfo2mqtt.py (c) 01/2020 Marco Gabriel <mail@marcogabriel.com>
#
# This is free software licensed under AGPLv3 or later license
#

from teleinfo import Parser
from teleinfo.hw_vendors import UTInfo2
from pprint import pprint
from time import time
import paho.mqtt.client as mqtt


class Linky(object):

    def __init__(self):
        self.mqttuser="mqttuser"
        self.mqttpass="mqttpass"
        self.mqtthost="mqtthost"

    def get_once(self):
        ti = Teleinfo(RpiDom())
        print ti.get_frame()

    def run(self):
        self.connect_mqtt()
        for frame in Parser(UTInfo2()):
            pprint(frame)
            for item in frame:
                pprint(item + ":" + frame[item])
                self.client.publish("linky/"+ item, frame[item])

    def connect_mqtt(self):
        self.client = mqtt.Client()
        #self.client.on_connect = self.on_connect
        self.client.username_pw_set(self.mqttuser", password=self.mqttpass)
        self.client.connect(self.mqtthost, 1883, 60)
        self.client.loop_start()

    #def on_connect(self, self.client, userdata, flags, rc):
    #    print("Connected with result code {}".format(rc))


if __name__ == '__main__':
    t = Linky()
    t.run()

