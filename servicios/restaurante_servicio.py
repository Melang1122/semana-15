from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Concentra las reglas y operaciones de negocio del restaurante."""

    def __init__(
        self,
        productos: list[Producto],
        usuarios: list[Usuario],
        ventas: list[Venta] | None = None,
        archivos: ArchivoServicio | None = None,
    ) -> None:
        self._productos = list(productos)
        self._usuarios = list(usuarios)
        self._ventas = list(ventas or [])
        self._archivos = archivos

    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        usuario = usuario.strip().lower()
        contrasena = contrasena.strip()
        if not usuario or not contrasena:
            return None
        for registrado in self._usuarios:
            coincide_usuario = (
                registrado.identificacion == usuario
                or registrado.correo.lower() == usuario
            )
            if coincide_usuario and registrado.contrasena == contrasena:
                return registrado
        return None

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)

    def cantidad_ventas(self) -> int:
        return len(self._ventas)

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = str(codigo).strip()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        identificacion = str(identificacion).strip()
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def registrar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> Producto:
        if self.buscar_producto(codigo) is not None:
            raise ValueError("Ya existe un producto con ese código.")
        producto = Producto(codigo, nombre, categoria, precio, stock)
        self._productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> Producto:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")
        producto.actualizar(nombre, categoria, precio, stock)
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> None:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")
        self._productos.remove(producto)
        self._guardar_productos()

    def _generar_identificador_venta(self) -> str:
        numeros = []
        for venta in self._ventas:
            if venta.identificador.startswith("V") and venta.identificador[1:].isdigit():
                numeros.append(int(venta.identificador[1:]))
        siguiente = max(numeros, default=0) + 1
        return f"V{siguiente:03d}"

    def registrar_venta(self, usuario_id: str, producto_codigo: str) -> Venta:
        """Valida y registra una venta. La UI solo coordina el evento."""
        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if self.buscar_usuario(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")
        if producto.stock <= 0:
            raise ValueError("El producto seleccionado no tiene stock disponible.")

        nueva_venta = Venta(
            self._generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )
        self._ventas.append(nueva_venta)
        self._guardar_ventas()
        return nueva_venta

    def _guardar_productos(self) -> None:
        if self._archivos is not None:
            self._archivos.guardar_productos(self._productos)

    def _guardar_ventas(self) -> None:
        if self._archivos is not None:
            self._archivos.guardar_ventas(self._ventas)
