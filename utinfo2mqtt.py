#!/usr/bin/env python2
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
from configparser import ConfigParser


class Linky(object):

    def __init__(self):
        pass

    def get_once(self):
        ti = Teleinfo(RpiDom())
        print(ti.get_frame())

    def run(self, config):
        self.config = config
        self.connect_mqtt()
        for frame in Parser(UTInfo2()):
            print(frame)
            for item in frame:
                pprint(item + ":" + frame[item])
                self.client.publish("linky/"+ item, frame[item])

    def connect_mqtt(self):
        self.client = mqtt.Client()
        #self.client.on_connect = self.on_connect
        self.client.username_pw_set(self.config["mqtt"]["mqtt_user"], password=self.config["mqtt"]["mqtt_pass"])
        self.client.connect(self.config["mqtt"]["mqtt_host"], 1883, 60)
        self.client.loop_start()

    #def on_connect(self, self.client, userdata, flags, rc):
    #    print("Connected with result code {}".format(rc))


if __name__ == '__main__':
    t = Linky()
    config = ConfigParser()
    print(config.read("utinfo2mqtt.conf"))
    t.run(config)

