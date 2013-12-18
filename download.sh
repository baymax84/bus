#!/bin/bash

url="http://bjgj.aibang.com:8899/bjgj.php?city=%E5%8C%97%E4%BA%AC&linename=%E8%BF%90%E9%80%9A113(%E6%9D%A5%E5%B9%BF%E8%90%A5%E5%8C%97-%E5%90%B4%E5%BA%84)&stationNo=31&datatype=json&type=0"
DATADIR="/home/chenyang/opt/bus/data"
NOW=`date +"%Y%m%d_%H%M%S"`

curl "$url" > "$DATADIR/$NOW.json"
