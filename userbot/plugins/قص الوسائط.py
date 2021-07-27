import asyncio
import io
import os
import time
from datetime import datetime

from userbot import iqthon

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _cattools, media_type, progress, reply_id

plugin_category = "utils"


FF_MPEG_DOWN_LOAD_MEDIA_PATH = os.path.join(
    Config.TMP_DOWNLOAD_DIRECTORY, "catuserbot.media.ffmpeg"
)




async def cult_small_video(
    video_file, output_directory, start_time, end_time, out_put_file_name=None
):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = out_put_file_name or os.path.join(
        output_directory, f"{str(round(time.time()))}.mp4"
    )
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None



@iqthon.iq_cmd(
    pattern="قص(?:\s|$)([\s\S]*)",
    command=("قص", plugin_category),
    info={
        "header": "⌔︙يقـوم بقـص الوسائـط المحفوظـة بفتـرة زمنـية محـددة ومخـرجات ڪفيديـو إذا ڪـان فيديـو ✁",
        "description": "⌔︙سيقـوم بقـص الوسائـط المحفوظـة بفتـرة زمنـية محـددة ✁",
        "note": "⌔︙إذا لم تڪـن قـد ذڪرت الفتـرة الزمنيـة بل الوقـت فقـط، فعندهـا سترسـل لقطـة شاشـة في ذلك الموقـع 💡",
        "usage": "{tr}قص +الوقـت المحـدد",
        "examples": "{tr}قص 00:00 00:10",
    },
)
async def ff_mpeg_trim_cmd(event):
    "⌔︙سيقـوم بقـص الوسائـط المحفوظـة بفتـرة زمنـية محـددة ✁"
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        return await edit_delete(
            event,
            f"**⌔︙يجـب تنزيـل ملـف وسائـط وحفظـه في المسـار التالـي  ⇨  :** `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
    reply_to_id = await reply_id(event)
    catevent = await edit_or_reply(event, "**⌔︙جـاري قـص الوسائـط ✁**")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    if len(cmt) == 3:
        # output should be video
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
        )
        if o is None:
            return await edit_delete(
                catevent, f"**⌔︙حـدث خـطأ : لايمڪن إتمـام العمليـة ✕ **"
            )
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await edit_delete(catevent, f"**⌔︙حـدث خـطأ ✕ : **`{e}`")
    elif len(cmt) == 2:
        # output should be image
        cmd, start_time = cmt
        o = await _cattools.take_screen_shot(FF_MPEG_DOWN_LOAD_MEDIA_PATH, start_time)
        if o is None:
            return await edit_delete(
                catevent, f"**⌔︙حـدث خـطأ : لايمڪن إتمـام العمليـة ✕ **"
            )
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=True,
                supports_streaming=True,
                allow_cache=False,
                reply_to=event.message.id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await edit_delete(catevent, f"**⌔︙ حـدث خـطأ  ✕  : **`{e}`")
    else:
        await edit_delete(catevent, "RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await edit_delete(catevent, f"**⌔︙ تـمّ إتمـام العمليـة في {ms} ثانيـة ⏱**", 3)

