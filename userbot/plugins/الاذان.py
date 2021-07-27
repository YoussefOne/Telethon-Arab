import json

import requests
from ..sql_helper.globals import gvarstatus
from . import iqthon, edit_delete, edit_or_reply

plugin_category = "extra"

@iqthon.iq_cmd(
    pattern="الاذان(?: |$)(.*)",
    command=("الاذان", plugin_category),
    info={
        "header": "يعرض لك أوقات الصلاة الإسلامية لاسم المدينة المحدد.",
        "note": "يمكنك تعيين المدينة الافتراضية باستخدام الأمر {tr} الاذان.",
        "usage": "{tr}الاذان +المحافظه",
        "examples": "{tr}الاذان بغداد ",
    },
)
async def get_adzan(adzan):
    LOKASI = adzan.pattern_match.group(1)
    url = f"https://api.pray.zone/v2/times/today.json?city={LOKASI}"
    request = requests.get(url)
    if request.status_code != 200:
        await edit_delete(
            adzan, f"**⌔︙لم يـتم العثور على معلومات لـهذه المدينه ⚠️ {LOKASI}\n يرجى كتابة اسم محافظتك وباللغه الانكليزي **", 5
        ) 
        return
    result = json.loads(request.text)
    iqthonresult = f"<b>اوقـات صـلاه المـسلمين 👳‍♂️ </b>\
            \n\n<b>المـدينة  Ⓜ️  : </b><i>{result['results']['location']['city']}</i>\
            \n<b>الـدولة  🏳️ : </b><i>{result['results']['location']['country']}</i>\
            \n<b>التـاريخ  🔢  : </b><i>{result['results']['datetime'][0]['date']['gregorian']}</i>\
            \n<b>الهـجري  ⏳  : </b><i>{result['results']['datetime'][0]['date']['hijri']}</i>\
            \n\n<b>الامـساك  🕒  : </b><i>{result['results']['datetime'][0]['times']['Imsak']}</i>\
            \n<b>شـروق الشمس  🌝 : </b><i>{result['results']['datetime'][0]['times']['Sunrise']}</i>\
            \n<b>الـفجر  🌔   : </b><i>{result['results']['datetime'][0]['times']['Fajr']}</i>\
            \n<b>الضـهر 🌞   : </b><i>{result['results']['datetime'][0]['times']['Dhuhr']}</i>\
            \n<b>العـصر  🌥    : </b><i>{result['results']['datetime'][0]['times']['Asr']}</i>\
            \n<b>غـروب الشمس  🌘 : </b><i>{result['results']['datetime'][0]['times']['Sunset']}</i>\
            \n<b>المـغرب 🌑 : </b><i>{result['results']['datetime'][0]['times']['Maghrib']}</i>\
            \n<b>العشـاء  🌚   : </b><i>{result['results']['datetime'][0]['times']['Isha']}</i>\
            \n<b>منتـصف الليل 🕛 : </b><i>{result['results']['datetime'][0]['times']['Midnight']}</i>\
    "
    await edit_or_reply(adzan, iqthonresult, "html")
