# Classe UsuarioTelefone e o encapsulamento dos atributos nome, numero e plano:
class UsuarioTelefone():
    def __init__(self, nome, numero, plano):
        self.nome = nome
        self.numero = numero
        self.plano = plano

    def fazer_chamada(self, destinatario, minutos):
        custo = self.plano.custo_chamada(minutos)
        if self.plano.saldo >= custo:
            self.plano.deduzir_saldo(custo)
            return f'Chamada para {destinatario} realizada com sucesso. Saldo $: {self.plano.saldo:.2f}'
        return 'Saldo insuficiente para realizar a chamada.'

# Classe Pano, ela representa o plano de um usuário de telefone:
class Plano:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.custo = 0.10

    def verificar_saldo(self):
        return self.saldo

    def custo_chamada(self, minutos):
        return self.custo * minutos

    def deduzir_saldo(self, custo):
        self.saldo -= custo

# Classe UsuarioPrePago, aqui vemos a herança onde UsuarioPrePago herda os atributos e métodos da classe UsuarioTelefone:
class UsuarioPrePago(UsuarioTelefone):
    def __init__(self, nome, numero, saldo_inicial):
        super().__init__(nome, numero, Plano(saldo_inicial))


# Recebendo as informações do usuário:
nome = 'Rodrigo'
numero = '(00)90000-0000'
saldo_inicial = 10.00

# Objeto de UsuarioPrePago com os dados fornecidos:
usuario_pre_pago = UsuarioPrePago(nome, numero, saldo_inicial)
destinatario = '(33)93333-3333'
duracao = 60

# Chama o método fazer_chamada do objeto usuario_pre_pago e imprime o resultado:
print(usuario_pre_pago.fazer_chamada(destinatario, duracao))