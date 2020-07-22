#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import json
import time
import sys

def noteyoudao(YNOTE_SESS: str, user: str, passwd: str):
    s = requests.Session()
    checkin_url = 'http://note.youdao.com/yws/mapi/user?method=checkin'
    cookies = {
        'YNOTE_LOGIN': 'true',
        'YNOTE_SESS': YNOTE_SESS
    }
    r = s.post(url=checkin_url, cookies=cookies, )
    if r.status_code == 200:
        info = json.loads(r.text)
        total = info['total'] / 1048576
        space = info['space'] / 1048576
        t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['time'] / 1000))
        print(user+'签到成功，本次获取'+str(space) +'M, 总共获取'+str(total)+'M, 签到时间'+str(t))
        api = "https://sc.ftqq.com/SCU97675Tac37b68944a572c1508cc24b57883f395ebb7472e5103.send"
        title = u"有道云笔记签到成功"
        content = user+'签到成功，本次获取'+str(space) +'M, 总共获取'+str(total)+'M, 签到时间'+str(t)
        data = {
            "text": title,
            "desp": content
        }
        req = requests.post(url=api, data=data)
    # cookie 登录失效，改用用户名密码登录
    else:
        login_url = 'https://note.youdao.com/login/acc/urs/verify/check?app=web&product=YNOTE&tp=ursto' \
                    'ken&cf=6&fr=1&systemName=&deviceType=&ru=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2Flo' \
                    'ginCallback.html&er=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&vc' \
                    'ode=&systemName=Windows&deviceType=WindowsPC&timestamp=1517235699501'
        parame = {
            'username': user,
            'password': passwd
        }

        r = s.post(url=login_url, data=parame, verify=False)
        x = [i.value for i in s.cookies if i.name == 'YNOTE_SESS']
        if x.__len__() == 0:
            YNOTE_SESS = "-1"
            print(user+"登录失败")
            print(r.history)
            print(s.cookies)
            return
        else:
            print(user+'登陆成功，更新YNOTE_SESS,重新签到')
            YNOTE_SESS = x[0]
            noteyoudao(YNOTE_SESS, user, passwd)
            return YNOTE_SESS

if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print("\n ------------"+now+"--------------")

    print("\n           ===有道云笔记签到===        ")
    f = open(sys.path[0] + '/data.json', 'r', encoding="utf8")
    data = json.load(f)
    f.close()

    note = data['noteyoudao']
    for index,item in enumerate(note):
        YNOTE_SESS = noteyoudao(item['YNOTE_SESS'], item['user'], item['passwd'])
        if YNOTE_SESS is not None:
            data['noteyoudao'][index]['YNOTE_SESS'] = YNOTE_SESS
            f = open(sys.path[0]+'/data.json', 'w', encoding="utf8",)
            json.dump(data, f, ensure_ascii=False)
