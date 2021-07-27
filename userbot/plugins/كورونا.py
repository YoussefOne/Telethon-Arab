from covid import Covid

from . import iqthon, covidindia, edit_delete, edit_or_reply

plugin_category = "extra"


@iqthon.iq_cmd(
    pattern="كورونا(?:\s|$)([\s\S]*)",
    command=("كورونا", plugin_category),
    info={
        "header": "To get latest information about covid-19.",
        "description": "Get information about covid-19 data in the given country/state(only Indian States).",
        "usage": "{tr}covid <state_name/country_name>",
        "examples": ["{tr}covid andhra pradesh", "{tr}covid india", "{tr}covid world"],
    },
)
async def corona(event):
    "للحصول على أحدث المعلومات حول كورونا."
    input_str = event.pattern_match.group(1)
    country = (input_str).title() if input_str else "العالم"
    catevent = await edit_or_reply(event, "**⌔︙يتـم جلـب معلومـات فـايروس كـورونا فـي البلـد المحـدد 🔎**")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⌔︙ الاصابات المؤكده 😟 : <code>{hmm1}</code>"
        data += f"\n⌔︙ الاصابات المشبوهه 🥺 : <code>{country_data['active']}</code>"
        data += f"\n⌔︙ الوفيات ⚰️ : <code>{hmm2}</code>"
        data += f"\n⌔︙ الحرجه 😔 : <code>{country_data['critical']}</code>"
        data += f"\n⌔︙ حالات الشفاء 😊 : <code>{country_data['recovered']}</code>"
        data += f"\n⌔︙ اجمالي الاختبارات 📊 : <code>{country_data['total_tests']}</code>"
        data += f"\n⌔︙ الاصابات الجديده 🥺 : <code>{country_data['new_cases']}</code>"
        data += f"\n⌔︙ الوفيات الجديده ⚰️ : <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>⌔︙ معلومـات فـايروس كـورونا. 💉 لـ {}:{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n⌔︙ الاصابات المؤكده 😟 : <code>{data['new_positive']}</code>\
                \n⌔︙ الاصابات المشبوهه 🥺 : <code>{data['new_active']}</code>\
                \n⌔︙ الوفيات ⚰️ : <code>{data['new_death']}</code>\
                \n⌔︙ حالات الشفاء 😊 : <code>{data['new_cured']}</code>\
                \n⌔︙ اجمالي الاختبارات 📊  : <code>{cat1}</code>\
                \n⌔︙ الاصابات الجديده 🥺 : <code>{cat2}</code>\
                \n⌔︙ الوفيات الجديده ⚰️ : <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                "**⌔︙ معلومـات فـايروس كـورونا. 💉  \n  فـي بـلد  - {} غـير مـوجودة ❌**".format(country),
                5,
            )
