def traducir_comandos(texto_nosql):
    lineas = texto_nosql.split('\n')
    traduccion_mongodb = []
    errores = []

    for linea in lineas:
        if not linea.strip():  # Ignorar líneas vacías
            continue
        
        if 'nueva' not in linea:
            errores.append(f"Error de sintaxis en la línea '{linea}': debe comenzar con 'nueva'.")
            continue
        
        partes = linea.split('nueva')[1].split('(')
        funcion = partes[0].strip()
        argumentos_str = partes[1].strip().rstrip(');').strip('""')

        traduccion = ""  # Inicializa la variable traduccion en cada iteración

        if funcion == 'CrearBD':
            traduccion = f"db = use('{argumentos_str}');"
        elif funcion == 'EliminarBD':
            traduccion = f"db.dropDataBase('{argumentos_str}');"
        elif funcion == 'CrearColeccion':
            traduccion = f"db.createCollection('{argumentos_str}');"
        elif funcion == 'EliminarColeccion':
            traduccion = f"db.{argumentos_str}.drop();"
        elif funcion == 'InsertarUnico':
            traduccion = f"db.{argumentos_str.split(',')[0]}.insertOne({argumentos_str.split(',')[1]});"
        elif funcion == 'ActualizarUnico':
            traduccion = f"db.{argumentos_str.split(',')[0]}.updateOne({argumentos_str.split(',')[1]}, {argumentos_str.split(',')[2]});"
        elif funcion == 'EliminarUnico':
            traduccion = f"db.{argumentos_str.split(',')[0]}.deleteOne({argumentos_str.split(',')[1]});"
        elif funcion == 'BuscarTodo':
            traduccion = f"db.{argumentos_str}.find();"
        elif funcion == 'BuscarUnico':
            traduccion = f"db.{argumentos_str}.findOne();"
        else:
            errores.append(f"Error: Función '{funcion}' no reconocida en la línea '{linea}'.")

        traduccion_mongodb.append(traduccion)

    return '\n'.join(traduccion_mongodb), errores
