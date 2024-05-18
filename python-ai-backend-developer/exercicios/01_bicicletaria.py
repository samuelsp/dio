class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor

    def buzinar(self):
       return 'Plim plim!...'

    def parar(self):
        return 'A bicicleta parou!'

    def correr(self):
        return 'A bicicleta está correndo!'

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{k}={v}' for k, v in self.__dict__.items()])}"

if __name__ == '__main__':
    bicicleta = Bicicleta('azul', 'caloi', 2020, 500.00)
    print(bicicleta.buzinar())
    print(bicicleta.parar())
    print(bicicleta.correr())
    print(bicicleta)

