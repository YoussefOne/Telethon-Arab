from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 1339827
    API_HASH = "97db196171301583052efbbcb00bac96"
    # the name to display in your alive message
    ALIVE_NAME = "Hi JOO Iam Alive"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://eygunscj:EHDfRkAI9LzpmZGafUkw_GZioO6uCjMW@kashin.db.elephantsql.com/eygunscj"
    # After cloning the repo and installing requirements do python3 telesetup.py an fill that value with this
    STRING_SESSION = "1BJWap1sBuyqh83Aq9mPK0E7PuUGDPCAPdptcLFzVK_D5optAkLOJEVXn-i27SqePSNaVrBe1xd0ohUsXliP_bywzOTfgysgXiepsd3Tf9Uc-rRdBn3rgUAscToymeCgA4AEhudPpN9nRruSzz9TxbR1ysWEm2FpJs6oMkyOMYrAFX2W61wiDFuLfqDRdgpI4NEIqjK8IbCVuvj83EzQY_voOsyr9zxYCuoxTB72wfseZtGuCp2kjvM8vQ17hCs9zomHj2Opb4hrPpQBuXnc9wcwBkcP3EmQzK1hE8eRFtk-IE2X-mHojfRfYMqMbEFfeQw4dRAjHO1lvMkc2vMbY81C-i6nOOqc="
    # create a new bot in @botfather and fill the following vales with bottoken and username respectively
    TG_BOT_TOKEN = "1903416856:AAFc2cha8Jt_8TPnK3jg-ZlMs2At8eIZVY0"
    TG_BOT_USERNAME = "TELETHON JOO"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -568342434
    # command handler
    COMMAND_HAND_LER = "."
    # sudo enter the id of sudo users userid's in that array
    SUDO_USERS = [1133074637]
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
