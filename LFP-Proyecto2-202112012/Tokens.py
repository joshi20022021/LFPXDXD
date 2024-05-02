class Token:
    def __init__(self, tipo, contenido, linea, columna):
        self.tipo = tipo
        self.contenido = contenido
        self.linea = linea
        self.columna = columna