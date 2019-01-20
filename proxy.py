# -*- coding: utf-8 -*-
import os, requests, uuid, json


def get_website(p_ip, p_port):
    print(p_ip)
    print(p_port)
    proxies = {
        'http': 'http://' + p_ip + ':' + str(p_port),
        'https': 'http://' + p_ip + ':' + str(p_port)
    }
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}
    suka_url = 'http://www.sukalifeindo.work/'
    response2 = requests.get(suka_url, proxies=proxies, headers=headers2)
    print(response2.status_code)

maxi = 10
base_url = 'http://pubproxy.com'
path = '/api/proxy'
params = '?limit=' + str(maxi) + '&format=json&http=true&type=http'
constructed_url = base_url + path + params

headers = {
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

request = requests.get(constructed_url, headers=headers, verify=False)
response = request.json()
#print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))

index = 0
while index < maxi:
    get_website(response['data'][index]['ip'], response['data'][index]['port'])
    index+=1

#print(response2.url)
#print(json.dumps(response2, sort_keys=True, indent=4, separators=(',', ': ')))
#print(response2.text)



