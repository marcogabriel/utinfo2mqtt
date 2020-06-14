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
from configparser import ConfigParser
from influxdb import InfluxDBClient
import datetime
import time


class Linky(object):

    def __init__(self):
        pass

    def get_once(self):
        ti = Teleinfo(RpiDom())
        print(ti.get_frame())

    def run(self, config):
        self.config = config
        self.connect_mqtt()
        self.connect_influxdb()
        for frame in Parser(UTInfo2()):
            print(frame)
            self.send_to_influx(frame)
            for item in frame:
                #print("{}:{}".format(item, frame[item]))
                self.client.publish("linky/"+ item, frame[item])

    def import_from_file(self, config):
        self.config = config

    def connect_mqtt(self):
        self.client = mqtt.Client()
        #self.client.on_connect = self.on_connect
        self.client.username_pw_set(self.config["mqtt"]["mqtt_user"], password=self.config["mqtt"]["mqtt_pass"])
        self.client.connect(self.config["mqtt"]["mqtt_host"], 1883, 60)
        self.client.loop_start()

    def connect_influxdb(self):
        client = InfluxDBClient(
                self.config['influxdb']['host'], 
                self.config['influxdb']['port'], 
                self.config['influxdb']['username'], 
                self.config['influxdb']['password'], 
                self.config['influxdb']['database'])
        self.influx = client

    def send_to_influx(self, frame):
        # type conversion for influx
        frame['HCHC'] = float(frame['HCHC'])
        frame['HCHP'] = float(frame['HCHP'])
        frame['PAPP'] = float(frame['PAPP'])
        frame['PMAX'] = float(frame['PMAX'])
        frame['IINST1'] = float(frame['IINST1'])
        frame['IINST2'] = float(frame['IINST2'])
        frame['IINST3'] = float(frame['IINST3'])
        frame['IMAX1'] = float(frame['IMAX1'])
        frame['IMAX2'] = float(frame['IMAX2'])
        frame['IMAX3'] = float(frame['IMAX3'])
        # create timestamp for influx
        dt = datetime.datetime.now()
        timestamp = dt.isoformat("T")
        # create frame for influx
        json_body = [{
            "measurement": "linky_frame",
            "tags": {
                "powermeter": "linky_1"
            },
            "time": timestamp,
            "fields": frame
        }]
        self.influx.create_database("linky")
        self.influx.write_points(json_body)


    #def on_connect(self, self.client, userdata, flags, rc):
    #    print("Connected with result code {}".format(rc))


if __name__ == '__main__':
    t = Linky()
    config = ConfigParser()
    #print(
    config.read("utinfo2mqtt.conf")
    #)
    t.run(config)

