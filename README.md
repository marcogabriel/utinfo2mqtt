# utinfo2mqtt

- reads data from french smart meter Linky
- uses UTInfo2 USB Module from http://hallard.me/utinfo/
- posts metrics to influxdb and mqtt
- data can be used then by using grafana or some other mqtt-enabled smart home software
- can be used on a Raspberry Pi - systemd utinfo2mqtt.service file for systemd included

