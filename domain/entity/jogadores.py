from domain.entity.role import Role


class Jogador:
    def __init__(self, id: int, nome: str, roles: list[Role]):
        self.nome = nome.strip()
        self.id = id
        self.roles = roles

    def __str__(self):
        return self.nome.title()
