import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Panel principal con navegación, gestión de productos, usuarios y ventas."""

    def __init__(
        self,
        master: tk.Misc,
        servicio: RestauranteServicio,
        usuario_actual: Usuario,
        on_logout,
        assets_dir: str | Path,
    ) -> None:
        super().__init__(master, padding=18)
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout
        self.assets_dir = Path(assets_dir)
        self.imagenes: dict[str, tk.PhotoImage] = {}

        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.estado_var = tk.StringVar()

        self.usuario_venta_var = tk.StringVar()
        self.producto_venta_var = tk.StringVar()
        self.estado_venta_var = tk.StringVar()
        self.opciones_usuarios: dict[str, str] = {}
        self.opciones_productos: dict[str, str] = {}

        self.tabla_productos = None
        self.tabla_ventas = None
        self.combo_usuario = None
        self.combo_producto = None

        self._crear_estilos()
        self._cargar_imagenes()
        self._crear_componentes()
        self._mostrar_inicio()

    def _crear_estilos(self) -> None:
        estilo = ttk.Style()
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("Menu.TButton", padding=(10, 8))
        estilo.configure("Accion.TButton", padding=(10, 6))

    def _cargar_imagenes(self) -> None:
        nombres = ["home", "products", "users", "sales", "logout", "add", "search", "edit", "delete", "clean"]
        for nombre in nombres:
            ruta = self.assets_dir / "icons" / f"{nombre}.png"
            try:
                self.imagenes[nombre] = tk.PhotoImage(file=str(ruta))
            except tk.TclError:
                pass
        ruta_logo = self.assets_dir / "logo" / "icono.png"
        try:
            self.imagenes["logo"] = tk.PhotoImage(file=str(ruta_logo))
        except tk.TclError:
            pass

    def _boton(self, master, texto: str, comando, icono: str | None = None, estilo="TButton"):
        opciones = {"text": texto, "command": comando, "style": estilo}
        if icono in self.imagenes:
            opciones.update({"image": self.imagenes[icono], "compound": "left"})
        return ttk.Button(master, **opciones)

    def _crear_componentes(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        encabezado.columnconfigure(1, weight=1)

        if "logo" in self.imagenes:
            ttk.Label(encabezado, image=self.imagenes["logo"]).grid(
                row=0, column=0, rowspan=2, padx=(0, 10)
            )

        ttk.Label(
            encabezado,
            text="RESTAURANTE APP",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(
            encabezado,
            text=f"Usuario: {self.usuario_actual.nombre}",
        ).grid(row=1, column=1, sticky="w", pady=(3, 0))

        self._boton(
            encabezado,
            "Cerrar sesión",
            self.on_logout,
            "logout",
        ).grid(row=0, column=2, rowspan=2, padx=(12, 0))

        menu = ttk.LabelFrame(self, text="Navegación", padding=10)
        menu.grid(row=1, column=0, sticky="ns", padx=(0, 15))

        opciones_menu = [
            ("Inicio", self._mostrar_inicio, "home"),
            ("Productos", self._mostrar_productos, "products"),
            ("Usuarios", self._mostrar_usuarios, "users"),
            ("Ventas", self._mostrar_ventas, "sales"),
        ]
        for texto, comando, icono in opciones_menu:
            boton = self._boton(menu, texto, comando, icono, "Menu.TButton")
            boton.configure(width=20)
            boton.pack(fill="x", pady=5)

        self.contenido = ttk.Frame(self)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)

    def _limpiar_contenido(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self) -> None:
        self._limpiar_contenido()
        self.contenido.rowconfigure(1, weight=0)

        ttk.Label(self.contenido, text="Resumen del sistema", style="Titulo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 15)
        )

        tarjeta = ttk.LabelFrame(self.contenido, text="Estado actual", padding=18)
        tarjeta.grid(row=1, column=0, sticky="ew")
        for col in range(3):
            tarjeta.columnconfigure(col, weight=1)

        resumen = [
            ("Productos registrados", self.servicio.cantidad_productos()),
            ("Usuarios registrados", self.servicio.cantidad_usuarios()),
            ("Ventas registradas", self.servicio.cantidad_ventas()),
        ]
        for col, (titulo, valor) in enumerate(resumen):
            cuadro = ttk.LabelFrame(tarjeta, text=titulo, padding=15)
            cuadro.grid(row=0, column=col, sticky="nsew", padx=6)
            ttk.Label(cuadro, text=str(valor), font=("Segoe UI", 22, "bold")).pack()

        ttk.Label(
            self.contenido,
            text=(
                "Semana 15: una acción del usuario activa un botón con command=, "
                "el callback delega la operación a RestauranteServicio, se persiste "
                "en JSON y la interfaz muestra el resultado."
            ),
            wraplength=760,
            justify="left",
        ).grid(row=2, column=0, sticky="w", pady=(18, 0))

    def _mostrar_productos(self) -> None:
        self._limpiar_contenido()
        self.contenido.rowconfigure(1, weight=0)

        ttk.Label(self.contenido, text="Gestión de productos", style="Titulo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )

        formulario = ttk.LabelFrame(self.contenido, text="Datos del producto", padding=12)
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        for col in range(4):
            formulario.columnconfigure(col, weight=1)

        campos = [
            ("Código", self.codigo_var, 0, 0),
            ("Nombre", self.nombre_var, 0, 2),
            ("Categoría", self.categoria_var, 1, 0),
            ("Precio", self.precio_var, 1, 2),
            ("Stock", self.stock_var, 2, 0),
        ]
        for texto, variable, fila, col in campos:
            ttk.Label(formulario, text=texto + ":").grid(
                row=fila, column=col, sticky="e", padx=5, pady=5
            )
            ttk.Entry(formulario, textvariable=variable, width=24).grid(
                row=fila, column=col + 1, sticky="ew", padx=5, pady=5
            )

        acciones = ttk.Frame(formulario)
        acciones.grid(row=3, column=0, columnspan=4, pady=(8, 2))
        for texto, comando, icono in [
            ("Registrar", self._registrar_producto, "add"),
            ("Cargar / Consultar", self._cargar_producto, "search"),
            ("Actualizar", self._actualizar_producto, "edit"),
            ("Eliminar", self._eliminar_producto, "delete"),
            ("Limpiar", self._limpiar_formulario, "clean"),
        ]:
            self._boton(acciones, texto, comando, icono, "Accion.TButton").pack(
                side="left", padx=4
            )

        ttk.Label(self.contenido, textvariable=self.estado_var).grid(
            row=2, column=0, sticky="w", pady=(0, 8)
        )

        tabla_frame = ttk.LabelFrame(self.contenido, text="Productos registrados", padding=8)
        tabla_frame.grid(row=3, column=0, sticky="nsew")
        self.contenido.rowconfigure(3, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        titulos = {
            "codigo": "Código",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock",
        }
        anchos = {"codigo": 90, "nombre": 220, "categoria": 150, "precio": 100, "stock": 90}
        for columna in columnas:
            self.tabla_productos.heading(columna, text=titulos[columna])
            self.tabla_productos.column(columna, width=anchos[columna], anchor="center")
        self.tabla_productos.column("nombre", anchor="w")
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_productos.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self._refrescar_tabla_productos()

    def _refrescar_tabla_productos(self) -> None:
        if self.tabla_productos is None:
            return
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "", "end",
                values=(producto.codigo, producto.nombre, producto.categoria, f"${producto.precio:.2f}", producto.stock),
            )

    def _obtener_datos_formulario(self) -> tuple[str, str, str, float, int]:
        codigo = self.codigo_var.get().strip()
        nombre = self.nombre_var.get().strip()
        categoria = self.categoria_var.get().strip()
        if not codigo or not nombre or not categoria:
            raise ValueError("Código, nombre y categoría son obligatorios.")
        try:
            precio = float(self.precio_var.get().strip())
            stock = int(self.stock_var.get().strip())
        except ValueError as exc:
            raise ValueError("Precio debe ser numérico y stock debe ser un entero.") from exc
        return codigo, nombre, categoria, precio, stock

    def _registrar_producto(self) -> None:
        try:
            self.servicio.registrar_producto(*self._obtener_datos_formulario())
            self.estado_var.set("Producto registrado correctamente.")
            self._refrescar_tabla_productos()
            self._limpiar_formulario()
        except ValueError as exc:
            messagebox.showerror("No se pudo registrar", str(exc))

    def _cargar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showerror("Consulta", "Ingrese el código del producto.")
            return
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Consulta", "No existe un producto con ese código.")
            return
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(str(producto.precio))
        self.stock_var.set(str(producto.stock))
        self.estado_var.set("Producto cargado correctamente.")

    def _actualizar_producto(self) -> None:
        try:
            self.servicio.actualizar_producto(*self._obtener_datos_formulario())
            self.estado_var.set("Producto actualizado correctamente.")
            self._refrescar_tabla_productos()
        except ValueError as exc:
            messagebox.showerror("No se pudo actualizar", str(exc))

    def _eliminar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showerror("Eliminar", "Ingrese el código del producto.")
            return
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Eliminar", "No existe un producto con ese código.")
            return
        if not messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar '{producto.nombre}'?"):
            return
        try:
            self.servicio.eliminar_producto(codigo)
            self.estado_var.set("Producto eliminado correctamente.")
            self._limpiar_formulario()
            self._refrescar_tabla_productos()
        except ValueError as exc:
            messagebox.showerror("No se pudo eliminar", str(exc))

    def _limpiar_formulario(self) -> None:
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")

    def _mostrar_usuarios(self) -> None:
        self._limpiar_contenido()
        self.contenido.rowconfigure(1, weight=1)
        ttk.Label(self.contenido, text="Usuarios registrados", style="Titulo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        tabla_frame = ttk.LabelFrame(self.contenido, text="Consulta de usuarios", padding=8)
        tabla_frame.grid(row=1, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        columnas = ("identificacion", "nombre", "correo")
        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        for columna, titulo in {
            "identificacion": "Identificación",
            "nombre": "Nombre",
            "correo": "Correo",
        }.items():
            tabla.heading(columna, text=titulo)
            tabla.column(columna, width=220, anchor="center")
        tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        tabla.configure(yscrollcommand=barra.set)
        for usuario in self.servicio.listar_usuarios():
            tabla.insert("", "end", values=(usuario.identificacion, usuario.nombre, usuario.correo))

    def _mostrar_ventas(self) -> None:
        """Sección Semana 15: selección → command= → callback → servicio → JSON → interfaz."""
        self._limpiar_contenido()
        self.contenido.rowconfigure(2, weight=1)

        ttk.Label(self.contenido, text="Registro de ventas", style="Titulo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )

        formulario = ttk.LabelFrame(self.contenido, text="Nueva venta", padding=14)
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        self.opciones_usuarios = {
            f"{u.identificacion} - {u.nombre}": u.identificacion
            for u in self.servicio.listar_usuarios()
        }
        self.opciones_productos = {
            f"{p.codigo} - {p.nombre}": p.codigo
            for p in self.servicio.listar_productos()
        }

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_usuario = ttk.Combobox(
            formulario,
            textvariable=self.usuario_venta_var,
            values=list(self.opciones_usuarios.keys()),
            state="readonly",
            width=36,
        )
        self.combo_usuario.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(formulario, text="Producto:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.combo_producto = ttk.Combobox(
            formulario,
            textvariable=self.producto_venta_var,
            values=list(self.opciones_productos.keys()),
            state="readonly",
            width=36,
        )
        self.combo_producto.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        # Fundamento de eventos: command= recibe el callback, sin paréntesis.
        if "sales" in self.imagenes:
            boton_venta = ttk.Button(
                formulario,
                text="Registrar venta",
                image=self.imagenes["sales"],
                compound="left",
                style="Accion.TButton",
                command=self._registrar_venta_callback,
            )
        else:
            boton_venta = ttk.Button(
                formulario,
                text="Registrar venta",
                style="Accion.TButton",
                command=self._registrar_venta_callback,
            )
        boton_venta.grid(row=1, column=0, columnspan=4, pady=(12, 5))

        ttk.Label(formulario, textvariable=self.estado_venta_var).grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(5, 0)
        )

        tabla_frame = ttk.LabelFrame(self.contenido, text="Ventas registradas", padding=8)
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        columnas = ("id", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        configuracion = {
            "id": ("Venta", 90),
            "usuario": ("Usuario", 280),
            "producto": ("Producto", 280),
            "fecha": ("Fecha", 120),
        }
        for columna, (titulo, ancho) in configuracion.items():
            self.tabla_ventas.heading(columna, text=titulo)
            self.tabla_ventas.column(columna, width=ancho, anchor="center")
        self.tabla_ventas.column("usuario", anchor="w")
        self.tabla_ventas.column("producto", anchor="w")
        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_ventas.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tabla_ventas.configure(yscrollcommand=barra.set)
        self._refrescar_tabla_ventas()

    def _registrar_venta_callback(self) -> None:
        """Callback: obtiene la selección y delega la regla de negocio al servicio."""
        usuario_id = self.opciones_usuarios.get(self.usuario_venta_var.get(), "")
        producto_codigo = self.opciones_productos.get(self.producto_venta_var.get(), "")
        try:
            venta = self.servicio.registrar_venta(usuario_id, producto_codigo)
            self.estado_venta_var.set(f"Venta {venta.identificador} registrada correctamente.")
            self.usuario_venta_var.set("")
            self.producto_venta_var.set("")
            self._refrescar_tabla_ventas()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as exc:
            messagebox.showerror("Ventas", str(exc))

    def _refrescar_tabla_ventas(self) -> None:
        if self.tabla_ventas is None:
            return
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        for venta in self.servicio.listar_ventas():
            usuario = self.servicio.buscar_usuario(venta.usuario_id)
            producto = self.servicio.buscar_producto(venta.producto_codigo)
            usuario_texto = venta.usuario_id if usuario is None else f"{usuario.identificacion} - {usuario.nombre}"
            producto_texto = venta.producto_codigo if producto is None else f"{producto.codigo} - {producto.nombre}"
            self.tabla_ventas.insert(
                "", "end",
                values=(venta.identificador, usuario_texto, producto_texto, venta.fecha),
            )
