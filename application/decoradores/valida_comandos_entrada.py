from discord.ext.commands import Context

from adapter.config.validacao_comandos_impl import ValidacaoComandosImpl


def valida_comandos_entrada(func):
    async def wrapper(ctx: Context, *args, **kwargs):
        validador = ValidacaoComandosImpl()
        if await validador.validar_autorizacao(ctx.message, ctx.bot):
            return await func(ctx, *args, **kwargs)
        return None

    return wrapper
