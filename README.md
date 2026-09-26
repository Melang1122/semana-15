# Restaurante App — Semana 15

## 1. Propósito

Esta versión corresponde a la **Semana 15 de Programación Orientada a Objetos** y continúa el mismo proyecto desarrollado en la Semana 14. El objetivo es evidenciar los **fundamentos básicos del manejo de eventos** en Tkinter mediante una operación de venta: el usuario selecciona un usuario y un producto, presiona un botón configurado con `command=`, se ejecuta un callback, la operación se delega a `RestauranteServicio`, se persiste en `ventas.json` y la interfaz se actualiza.

## 2. Evolución desde la Semana 14

Se mantienen el inicio de sesión, la navegación, la gestión de productos, la consulta de usuarios, la arquitectura modular y la persistencia JSON ya existentes. Para la Semana 15 se añadieron:

- Modelo `Venta`.
- Archivo `datos/ventas.json`.
- Métodos de ventas en `RestauranteServicio`.
- Lectura y escritura de ventas en `ArchivoServicio`.
- Sección visual **Ventas** con selectores `ttk.Combobox`.
- Botón **Registrar venta** mediante `command=self._registrar_venta_callback`.
- Tabla `ttk.Treeview` para presentar las ventas registradas.
- Actualización inmediata de la tabla después de registrar una venta.
- Carpeta `assets/` con íconos y logotipo utilizados en la interfaz.

## 3. Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── icons/
│   └── logo/
├── main.py
└── README.md
```

## 4. Flujo de manejo de eventos

El fundamento de la Semana 15 se observa en el siguiente flujo:

```text
USUARIO
   ↓
selecciona usuario y producto
   ↓
BOTÓN "Registrar venta"
   ↓
command=self._registrar_venta_callback
   ↓
CALLBACK
   ↓
RestauranteServicio.registrar_venta(...)
   ↓
ArchivoServicio.guardar_ventas(...)
   ↓
ventas.json
   ↓
actualización del Treeview + mensaje visual
```

El callback únicamente obtiene las selecciones, solicita la operación al servicio y actualiza la vista. Las validaciones y la persistencia no se realizan directamente desde `main_view.py`.

## 5. Gestión de ventas

La venta relaciona:

- `usuario_id`: identificación de un usuario existente.
- `producto_codigo`: código de un producto existente.
- `fecha`: fecha de registro en formato ISO (`AAAA-MM-DD`).
- `identificador`: código automático `V001`, `V002`, etc.

Antes de registrar una venta, `RestauranteServicio` verifica que:

1. Se haya seleccionado un usuario.
2. Se haya seleccionado un producto.
3. El usuario exista.
4. El producto exista.
5. El producto tenga stock disponible.

Si la operación es válida, la venta se guarda en `datos/ventas.json` y queda disponible al volver a abrir la aplicación.

## 6. Persistencia JSON

- `productos.json`: productos del restaurante.
- `usuarios.json`: usuarios registrados.
- `ventas.json`: ventas realizadas.

`ArchivoServicio` es la única clase responsable de leer y escribir JSON. La interfaz no abre ni modifica archivos directamente.

## 7. Interfaz y assets

La aplicación conserva una interfaz modular con menú lateral, formularios y tablas. La carpeta `assets/` contiene el logotipo y los íconos usados en Login y MainView, cumpliendo el requisito visual de la Semana 15.

## 8. Ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

En Windows también puede utilizarse:

```powershell
py main.py
```

No requiere librerías externas: utiliza Python y Tkinter/ttk.

### Credenciales de prueba

- Usuario: `0922248737` o `castromelvinisaias2014@gmail.com`
- Contraseña: `1234`

## 9. Comprobación manual sugerida

1. Ejecutar `main.py`.
2. Iniciar sesión.
3. Verificar las secciones Inicio, Productos y Usuarios.
4. Entrar en **Ventas**.
5. Seleccionar un usuario.
6. Seleccionar un producto.
7. Presionar **Registrar venta**.
8. Confirmar el mensaje de éxito y la nueva fila en la tabla.
9. Revisar `datos/ventas.json` y comprobar que la venta quedó almacenada.
10. Cerrar y volver a ejecutar la aplicación para verificar que la venta se recupera.

## 10. Alcance

Esta entrega se limita al fundamento solicitado para la Semana 15. No implementa facturación, carrito de compras, base de datos, eventos avanzados de teclado/mouse, doble clic ni selección reactiva de filas.
