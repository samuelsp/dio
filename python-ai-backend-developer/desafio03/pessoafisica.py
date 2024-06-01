from cliente import Cliente

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def endereco(self):
        return self._endereco

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.data_nascimento}', '{self.cpf}', '{self.endereco}')>"


    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"Data Nascimento: {self.data_nascimento}\n"
                f"CPF: {self.cpf}\n"
                f"Endereço: {self.endereco}\n")


