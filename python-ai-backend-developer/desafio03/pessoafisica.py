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

    def __str__(self):
        return (f"Nome: {self._nome}\n"
                f"Data Nascimento: {self._data_nascimento}\n"
                f"CPF: {self._cpf}\n"
                f"Endereço: {self.endereco}\n")


