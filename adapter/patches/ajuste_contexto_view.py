import discord
from discord import Interaction
from functools import wraps
from adapter.config.logs.transaction_context import transaction_context


def aplicar_ajuste_de_contexto():
    original_init = discord.ui.View.__init__

    @wraps(original_init)
    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        transaction_id = transaction_context.get_id()
        if not transaction_id:
            return

        original_interaction_check = self.interaction_check

        @wraps(original_interaction_check)
        async def wrapped_interaction_check(interaction: Interaction) -> bool:
            transaction_context.set_id(transaction_id)
            return await original_interaction_check(interaction)

        self.interaction_check = wrapped_interaction_check

        original_on_timeout = self.on_timeout

        @wraps(original_on_timeout)
        async def wrapped_on_timeout():
            transaction_context.set_id(transaction_id)
            await original_on_timeout()

        self.on_timeout = wrapped_on_timeout

    discord.ui.View.__init__ = patched_init
