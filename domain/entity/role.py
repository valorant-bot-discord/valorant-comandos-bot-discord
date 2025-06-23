class Role:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome.strip()

    def __str__(self):
        return self.nome.title()
