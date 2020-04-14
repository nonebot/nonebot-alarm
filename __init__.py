#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-04-14 20:45:51
@LastEditors: yanyongyu
@LastEditTime: 2020-04-14 21:40:51
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from nonebot import get_bot

__plugin_name__ = "alarm"


def __plugin_usage__(target: str = None, *args, **kwargs):
    if target == "name":
        return "⏰ 闹钟提醒"
    else:
        return "⏰ 闹钟提醒\n用自然语言说出你需要提醒的事项即可~"


bot = get_bot()
nickname = getattr(bot.config, "NICKNAME", "我")
nickname = nickname if isinstance(nickname, str) else nickname[0]

EXPR_COULD_NOT = (f"哎鸭，{nickname}没有时光机，这个时间没办法提醒你。",
                  f"你这是要穿越吗？这个时间{nickname}没办法提醒你。")

EXPR_TOO_LONG = ("很抱歉，现在暂时不能设置超过一个月的提醒呢。",
                 f"……时间这么久的话，{nickname}可能也记不住。还是换个时间吧。")

EXPR_OK = ("遵命！我会在{time}叫你{action}！\n", "好！我会在{time}提醒你{action}！\n",
           "没问题！我一定会在{time}通知你{action}。\n", "好鸭~ 我会准时在{time}提醒你{action}。\n",
           "嗯嗯！我会在{time}准时叫你{action}哒\n", "好哦！我会在{time}准时叫你{action}~\n")

EXPR_REMIND = ("提醒通知：\n提醒时间到啦！该{action}了！", "提醒通知：\n你设置的提醒时间已经到了~ 赶快{action}！",
               "提醒通知：\n你应该没有忘记{action}吧？", "提醒通知：\n你定下的提醒时间已经到啦！快{action}吧！")

from . import commands, nlp
