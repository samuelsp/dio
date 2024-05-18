from transacao import Transacao

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = list()

    @property
    def contas(self):
        return self._contas

    @contas.setter
    def contas(self, conta):
        self._contas.append(conta)

    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)