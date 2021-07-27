import sys

import userbot
from telethon import functions
from userbot import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import iqthon
from .utils import (
    add_bot_to_logger_group,
    ipchange,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("تليثون العرب")

print(userbot.__copyright__)
print("المرخصة بموجب شروط " + userbot.__license__)

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("بدء تنزيل تليثون العرب")
    iqthon.loop.run_until_complete(setup_bot())
    LOGS.info("بدء تشغيل البوت")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()


class CatCheck:
    def __init__(self):
        self.sucess = True


Catcheck = CatCheck()


async def startup_process():
    check = await ipchange()
    if check is not None:
        Catcheck.sucess = False
        return
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖\n")
    print("حسنا لقد تم تنصيب تليثون العرب بدون مشاكل")
    print(
        f"⌔︙ا  تهانينا ، اكتب الآن -  .السورس  - لروئيه المعلومات\
        \nقم بتوجه الى القناه لمعرفه الاوامر وباقي معلومات https://t.me/JooTech"
    )
    print("❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return

iqthon.loop.run_until_complete(startup_process())
def start_bot():
	try:
		iqthon.loop.run_until_complete(iqthon(
			functions.channels.JoinChannelRequest("JooTech")
		))
		iqthon.loop.run_until_complete(iqthon(
			functions.channels.JoinChannelRequest("Aflamy2021")
		))
		iqthon.loop.run_until_complete(iqthon(
			functions.channels.JoinChannelRequest("aflam_ar")
		))
	except Exception as e:
		print(e)
		return False
Checker = start_bot()
if Checker == False:
    print("لايمكن البدء حتى الاشتراك بالقنوات التاليه في تليجرام @JooTech - @Aflamy2021 - @aflam_ar")
    iqthon.disconnect()
    sys.exit()
if len(sys.argv) not in (1, 3, 4):
    iqthon.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        iqthon.run_until_disconnected()
    except ConnectionError:
        pass
