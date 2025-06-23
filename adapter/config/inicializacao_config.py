import os
from dotenv import load_dotenv
from adapter.exception.config_exceptions import TokenAusenteException, ErroCarregamentoEnvException


class BotConfig:
    def __init__(self):
        self._carregar_variaveis()

    def _carregar_variaveis(self):
        try:
            self.TOKEN_BOT = os.getenv("TOKEN_BOT")
            self.TOKEN_SERVER = os.getenv("TOKEN_SERVER")
            self.APPLICATION_NAME = os.getenv("APPLICATION_NAME")

            if not self.TOKEN_BOT:
                raise TokenAusenteException("TOKEN_BOT")
            if not self.TOKEN_SERVER:
                raise TokenAusenteException("TOKEN_SERVER")

        except TokenAusenteException:
            raise
        except Exception:
            raise

    @classmethod
    def carregar_env(cls):
        try:
            dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                       ".env")
            if not os.path.isfile(dotenv_path):
                raise ErroCarregamentoEnvException(f"Arquivo .env não encontrado em: {dotenv_path}")

            load_dotenv(dotenv_path)
        except ErroCarregamentoEnvException as ex:
            raise
        except Exception as ex:
            raise


BotConfig.carregar_env()
config = BotConfig()
