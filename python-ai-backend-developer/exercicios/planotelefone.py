class PlanoTelefone:
  def __init__(self, nome, saldo):
    self._nome = nome
    self._saldo = saldo

  @property
  def saldo(self):
      return self._saldo

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
  def __init__(self, nome, plano, saldo):
    self._nome = nome
    self._plano = plano
    super().__init__(plano, saldo)


# Recebendo as entradas do usuário (nome, plano, saldo):
nome_usuario = input()
nome_plano = input()
saldo_inicial = float(input())

 # Criação de objetos do plano de telefone e usuário de telefone com dados fornecidos:
plano_usuario = PlanoTelefone(nome_plano, saldo_inicial)
usuario = UsuarioTelefone(nome_usuario, plano_usuario, saldo_inicial)

# Chamada do método para verificar_saldo sem acessar diretamente os atributos do plano:
saldo_usuario, mensagem_usuario = usuario.verificar_saldo()
print(mensagem_usuario)