"""Servicio centralizado que gestiona las operaciones de la tienda online."""

from typing import Dict, List, Tuple

from models.pedido import Pedido
from models.producto import Producto
from models.usuario import Administrador, Cliente, Usuario


class TiendaService:
    """Actúa como intermediario entre los usuarios y los productos de la tienda."""

    def __init__(self) -> None:
        """Inicializa los almacenes en memoria de usuarios, productos y pedidos."""
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: List[Pedido] = []

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    def registrar_usuario(self, tipo: str, **kwargs) -> Usuario:
        """Registra un nuevo usuario en la tienda.

        Args:
            tipo: "cliente" o "administrador".
            **kwargs: atributos necesarios para crear el usuario
                (nombre, email y, si es cliente, direccion).

        Returns:
            El usuario creado.
        """
        tipo_normalizado = tipo.strip().lower()

        if tipo_normalizado == "cliente":
            usuario: Usuario = Cliente(
                nombre=kwargs["nombre"],
                email=kwargs["email"],
                direccion=kwargs["direccion"],
            )
        elif tipo_normalizado == "administrador":
            usuario = Administrador(nombre=kwargs["nombre"], email=kwargs["email"])
        else:
            raise ValueError(f"Tipo de usuario no soportado: {tipo}")

        self.usuarios[usuario.id] = usuario
        return usuario

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def anadir_producto(self, producto: Producto) -> Producto:
        """Añade un producto (de cualquier categoría) al inventario."""
        self.productos[producto.id] = producto
        return producto

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto del inventario a partir de su identificador."""
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        return False

    def listar_productos(self) -> List[Producto]:
        """Devuelve la lista de todos los productos disponibles en la tienda."""
        return list(self.productos.values())

    # ------------------------------------------------------------------
    # Pedidos
    # ------------------------------------------------------------------
    def realizar_pedido(
        self, usuario_id: str, lineas: List[Tuple[str, int]]
    ) -> Pedido:
        """Realiza un pedido para un usuario, verificando existencia y stock.

        Args:
            usuario_id: id del usuario (debe existir y ser un Cliente).
            lineas: lista de tuplas (producto_id, cantidad) solicitadas.

        Returns:
            El pedido generado.

        Raises:
            ValueError: si el usuario no existe, no es cliente, algún producto
                no existe o no hay stock suficiente.
        """
        usuario = self.usuarios.get(usuario_id)
        if usuario is None:
            raise ValueError(f"El usuario {usuario_id} no existe.")
        if not isinstance(usuario, Cliente):
            raise ValueError("Solo los clientes pueden realizar pedidos.")

        lineas_pedido: List[Tuple[Producto, int]] = []
        for producto_id, cantidad in lineas:
            producto = self.productos.get(producto_id)
            if producto is None:
                raise ValueError(f"El producto {producto_id} no existe.")
            if not producto.hay_stock(cantidad):
                raise ValueError(
                    f"Stock insuficiente para '{producto.nombre}' "
                    f"(solicitado: {cantidad}, disponible: {producto.stock})."
                )
            lineas_pedido.append((producto, cantidad))

        # Todo verificado: descontamos stock y creamos el pedido
        for producto, cantidad in lineas_pedido:
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(cliente=usuario, lineas=lineas_pedido)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> List[Pedido]:
        """Lista todos los pedidos de un usuario, ordenados por fecha."""
        pedidos_usuario = [
            pedido for pedido in self.pedidos if pedido.cliente.id == usuario_id
        ]
        return sorted(pedidos_usuario, key=lambda pedido: pedido.fecha)
