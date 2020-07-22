#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import time
import requests
import urllib3

urllib3.disable_warnings()

def wps_invite(userid):
    i = 1
    invite_sids = ["V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d",
                   "V02StVuaNcoKrZ3BuvJQ1FcFS_xnG2k00af250d4002664c02f",
                   "V02SWIvKWYijG6Rggo4m0xvDKj1m7ew00a8e26d3002508b828",
                   "V02Sr3nJ9IicoHWfeyQLiXgvrRpje6E00a240b890023270f97",
                   "V02SBsNOf4sJZNFo4jOHdgHg7-2Tn1s00a338776000b669579",
                   "V02ScVbtm2pQD49ArcgGLv360iqQFLs014c8062e000b6c37b6",
                   "V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96",
                   "V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c",
                   "V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1",
                   "V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526",
                   "V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c",
                   "V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17",
                   "V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f",
                   "V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d",
                   ]  # 抓取到的sid
    invite_url = "https://zt.wps.cn/2018/clock_in/api/invite"
    data = '{"invite_userid":"' + userid + '"}'
    print("++给ID：" + userid + '拉满++')

    for sid in invite_sids:
        headers = {
            'Host': 'zt.wps.cn',
            'content-type': 'application/json',
            'sid': sid,
            'Accept-Encoding': 'gzip, deflate'
        }
        r = requests.post(url=invite_url, headers=headers, data=data, verify=False)
        if r.status_code == 200:
            if i <= 13:
                html = json.loads(r.text)
                print(html['result'] + "   增加成功！----------" + str(i))
                time.sleep(1)
                i = i + 1
            else:
                print('「已拉满10人，请检查！」')
                break
        else:
            continue

def main():
    userids = ['5xxxxx72',
               ]
    for userid in userids:
        wps_invite(userid)

#腾讯云函数使用模块
def main_handler(event, context):
    return main()

if __name__ == '__main__':
    main()
