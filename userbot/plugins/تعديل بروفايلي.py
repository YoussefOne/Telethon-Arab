import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

from userbot import iqthon

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "utils"


# ====================== CONSTANT ===============================
INVALID_MEDIA = "**⌔︙إمتداد هذه الصورة غير صالح  ❌**"
PP_CHANGED = "**⌔︙تم تغير صورة حسابك بنجاح  ✅**"
PP_TOO_SMOL = "**⌔︙هذه الصورة صغيرة جدًا قم بإختيار صورة أخرى  ⚠️**"
PP_ERROR = "**⌔︙حدث خطأ أثناء معالجة الصورة  ⚠️**"
BIO_SUCCESS = "**⌔︙تم تغيير بايو حسابك بنجاح  ✅**"
NAME_OK = "**⌔︙تم تغيير اسم حسابك بنجاح  ✅**"
USERNAME_SUCCESS = "**⌔︙تم تغيير معرّف حسابك بنجاح  ✅**"
USERNAME_TAKEN = "**⌔︙هذا المعرّف مستخدم  ❌**"
# ===============================================================


@iqthon.iq_cmd(
    pattern="وضع بايو (.*)",
    command=("وضع بايو", plugin_category),
    info={
        "header": "⌔︙لتعيين بايو لهذا الحساب  🔖",
        "usage": "{tr}وضع بايو <البايو الخاص بك>",
    },
)
async def _(event):
    "⌔︙لتعيين بايو لهذا الحساب  🔖"
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await edit_delete(event, "**⌔︙تم تغيير البايو بنجاح  ✅**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")


@iqthon.iq_cmd(
    pattern="وضع اسم (.*)",
    command=("وضع اسم", plugin_category),
    info={
        "header": "⌔︙لتعيين/تغيير اسم لهذا الحساب  🔖.",
        "usage": ["{tr}وضع اسم الاسم الأول ؛ الكنية", "{tr}وضع اسم الاسم الأول"],
    },
)
async def _(event):
    "⌔︙لتعيين/تغيير اسم لهذا الحساب  🔖"
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split("|", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await edit_delete(event, "**⌔︙تم تغيير الاسم بنجاح  ✅**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")


@iqthon.iq_cmd(
    pattern="وضع صورة$",
    command=("وضع صورة", plugin_category),
    info={
        "header": "⌔︙لوضع صوره ل هذا الحساب  📂.",
        "usage": "{tr}وضع صورة <الرد على الصورة أو gif>",
    },
)
async def _(event):
    "⌔︙لوضع صوره ل هذا الحساب  📂"
    reply_message = await event.get_reply_message()
    catevent = await edit_or_reply(
        event, "**...**"
    )
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await catevent.edit(str(e))
    else:
        if photo:
            await catevent.edit("**⌔︙ أشترك @IQTHON **")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = os.stat(photo).st_size
                if size > 2097152:
                    await catevent.edit("**⌔︙ يجب ان يكون الحجم اقل من 2 ميغا ✅**")
                    os.remove(photo)
                    return
                catpic = None
                catvideo = await event.client.upload_file(photo)
            else:
                catpic = await event.client.upload_file(photo)
                catvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=catpic, video=catvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await catevent.edit(f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")
            else:
                await edit_or_reply(
                    catevent, "**⌔︙ تم تغيير الصورة بنجاح ✅**"
                )
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.info(str(e))


@iqthon.iq_cmd(
    pattern="وضع معرف (.*)",
    command=("وضع معرف", plugin_category),
    info={
        "header": "⌔︙ لتعيين / تحديث اسم المستخدم لهذا الحساب 👥.",
        "usage": "{tr}وضع معرف <اسم مستخدم جديد>",
    },
)
async def update_username(username):
    """ .وضع معرف` الأمر ، قم بتعيين اسم مستخدم جديد في تليجرام.`"""
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await edit_delete(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await edit_or_reply(event, USERNAME_TAKEN)
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")


@iqthon.iq_cmd(
    pattern="الحساب$",
    command=("الحساب", plugin_category),
    info={
        "header": "⌔︙ للحصول على معلومات هذا الحساب  📂.",
        "usage": "{tr}الحساب",
    },
)
async def count(event):
    """`ل `.الحساب الأمر ، احصل على إحصائيات الملف الشخصي."""
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    catevent = await edit_or_reply(event, "**⌔︙ يتم الحساب إنتظر قليلا  ⏳**")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            LOGS.info(d)

    result += f"**⌔︙ الأشخاص  👥:**\t**{u}**\n"
    result += f"**⌔︙المجموعات  🛗 :**\t**{g}**\n"
    result += f"**⌔︙المجموعات الخارقة  ✳️:**\t**{c}**\n"
    result += f"**⌔︙القنوات  ❇️ :**\t**{bc}**\n"
    result += f"**⌔︙البوتات  ℹ️ :**\t**{b}**"

    await catevent.edit(result)


@iqthon.iq_cmd(
    pattern="حذف صوره ?(.*)",
    command=("حذف صوره", plugin_category),
    info={
        "header": "⌔︙لحذف صورة الملف الشخصي لهذا الحساب  🗑.",
        "description": "⌔︙إذ لم تذكر أي صورة عندها سيتم حذف صورة واحدة فقط  ⚠️.",
        "usage": ["{tr}حذف صوره <⌔︙ليس هناك من الصور ليتم حذفها  ⚠️>", "{tr}حذف صوره"],
    },
)
async def remove_profilepic(delpfp):
    """⌔︙لأمر `.حذف صورة` الملف الشخصي ، قم بحذف صورتك الحالية على تليجرام  ⚠️."""
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await edit_delete(
        delpfp, f"**⌔︙ تم الحذف بنجاح  ✅ {len(input_photos)} من صور حسابك بنجاح**"
    )


@iqthon.iq_cmd(
    pattern="انشائي$",
    command=("انشائي", plugin_category),
    info={
        "header": "⌔︙لعرض قائمة القنوات العامة أو المجموعات التي تم إنشائها من قبل هذا الحساب  💠.",
        "usage": "{tr}انشائي",
    },
)
async def _(event):
    "⌔︙لعرض قائمة القنوات العامة أو المجموعات التي تم إنشائها من قبل هذا الحساب  💠."
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "**⌔︙جميع القنوات والمجموعات التي قمت بإنشائها  💠  :**\n"
    output_str += "".join(
        f"⌔︙  - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await edit_or_reply(event, output_str)
