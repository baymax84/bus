<?php
define("ENV", "ONLINE");
define('REDIS_SERVER_ENV', '__ONLINE__');
        
$city = $_GET['city'];
$linename = $_GET['linename'];
$type = $_GET['type'];
$json = ("json" == $_GET['datatype']) ? true : false;
$stationNo = $_GET['stationNo'];
if (empty($city) || empty($linename)){
    $message = errorMsg($json);
}else {
    $data = getBusRealtimeInfo($city, $linename, $type, $stationNo);
    if ($data){
        $busNum=count($data);
        $status=200;
        $msg='success';
    }else {
        $busNum=0;
        $status=502;
        $msg='获取数据失败';
    }
    
    if ($json){
        $linename = str_replace('"', '\"', $linename);
        $message = '{"root":{'
                    .'"status":"'.$status.'",'
                    .'"message":"'.$msg.'",'
                    .'"city":"'.$city.'",'
                    .'"linename":"'.$linename.'",'
                    .'"busnum":"'.$busNum.'"';
        if ($data){
            $message .= ',"dataList":{"bus":[';
            foreach ($data as $i => $bus){
                $sname = str_replace('"', '\"', $bus['nextStation']);
                $message .= '{'
                    .'"busid":"'.$bus['busid'].'",'
                    .'"type":"'.$bus['type'].'",'
                    .'"nextStation":"'.$sname.'",'
                    .'"nextStationNo":"'.$bus['nextStationNo'].'",'
                    .'"nextStationDistince":"'.$bus['nextStationDistince'].'",'
                    .'"nextStationRunTimes":"'.$bus['nextStationRunTimes'].'",'         
                    .'"nextStationTime":"'.$bus['nextStationTime'].'",'
                    .'"stationDistince":"'.$bus['stationDistince'].'",'
                    .'"stationRunTimes":"'.$bus['stationRunTimes'].'",'
                    .'"stationTime":"'.$bus['stationTime'].'",'
                    .'"speed":"'.$bus['speed'].'",'
                    .'"extraInfo":"'.$bus['extraInfo'].'",'
                    .'"gpsupdateTime":"'.$bus['gpsupdateTime'].'",'
                    .'"lon":"'.$bus['lon'].'",'
                    .'"lat":"'.$bus['lat'].'",'
                    .'"updateTime":"'.$bus['updateTime'].'"'
                    .'}';
                
                if ($i != count($data) - 1){
                    $message .= ",";
                }
            }
            
            $message .= "]}";
        }
        
        $message .= "}}";
    }else { 
        $linename = str_replace('<', '&lt;', $linename);
        $message = "<?xml version='1.0' encoding='utf-8' ?><root>"
                    ."<status>{$status}</status>"
                    ."<message>{$msg}</message>"
                    ."<city>{$city}</city>"
                    ."<linename>{$linename}</linename>"
                    ."<busnum>{$busNum}</busnum>";
        if ($data){
            $message .= '<dataList>';
            foreach ($data as $bus){
                $sname = str_replace('<', '&lt;', $bus['nextStation']);
                $message .= '<bus>'
                    ."<busid>".$bus['busid'].'</busid>'
                    ."<type>".$bus['type'].'</type>'
                    ."<nextStation>".$sname.'</nextStation>'
                    ."<nextStationNo>".$bus['nextStationNo'].'</nextStationNo>'
                    ."<nextStationDistince>".$bus['nextStationDistince']."</nextStationDistince>"
                    ."<nextStationRunTimes>".$bus['nextStationRunTimes']."</nextStationRunTimes>"          
                    ."<nextStationTime>".$bus['nextStationTime']."</nextStationTime>"
                    ."<stationDistince>".$bus['stationDistince']."</stationDistince>"
                    ."<stationRunTimes>".$bus['stationRunTimes']."</stationRunTimes>"
                    ."<stationTime>".$bus['stationTime']."</stationTime>"
                    ."<speed>".$bus['speed']."</speed>"
                    ."<extraInfo>".$bus['extraInfo']."</extraInfo>"
                    ."<gpsupdateTime>".$bus['gpsupdateTime']."</gpsupdateTime>"
                    ."<lon>".$bus['lon']."</lon>"
                    ."<lat>".$bus['lat']."</lat>"
                    ."<updateTime>".$bus['updateTime']."</updateTime>"
                ."</bus>";
            }
            
            $message .= "</dataList>";
        }
        
        $message .= "</root>";
    }
}

if ($json){
    header('Content-Type: application/json;charset=utf-8');
}else {
    header("Content-Type: text/xml;charset=utf-8"); 
}
echo $message;
die();

function errorMsg($json = true){
    if ($json){
        return '{"root":{"status":501,"info":"请求错误，缺少必要字段"}}';
    }else {
        return "<?xml version='1.0' encoding='utf-8'?><root><status>501</status><info>请求错误，缺少必要字段</info></root>";
    }
}

function getBusRealtimeInfo($city, $linename, $linetype, $stationNo = null){
    require_once dirname(__FILE__) .'/BJGJRedisUtil.class.php';
    //$key = "JW_REALBUS_{$city}_{$linename}";
    // 取实时车辆数据
    $key = ENV."_BJJW_BUS_DISTDATA_{$city}_{$linename}_{$linetype}";
    
    $data = BJGJRedisUtil::get($key);
    if (empty($data)){
        return null;
    }
    
    //$tmp = explode("|||", $data[0]);
    $type = $linetype;//$tmp[3];
    // 站间的距离
    //$key = "JW_REALBUS_{$city}_{$line}_{$type}_DISTINCE";
    $line = preg_replace('/\((.*)$/', '', $linename);
    $key = ENV."_BJJW_BUS_STATION_DISTINCE_{$city}_{$line}_{$type}";
    $distince = BJGJRedisUtil::get($key);
    if ($distince){
        $distinceArr = explode("|||", $distince);
    }else {
        $distinceArr = false;
    }
    
    // 站间的时间
    //$key = "JW_REALBUS_{$city}_{$line}_{$type}_STATTIME";
    $key = ENV."_BJJW_BUS_STATTIME_{$city}_{$linename}_{$linetype}";
    $stattime = BJGJRedisUtil::get($key);
    if ($stattime){
        $stattimeArr = explode("|||", $stattime);
    }else {
        $stattimeArr = false;
    }
       
    if (!empty($data)){
        $newData = array();
        foreach ($data as $d){
            $tmp = explode("|||", $d);
            $arr = array(
                'busid' => $tmp[2],
                'type' => $tmp[3],
                'nextStation' => $tmp[4],
                'nextStationNo' => $tmp[5],
                'nextStationDistince' => $tmp[6],
                'nextStationRunTimes' => $tmp[7],
                'nextStationTime' => $tmp[8],
                'stationDistince' => -1,
                'stationRunTimes' => -1,
                'stationTime' => -1,
                'extraInfo' => $tmp[9],
                'gpsupdateTime' => $tmp[10],
                'lon' => $tmp[11],
                'lat' => $tmp[12],
                'updateTime' => $tmp[13]
            );

            if (-1 != $arr['nextStationDistince'] && -1 != $arr['nextStationRunTimes']){
                $speed = round($arr['nextStationDistince']/$arr['nextStationRunTimes']);
            }else {
                $speed = 0;
            }

            // 及时速度
            $arr['speed'] = round($speed*3.6, 1);

            $stationNo = intval($stationNo);
            if ($stationNo == $arr['nextStationNo']){
                $arr['stationDistince'] = $arr['nextStationDistince'];
                $arr['stationRunTimes'] = $arr['nextStationRunTimes'];
                $arr['stationTime'] = $arr['nextStationTime'];
            }else if ($stationNo > $arr['nextStationNo']){
                //$type = $arr['type'];
                //$line = preg_replace('/\((.*)$/', '', $linename);
                if (!empty($distinceArr)){
                    $alldis = 0;
                    if (-1 != $arr['nextStationDistince']){
                        $alldis += intval($arr['nextStationDistince']);
                    }

                    for ($i = $arr['nextStationNo']; $i < $stationNo; $i++){
                        $alldis += intval($distinceArr[$i]);
                    }

                    $arr['stationDistince'] = $alldis;
                    // if ($speed > 0 && $alldis > 0){
                        // $arr['stationRunTimes'] = round($alldis / $speed);
                    // }
                }
                
                if (!empty($stattimeArr)){
                    $alltime = 0;
                    if (-1 != $arr['nextStationRunTimes']){
                        $alltime += intval($arr['nextStationRunTimes']);
                    }

                    for ($i = $arr['nextStationNo']; $i < $stationNo; $i++){
                        $alltime += intval($stattimeArr[$i-1]);
                    }

                    $arr['stationRunTimes'] = $alltime;
                    $arr['stationTime'] = $arr['gpsupdateTime'] + $alltime;
                }
            }

            $newData[] = $arr;
        }

        return $newData;
    }


    return null;
}