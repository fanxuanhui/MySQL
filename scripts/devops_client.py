#!/usr/bin/env python
#coding:utf8


import json
import time 
import requests
import commands



config_file="/usr/local/scripts/devops_redis_monitor/configure_devops.json"

upload_list=[]

def json_parse(file_path):
    with open(file_path,"r") as fd:
            data = json.load(fd)
    return data

def upload(upload_list):
    data=json.dumps(upload_list)
    r = requests.post(falcon_client,data)
    return r


def alive(IP,port):
    command = "/usr/local/redis-4.0.2/src/redis-cli -h %s -p %s ping" %(IP,port)
    redis_alive = commands.getoutput(command)  
    if redis_alive == "PONG": 
        redis_alive=1
    else: 
        redis_alive=0
        
    return redis_alive

json_data = json_parse(config_file)



falcon_protocol=json_data['open-falcon']['protocol']
falcon_host=json_data['open-falcon']['host']
falcon_port=json_data['open-falcon']['port']
falcon_path=json_data['open-falcon']['path']
falcon_interval=json_data['open-falcon']['interval']
falcon_client="%s://%s:%s%s" % (falcon_protocol,falcon_host,falcon_port,falcon_path)

config_data =  json_data['database']['redis']['ports']
ip=json_data['database']['redis']['ip']
for config_line in config_data:
    port = config_line['port']
    endpoint = config_line['endpoint']
    targs = 'port=%s' % port 
    timestamp = int(time.time())
    metric = 'redis_alive_1' 
    #value = zb_value
    counterType = 'GAUGE'
    step = falcon_interval
    values = alive(ip,port)    

    upload_list.append({'endpoint':endpoint,'tags':targs,'timestamp':timestamp,'metric':metric,'value':values,'counterType':counterType,'step':step})
print(upload_list)
ret = upload(upload_list)
print(ret)


