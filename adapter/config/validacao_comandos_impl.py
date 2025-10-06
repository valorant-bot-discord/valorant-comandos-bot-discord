from adapter.config.logs.config_structure_logger import logger
from adapter.constantes import AUTHORIZED_SERVER_ID
from domain.services.validacao_comandos import ValidacaoComandos

LOG_CODE = "valida-eventos-entrada"

class ValidacaoComandosImpl(ValidacaoComandos):
    def __init__(self):
        self.authorized_server_id = AUTHORIZED_SERVER_ID

    async def validar_autorizacao(self, mensagem, bot) -> bool:
        if mensagem.author == bot.user:
            return False

        server_id = getattr(mensagem.guild, 'id', None)
        server_name = mensagem.guild.name

        if mensagem.guild and str(server_id) == self.authorized_server_id:
            logger.info(code=LOG_CODE, message=f"Comando {mensagem.content} executado pelo usuário {mensagem.author}")
            return True

        logger.warning(code=LOG_CODE, message=f"Acesso não autorizado ao servidor {server_id}:{server_name}")
        await mensagem.channel.send("Este servidor não tem permissão para usar o bot.")
        return False