import asyncio
import io
import os
import pathlib
import re
import time
from datetime import datetime

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import types
from telethon.utils import get_attributes
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)


from ..helpers.utils import _format
from . import iqthon, edit_delete, edit_or_reply, hmention, progress, reply_id, ytsearch

plugin_category = "misc"

audio_opts = {
    "format": "bestaudio",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
    "outtmpl": "%(title)s.mp3",
    "quiet": True,
    "logtostderr": False,
}

video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    "outtmpl": "%(title)s.mp4",
    "logtostderr": False,
    "quiet": True,
}


async def ytdl_down(event, opts, url):
    try:
        await event.edit("**⌔︙يتم جلب البيانات إنتظر قليلا ⏳**")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await event.edit("**⌔︙عُذرا هذا المحتوى قصير جدًا لتنزيله ⚠️**")
        return None
    except GeoRestrictedError:
        await event.edit(
            "**⌔︙الفيديو غير متاح من موقعك الجغرافي بسبب القيود الجغرافية التي يفرضها موقع الويب 🌍**"
        )
        return None
    except MaxDownloadsReached:
        await event.edit("**⌔︙ تم الوصول إلى الحد الأقصى لعدد التنزيلات 🛑**")
        return None
    except PostProcessingError:
        await event.edit("**⌔︙ كان هناك خطأ أثناء المعالجة ⚠️**")
        return None
    except UnavailableVideoError:
        await event.edit("**⌔︙ الوسائط غير متوفرة بالتنسيق المطلوب ⚠️**")
        return None
    except XAttrMetadataError as XAME:
        await event.edit(f"⌔︙ `{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return None
    except ExtractorError:
        await event.edit("**⌔︙ حدث خطأ أثناء استخراج المعلومات يرجى وضعها بشكل صحيح ❗️**")
        return None
    except Exception as e:
        await event.edit(f"**⌔︙حـدث خطأ  ⚠️ : **\n__{str(e)}__")
        return None
    return ytdl_data


async def fix_attributes(
    path, info_dict: dict, supports_streaming: bool = False, round_message: bool = False
) -> list:
    """⌔︙تجنب الحالات المتعددة للميزة ✳️"""
    new_attributes = []
    video = False
    audio = False

    uploader = info_dict.get("uploader", "Unknown artist")
    duration = int(info_dict.get("duration", 0))
    suffix = path.suffix[1:]
    if supports_streaming and suffix != "mp4":
        supports_streaming = False

    attributes, mime_type = get_attributes(path)
    if suffix == "mp3":
        title = str(info_dict.get("title", info_dict.get("id", "Unknown title")))
        audio = types.DocumentAttributeAudio(duration, None, title, uploader)
    elif suffix == "mp4":
        width = int(info_dict.get("width", 0))
        height = int(info_dict.get("height", 0))
        for attr in attributes:
            if isinstance(attr, types.DocumentAttributeVideo):
                duration = duration or attr.duration
                width = width or attr.w
                height = height or attr.h
                break
        video = types.DocumentAttributeVideo(
            duration, width, height, round_message, supports_streaming
        )

    if audio and isinstance(audio, types.DocumentAttributeAudio):
        new_attributes.append(audio)
    if video and isinstance(video, types.DocumentAttributeVideo):
        new_attributes.append(video)

    for attr in attributes:
        if (
            isinstance(attr, types.DocumentAttributeAudio)
            and not audio
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not video
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not isinstance(attr, types.DocumentAttributeVideo)
        ):
            new_attributes.append(attr)
    return new_attributes, mime_type


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@iqthon.iq_cmd(
    pattern="تحميل ص(?: |$)(.*)",
    command=("تحميل ص", plugin_category),
    info={
        "header": "⌔︙ لتنزيل الصوت من العديد من المواقع مثل Youtube",
        "description": "⌔︙ تحميل المقطع الصوتي من الرابط المعطى ( يدعم جميع المواقع التي تدعم yt-dl)  📮",
        "examples": [
            "{tr}<تحميل ص <الرد على رابط",
            "{tr}<تحميل ص <الرابط",
        ],
    },
)
async def download_audio(event):
    """⌔︙لتحميل مقطع صوتي من اليوتيوب ومواقع أخرى 🎙."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await edit_or_reply(event, "**⌔︙ يجب وضع رابط لتحميله  ❗️**")
    catevent = await edit_or_reply(event, "**⌔︙ يتم الإعداد إنتظر قليلا  ⏱**")
    reply_to_id = await reply_id(event)
    ytdl_data = await ytdl_down(catevent, audio_opts, url)
    if ytdl_data is None:

        return
    await catevent.edit(
        f"**⌔︙ يتم لتحميل الأغنية 🎙 :**\
        \n**{ytdl_data['title']}**\
        \n⌔︙بواسطة 📝 : **{ytdl_data['uploader']}**"
    )
    f = pathlib.Path(f"{ytdl_data['title']}.mp3".replace("|", "_"))
    catthumb = pathlib.Path(f"{ytdl_data['title']}.mp3.jpg".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = pathlib.Path(f"{ytdl_data['title']}.mp3.webp".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = None
    c_time = time.time()
    ul = io.open(f, "rb")
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, catevent, c_time, "upload", file_name=f)
        ),
    )
    ul.close()
    attributes, mime_type = await fix_attributes(f, ytdl_data, supports_streaming=True)
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        thumb=await event.client.upload_file(catthumb) if catthumb else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        reply_to=reply_to_id,
        caption=ytdl_data["title"],
        supports_streaming=True,
        force_document=False,
    )
    os.remove(f)
    if catthumb:
        os.remove(catthumb)
    await catevent.delete()


@iqthon.iq_cmd(
    pattern="تحميل ف(?: |$)(.*)",
    command=("تحميل ف", plugin_category),
    info={
        "header": "⌔︙ لتحميل فيديو من مواقع عديدة مثل يوتيوب  📮",
        "description": "⌔︙ تحميل الفيديو من الرابط المعطى ( يدعم جميع المواقع التي تدعم yt-dl)  📮",
        "examples": [
            "{tr}<تحميل ف <الرد بالرابط",
            "{tr}<تحميل ف <الرابط",
        ],
    },
)
async def download_video(event):
    """⌔︙لتحميل فيديو من يوتيوب ومواقع اخرى عديدة 📮."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await edit_or_reply(event, "**⌔︙ عليك وضع رابـط اولا ليتم تنـزيله ❗️**")
    catevent = await edit_or_reply(event, "**⌔︙ يتم التحميل إنتظر قليلا  ⏱**")
    reply_to_id = await reply_id(event)
    ytdl_data = await ytdl_down(catevent, video_opts, url)
    if ytdl_down is None:
        return
    f = pathlib.Path(f"{ytdl_data['title']}.mp4".replace("|", "_"))
    catthumb = pathlib.Path(f"{ytdl_data['title']}.jpg".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = pathlib.Path(f"{ytdl_data['title']}.webp".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = None
    await catevent.edit(
        f"**⌔︙ التحضيـر للـرفع إنتظر ♻️ **:\
        \n**{ytdl_data['title']}**\
        \n⌔︙بواسطة 📝 : *{ytdl_data['uploader']}*"
    )
    ul = io.open(f, "rb")
    c_time = time.time()
    attributes, mime_type = await fix_attributes(f, ytdl_data, supports_streaming=True)
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, catevent, c_time, "upload", file_name=f)
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        thumb=await event.client.upload_file(catthumb) if catthumb else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        reply_to=reply_to_id,
        caption=ytdl_data["title"],
    )
    os.remove(f)
    if catthumb:
        os.remove(catthumb)
    await event.delete()


@iqthon.iq_cmd(
    pattern="نتائج بحث(?: |$)(\d*)? ?(.*)",
    command=("نتائج بحث", plugin_category),
    info={
        "header": "⌔︙ للبحث عن فيديوات في اليوتيوب  🔍",
        "description": "⌔︙ يجلب نتائج بحث youtube مع المشاهدات والمدة مع عدد النتائج المطلوبة بشكل افتراضي ، فإنه يجلب 10 نتائج ⚜️",
        "examples": [
            "{tr}<نتائج بحث <استفسار",
            "{tr}<نتائج بحث <1-9> <استفسار",
        ],
    },
)
async def yt_search(event):
    "⌔︙للبحث عن فيديوات في اليوتيوب 🔍"
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_delete(
            event, "**⌔︙ يرجى الرّد على الرسالة أو كتابة الرابط أولا  ⚠️**"
        )
    video_q = await edit_or_reply(event, "**⌔︙ يتم البحث عن المطلوب إنتظر قليلا  ⏱**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim <= 0:
            lim = int(10)
    else:
        lim = int(10)
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edit_delete(video_q, str(e), time=10, parse_mode=_format.parse_pre)
    reply_text = f"**⌔︙ البحث 🔍 :**\n`{query}`\n\n**⌔︙  النتائج :**\n{full_response}"
    await edit_or_reply(video_q, reply_text)


@iqthon.iq_cmd(
    pattern="انستا (.*)",
    command=("انستا", plugin_category),
    info={
        "header": "⌔︙لتحميل فيديو/صورة من الإنستكرام 🌠",
        "description": "⌔︙ملاحظة، يتم تحميل الفيديوات/الصور العامة فقط ❗️",
        "examples": [
            "{tr}انستا <الرابط",
        ],
    },
)
async def kakashi(event):
    "⌔︙لتحميل فيديو/صورة من الإنستكرام 🌠"
    chat = "@instasavegrambot"
    link = event.pattern_match.group(1)
    if "www.instagram.com" not in link:
        await edit_or_reply(
            event, "**⌔︙ يجب كتابة رابط من الإنستكرام ليتم تحميله ❗️**"
        )
    else:
        start = datetime.now()
        catevent = await edit_or_reply(event, "**⌔︙ جاري التحميل إنتظر قليلا  ⏱**")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(link)
            video = await conv.get_response()
            details = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**⌔︙قم بفتح الحظر عن البوت ❗️ :** @instasavegrambot")
            return
        await catevent.delete()
        cat = await event.client.send_file(
            event.chat_id,
            video,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await cat.edit(
            f"⌔︙تم التنزيل بواسطة : @IQTHON",
            parse_mode="html",
        )
    await event.client.delete_messages(
        conv.chat_id, [msg_start.id, response.id, msg.id, video.id, details.id]
    )
