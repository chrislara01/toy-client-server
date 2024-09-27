import socket
import random
import json

PUERTO = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PUERTO)
HEADER = 128
FORMATO = 'utf-8'
JUEGO_LISTO = "JUEGO-CREADO"
JUEGO_GANADO = "GANASTE"
DESCONECTAR_MENSAJE = "Desconectar!"

# Genera numero aleatorio de 2 cifras que solo contenga 1,2 y 3 
def generar_numero_secreto():
    unidades = random.randint(1,3)
    decenas = random.randint(1,3)
    numero_generado = str(decenas) + str(unidades)
    return numero_generado

#  Funcion auxiliar para calcular los toros y vacas para la pista
#  Esta funcion sirve para cualesquiera 2 numeros de 
# igual longitud, para cualquiera longitud que tengan 
def procesar_pista(propuesta, numero):
    toros = 0
    vacas = 0

    idx = 0

    # Garantizar que los numeros esten representados como tipo string
    numero = str(numero)
    propuesta = str(propuesta)

    # Comprobar los toros
    for digito_propuesta, digito_numero in zip(propuesta, numero):
        if digito_propuesta == digito_numero:
            toros+=1
            #  Eliminar las posiciones que coinciden para evitar 
            # solapamiento al calcular las vacas
            propuesta = propuesta[:idx] + propuesta[(idx+1):]
            numero = numero[:idx] + numero[(idx+1):]
        idx+=1
    
    # Comprobar las vacas
    for i in range(len(numero)):
        if propuesta[i] in numero:
            vacas+=1
            numero = numero.replace(propuesta[i],"",1)
        
    return {"Toro": toros, "Vaca": vacas}

# Funcion auxiliar para devolver un string en formato json
def crear_json(tipo, contenido):
    diccionario = {"tipo": tipo, "contenido": contenido}
    return json.dumps(diccionario)

# Funcion auxiliar para enviar mensajes al cliente
def enviar(msg):
    mensaje = msg.encode(FORMATO)
    longitud_mensaje = len(mensaje)
    longitud_envio = str(longitud_mensaje).encode(FORMATO)
    longitud_envio += b' ' * (HEADER - len(longitud_envio))
    cliente_socket.send(longitud_envio)
    cliente_socket.send(mensaje)

# Funcion auxiliar para recibir mensajes del cliente
def recibir():
    mensaje = {}

    longitud_mensaje = cliente_socket.recv(HEADER).decode(FORMATO)
    if longitud_mensaje:
        longitud_mensaje = int(longitud_mensaje)
        mensaje = json.loads(cliente_socket.recv(longitud_mensaje).decode(FORMATO))
    
    return mensaje


# Crear socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
    servidor_socket.bind(ADDR)
    print("El servidor se esta iniciando...")

    servidor_socket.listen(1)
    print(f"Servidor escuchando en {SERVER}:{PUERTO}")

    # Esperar conexión
    cliente_socket, direccion_cliente = servidor_socket.accept()
    print("Conexión establecida desde", direccion_cliente)

    # Generar número secreto
    numero_secreto = generar_numero_secreto()

    # Enviar mensaje inicial
    mensaje_inicial = crear_json("estado", JUEGO_LISTO)
    enviar(mensaje_inicial)

    while True:
        # Recibir mensaje del cliente
        mensaje = recibir()

        if mensaje["tipo"] == "proposicion":
            digitos_propuestos = mensaje["contenido"]
            
            if digitos_propuestos == numero_secreto:
                respuesta = crear_json("estado", JUEGO_GANADO)
            else:
                pista = procesar_pista(digitos_propuestos, numero_secreto)
                respuesta = crear_json("pista", pista)
            
            enviar(respuesta)
        elif mensaje["tipo"] == "estado":
            if mensaje["contenido"] == DESCONECTAR_MENSAJE:
                break

print("Conexión finalizada")