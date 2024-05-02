from Tokens import Token

class AnalizadorLexicoSintactico:
    def __init__(self):
        self.tokens = []
        self.errores_lexicos = []
        self.errores_sintacticos = []
        self.caracteres_validos = ['{', '}', '"', '“', '”', ',', ':', '=', ';', '-', '*', '/']
        self.palabras_reservadas = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                                    'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']
        self.analizador_sintactico = AnalizadorSintactico()

    def agregarError(self, tipo, linea, columna, caracter=None, token_esperado=None, descripcion=None):
        self.errores_lexicos.append({
            "tipo": tipo,
            "linea": linea,
            "columna": columna,
            "caracter": caracter,
            "token_esperado": token_esperado,
            "descripcion": descripcion
        })

    def agregarToken(self, tipo, token, linea, columna):
        self.tokens.append(Token(tipo, token, linea, columna))

    def analizar(self, cadena):
        estado = 0
        buffer = ''
        linea = 1
        columna = 1
        i = 0

        while i < len(cadena):
            caracter = cadena[i]

            if estado == 0:
                if caracter == '-':
                    estado = 1
                    buffer += caracter
                elif caracter == '/':
                    estado = 6
                    buffer += caracter
                elif caracter.isalpha():
                    estado = 11
                    buffer += caracter
                elif caracter == '=':
                    estado = 12
                    buffer += caracter
                elif caracter == '(':
                    estado = 13
                    buffer += caracter
                elif caracter == ')':
                    estado = 14
                    buffer += caracter
                elif caracter == ';':
                    estado = 15
                    buffer += caracter
                elif caracter == ',':
                    estado = 16
                    buffer += caracter
                elif caracter == '"':
                    estado = 17
                    buffer += caracter
                elif caracter in [' ']:
                    pass
                elif caracter == '\n':
                    linea += 1
                    columna = 1
                elif caracter == '#':
                    pass
                elif caracter not in self.caracteres_validos:
                    self.agregarError('Léxico', linea, columna, caracter, descripcion=f"Carácter no reconocido: {caracter}")
                    estado = 0
                    buffer = ''

            elif estado == 1:
                if caracter == '-':
                    estado = 2
                    buffer += caracter
                else:
                    self.agregarError('Léxico', linea, columna, buffer, "Se esperaba un '-'")
                    estado = 0
                    buffer = ''

            elif estado == 2:
                if caracter == '-':
                    estado = 3
                    buffer += caracter
                else:
                    self.agregarError('Léxico', linea, columna, buffer, "Se esperaba un segundo '-'")
                    estado = 0
                    buffer = ''

            elif estado == 3:
                if caracter != '\n':
                    estado = 4
                    buffer += caracter
                else:
                    estado = 5
                    linea += 1
                    columna = 1

            elif estado == 4:
                if caracter != '\n':
                    buffer += caracter
                else:
                    estado = 5
                    linea += 1
                    columna = 1

            elif estado == 5:
                self.agregarToken('Comentario', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 6:
                if caracter == '*':
                    estado = 7
                    buffer += caracter
                else:
                    self.agregarError('Léxico', linea, columna, buffer, "Se esperaba un '*'")
                    estado = 0
                    buffer = ''

            elif estado == 7:
                if caracter != '*':
                    estado = 8
                    buffer += caracter
                else:
                    estado = 9
                    buffer += caracter

            elif estado == 8:
                if caracter != '*':
                    buffer += caracter
                else:
                    estado = 9
                    buffer += caracter

            elif estado == 9:
                if caracter != '/':
                    estado = 8
                    buffer += caracter
                else:
                    estado = 10
                    buffer += caracter

            elif estado == 10:
                self.agregarToken('Comentario', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 11:
                if caracter.isalpha():  
                    buffer += caracter
                    columna += 1  # Incrementa la columna para cada carácter alfanumérico
                else:
                    if buffer in self.palabras_reservadas:
                        self.agregarToken(f'Reservada_{buffer}', buffer, linea, columna - len(buffer))
                        buffer = ''
                        estado = 0
                    else:
                        self.agregarToken('Identificador', buffer, linea, columna - len(buffer))
                        buffer = ''
                        estado = 0
                    continue

            elif estado == 12:
                self.agregarToken('Igual', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 13:
                self.agregarToken('Parentesis_A', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 14:
                self.agregarToken('Parentesis_C', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 15:
                self.agregarToken('Punto_Comma', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 16:
                self.agregarToken('Coma', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 17:
                if caracter == '"':
                    estado = 19
                    buffer += caracter
                elif caracter == '{':
                    estado = 21  # Cambiar al estado 21 para manejar el contenido entre llaves como un solo token
                    buffer += caracter  # Agregar la llave de apertura al buffer
                elif caracter == '}':
                    self.agregarToken('Llave_C', caracter, linea, columna)  # Agregar el token de llave cerrada
                elif caracter in ['“', '”', ':', ',', ';']:
                    self.agregarToken('Caracter_Especial', caracter, linea, columna)
                elif caracter == '\n':
                    linea += 1
                    columna = 1
                elif caracter.isspace():
                    tokens_dentro_comillas = buffer.split()
                    for token in tokens_dentro_comillas:
                        if token in self.palabras_reservadas:
                            self.agregarToken(f'Reservada_{token}', token, linea, columna - len(token))
                        else:
                            self.agregarToken('Identificador', token, linea, columna - len(token))
                    buffer = ''
                else:
                    buffer += caracter

            elif estado == 18:
                if caracter in ['"', '”']:
                    estado = 19
                    buffer += caracter
                else:
                    buffer += caracter

            elif estado == 19:
                self.agregarToken('Cadena', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 20:
                if caracter != '}':
                    buffer += caracter
                else:
                    self.agregarToken('Cadena', buffer.strip(), linea, columna - len(buffer))  # Agregar el token de cadena
                    self.agregarToken('Llave_C', caracter, linea, columna)  # Agregar el token de llave cerrada
                    estado = 0

            elif estado == 21:
                buffer += caracter
                if caracter == '}':
                    self.agregarToken('Cadena', buffer.strip(), linea, columna - len(buffer))  # Agregar el token de cadena
                    estado = 0

            i += 1

        self.analizador_sintactico.analizar_sintacticamente(self.tokens)

        return self.tokens, self.errores_lexicos, self.errores_sintacticos
    
class NoSQLToMongoDBTranslator:

    def traducir(self, texto_nosql):
        lineas = texto_nosql.split('\n')
        comandos_mongodb = []
        errores = []

        for linea in lineas:
            linea = linea.strip()
            if linea:
                # Aquí se maneja cada línea individualmente
                resultado = self.traducir_linea(linea)
                if isinstance(resultado, str):
                    comandos_mongodb.append(resultado)
                elif isinstance(resultado, tuple):
                    comando, error = resultado
                    if comando:
                        comandos_mongodb.append(comando)
                    if error:
                        if isinstance(error, str):
                            errores.append(error)
                        elif isinstance(error, dict):
                            errores.append(error["descripcion"])

        # Convertir la lista de comandos en una cadena
        comandos_str = '\n'.join([str(item) for item in comandos_mongodb])

        # Unir los errores en una cadena
        errores_str = '\n'.join(errores)

        return comandos_str, errores_str

    def procesar_linea(self, linea):
        # Si la línea termina con ';', la procesamos normalmente
        if linea.endswith(';'):
            return self.traducir_linea(linea)
        else:
            # Si la línea no termina con ';', la concatenamos con la siguiente línea
            # hasta encontrar una que sí termine con ';'
            linea_concatenada = linea
            siguiente_linea = self.obtener_siguiente_linea()
            while siguiente_linea and not siguiente_linea.strip().endswith(';'):
                linea_concatenada += siguiente_linea.strip()
                siguiente_linea = self.obtener_siguiente_linea()

            # Una vez que tenemos la línea completa, la procesamos
            return self.traducir_linea(linea_concatenada)

    def traducir_linea(self, linea):
        # Identificar el tipo de comando NoSQL
        if linea.startswith('CrearBD'):
            return self.traducir_crear_bd(linea)
        elif linea.startswith('EliminarBD'):
            return self.traducir_eliminar_bd(linea)
        elif linea.startswith('CrearColeccion'):
            return self.traducir_crear_coleccion(linea)
        elif linea.startswith('EliminarColeccion'):
            return self.traducir_eliminar_coleccion(linea)
        elif 'InsertarUnico' in linea:
            return self.traducir_insertar_unico(linea)
        elif 'ActualizarUnico' in linea:
            return self.traducir_actualizar_unico(linea)
        elif 'EliminarUnico' in linea:
            return self.traducir_eliminar_unico(linea)
        elif 'BuscarTodo' in linea:
            return self.traducir_buscar_todo(linea)
        elif 'BuscarUnico' in linea:
            return self.traducir_buscar_unico(linea)
        # Manejo de comentarios
        elif linea.startswith('//') or linea.startswith('#'):
            return self.traducir_comentario_una_linea(linea)
        elif linea.startswith('/*'):
            return self.traducir_comentario_multilinea(linea.split('\n'))
        else:
            # Devolver error sintáctico
            return None, {"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"}


    
    def obtener_nombre_variable(self, linea):
        partes = linea.split()
        if len(partes) >= 2:
            return partes[1].strip('();')
        else:
            return None
    def traducir_crear_bd(self, linea):
            nombre_variable = self.obtener_nombre_variable(linea)
            if nombre_variable:
                return f'db = use("{nombre_variable}");', None
            else:
                return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer el nombre de la base de datos."}

    def traducir_eliminar_bd(self, linea):
        nombre_variable = self.obtener_nombre_variable(linea)
        if nombre_variable:
            return f'db.dropDatabase("{nombre_variable}");', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer el nombre de la base de datos."}

    def traducir_crear_coleccion(self, linea):
        # Extraer el nombre de la colección manualmente
        partes = linea.split('"')
        if len(partes) >= 2:
            nombre_coleccion = partes[1]
            return f'db.createCollection("{nombre_coleccion}");', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer el nombre de la colección."}

    def traducir_eliminar_coleccion(self, linea):
        # Extraer el nombre de la colección manualmente
        partes = linea.split('"')
        if len(partes) >= 2:
            nombre_coleccion = partes[1]
            return f'db.{nombre_coleccion}.drop();', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer el nombre de la colección."}

    def traducir_insertar_unico(self, linea):
        # Extraer el nombre de la colección y los datos JSON manualmente
        partes = linea.split('"')
        if len(partes) >= 4:
            nombre_coleccion = partes[1]
            datos_json = linea[linea.find('{') + 1:linea.rfind('}')]
            return f'db.{nombre_coleccion}.insertOne({datos_json});', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer la información necesaria para insertar un documento."}

    def traducir_actualizar_unico(self, linea):
        # Extraer el nombre de la colección, el filtro y la actualización JSON manualmente
        partes = linea.split('"')
        if len(partes) >= 6:
            nombre_coleccion = partes[1]
            filtro = partes[3].strip()
            actualizacion = partes[5].strip()
            return f'db.{nombre_coleccion}.updateOne({filtro},{actualizacion});', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer la información necesaria para actualizar un documento."}

    def traducir_eliminar_unico(self, linea):
        # Extraer el nombre de la colección y el filtro JSON manualmente
        partes = linea.split('"')
        if len(partes) >= 4:
            nombre_coleccion = partes[1]
            filtro = partes[3].strip()
            return f'db.{nombre_coleccion}.deleteOne({filtro});', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer la información necesaria para eliminar un documento."}

    def traducir_buscar_todo(self, linea):
        # Extraer el nombre de la colección manualmente
        partes = linea.split('"')
        if len(partes) >= 2:
            nombre_coleccion = partes[1]
            return f'db.{nombre_coleccion}.find();', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer el nombre de la colección."}

    def traducir_buscar_unico(self, linea):
        # Extraer el nombre de la colección manualmente
        partes = linea.split('"')
        if len(partes) >= 2:
            nombre_coleccion = partes[1]
            return f'db.{nombre_coleccion}.findOne();', None
        else:
            return None, {"tipo": "Error sintáctico", "descripcion": "No se pudo extraer el nombre de la colección."}
        
    def traducir_comentario_una_linea(self, linea):
            return f'# {linea[3:].strip()}', None

    def traducir_comentario_multilinea(self, lineas):
        comentario = []
        for linea in lineas:
            if linea.startswith('/*'):
                comentario.append(linea[linea.find('/*') + 2:])
            elif '*/' in linea:
                comentario.append(linea[:linea.find('*/')])
                break
            else:
                comentario.append(linea)
        return "''' " + ' '.join(comentario) + " '''", None

class AnalizadorSintactico:
    def __init__(self):
        self.errores_sintacticos = []
        self.palabras_reservadas = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                                    'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']

    def agregarError(self, tipo, linea, columna, caracter=None, token_esperado=None, descripcion=None):
        self.errores_sintacticos.append({
            "tipo": tipo,
            "linea": linea,
            "columna": columna,
            "caracter": caracter,
            "token_esperado": token_esperado,
            "descripcion": descripcion
        })

    def analizar_sintacticamente(self, tokens):
        for token in tokens:
            if token.tipo.startswith('Reservada'):
                if token.contenido not in self.palabras_reservadas:
                    self.agregarError('Sintáctico', token.linea, token.columna,
                                      caracter=token.contenido,
                                      token_esperado="Palabra reservada válida",
                                      descripcion=f"Palabra reservada incorrecta: {token.contenido}")


