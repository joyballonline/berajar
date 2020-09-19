# -*- coding: utf-8 -*-
import os, requests, uuid, json, postgresql, datetime, re
from requests.exceptions import ProxyError
from requests.exceptions import TooManyRedirects
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


def insert_log(url_, sc_):
    db = postgresql.open("pq://postgres:kaoato@localhost/postgres")
    ps = db.prepare(
        "INSERT INTO public.f_get_url_log_tab(get_datetime, url, status_code) VALUES ($1, $2, $3)"
    )
    with db.xact():
        dt_ = datetime.datetime.now()
        ps(dt_, url_, sc_)


def update_proxy_pool(p_ip, p_port, uc_, x_):
    db = postgresql.open("pq://postgres:kaoato@localhost/postgres")
    ps = db.prepare(
        "UPDATE public.f_proxy_pool_tab SET isactive = $1, udate = $2, use_count = $3 WHERE host = $4 AND port = $5"
    )
    with db.xact():
        dt_ = datetime.datetime.now()
        ps(x_, dt_, (uc_ + 1), p_ip, p_port)


def check_proxy_pool():
    db = postgresql.open("pq://postgres:kaoato@localhost/postgres")
    ps = db.prepare(
        "SELECT count(*) FROM f_proxy_pool_tab WHERE isactive IN (0,1)")
    h_ = -1
    for row in ps:
        h_ = row[0]

    if h_ == 0:
        ps = db.prepare(
            "update f_proxy_pool_tab set isactive=0 where isactive in (8,9) and use_count > $1"
        )
        with db.xact():
            ps(0)

        print("Update proxy pool!")


def get_website0(p_ip, p_port, uc_, suka_url_):
    print(p_ip)
    print(p_port)
    proxies = {
        'http': 'http://' + p_ip + ':' + str(p_port),
        'https': 'http://' + p_ip + ':' + str(p_port)
    }
    #suka_url = 'http://www.sukalifeindo.work/'
    headers2 = {
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.13',
        'Referer': suka_url_
    }
    try:
        response2 = requests.get(suka_url_,
                                 proxies=proxies,
                                 headers=headers2,
                                 timeout=(60, 60))
        m_ = False
        m_ = re.search(rb"HTTP(.*)400(.*)", response2.content[0:50])
        if m_:
            update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
            insert_log(suka_url_, 400)
        else:
            update_proxy_pool(p_ip, p_port, uc_, 1)
            insert_log(suka_url_, response2.status_code)

        print(response2.content[0:50])
    except ProxyError:
        print('proxy-err')
        update_proxy_pool(p_ip, p_port, (uc_ - 1), 8)
        insert_log(suka_url_, 901)
    except TooManyRedirects:
        print('Too many redirects')
        update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
        insert_log(suka_url_, 902)
    except ReadTimeout:
        print('read-timeout')
        update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
        insert_log(suka_url_, 903)
    except ConnectionError:
        print('conn-timeout')
        update_proxy_pool(p_ip, p_port, (uc_ - 1), 9)
        insert_log(suka_url_, 904)


def get_website(p_ip, p_port, uc_, u_):
    get_website0(p_ip, p_port, uc_, u_)


def get_proxy():
    db = postgresql.open("pq://postgres:kaoato@localhost/postgres")
    ps = db.prepare(
        "SELECT host, port, use_count FROM f_proxy_pool_tab WHERE isactive IN (0, 1) LIMIT 1"
    )
    h_ = ""
    p_ = 8080
    c_ = 0
    for row in ps:
        h_ = row[0]
        p_ = row[1]
        c_ = row[2]
    return h_, p_, c_


# start code
if __name__ == '__main__':

    check_proxy_pool()

    urls_ = [
        'https://www13.a8.net/0.gif?a8mat=3B5ADU+CL2W4Y+348+66OZ6',
        'https://www14.a8.net/0.gif?a8mat=359020+M125U+CO4+1050F5',
        'https://www18.a8.net/0.gif?a8mat=3BM9IN+E1H1DE+CO4+6B70I'
    ]
    len_ = len(urls_)
    index = 0
    maxi = 20
    while index < maxi:
        index2 = 0
        while index2 < len_:
            proxy_ = get_proxy()
            get_website(proxy_[0], proxy_[1], proxy_[2], urls_[index2])
            index2 += 1
        index += 1
