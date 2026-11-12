# santisantos_practica_3_as

**Autor:** Santiago Santos

## Descripcion

API REST de una tienda online hecha en python con fastapi. Es el codigo de la practica 2: permite gestionar usuarios (clientes y administradores), productos (genericos, electronicos y ropa) y pedidos usando la clase TiendaService de la practica 1.

## Estructura

```
src/
  main.py            -> endpoints de la api
  schemas.py         -> esquemas pydantic
  models/            -> clases producto, usuario y pedido
  services/          -> TiendaService
requirements.txt
```

## Ejecutar en local

```bash
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

La documentacion de la api queda en http://localhost:8000/docs

## Docker

### Construir la imagen

Desde la raiz del repositorio:

```bash
docker build -t tienda-api:1.0 .
```

### Ejecutar el contenedor

```bash
docker run -d --name tienda-api -p 8000:8000 tienda-api:1.0
```

Para usar otro puerto dentro del contenedor:

```bash
docker run -d --name tienda-api -p 9000:9000 -e PORT=9000 tienda-api:1.0
```

Ver los logs y parar el contenedor:

```bash
docker logs tienda-api
docker stop tienda-api
docker rm tienda-api
```

### Variables de entorno

| Variable | Por defecto | Descripcion |
|----------|-------------|-------------|
| PORT | 8000 | puerto en el que escucha uvicorn dentro del contenedor |

La app no usa secretos ni claves.

### Salida esperada y pruebas

Al arrancar, `docker logs tienda-api` deberia mostrar algo como:

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Pruebas:

- Abrir http://localhost:8000/docs y probar los endpoints desde swagger.
- Crear un usuario:

```bash
curl -X POST http://localhost:8000/usuarios -H "Content-Type: application/json" -d '{"nombre":"Ana","email":"ana@mail.com","tipo":"cliente","direccion_postal":"Calle 1"}'
```

- Crear un producto:

```bash
curl -X POST http://localhost:8000/productos -H "Content-Type: application/json" -d '{"tipo":"electronico","nombre":"Portatil","precio":800,"stock":5,"meses_garantia":24}'
```

- Listar usuarios y productos:

```bash
curl http://localhost:8000/usuarios
curl http://localhost:8000/productos
```

- Crear un pedido (con los ids devueltos antes) y ver los pedidos del cliente:

```bash
curl -X POST http://localhost:8000/pedidos -H "Content-Type: application/json" -d '{"cliente_id":"<id_usuario>","items":[{"producto_id":"<id_producto>","cantidad":2}]}'
curl http://localhost:8000/usuarios/<id_usuario>/pedidos
```

Endpoints disponibles:

| Metodo | Ruta |
|--------|------|
| POST | /usuarios |
| GET | /usuarios |
| GET | /usuarios/{usuario_id} |
| POST | /productos |
| GET | /productos |
| GET | /productos/{producto_id} |
| DELETE | /productos/{producto_id} |
| POST | /pedidos |
| GET | /usuarios/{cliente_id}/pedidos |

### Publicar la imagen (GitHub Container Registry)

```bash
docker tag tienda-api:1.0 ghcr.io/santiisantoss/tienda-api:1.0
docker tag tienda-api:1.0 ghcr.io/santiisantoss/tienda-api:latest
docker push ghcr.io/santiisantoss/tienda-api:1.0
docker push ghcr.io/santiisantoss/tienda-api:latest
```

### Descargar y ejecutar la imagen publicada

```bash
docker pull ghcr.io/santiisantoss/tienda-api:1.0
docker run -d -p 8000:8000 ghcr.io/santiisantoss/tienda-api:1.0
```
