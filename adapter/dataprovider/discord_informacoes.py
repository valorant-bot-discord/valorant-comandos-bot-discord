from domain.entity.jogadores import Jogador


class DiscordInformacoes:
    @staticmethod
    def listar_membros_canal(canal_discord) -> list[Jogador]:
        membros = [
            m for m in canal_discord.members
            if not m.bot
        ]
        return [Jogador(id=m.id, nome=m.display_name) for m in membros]
