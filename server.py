import asyncio
import websockets
import json


clientes_conectados = set()

async def manejar_cliente(websocket):
    """ Maneja la conexión de cada cliente y retransmite mensajes """
    clientes_conectados.add(websocket)
    # print(f" Nuevo cliente conectado. Total clientes: {len(clientes_conectados)}") 

    try:
        # Recibir el nombre del usuario
        mensaje_inicial = await websocket.recv()
        data_usuario = json.loads(mensaje_inicial)
        usuario = data_usuario.get("usuario")

       # print(f" {usuario} se ha conectado. Clientes conectados: {len(clientes_conectados)}")  

        # Notificar a todos los clientes
        await enviar_a_todos(f"🔔 {usuario} se ha unido al chat.", "sistema")

        # Escuchar mensajes del cliente
        async for mensaje in websocket:
            # print(f" Mensaje recibido de {usuario}: {mensaje}") 
            data = json.loads(mensaje)
            texto = data.get("mensaje", "")

            
            await enviar_a_todos(f"{usuario}: {texto}")

    except websockets.exceptions.ConnectionClosed:
        print(f"❌ {usuario} se ha desconectado.")
    finally:
        clientes_conectados.remove(websocket)
        # print(f" Clientes conectados después de desconexión: {len(clientes_conectados)}")  
        await enviar_a_todos(f"❌ {usuario} ha salido del chat.", "sistema")


async def enviar_a_todos(mensaje, tipo="mensaje"):
    """ Envía un mensaje a todos los clientes conectados """
    if clientes_conectados:
        data = json.dumps({"tipo": tipo, "mensaje": mensaje})
        # print(f" Enviando mensaje a todos: {data}")  
        # Se envía el mensaje a todos los clientes de forma concurrente
        await asyncio.gather(
            *(cliente.send(data) for cliente in clientes_conectados),
            return_exceptions=True
        )



async def main():
    print("📡 Servidor de chat iniciado en ws://localhost:8000")
    server = await websockets.serve(manejar_cliente, "localhost", 8000)
    await server.wait_closed()

asyncio.run(main())
