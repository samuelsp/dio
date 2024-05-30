class ClientesIterator:
    def __init__(self, clientes):
        self.clientes = clientes
        self._index = 0
    def __iter__(self):
        return self

    def __next__(self):
        try:
            cliente = self.clientes[self._index]
            return f"""\
            Nome: \t\t{cliente.nome}
            CPF: \t\t{cliente.cpf}
            Data de Nascimento: \t{cliente.data_nascimento}
            Endereço: \t{cliente.endereco}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

