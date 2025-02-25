import asyncio
import websockets
import json

async def chat():
    usuario = input("Ingrese su nombre de usuario: ")

    async with websockets.connect("ws://localhost:8000") as websocket:
        print("✅ Conectado al chat en vivo.")

        # Enviar nombre de usuario al servidor
        await websocket.send(json.dumps({"usuario": usuario}))
        

        async def recibir_mensajes():
            print("🕐 Esperando mensajes del servidor...")
            while True:
                try:
                    mensaje = await websocket.recv()
                    
                    data = json.loads(mensaje)
                    print(f"\n💬 {data['mensaje']}")
                except websockets.exceptions.ConnectionClosed:
                    print("❌ Se perdió la conexión con el servidor.")
                    break

        async def enviar_mensajes():
            loop = asyncio.get_event_loop()
            while True:
                texto = await loop.run_in_executor(None, input, "")
                data = {"usuario": usuario, "mensaje": texto}
                await websocket.send(json.dumps(data))


        await asyncio.gather(recibir_mensajes(), enviar_mensajes())

asyncio.run(chat())
