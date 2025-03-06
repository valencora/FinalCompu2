import asyncio
import socket
import websockets
import json
import random
import argparse
from multiprocessing import Process, Queue
import sqlite3 

clientes_conectados = set()
usuarios_conectados = set()

async def manejar_cliente(websocket):
    global clientes_conectados, usuarios_conectados, persist_queue
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

        async for mensaje in websocket:
            data = json.loads(mensaje)
            texto = data.get("mensaje", "")
            
            await enviar_a_todos(f"{usuario}: {texto}", sender=websocket)
            
            if persist_queue:
                persist_queue.put((usuario, texto))

    except websockets.exceptions.ConnectionClosed:
        print(f"❌ {usuario} se ha desconectado.")
    finally:
        clientes_conectados.remove(websocket)
        if usuario in usuarios_conectados:
            usuarios_conectados.remove(usuario)
        await enviar_a_todos(f"❌ {usuario} ha salido del chat.", "sistema")

async def enviar_a_todos(mensaje, tipo="mensaje", sender=None):
    if clientes_conectados:
        data = json.dumps({"tipo": tipo, "mensaje": mensaje})
        await asyncio.gather(
            *(cliente.send(data) for cliente in clientes_conectados if cliente != sender),
            return_exceptions=True
        )

async def main(host, port):
    print(f"📡 Servidor de chat iniciado en ws://{host}:{port}")
    addrinfo = socket.getaddrinfo(host, port, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
    af, socktype, proto, canonname, sa = addrinfo[0]

    sock = socket.socket(af, socktype, proto)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if af == socket.AF_INET6:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    sock.bind(sa)
    sock.listen()
    sock.setblocking(False)
    server = await websockets.serve(manejar_cliente, host=None, port=None, sock=sock)
    await server.wait_closed()


def persist_worker(queue: Queue):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            mensaje TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    while True:
        data = queue.get()
        if data is None:
            break
        usuario, mensaje = data
        try:
            cursor.execute('INSERT INTO mensajes (usuario, mensaje) VALUES (?, ?)', (usuario, mensaje))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar mensaje en la base de datos: {e}")

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Servidor de chat con websockets y persistencia en SQLite"
    )
    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="Dirección IP del servidor (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Puerto del servidor (default: 8000)")
    args = parser.parse_args()

    persist_queue = Queue()
    persistencia_proceso = Process(target=persist_worker, args=(persist_queue,))
    persistencia_proceso.start()

    try:
        asyncio.run(main(args.host, args.port))
    finally:
        persist_queue.put(None)
        persistencia_proceso.join()
