from dataclasses import dataclass


@dataclass(frozen=True)
class DonoServidor:
    id: int
    nome: str

    @classmethod
    def to_dict(cls, guild_owner):
        return {"id": guild_owner.id, "nome": guild_owner.name}
