import socket
import random
import json

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

# Crear socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
    servidor_socket.bind(('localhost', 12345))
    servidor_socket.listen(1)
    print("Servidor escuchando en localhost:12345")

    # Esperar conexión
    cliente_socket, direccion_cliente = servidor_socket.accept()
    print("Conexión establecida desde", direccion_cliente)

    # Generar número secreto
    numero_secreto = generar_numero_secreto()

    # Enviar mensaje inicial
    mensaje_inicial = {"tipo": "estado", "contenido": "JUEGO-CREADO"}
    cliente_socket.send(json.dumps(mensaje_inicial).encode())

    while True:
        # Recibir mensaje del cliente
        mensaje_recibido = cliente_socket.recv(1024).decode()
        if not mensaje_recibido:
            break
        
        mensaje = json.loads(mensaje_recibido)
        
        if mensaje["tipo"] == "proposicion":
            digitos_propuestos = mensaje["contenido"]
            
            pista = procesar_pista(digitos_propuestos, numero_secreto)
            
            if digitos_propuestos == numero_secreto:
                respuesta = {"tipo": "estado", "contenido": "GANASTE"}
            else:
                respuesta = {"tipo": "pista", "pistas": pista}
            
            cliente_socket.send(json.dumps(respuesta).encode())

print("Conexión finalizada")