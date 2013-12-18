#!/bin/bash

BHOST=mc.aibang.com

# 1

BPATH=/aiguang/platform.c?m=version

# 2

BPATH=/aiguang/bus.c?p=1&pn=1&city=%E5%8C%97%E4%BA%AC&m=getNews

# 3

#BPATH=/aiguang/bus.c?m=getOfflineDataVersion

# 4

BPATH=/aiguang/platform.c?m=active

# 5

BPATH=/aiguang/bus.c?m=getOfflineData

#

h1="IMEI: e24be69b393325479882447e47ab3229cd74ca6b"
h2="RESOLUTION: {640, 960}"
h3="Connection: keep-alive"
h4="SOURCE: 1"
h5="CUSTOM: aibang"
h6="ROM: 7.0.3"
h7="IMEI: e24be69b393325479882447e47ab3229cd74ca6b"
h8="RESOLUTION: {640, 960}"
h9="Connection: keep-alive"
h10="SOURCE: 1"
h11="CUSTOM: aibang"
h12="ROM: 7.0.3"
h13="OS: iPhone OS"
#h14="Accept-Encoding: gzip"
h14="Accept-Encoding: "
h15="Accept: */*"
h16="Accept-Language: zh-cn"
h17="VERSIONID: 3"
h18="User-Agent: RealTimeBus/1.0.3 CFNetwork/672.0.8 Darwin/14.0.0"
h19="CID: e24be69b393325479882447e47ab3229cd74ca6b35d2874"
h20="MODEL: iPhone"
h21="CONTENTTYPE: json"
h22="PLATFORM: iphone"
h23="PRODUCTID: 5"
h24="IMSI: "
h25="MANUFACTURER: Apple.Inc"

curl "$BHOST$BPATH" \
-H "$h1" \
-H "$h2" \
-H "$h3" \
-H "$h4" \
-H "$h5" \
-H "$h6" \
-H "$h7" \
-H "$h8" \
-H "$h9" \
-H "$h11" \
-H "$h12" \
-H "$h13" \
-H "$h14" \
-H "$h15" \
-H "$h16" \
-H "$h17" \
-H "$h18" \
-H "$h19" \
-H "$h20" \
-H "$h21" \
-H "$h22" \
-H "$h23" \
-H "$h24" \
-H "$h25" \
#-o platform.gz
