"""Esquemas Pydantic para validación y serialización de la API REST."""

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


# ==========================================
# 1.1 Esquemas de Usuario
# ==========================================

class UsuarioCreate(BaseModel):
    """Esquema para crear usuarios (nombre, email, tipo y dirección postal)."""
    nombre: str = Field(..., min_length=1, description="Nombre del usuario")
    email: str = Field(..., min_length=3, description="Email del usuario")
    tipo: Literal["cliente", "administrador", "admin"] = Field(
        ..., description="Tipo de usuario: 'cliente' o 'administrador'"
    )
    direccion_postal: Optional[str] = Field(
        default=None, description="Dirección postal (obligatoria si es cliente)"
    )


class UsuarioRead(BaseModel):
    """Esquema para devolver información de un usuario al cliente."""
    id: str
    nombre: str
    email: str
    es_admin: bool

    class Config:
        orm_mode = True
        from_attributes = True


# ==========================================
# 1.2 Esquemas de Producto
# ==========================================

class ProductoCreate(BaseModel):
    """Esquema para crear productos (genérico, electrónico o ropa)."""
    tipo: Literal["generico", "electronico", "ropa"] = Field(
        default="generico",
        description="Tipo de producto: 'generico', 'electronico' o 'ropa'",
    )
    nombre: str = Field(..., min_length=1, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (> 0)")
    stock: int = Field(..., ge=0, description="Stock inicial (>= 0)")
    # Atributo para ProductoElectronico
    meses_garantia: Optional[int] = Field(
        default=None, ge=0, description="Meses de garantía (para electrónicos)"
    )
    # Atributos para ProductoRopa
    talla: Optional[str] = Field(
        default=None, description="Talla de la prenda (para ropa)"
    )
    color: Optional[str] = Field(
        default=None, description="Color de la prenda (para ropa)"
    )


class ProductoRead(BaseModel):
    """Estructura de salida de un producto."""
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


# ==========================================
# 1.3 Esquemas de Pedido
# ==========================================

class PedidoItemCreate(BaseModel):
    """Representa un producto y cantidad durante la creación de un pedido."""
    producto_id: str = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad solicitada (> 0)")


class PedidoCreate(BaseModel):
    """Incluye el ID del cliente y la lista de líneas de pedido."""
    cliente_id: str = Field(..., description="ID del cliente que realiza el pedido")
    items: List[PedidoItemCreate] = Field(
        ..., min_length=1, description="Lista de líneas de pedido"
    )


class PedidoItemRead(BaseModel):
    """Estructura de salida con información de cada línea de pedido."""
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    """Estructura completa de un pedido con fecha, cliente, total e items."""
    id: str
    fecha: datetime
    cliente: UsuarioRead
    items: List[PedidoItemRead]
    total: float

    class Config:
        orm_mode = True
        from_attributes = True