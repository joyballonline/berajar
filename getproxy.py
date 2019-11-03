# -*- coding: utf-8 -*-
import os, requests, uuid, json, postgresql, datetime, re

def insert_proxy(url_, sc_):
    db = postgresql.open("pq://postgres:kaoato@localhost/postgres")
    sql = "INSERT INTO public.f_proxy_pool_tab(host, port, isactive, udate, use_count) VALUES ($1, $2, $3, $4, $5) "
    sql = sql + "ON CONFLICT (host, port) DO UPDATE SET udate = $6, isactive = 0"
    ps = db.prepare(sql)
    with db.xact():
        dt_ = datetime.datetime.now()
        ps(url_, int(sc_), 0, dt_, 0, dt_)

# start code
maxi = 5
base_url = 'http://pubproxy.com'
path = '/api/proxy'
params = '?limit=' + str(maxi) + '&format=json&http=true&type=http&level=anonymous'
constructed_url = base_url + path + params

headers = {
    'Content-type': 'application/json'
}

request = requests.get(constructed_url, headers=headers, verify=False)
response = request.json()
#print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))

index = 0
while index < maxi:
    insert_proxy(response['data'][index]['ip'], response['data'][index]['port'])
    index+=1




