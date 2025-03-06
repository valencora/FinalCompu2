# Chat en Vivo con WebSockets

Este proyecto es una aplicación de chat en vivo que permite la comunicación en tiempo real entre múltiples clientes a través de un servidor asyncio basado en WebSockets.

## Características

- **Comunicación en tiempo real:**  
  Utiliza WebSockets para una comunicación persistente y bidireccional.
- **Concurrencia asíncrona:**  
  Se implementa con `asyncio` para gestionar múltiples conexiones de forma concurrente.
- **Validación de nombres de usuario:**  
  Garantiza unicidad de nombres, añadiendo un sufijo si es necesario.
- **Persistencia de mensajes:**  
  Se almacena en una base de datos SQLite a través de un proceso separado (usando `multiprocessing` y una cola de mensajes).
- **Soporte dual-stack:**  
  El servidor está configurado para aceptar conexiones tanto IPv4 como IPv6.

## Uso Básico

### Iniciar el Servidor
```bash

python3 server.py --host 127.0.0.1 --port 8000
python3 server.py --host "::" --port 8000
```
### Conectar un cliente
```bash
python3 client.py --uri ws://127.0.0.1:8000 --usuario nombreDeUsuario
python3 client.py --uri ws://[::1]:8000 --usuario nombreDeUsuario

