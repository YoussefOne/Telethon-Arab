import nekos

from userbot import iqthon

from ..core.managers import edit_or_reply

plugin_category = "fun"


@iqthon.iq_cmd(
    pattern="tcat$",
    command=("tcat", plugin_category),
    info={
        "header": "Some random cat facial text art",
        "usage": "{tr}tcat",
    },
)
async def hmm(cat):
    "Some random cat facial text art"
    reactcat = nekos.textcat()
    await edit_or_reply(cat, reactcat)


@iqthon.iq_cmd(
    pattern="why$",
    command=("why", plugin_category),
    info={
        "header": "Sends you some random Funny questions",
        "usage": "{tr}why",
    },
)
async def hmm(cat):
    "Some random Funny questions"
    whycat = nekos.why()
    await edit_or_reply(cat, whycat)


@iqthon.iq_cmd(
    pattern="fact$",
    command=("fact", plugin_category),
    info={
        "header": "Sends you some random facts",
        "usage": "{tr}fact",
    },
)
async def hmm(cat):
    "Some random facts"
    factcat = nekos.fact()
    await edit_or_reply(cat, factcat)
