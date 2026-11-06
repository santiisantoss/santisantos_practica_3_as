"""Punto de entrada de la API REST de la Tienda Online con FastAPI."""

from typing import List
from fastapi import FastAPI, HTTPException, status

from models.pedido import Pedido
from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.usuario import Usuario
from services.tienda_service import TiendaService
import schemas

app = FastAPI(
    title="Tienda Online API",
    description="API REST para gestionar usuarios, productos y pedidos usando TiendaService.",
    version="1.0.0",
)

# Instancia del servicio de negocio de la Práctica 1
tienda = TiendaService()


# =====================================================================
# Funciones auxiliares para convertir objetos de dominio a Schemas Read
# =====================================================================

def usuario_to_read(usuario: Usuario) -> schemas.UsuarioRead:
    """Convierte un objeto Usuario/Cliente/Administrador a UsuarioRead."""
    return schemas.UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )


def producto_to_read(producto: Producto) -> schemas.ProductoRead:
    """Convierte un objeto Producto (o subclase) a ProductoRead."""
    if isinstance(producto, ProductoElectronico):
        return schemas.ProductoRead(
            id=producto.id,
            tipo="electronico",
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock,
            meses_garantia=producto.meses_garantia,
        )
    if isinstance(producto, ProductoRopa):
        return schemas.ProductoRead(
            id=producto.id,
            tipo="ropa",
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock,
            talla=producto.talla,
            color=producto.color,
        )
    return schemas.ProductoRead(
        id=producto.id,
        tipo="generico",
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
    )


def pedido_to_read(pedido: Pedido) -> schemas.PedidoRead:
    """Convierte un objeto Pedido (con self.lineas) a PedidoRead."""
    items_read: List[schemas.PedidoItemRead] = []
    for producto, cantidad in pedido.lineas:
        items_read.append(
            schemas.PedidoItemRead(
                producto_id=producto.id,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=cantidad,
                subtotal=round(producto.precio * cantidad, 2),
            )
        )

    return schemas.PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente=usuario_to_read(pedido.cliente),
        items=items_read,
        total=round(pedido.calcular_total(), 2),
    )


# =====================================================================
# Endpoints de Usuarios (3p)
# =====================================================================

@app.post(
    "/usuarios",
    response_model=schemas.UsuarioRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"],
)
def crear_usuario(datos: schemas.UsuarioCreate):
    """Crea un nuevo usuario (cliente o administrador) mediante TiendaService."""
    tipo_norm = datos.tipo.strip().lower()
    if tipo_norm == "admin":
        tipo_norm = "administrador"

    if tipo_norm == "cliente" and not datos.direccion_postal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo 'direccion_postal' es obligatorio para clientes.",
        )

    try:
        if tipo_norm == "cliente":
            usuario = tienda.registrar_usuario(
                tipo="cliente",
                nombre=datos.nombre,
                email=datos.email,
                direccion=datos.direccion_postal,
            )
        else:
            usuario = tienda.registrar_usuario(
                tipo="administrador",
                nombre=datos.nombre,
                email=datos.email,
            )
        return usuario_to_read(usuario)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/usuarios",
    response_model=List[schemas.UsuarioRead],
    tags=["Usuarios"],
)
def listar_usuarios():
    """Devuelve la lista de todos los usuarios registrados."""
    return [usuario_to_read(u) for u in tienda.usuarios.values()]


@app.get(
    "/usuarios/{usuario_id}",
    response_model=schemas.UsuarioRead,
    tags=["Usuarios"],
)
def obtener_usuario(usuario_id: str):
    """Devuelve un usuario concreto por su ID."""
    usuario = tienda.usuarios.get(usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id '{usuario_id}' no encontrado.",
        )
    return usuario_to_read(usuario)


# =====================================================================
# Endpoints de Productos (2p)
# =====================================================================

@app.post(
    "/productos",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"],
)
def crear_producto(datos: schemas.ProductoCreate):
    """Crea un producto (genérico, electrónico o ropa) y lo añade a TiendaService."""
    tipo_norm = datos.tipo.strip().lower()

    if tipo_norm == "electronico":
        if datos.meses_garantia is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo 'meses_garantia' es obligatorio para productos electrónicos.",
            )
        nuevo_producto: Producto = ProductoElectronico(
            nombre=datos.nombre,
            precio=datos.precio,
            stock=datos.stock,
            meses_garantia=datos.meses_garantia,
        )
    elif tipo_norm == "ropa":
        if not datos.talla or not datos.color:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los campos 'talla' y 'color' son obligatorios para productos de ropa.",
            )
        nuevo_producto = ProductoRopa(
            nombre=datos.nombre,
            precio=datos.precio,
            stock=datos.stock,
            talla=datos.talla,
            color=datos.color,
        )
    else:
        nuevo_producto = Producto(
            nombre=datos.nombre,
            precio=datos.precio,
            stock=datos.stock,
        )

    producto_guardado = tienda.anadir_producto(nuevo_producto)
    return producto_to_read(producto_guardado)


@app.get(
    "/productos",
    response_model=List[schemas.ProductoRead],
    tags=["Productos"],
)
def listar_productos():
    """Devuelve todos los productos del inventario usando TiendaService."""
    productos = tienda.listar_productos()
    return [producto_to_read(p) for p in productos]


@app.get(
    "/productos/{producto_id}",
    response_model=schemas.ProductoRead,
    tags=["Productos"],
)
def obtener_producto(producto_id: str):
    """Devuelve un producto concreto por su ID."""
    producto = tienda.productos.get(producto_id)
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id '{producto_id}' no encontrado.",
        )
    return producto_to_read(producto)


@app.delete(
    "/productos/{producto_id}",
    tags=["Productos"],
)
def eliminar_producto(producto_id: str):
    """Elimina un producto del inventario por su ID."""
    eliminado = tienda.eliminar_producto(producto_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id '{producto_id}' no encontrado.",
        )
    return {"message": "Producto eliminado correctamente"}


# =====================================================================
# Endpoints de Pedidos (2p)
# =====================================================================

@app.post(
    "/pedidos",
    response_model=schemas.PedidoRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Pedidos"],
)
def crear_pedido(datos: schemas.PedidoCreate):
    """Crea un pedido verificando cliente, productos y stock mediante TiendaService."""
    # Verificamos 404 si el cliente o algún producto no existen antes de procesar
    if datos.cliente_id not in tienda.usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id '{datos.cliente_id}' no existe.",
        )
    for item in datos.items:
        if item.producto_id not in tienda.productos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con id '{item.producto_id}' no existe.",
            )

    lineas_tuplas = [(item.producto_id, item.cantidad) for item in datos.items]

    try:
        pedido = tienda.realizar_pedido(
            usuario_id=datos.cliente_id,
            lineas=lineas_tuplas,
        )
        return pedido_to_read(pedido)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/usuarios/{cliente_id}/pedidos",
    response_model=List[schemas.PedidoRead],
    tags=["Pedidos"],
)
def listar_pedidos_cliente(cliente_id: str):
    """Devuelve el historial de pedidos de un cliente."""
    if cliente_id not in tienda.usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id '{cliente_id}' no existe.",
        )

    pedidos = tienda.listar_pedidos_usuario(cliente_id)
    return [pedido_to_read(p) for p in pedidos]