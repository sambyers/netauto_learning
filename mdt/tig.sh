#!/bin/bash
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
apt-get update
apt-get install telegraf influxdb
systemctl start influxdb.service
systemctl status telegraf
systemctl start influxdb.service
systemctl status influxdb.service
systemctl enable influxdb.service
systemctl enable telegraf.service
wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
apt-get update
apt-get install grafana
systemctl start grafana-server
systemctl status grafana-server
systemctl enable grafana-server.service
journalctl -f -u telegraf.service