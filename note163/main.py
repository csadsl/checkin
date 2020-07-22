# !/usr/bin/env python3
# coding=utf-8

import json
import sys
from note163 import *


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
