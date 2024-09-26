import socket
import json

# Para generar todos los numeros de 2 digitos que solo contienen 1,2 y 3
def generar_combinaciones():
    return [f"{num1}{num2}" for num1 in range(1, 4) for num2 in range(1, 4)]

# Funcion auxiliar para dar formato a la respuesta
def procesar_pista(respuesta):
    toros = respuesta["pistas"]["Toro"]
    vacas = respuesta["pistas"]["Vaca"]
    return f"Toro: {toros}, Vaca: {vacas}"

# Crear socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
    cliente_socket.connect(('localhost', 12345))

    print("Conectando al servidor...")

    mensaje_inicial = json.loads(cliente_socket.recv(1024).decode())
    
    if mensaje_inicial:
        print(mensaje_inicial["contenido"])

        combinaciones = generar_combinaciones()
            
        for combinacion in combinaciones:
            intento = {"tipo": "proposicion", "contenido": combinacion}
            cliente_socket.send(json.dumps(intento).encode())
            
            respuesta = json.loads(cliente_socket.recv(1024).decode())
            
            if respuesta["tipo"] == "pista":
                pista = procesar_pista(respuesta)
                print(pista)
                
            elif respuesta["tipo"] == "estado":
                if respuesta["contenido"] == "GANASTE":
                    print("Felicidades, has ganado!!!")
                    break