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
