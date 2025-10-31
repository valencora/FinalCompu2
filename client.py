import argparse
import asyncio
import websockets
import json

async def chat(uri, usuario):
    async with websockets.connect(uri) as websocket:
        print("✅ Conectado al chat en vivo.")

        await websocket.send(json.dumps({"usuario": usuario}))

        async def recibir_mensajes():
            print("🕐 Esperando mensajes del servidor...")
            while True:
                try:
                    mensaje = await websocket.recv()
                    data = json.loads(mensaje)
                    print(f"\n💬 {data['mensaje']}")
                except websockets.exceptions.ConnectionClosed:
                    print("❌ See perdió la conexión con el servidor.")
                    break

        async def enviar_mensajes():
            loop = asyncio.get_event_loop()
            while True:
                texto = await loop.run_in_executor(None, input, "")
                data = {"usuario": usuario, "mensaje": texto}
                await websocket.send(json.dumps(data))

        await asyncio.gather(recibir_mensajes(), enviar_mensajes())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente de chat con websockets")
    parser.add_argument("--uri", type=str, default="ws://127.0.0.1:8000",
                        help="URI del servidor (default: ws://127.0.0.1:8000)")
    parser.add_argument("--usuario", type=str, required=True,
                        help="Nombre de usuario para el chat")
    args = parser.parse_args()

    
    asyncio.run(chat(args.uri, args.usuario))
