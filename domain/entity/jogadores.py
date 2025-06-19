class Jogador:
    def __init__(self, id: int, nome: str):
        self.nome = nome.strip()
        self.id = id

    def __str__(self):
        return self.nome.title()
