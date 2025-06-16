import os
from dotenv import load_dotenv
from adapter.config.logs.logger_config import ConfigStructureLogger

logger = ConfigStructureLogger()
LOG_CODE = "config-inicializacao"


class BotConfig:
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    try:
        load_dotenv(dotenv_path)
    except Exception as ex:
        logger.error(code=LOG_CODE, message="Erro ao carregar arquivo .env", throw=ex)
        raise

    def __init__(self):
        try:
            self.TOKEN_BOT = os.getenv("TOKEN_BOT")
            self.TOKEN_SERVER = os.getenv("TOKEN_SERVER")
            self.APPLICATION_NAME = os.getenv("APPLICATION_NAME")

            if not self.TOKEN_BOT or not self.TOKEN_SERVER:
                raise ValueError("TOKEN_BOT e TOKEN_SERVER são obrigatórios no .env")

        except ValueError as ex:
            logger.error(code=LOG_CODE, message="Tokens obrigatórios não encontrados", throw=ex)
            raise
        except Exception as ex:
            logger.error(code=LOG_CODE, message="Erro ao inicializar configurações", throw=ex)
            raise


config = BotConfig()
