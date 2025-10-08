from adapter.constantes import ROLES_PERMITIDAS
from domain.entity.jogadores import Jogador
from domain.entity.role import Role


class DiscordInformacoes:
    @staticmethod
    def listar_membros_canal(canal_discord) -> list[Jogador]:
        jogadores = []

        for membro in canal_discord.members:
            if membro.bot:
                continue

            roles = [
                Role(id_role=role.id, nome=role.name)
                for role in membro.roles
            ]

            if not any(role.nome.lower() in ROLES_PERMITIDAS for role in roles):
                continue

            jogador = Jogador(
                id_role=membro.id,
                nome=membro.display_name,
                roles=roles
            )
            jogadores.append(jogador)

        return jogadores
