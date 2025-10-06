from dataclasses import dataclass

from domain.entity.dono_servidor import DonoServidor


@dataclass(frozen=True)
class ServidorDiscord:
    id: int
    nome: str
    donoServidor: DonoServidor
    numeroMembros: int

    @classmethod
    def to_dict(cls, guild):
        return {
            "id": guild.id,
            "nome": guild.name,
            "dono_servidor": DonoServidor.to_dict(guild.owner),
            "membros": guild.member_count,
        }


servidor_discord = ServidorDiscord
