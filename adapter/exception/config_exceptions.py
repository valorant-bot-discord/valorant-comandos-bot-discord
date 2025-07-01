class ExcecaoConfiguracao(Exception):
    pass

class ErroCarregamentoEnvException(ExcecaoConfiguracao):
    def __init__(self, path: str):
        super().__init__(f"Arquivo .env inválido ou não encontrado: {path}")
        self.path = path


class TokenAusenteException(ExcecaoConfiguracao):
    def __init__(self, variavel: str):
        super().__init__(f"Variável de ambiente ausente: {variavel}")
        self.variavel = variavel
