import asyncio
from collections import deque

from . import iqthon, edit_delete, edit_or_reply, mention

plugin_category = "fun"


@iqthon.iq_cmd(
    pattern="فراشه$",
    command=("فراشه", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}فراشه",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "**فراشه..**")
    deq = deque(list("🦋✨🦋✨🦋✨🦋✨"))
    for _ in range(48):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@iqthon.iq_cmd(
    pattern="مكعبات$",
    command=("مكعبات", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}مكعبات",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "**مكعبات...**")
    deq = deque(list("🟥🟧🟨🟩🟦🟪🟫⬛⬜"))
    for _ in range(999):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@iqthon.iq_cmd(
    pattern="مطر$",
    command=("مطر", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}مطر",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "`مطر.......`")
    deq = deque(list("🌬☁️🌩🌨🌧🌦🌥⛅🌤"))
    for _ in range(48):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@iqthon.iq_cmd(
    pattern="تحركات$",
    command=("تحركات", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}تحركات",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    animation_interval = 1
    animation_ttl = range(10)
    animation_chars = [
        "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
        "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
        "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
    ]
    event = await edit_or_reply(event, "تحركات ....")
    await asyncio.sleep(2)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])


@iqthon.iq_cmd(
    pattern="ايموجيات$",
    command=("ايموجيات", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}ايموجيات",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    animation_interval = 0.5
    animation_ttl = range(70)
    event = await edit_or_reply(event, "ايموجيات")
    animation_chars = [
        "😀",
        "👩‍🎨",
        "😁",
        "😂",
        "🤣",
        "😃",
        "😄",
        "😅",
        "😊",
        "☺",
        "🙂",
        "🤔",
        "🤨",
        "😐",
        "😑",
        "😶",
        "😣",
        "😥",
        "😮",
        "🤐",
        "😯",
        "😴",
        "😔",
        "😕",
        "☹",
        "🙁",
        "😖",
        "😞",
        "😟",
        "😢",
        "😭",
        "🤯",
        "💔",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])


@iqthon.iq_cmd(
    pattern="طائره$",
    command=("طائره", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}طائره",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "انتظر الطائره...")
    await event.edit("✈-------------")
    await event.edit("-✈------------")
    await event.edit("--✈-----------")
    await event.edit("---✈----------")
    await event.edit("----✈---------")
    await event.edit("-----✈--------")
    await event.edit("------✈-------")
    await event.edit("-------✈------")
    await event.edit("--------✈-----")
    await event.edit("---------✈----")
    await event.edit("----------✈---")
    await event.edit("-----------✈--")
    await event.edit("------------✈-")
    await event.edit("-------------✈")
    await asyncio.sleep(3)


@iqthon.iq_cmd(
    pattern="شرطه$",
    command=("شرطه", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}شرطه",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    animation_interval = 0.3
    animation_ttl = range(12)
    event = await edit_or_reply(event, "شرطه")
    animation_chars = [
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        f"{mention} **الشرطي هنا**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])


@iqthon.iq_cmd(
    pattern="النضام الشمسي$",
    command=("النضام الشمسي", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}النضام الشمسي",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    animation_interval = 0.1
    animation_ttl = range(80)
    event = await edit_or_reply(event, "النضام الشمسي")
    animation_chars = [
        "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️🌎◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️◼️◼️◼️`",
        "`◼️🌕◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️☀◼️`",
        "`◼️◼️◼️🌕◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️☀◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️🌎◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️◼️◼️◼️`",
        "`◼️☀◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️🌕◼️`",
        "`◼️◼️◼️☀◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️🌕◼️◼️◼️`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 8])
