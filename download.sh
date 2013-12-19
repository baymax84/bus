#!/bin/bash

CITY="%E5%8C%97%E4%BA%AC"
DATADIR="/home/chenyang/opt/bus/data"

LINENAME113="%E8%BF%90%E9%80%9A113(%E6%9D%A5%E5%B9%BF%E8%90%A5%E5%8C%97-%E5%90%B4%E5%BA%84)"
LINENAME113_2="%E8%BF%90%E9%80%9A113(%E5%90%B4%E5%BA%84-%E6%9D%A5%E5%B9%BF%E8%90%A5%E5%8C%97)"

url113="http://bjgj.aibang.com:8899/bjgj.php?city=$CITY&linename=$LINENAME113&stationNo=31&datatype=json&type=0"
url113_2="http://bjgj.aibang.com:8899/bjgj.php?city=$CITY&linename=$LINENAME113_2&stationNo=31&datatype=json&type=0"


BDATE=`date +"%Y%m%d"`
NOW=`date +"%Y%m%d_%H%M%S"`
b_output="$DATADIR/$BDATE/113/$NOW.json"

mkdir -p "$DATADIR/$BDATE/113"

curl "$url113" > "$b_output"

sleep 5

BDATE=`date +"%Y%m%d"`
NOW=`date +"%Y%m%d_%H%M%S"`
b_output="$DATADIR/$BDATE/113_2/$NOW.json"

mkdir -p "$DATADIR/$BDATE/113_2"

curl "$url113_2" > "$b_output"
