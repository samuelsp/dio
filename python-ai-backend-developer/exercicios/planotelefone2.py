class PlanoTelefone:
    def __init__(self, nome, saldo):
        self._nome = nome
        self._saldo = saldo
    @property
    def saldo(self):
        return self._saldo
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    def verificar_saldo(self):
        return self.mensagem_personalizada()

    def mensagem_personalizada(self):
        mensagem = None
        if self.saldo < 10:
            mensagem = "Seu saldo está baixo. Recarregue e use os serviços do seu plano."
        elif self.saldo >= 50:
            mensagem = "Parabéns! Continue aproveitando seu plano sem preocupações."
        else:
            mensagem = "Seu saldo está razoável. Aproveite o uso moderado do seu plano."
        return self.saldo, mensagem

# Classe UsuarioTelefone:
class UsuarioTelefone(PlanoTelefone):
    def __init__(self, nome, plano):
        self.nome = nome
        super().__init__(plano.nome, plano.saldo)

# Recebendo as entradas do usuário (nome, plano, saldo):
nome_usuario = 'João'
nome_plano = 'Essencial'
saldo_inicial = 9

# Criação de objetos do plano de telefone e usuário de telefone com dados fornecidos:
plano_usuario = PlanoTelefone(nome_plano, saldo_inicial)
usuario = UsuarioTelefone(nome_usuario, plano_usuario)

# Chamada do método para verificar_saldo sem acessar diretamente os atributos do plano:
saldo_usuario, mensagem_usuario = usuario.verificar_saldo()
print(mensagem_usuario)