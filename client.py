import socket
import json

PUERTO = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PUERTO)
HEADER = 128
FORMATO = 'utf-8'
JUEGO_LISTO = "JUEGO-CREADO"
JUEGO_GANADO = "GANASTE"
DESCONECTAR_MENSAJE = "Desconectar!" 

# Para generar todos los numeros de 2 digitos que solo contienen 1,2 y 3
def generar_combinaciones():
    return [f"{num1}{num2}" for num1 in range(1, 4) for num2 in range(1, 4)]

# Funcion auxiliar para dar formato a la respuesta
def procesar_pista(respuesta):
    toros = respuesta["contenido"]["Toro"]
    vacas = respuesta["contenido"]["Vaca"]
    return f"Toro: {toros}, Vaca: {vacas}"

# Funcion auxiliar para devolver un string en formato json
def crear_json(tipo, contenido):
    diccionario = {"tipo": tipo, "contenido": contenido}
    return json.dumps(diccionario)

# Funcion auxiliar par enviar mensajes al servidor
def enviar(msg):
    mensaje = msg.encode(FORMATO)
    longitud_mensaje = len(mensaje)
    longitud_envio = str(longitud_mensaje).encode(FORMATO)
    longitud_envio += b' ' * (HEADER - len(longitud_envio))
    cliente_socket.send(longitud_envio)
    cliente_socket.send(mensaje)

# Funcion auxiliar para recibir mesajes del servidor
def recibir():
    mensaje = {}

    longitud_mensaje = cliente_socket.recv(HEADER).decode(FORMATO)
    if longitud_mensaje:
        longitud_mensaje = int(longitud_mensaje)
        mensaje = json.loads(cliente_socket.recv(longitud_mensaje).decode(FORMATO))
    
    return mensaje



# Crear socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
    cliente_socket.connect(ADDR)

    print("Conectando al servidor...")

    mensaje_inicial = recibir()
    if mensaje_inicial:
        if mensaje_inicial["contenido"] == JUEGO_LISTO:
            print("Ya el juego esta listo!")

            combinaciones = generar_combinaciones()
                
            for combinacion in combinaciones:
                intento = crear_json("proposicion", combinacion)
                enviar(intento)
                
                respuesta = recibir()
                
                if respuesta["tipo"] == "pista":
                    pista = procesar_pista(respuesta)
                    print(pista)
                    
                elif respuesta["tipo"] == "estado":
                    if respuesta["contenido"] == JUEGO_GANADO:
                        print("Felicidades, has ganado!!!")
                        enviar(crear_json("estado", DESCONECTAR_MENSAJE))
                        break
    else:
        print("Error en el servidor. Terminando sesion...")