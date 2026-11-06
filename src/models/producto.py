"""Modelo de productos de la tienda online."""

import uuid


class Producto:
    """Clase padre que representa un producto genérico de la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        """Inicializa un producto con id autogenerado, nombre, precio y stock."""
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """Comprueba si hay stock suficiente para la cantidad solicitada."""
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        """Actualiza el stock del producto.

        Un valor positivo repone stock, un valor negativo lo descuenta
        (por ejemplo, al realizar una compra).
        """
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError("El stock no puede quedar en negativo.")
        self.stock = nuevo_stock

    def __str__(self) -> str:
        """Devuelve una representación legible del producto."""
        return (
            f"[{self.id[:8]}] {self.nombre} - {self.precio:.2f} EUR "
            f"(Stock: {self.stock})"
        )


class ProductoElectronico(Producto):
    """Producto electrónico, con meses de garantía adicionales."""

    def __init__(
        self, nombre: str, precio: float, stock: int, meses_garantia: int
    ) -> None:
        """Inicializa un producto electrónico."""
        super().__init__(nombre, precio, stock)
        self.meses_garantia: int = meses_garantia

    def __str__(self) -> str:
        """Devuelve una representación legible del producto electrónico."""
        return f"{super().__str__()} | Garantía: {self.meses_garantia} meses"


class ProductoRopa(Producto):
    """Producto de ropa, con talla y color adicionales."""

    def __init__(
        self, nombre: str, precio: float, stock: int, talla: str, color: str
    ) -> None:
        """Inicializa un producto de ropa."""
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        """Devuelve una representación legible del producto de ropa."""
        return f"{super().__str__()} | Talla: {self.talla} | Color: {self.color}"
