class Error:
    def __init__(self, tipo, caracter, linea, columna):
        self.tipo = tipo
        self.caracter = caracter
        self.linea = linea
        self.columna = columna