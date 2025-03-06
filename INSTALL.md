# Instalación y Despliegue

## Requisitos

- Python 3.10 o superior.
- Librería `websockets` (se puede instalar con `pip install websockets`).

## Clonar el repositorio

```bash
git clone https://github.com/valencora/FinalCompu2
cd FinalCompu2
```
### Luego ejecutar

./install.sh

Para crear el entorno virtual y descargar las librerias.

### Iniciar el Servidor
```bash

python3 server.py --host 127.0.0.1 --port 8000
python3 server.py --host "::" --port 8000
```
### Conectar un cliente
```bash
python3 client.py --uri ws://127.0.0.1:8000 --usuario nombreDeUsuario
python3 client.py --uri ws://[::1]:8000 --usuario nombreDeUsuario
```
