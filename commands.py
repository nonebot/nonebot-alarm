#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-04-14 21:00:04
@LastEditors: yanyongyu
@LastEditTime: 2020-04-14 21:34:58
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from datetime import datetime, timedelta

from aiocqhttp import Event as CQEvent
from nonebot import get_bot, scheduler
from nonebot import on_command, CommandSession
from nonebot.helpers import render_expression

from . import EXPR_COULD_NOT, EXPR_TOO_LONG, EXPR_OK, EXPR_REMIND

assert scheduler, "Apscheduler not installed! Try using `pip install nonebot[scheduler]` to install it."


async def remind(target: str, event: CQEvent):
    """Send shake and remind notification to user
    
    Args:
        target (str): Thing to remind
        event (CQEvent): Message event
    """
    bot = get_bot()
    # 发送戳一戳
    await bot.send_private_msg(self_id=event["self_id"],
                               user_id=event["user_id"],
                               message="[CQ:shake]")
    # 发送提醒
    await bot.send_private_msg(self_id=event["self_id"],
                               user_id=event["user_id"],
                               message=render_expression(EXPR_REMIND,
                                                         action=target,
                                                         escape_args=False))


@on_command("_alarm")
async def alarm(session: CommandSession):
    time: datetime = session.get("time")
    target: str = session.get("target")

    # 过滤时间
    now = datetime.now()
    # 过去的时间
    if time <= now:
        session.finish(render_expression(EXPR_COULD_NOT))
    # 超过30天的时间
    elif time - now > timedelta(days=30):
        session.finish(render_expression(EXPR_TOO_LONG))

    # 添加job
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    scheduler.add_job(  # type: ignore
        remind,
        "date",
        run_date=time,
        args=[target, session.event])
    session.finish(
        render_expression(
            EXPR_OK, time=time_str, action=target, escape_args=False) +
        f"\n提醒创建成功：\n"
        f"> 提醒时间：{time_str}\n"
        f"> 内容：{target}")
