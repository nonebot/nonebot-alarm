#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-04-14 21:30:20
@LastEditors    : yanyongyu
@LastEditTime   : 2020-04-14 21:30:20
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

import re
import json
from datetime import datetime, timedelta

from cocoNLP.extractor import extractor
from nonebot import on_natural_language, NLPSession, IntentCommand


@on_natural_language(keywords={"提醒", "通知", "叫"})
async def _(session: NLPSession):
    stripped_arg = session.msg_text.strip()

    # 将消息分为两部分（时间|事件）
    time, target = re.split(r"(?:提醒)|(?:通知)|(?:叫)", stripped_arg, maxsplit=1)

    # 解析时间
    ex = extractor()
    try:
        time_json = json.loads(ex.extract_time(time))
    except TypeError:
        return

    if "error" in time_json.keys() or not target:
        return
    # 时间差转换为时间点
    elif time_json['type'] == "timedelta":
        time_diff = time_json['timedelta']
        time_diff = timedelta(days=time_diff['day'],
                              hours=time_diff['hour'],
                              minutes=time_diff['minute'],
                              seconds=time_diff['second'])
        time_target = datetime.now() + time_diff
    elif time_json['type'] == "timestamp":
        time_target = datetime.strptime(time_json['timestamp'],
                                        "%Y-%m-%d %H:%M:%S")
        # 默认时间点为中午12点
        if not re.search(r"[\d+一二两三四五六七八九十]+点", time)\
                and time_target.hour == 0\
                and time_target.minute == 0\
                and time_target.second == 0:
            time_target.hour = 12

    return IntentCommand(90.0,
                         "_alarm",
                         args={
                             "time": time_target,
                             "target": target.lstrip("我")
                         })
