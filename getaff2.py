# -*- coding: utf-8 -*-
import os, requests, uuid, json, re
from requests.exceptions import ProxyError
from requests.exceptions import TooManyRedirects
from requests.exceptions import ReadTimeout
import proxy
from requests.exceptions import ConnectionError
from requests.exceptions import InvalidProxyURL
import getaff

def get_website(p_ip, p_port, uc_, aff_url):
    print(p_ip)
    print(p_port)
    proxies = {
        'http': 'http://' + p_ip + ':' + str(p_port),
        'https': 'http://' + p_ip + ':' + str(p_port)
    }
    suka_url = 'http://www.yaseru-com.work/'
    headers2 = {
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.13',
        'Referer': suka_url
    }

    rtn = 0
    try:
        response2 = requests.get(aff_url,
                                 proxies=proxies,
                                 headers=headers2,
                                 verify=False,
                                 timeout=(60, 60))
        m_ = False
        m_ = re.search(rb"HTTP(.*)400(.*)", response2.content[0:50])
        if m_:
            rtn = 400
            proxy.update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
        else:
            rtn = 200
            proxy.update_proxy_pool(p_ip, p_port, uc_, 1)
            proxy.insert_log(aff_url, 2000)
        print(response2.status_code)
        print(response2.content[0:100])
    except ProxyError:
        print('timeout')
        rtn = 500
        proxy.update_proxy_pool(p_ip, p_port, (uc_ - 1), 8)
    except TooManyRedirects:
        print('Too many redirects')
        rtn = 500
        proxy.update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
    except ReadTimeout:
        print('read-timeout')
        rtn = 903
        proxy.update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
    except ConnectionError:
        print('Connection Error')
        rtn = 500
        proxy.update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
    except InvalidProxyURL:
        print('Connection Error')
        rtn = 500
        # proxy.update_proxy_pool(p_ip, p_port, (uc_ - 1), 8)

    return rtn


# start code
urls_ = [
    'http://www.yaseru-com.work/',  # a8 moomoo s00000000404008'''''a5
    'http://www.yaseru-com.work/',  # a8 futon s00000014566001''''''a1
    'http://www.yaseru-com.work/',  # a8 rirakuru s00000020052001'''''a4
    'http://www.yaseru-com.work/',  # a8 lolipop s00000000404001'''''s1
    'http://www.yaseru-com.work/',  # a8 futon s00000014566001'''''a2
    'http://www.yaseru-com.work/'  # a8 lolipop s00000000404001'''''s1
]

len_ = len(urls_)

maxi = 80
index = 0
i2_ = 0
while index < maxi:
    proxy_ = proxy.get_proxy()
    z = get_website(proxy_[0], proxy_[1], proxy_[2], urls_[i2_])
    if z == 200:
        i2_ += 1
    else:
        index += 1
    if i2_ == len_:
        break
