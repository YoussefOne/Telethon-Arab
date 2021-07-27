import sys
from asyncio.exceptions import CancelledError
from time import sleep

from userbot import iqthon

from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP

LOGS = logging.getLogger(__name__)
plugin_category = "tools"


@iqthon.iq_cmd(
    pattern="اعاده تشغيل$",
    command=("اعاده تشغيل", plugin_category),
    info={
        "header": "اعاد the bot !!",
        "usage": "{tr}اعاده تشغيل",
    },
    disable_errors=True,
)
async def _(event):
    "⌔︙إعـادة تشغيـل البـوت ↻"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙إعـادة التشغيـل ↻** \n" "**⌔︙ تم إعـادة تشغيـل البـوت ↻**")
    sandy = await edit_or_reply(
        event,
        "**⌔︙ جـاري إعـادة التشغيـل، قـد يستغـرق الأمـر 2-3 دقائـق لاتقم بترسيـت مـره اخـرى انتـظـر ⏱**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    try:
        delgvar("ipaddress")
        await catub.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@iqthon.iq_cmd(
    pattern="اطفاء تليثون$",
    command=("اطفاء تليثون", plugin_category),
    info={
        "header": "⌔︙ إيقاف التشغيـل ✕",
        "description": "⌔︙لإيقـاف الدايـنو لموقـع هيروڪو، عندها لايمڪنك التشغيـل من البوت وبذلك عليك الذهـاب لموقـع هيروڪو لتشغيـله 💡",
        "usage": "{tr}اطفاء تليثون",
    },
)
async def _(event):
    "⌔︙ إيقاف التشغيـل ✕"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙ إيقاف التشغيـل ✕ **\n" "**⌔︙ تـم إيقـاف تشغيـل البـوت بنجـاح ✓**")
    await edit_or_reply(event, "**⌔︙جـاري إيقـاف تشغيـل البـوت الآن ..**\n **أعـد تشغيـلي يدويـاً لاحقـاً عـبر هيـروڪو ..**\n**سيبقى البـوت متوقفـاً عن العمـل لغايـة** \n**الوقـت المذڪـور 💡**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@iqthon.iq_cmd(
    pattern="اطفاء مؤقت( [0-9]+)?$",
    command=("اطفاء مؤقت", plugin_category),
    info={
        "header": "Userbot will stop working for the mentioned time.",
        "usage": "{tr}sleep <seconds>",
        "examples": "{tr}sleep 60",
    },
)
async def _(event):
    "To sleep the userbot"
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "⌔︙بنـاء الجمـلة ⎀ : `.اطفاء مؤقت + الوقت`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**⌔︙ تـم وضـع البـوت في وضـع السڪون لـ : ** " + str(counter) + " **⌔︙عـدد الثوانـي ⏱**",
        )
    event = await edit_or_reply(event, f"`⌔︙ حسنـاً، سأدخـل وضـع السڪون لـ : {counter} ** عـدد الثوانـي ⏱** ")
    sleep(counter)
    await event.edit("** ⌔︙حسنـاً، أنـا نشـط الآن ᯤ **")


@iqthon.iq_cmd(
    pattern="التحديثات (تشغيل|ايقاف)$",
    command=("التحديثات", plugin_category),
    info={
        "header": "⌔︙ لتحديـث الدردشـة بعـد إعـادة التشغيـل  أو إعـادة التحميـل  ෴",
        "description": "⌔︙سيتـم إرسـال بنـك cmds ڪـرد على الرسالـة السابقـة الأخيـرة لـ (إعادة تشغيل/إعادة تحميل/تحديث cmds) 💡.",
        "usage": [
            "{tr}التحديثات <تشغيل/ايقاف",
        ],
    },
)
async def set_pmlog(event):
    "⌔︙ لتحديـث الدردشـة بعـد إعـادة التشغيـل  أو إعـادة التحميـل  ෴"
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "**⌔︙ تـم تعطيـل التـحديـثات بالفعـل ❗️**")
        delgvar("restartupdate")
        return await edit_or_reply(event, "**⌔︙تـم تعطيـل التـحديـثات بنجـاح ✓**")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "**⌔︙تـم تشغيل التـحديـثات بنجـاح ✓**")
    await edit_delete(event, "**⌔︙ تـم تشغيل التـحديـثات بالفعـل ❗️**")
