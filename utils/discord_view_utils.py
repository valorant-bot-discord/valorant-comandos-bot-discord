from adapter.config.logs.logger_config import ConfigStructureLogger

logger = ConfigStructureLogger()
LOG_CODE = "cria-view-timeout"


async def handle_view_timeout(view, message, timeout_message="Tempo para interação esgotado."):
    for item in view.children:
        item.disabled = True
    try:
        await message.edit(content=timeout_message, view=view)
        logger.info(code=LOG_CODE, message="View timeout: botões desabilitados e mensagem atualizada.")
    except Exception as ex:
        logger.error(code=LOG_CODE, message="Erro ao editar mensagem no timeout da view.", throw=ex)
