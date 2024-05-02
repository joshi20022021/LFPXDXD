from Errores import Error
from Tokens import Token

class AnalizadorSintactico:
    palabras_reservadas = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                           'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']

    def __init__(self):
        pass

    def analizar(self, tokens):
        errores_sintacticos = []

        # Función auxiliar para agregar errores
        def agregar_error(tipo, linea, columna, caracter, token_esperado, descripcion):
            errores_sintacticos.append({
                "tipo": tipo,
                "linea": linea,
                "columna": columna,
                "caracter": caracter,
                "token_esperado": token_esperado,
                "descripcion": descripcion
            })

        estado = 'INICIO'
        palabra_esperada = None

        for token in tokens:
            if estado == 'INICIO':
                if token.tipo == 'Reservada':
                    if token.contenido not in self.palabras_reservadas:
                        agregar_error("Sintactico", token.linea, token.columna, token.contenido, None,
                                      f"Palabra reservada incorrecta: {token.contenido}")
                elif token.tipo == 'Parentesis_A':
                    estado = 'INSIDE_FUNC'
                    palabra_esperada = 'Reservada'
                elif token.tipo == 'Parentesis_C' or token.tipo == 'Llave_C':
                    agregar_error("Sintactico", token.linea, token.columna, token.contenido, token.contenido,
                                  f"Símbolo de cierre '{token.contenido}' inesperado")
            elif estado == 'INSIDE_FUNC':
                if token.tipo == palabra_esperada:
                    estado = 'AFTER_FUNC'
                    palabra_esperada = 'Parentesis_C' if token.contenido == '(' else 'Parentesis_A'
                elif token.tipo == 'Parentesis_A':
                    agregar_error("Sintactico", token.linea, token.columna, token.contenido, palabra_esperada,
                                  f"Se esperaba '{palabra_esperada}' en lugar de '{token.contenido}'")
                elif token.tipo == 'Parentesis_C' or token.tipo == 'Llave_C':
                    agregar_error("Sintactico", token.linea, token.columna, token.contenido, token.contenido,
                                  f"Símbolo de cierre '{token.contenido}' inesperado")
            elif estado == 'AFTER_FUNC':
                if token.tipo == palabra_esperada:
                    estado = 'INICIO'
                    palabra_esperada = None
                elif token.tipo == 'Parentesis_A':
                    agregar_error("Sintactico", token.linea, token.columna, token.contenido, palabra_esperada,
                                  f"Se esperaba '{palabra_esperada}' en lugar de '{token.contenido}'")
                elif token.tipo == 'Parentesis_C' or token.tipo == 'Llave_C':
                    agregar_error("Sintactico", token.linea, token.columna, token.contenido, token.contenido,
                                  f"Símbolo de cierre '{token.contenido}' inesperado")

        return errores_sintacticos
