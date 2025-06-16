class Jogador:
    def __init__(self, nome: str):
        self.nome = nome.strip()

    def __str__(self):
        return self.nome.title()
