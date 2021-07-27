import asyncio
import random

from userbot import iqthon

from ..core.managers import edit_or_reply
from . import catmemes

plugin_category = "extra"

@iqthon.iq_cmd(
    pattern="بوسه$",
    command=("بوسه", plugin_category),
    info={
        "header": "يظهر لك تقبيل الرسوم المتحركة متعة",
        "usage": "{tr}بوسه",
    },
)
async def _(event):
    "متعة الرسوم المتحركة"
    catevent = await edit_or_reply(event, "`kiss`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵💋👰"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await catevent.edit(animation_chars[i % 4])


@iqthon.iq_cmd(
    pattern="زرفه$",
    command=("زرفه", plugin_category),
    info={
        "header": "يظهر لك الرسوم المتحركة اللعينة متعة",
        "usage": "{tr}زرفه",
    },
)
async def _(event):
    "fun animation"
    catevent = await edit_or_reply(event, "**💦 جاي زرف الشخص تف**")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["👉       ✊️", "👉     ✊️", "👉  ✊️", "👉✊️💦"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await catevent.edit(animation_chars[i % 4])


@iqthon.iq_cmd(
    pattern="بيبي$",
    command=("بيبي", plugin_category),
    info={
        "header": "يظهر لك الرسوم المتحركة الجنسية الممتعة",
        "usage": "{tr}بيبي",
    },
)
async def _(event):
    "متعة الرسوم المتحركة"
    catevent = await edit_or_reply(event, "**جاري جلب بيبي**")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵👼👰"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await catevent.edit(animation_chars[i % 4])
