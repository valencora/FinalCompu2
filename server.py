import asyncio
import websockets
import json
import random


clientes_conectados = set()

usuarios_conectados = set()

async def manejar_cliente(websocket):
    global clientes_conectados, usuarios_conectados
    clientes_conectados.add(websocket)

    usuario = None  
    try:
        
        mensaje_inicial = await websocket.recv()
        data_usuario = json.loads(mensaje_inicial)
        usuario = data_usuario.get("usuario")
        
       
        if usuario in usuarios_conectados:
            nuevo_sufijo = str(random.randint(100, 999))
            usuario = usuario + nuevo_sufijo
        usuarios_conectados.add(usuario)
        

        
        await enviar_a_todos(f"🔔 {usuario} se ha unido al chat.", "sistema")

        # Escuchar mensajes del cliente
        async for mensaje in websocket:
            data = json.loads(mensaje)
            texto = data.get("mensaje", "")
            await enviar_a_todos(f"{usuario}: {texto}")

    except websockets.exceptions.ConnectionClosed:
        print(f"❌ {usuario} se ha desconectado.")
    finally:
        clientes_conectados.remove(websocket)
        if usuario is not None and usuario in usuarios_conectados:
            usuarios_conectados.remove(usuario)
        await enviar_a_todos(f"❌ {usuario} ha salido del chat.", "sistema")


async def enviar_a_todos(mensaje, tipo="mensaje"):
    """ Envía un mensaje a todos los clientes conectados """
    if clientes_conectados:
        data = json.dumps({"tipo": tipo, "mensaje": mensaje})
        await asyncio.gather(
            *(cliente.send(data) for cliente in clientes_conectados),
            return_exceptions=True
        )

async def main(host, port):
    print(f"📡 Servidor de chat iniciado en ws://{host}:{port}")
    server = await websockets.serve(manejar_cliente, host, port)
    await server.wait_closed()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Servidor de chat con websockets")
    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="Dirección IP del servidor (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Puerto del servidor (default: 8000)")
    args = parser.parse_args()

    asyncio.run(main(args.host, args.port))
