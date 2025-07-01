class Role:
    def __init__(self, id_role: int, nome: str):
        self.id_role = id_role
        self.nome = nome.strip()

    def __str__(self):
        return self.nome.title()
