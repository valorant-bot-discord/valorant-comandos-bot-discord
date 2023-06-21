from dotenv import load_dotenv
import os


class BotConfig:
    load_dotenv(".env")

    def __init__(self):
        self.TOKEN_BOT = os.getenv("TOKEN_BOT")
        self.TOKEN_SERVER = os.getenv("TOKEN_SERVER")
        self.TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
