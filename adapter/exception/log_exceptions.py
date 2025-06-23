class ExcecaoLogger(Exception):
    pass

class LoggerErrorException(ExcecaoLogger):
    def __init__(self, ex: Exception):
        super().__init__(f"Erro ao gerar o throw: {ex}")
