### INFO.md

```markdown
# Informe de Diseño

Este documento describe las principales decisiones de diseño para el sistema de chat en vivo.

## Arquitectura del Sistema

El sistema se compone de tres componentes principales:
- **Cliente:**  
  Implementado en Python, utiliza la librería `websockets` y `asyncio` para establecer conexiones en tiempo real.
- **Servidor:**  
  Utiliza `websockets` y `asyncio` para gestionar múltiples clientes, validar nombres de usuario y difundir mensajes (broadcast).
- **Persistencia:**  
  Se implementa en un proceso separado mediante `multiprocessing`. Un proceso dedicado (persist_worker) recibe mensajes desde el servidor a través de una cola (Queue) y los inserta en una base de datos SQLite.

## Decisiones de Diseño

- **Uso de WebSockets y Asyncio:**  
  Se eligieron para facilitar la comunicación bidireccional en tiempo real, permitiendo manejar múltiples clientes sin bloquear el servidor.
  
- **Multiprocessing para la Persistencia:**  
  La persistencia en SQLite es bloqueante. Para evitar que las operaciones de E/S ralenticen el servidor, se delega en un proceso separado que se comunica mediante una cola.
  
- **Validación de Nombres de Usuario:**  
  Se implementa para garantizar que cada cliente tenga un identificador único, añadiendo un sufijo aleatorio si un nombre ya está en uso.
  
- **Soporte Dual-Stack:**  
  Se configura el socket con `AF_UNSPEC` y se ajusta para desactivar `IPV6_V6ONLY` en caso de usar IPv6, lo que permite aceptar conexiones tanto de IPv4 como de IPv6.

## Justificación del Modelo de Datos

- **SQLite:**  
  Se utiliza por su simplicidad, facilidad de integración y porque es suficiente para la escala del proyecto.
- **Tabla de Mensajes:**  
  Se registra el usuario, el mensaje y la marca de tiempo, proporcionando un historial cronológico sencillo de las conversaciones.


