#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import random
import string

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

url_login = 'https://www.t00ls.net/login.html'
url_checklogin = 'https://www.t00ls.net/checklogin.html'
url_signin = 'https://www.t00ls.net/ajax-sign.json'
url_querydomain = 'https://www.t00ls.net/domain.html'
url_tubilog = 'https://www.t00ls.net/members-tubilog-{0}.html'

def get_formhash(req):
    res = req.get(url=url_login, headers=headers)
    formhash_1 = re.findall('value=\"[0-9a-f]{8}\"', res.content)
    formhash = re.findall('[0-9a-f]{8}', formhash_1[0])[0]
    time.sleep(1)
    return req, formhash

def pack_header(uid):
    headers['Referer'] = 'https://www.t00ls.net/members-profile-{uid}.html'.format(uid=uid)
    return headers

def get_current_user(res, username):
    # print str(res).decode('utf-8')
    current_user = re.findall(r'<a href="members-profile-[\d+].*\.html" target="_blank">{username}</a>'.format(username=username), res)
    # print ''.join(current_user)
    cuser = re.findall(r'[\d+]{4,5}', ''.join(current_user))[0]
    print cuser
    return cuser

def login_t00ls(req, info):
    formhash = get_formhash(req)
    passwords = info['password'] if info['password_hash'] else hashlib.md5(info['password']).hexdigest()
    data = {
        'username': info['username'],
        'password': passwords,
        'questionid': info['questionid'],
        'answer': info['answer'],
        'formhash': formhash,
        'loginsubmit': '登录',
        'redirect': 'https://www.t00ls.net',
        'cookietime': '2592000'
    }

    headers['Referer'] = 'https://www.t00ls.net/'
    res = req.post(url=url_login, headers=headers, data=data)
    time.sleep(1)
    return res, formhash

def get_domain():
    length = random.randint(4,6)
    domain = ''.join(random.sample(string.lowercase, length))
    domain += '.com'
    return domain

def get_formhash_1(req, username):
    res = req.get(url=url_checklogin, headers=headers)
    uid = get_current_user(res.content, username)
    formhash = re.findall('[0-9a-f]{8}', res.content)[0]
    return formhash, uid

def check_domain(req, domain, uid):
    headers['Referer'] = url_querydomain
    res = req.get(url=url_tubilog.format(uid), headers=headers)
    if domain in res.content:
        return True
    else:
        return False

def query_domain(req, formhash, headers, uid):
    domain = get_domain()
    data = {
        'domain': domain,
        'formhash': formhash,
        'querydomainsubmit': '查询'
    }
    res = req.post(url=url_querydomain, headers=headers, data=data)
    time.sleep(1)
    if '1 TuBi<br>' not in res.content and not check_domain(req, domain, uid):
        res = query_domain(req, formhash, headers, uid)
    return domain

def signin_t00ls(req, formhash, headers):
    data = {
        'formhash': formhash,
        'signsubmit': 'apply'
    }
    res = req.post(url=url_signin, data=data, headers=headers)
    return res

def t00ls_sign():
    # questionid
    # 1 母亲的名字
    # 2 爷爷的名字
    # 3 父亲出生的城市
    # 4 您其中一位老师的名字
    # 5 您个人计算机的型号
    # 6 您最喜欢的餐馆名称
    # 7 驾驶执照的最后四位数字

    info = [
        {
            'username': 'T',  #论坛的用户名
            'password': '7ffb0e',  #论坛密码的MD5
            'password_hash': True,  #上面password明文这里写False，使用MD5就True
            'questionid': '6',   #登录的验证问题
            'answer': ''   #登录验证问题的答案
        }
    ]
    for s_info in info:
        req = requests.session()
        login_t00ls(req, s_info)
        formhash, uid = get_formhash_1(req, s_info['username'])
        headers = pack_header(uid)
        res_signin = signin_t00ls(req, formhash, headers)
        print res_signin.content
        time.sleep(1)
        res_domain = query_domain(req, formhash, headers, uid)
        print res_domain

        if res_signin.status_code == 200:
            api = "https://sc.ftqq.com/"  #server酱地址
            title = u"T00LS论坛签到成功"
            content = res_signin.content + '\r\n' + res_domain
            data = {
                "text": title,
                "desp": content,
            }
            req = requests.post(url=api, data=data)
        else:
            continue
        requests.session().close()
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

if __name__ == '__main__':
    t00ls_sign()
