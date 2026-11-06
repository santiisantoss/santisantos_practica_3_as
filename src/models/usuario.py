"""Modelo de usuarios de la tienda online."""

import uuid


class Usuario:
    """Clase padre que representa a cualquier persona que usa la tienda."""

    def __init__(self, nombre: str, email: str) -> None:
        """Inicializa un usuario con id autogenerado, nombre y email."""
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Indica si el usuario tiene permisos de administrador."""
        return False

    def __str__(self) -> str:
        """Devuelve una representación legible del usuario."""
        return f"[{self.id[:8]}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    """Usuario de tipo cliente, con dirección postal."""

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        """Inicializa un cliente."""
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        """Devuelve una representación legible del cliente."""
        return f"{super().__str__()} | Dirección: {self.direccion}"


class Administrador(Usuario):
    """Usuario de tipo administrador, gestor de la tienda."""

    def is_admin(self) -> bool:
        """Los administradores siempre devuelven True."""
        return True

    def __str__(self) -> str:
        """Devuelve una representación legible del administrador."""
        return f"{super().__str__()} | Rol: Administrador"
