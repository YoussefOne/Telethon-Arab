from telethon import functions

from userbot import iqthon

from ..Config import Config
from ..core import CMD_INFO, GRP_INFO, PLG_INFO
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

cmdprefix = Config.COMMAND_HAND_LER

plugin_category = "tools"

hemojis = {
    "اوامر الادمن": "👮‍♂️",
    "استخدامات البوت": "🤖",
    "اوامر الترفيهيه": "🎨",
    "اوامر عشوائيه": "🧩",
    "اوامر الحساب": "🧰",
    "اوامر الادارة": "🗂",
    "اوامر الحفض": "➕",
}


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


async def cmdinfo(input_str, event, plugin=False):
    if input_str[0] == cmdprefix:
        input_str = input_str[1:]
    try:
        about = CMD_INFO[input_str]
    except KeyError:
        if plugin:
            await edit_delete(
                event,
                f"**⌔︙ لا يـوجد مكـون إضـافـي أو أمـر مثـل **`{input_str}`** فـي تلـيثون العـرب .**",
            )
            return None
        await edit_delete(
            event, f"**⌔︙ لا يـوجـد أمـر مثـل **`{input_str}`**في تلـيثون العـرب .**"
        )
        return None
    except Exception as e:
        await edit_delete(event, f"**⌔︙ هنـاك خطـأ**\n`{str(e)}`")
        return None
    outstr = f"**⌔︙ الأمر :** `{cmdprefix}{input_str}`\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"**⌔︙ عـدد الملفـات :** `{plugin}`\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"**⌔︙ الفـئـة :** `{category}`\n\n"
    outstr += f"**⌔︙ الـمقدمـة :**\n{about[0]}"
    return outstr


async def plugininfo(input_str, event, flag):
    try:
        cmds = PLG_INFO[input_str]
    except KeyError:
        outstr = await cmdinfo(input_str, event, plugin=True)
        return outstr
    except Exception as e:
        await edit_delete(event, f"**⌔︙ هنـاك خطـأ**\n`{str(e)}`")
        return None
    if len(cmds) == 1 and (flag is None or (flag and flag != "-p")):
        outstr = await cmdinfo(cmds[0], event, plugin=False)
        return outstr
    outstr = f"**⌔︙ عـدد الملفـات : **`{input_str}`\n"
    outstr += f"**⌔︙ الأوامـر المتوفـرة :** `{len(cmds)}`\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"**⌔︙ الفـئة :** `{category}`\n\n"
    for cmd in cmds:
        outstr += f"⌔︙  **الأمـر :** `{cmdprefix}{cmd}`\n"
        try:
            outstr += f"⌔︙  **يقـوم بـ :** `{CMD_INFO[cmd][1]}`\n\n"
        except IndexError:
            outstr += f"⌔︙  **يقـوم بـ :** `لا شـيئ مكـتـوب`\n\n"
    outstr += f"**⌔︙ الاستـعـمال : ** `{cmdprefix}الاوامر + اسم الامـر\
        \n**⌔︙ ملاحـضـه عـزيـزي : **إذا كـان اسـم الأمـر هـو نـفسه اسـم البرنامج المساعد ، فاستـخدم هـذا الاسـم `{cmdprefix}الاوامر -c <اسم الامـر او الملـف>`."
    return outstr


async def grpinfo():
    outstr = "**⌔︙ المـلفـات في تلـيثـون العـرب :**\n\n"
    outstr += f"**⌔︙ الاستعمال : ** `{cmdprefix}الاوامر <اسم الملف او الامر>`\n\n"
    category = ["اوامر الادمن", "استخدامات البوت", "اوامر الترفيهيه", "اوامر عشوائيه", "اوامر الحساب", "اوامر الادارة", "اوامر الحفض"]
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} **({len(plugins)})\n"
        for plugin in plugins:
            outstr += f"`{plugin}`  "
        outstr += "\n\n"
    return outstr


async def cmdlist():
    outstr = "**⌔︙ القائمة الإجمالية للأوامر في تليثون العرب :**\n\n"
    category = ["اوامر الادمن", "استخدامات البوت", "اوامر الترفيهيه", "اوامر عشوائيه", "اوامر الحساب", "اوامر الادارة", "اوامر الحفض"]
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} ** - {len(plugins)}\n\n"
        for plugin in plugins:
            cmds = PLG_INFO[plugin]
            outstr += f"• **{plugin.title()} has {len(cmds)} الأوامر**\n"
            for cmd in cmds:
                outstr += f"  - `{cmdprefix}{cmd}`\n"
            outstr += "\n"
    outstr += f"**⌔︙ الاستعمال : ** `{cmdprefix}الاوامر -c <اسم الامر>`"
    return outstr


@iqthon.iq_cmd(
    pattern="الاوامر ?(-c|-p|-t)? ?([\s\S]*)?",
    command=("الاوامر", plugin_category),
    info={
        "header": "To get guide for catuserbot.",
        "description": "To get information or guide for the command or plugin",
        "note": "if command name and plugin name is same then you get guide for plugin. So by using this flag you get command guide",
        "flags": {
            "c": "To get info of command.",
            "p": "To get info of plugin.",
            "t": "To get all plugins in text format.",
        },
        "usage": [
            "{tr}help (plugin/command name)",
            "{tr}help -c (command name)",
        ],
        "examples": ["{tr}help help", "{tr}help -c help"],
    },
)
async def _(event):
    "To get guide for catuserbot."
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if flag and flag == "-c" and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    else:
        if flag == "-t":
            outstr = await grpinfo()
        else:
            results = await event.client.inline_query(Config.TG_BOT_USERNAME, "help")
            await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
            await event.delete()
            return
    await edit_or_reply(event, outstr)


@iqthon.iq_cmd(
    pattern="جميع الاوامر(?:\s|$)([\s\S]*)",
    command=("جميع الاوامر", plugin_category),
    info={
        "header": "لإظهار قائمة الاوامر.",
        "description": "إذا لم يتم تقديم أي إدخال ، فسيتم عرض قائمة بجميع الأوامر.",
        "usage": [
            "{tr}جميع الاوامر للكل",
            "{tr}جميع الاوامر + اسم الامر",
        ],
    },
)
async def _(event):
    "To get list of commands."
    input_str = event.pattern_match.group(1)
    if not input_str:
        outstr = await cmdlist()
    else:
        try:
            cmds = PLG_INFO[input_str]
        except KeyError:
            return await edit_delete(event, "**⌔︙ اسم البرنامج المساعد غير صالح أعد التحقق منه**")
        except Exception as e:
            return await edit_delete(event, f"**⌔︙ هناك خطا**\n`{str(e)}`")
        outstr = f"• **{input_str.title()} has {len(cmds)} commands**\n"
        for cmd in cmds:
            outstr += f"  - `{cmdprefix}{cmd}`\n"
        outstr += f"**⌔︙ الاستعمال : ** `{cmdprefix}الاوامر -c <اسم الامر>`"
    await edit_or_reply(
        event, outstr, aslink=True, linktext="**⌔︙ جميع الاوامر في تليثون العرب ** :"
    )


@iqthon.iq_cmd(
    pattern="ssssssssssssssssss ([\s\S]*)",
    command=("ssssssssssssssssss", plugin_category),
    info={
        "header": ".",
        "examples": "{tr}.",
    },
)
async def _(event):
    "To search commands."
    cmd = event.pattern_match.group(1)
    found = [i for i in sorted(list(CMD_INFO)) if cmd in i]
    if found:
        out_str = "".join(f"`{i}`    " for i in found)
        out = f"**I found {len(found)} command(s) for: **`{cmd}`\n\n{out_str}"
        out += f"\n\n__For more info check {cmdprefix}help -c <command>__"
    else:
        out = f"I can't find any such command `{cmd}` in CatUserbot"
    await edit_or_reply(event, out)


@iqthon.iq_cmd(
    pattern="dcccccccccccc$",
    command=("dcccccccccccc", plugin_category),
    info={
        "header": ".",
        "description": ".",
        "usage": "{tr}.",
    },
)
async def _(event):
    "To get dc of your bot"
    result = await event.client(functions.help.GetNearestDcRequest())
    result = f"**⌔︙ تفاصيل Dc لحسابك :**\
              \n**دولة :** {result.country}\
              \n**Current Dc :** {result.this_dc}\
              \n**Nearest Dc :** {result.nearest_dc}\
              \n\n**List Of Telegram Data Centres:**\
              \n**DC1 : **Miami FL, USA\
              \n**DC2 :** Amsterdam, NL\
              \n**DC3 :** Miami FL, USA\
              \n**DC4 :** Amsterdam, NL\
              \n**DC5 : **Singapore, SG\
                "
    await edit_or_reply(event, result)
