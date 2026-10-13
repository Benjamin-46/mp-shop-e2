# MP Shop — Music Pro Company (Sucursal / Punto de Venta)

Proyecto del caso semestral de **Programación Backend** (INACAP).

| Evaluación | Unidad | Contenido |
|---|---|---|
| E1 | Tecnologías del lado del servidor | Sitio Django sin base de datos, datos mock en JSON |
| **E2** | **Framework back end** | **Base de datos, modelos, migraciones, diagrama, Django Admin y datos de prueba con Faker** |

## Puesta en marcha

```bash
python -m venv venv
venv\Scripts\activate            # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt

python manage.py migrate                 # crea las tablas a partir de las migraciones
python manage.py verificar_bd            # revisa conexión, motor y migraciones
python manage.py cargar_json_inicial     # pasa los datos de la E1 (JSON) a la base de datos
python manage.py createsuperuser         # usuario para entrar a Django Admin
python manage.py runserver
```

* Sitio público: <http://127.0.0.1:8000/>
* Django Admin: <http://127.0.0.1:8000/admin/>

## Base de datos (2.1.1)

Por defecto usa **SQLite** (`db.sqlite3`, no requiere instalar nada). La configuración está
en `mp_shop/settings.py` → `DATABASES`. Para usar PostgreSQL basta con definir variables de entorno
(`DB_ENGINE=postgresql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).

`python manage.py verificar_bd` muestra qué base de datos se está usando, prueba la conexión
con un `SELECT 1`, indica si hay migraciones pendientes y cuenta los registros por tabla.

## Modelos y diagrama

`Sucursal`, `Categoria`, `Marca`, `Producto`, `Inventario` (stock por sucursal),
`Cliente`, `Venta` y `DetalleVenta`.

* Código: `tienda/models.py`
* Diagrama: `docs/diagrama_bd.png` (se regenera desde los modelos con
  `python manage.py generar_diagrama`; requiere Graphviz para el PNG).

Relaciones: Categoria 1—N Producto · Marca 1—N Producto · Cliente 1—N Venta · Sucursal 1—N Venta ·
Venta 1—N DetalleVenta · Producto 1—N DetalleVenta · Producto N—M Sucursal (a través de `Inventario`).

## Migraciones

Historial en `tienda/migrations/`:

| Migración | Qué hace |
|---|---|
| `0001_initial` | Crea las 8 tablas, claves foráneas, índice y restricción única de inventario |
| `0002_producto_destacado` | Modificación del modelo: agrega `Producto.destacado` |

Flujo de trabajo: editar `models.py` → `python manage.py makemigrations` → `python manage.py migrate`.
Estado actual: `python manage.py showmigrations tienda`.

## Django Admin (2.1.2)

Configurado en `tienda/admin.py`: columnas (`list_display`), filtros (`list_filter`),
búsqueda (`search_fields`), edición en línea del stock y del detalle de venta (inlines),
acciones masivas (activar/desactivar productos), jerarquía por fecha, campos de solo
lectura y `autocomplete_fields` (para no cargar un desplegable con miles de productos).
Crear, consultar, modificar y eliminar registros se hace desde el panel.

## Datos de prueba con Faker

```bash
python manage.py poblar_datos productos 100
python manage.py poblar_datos productos 1000
python manage.py poblar_datos productos 100000
python manage.py poblar_datos productos 1000000 --lote 10000
python manage.py poblar_datos clientes 1000
python manage.py poblar_datos ventas 1000        # requiere productos y clientes
```

Usa `bulk_create()` por lotes dentro de transacciones (un INSERT por lote, no por fila).
Cada producto genera además un registro de inventario por sucursal. Opción `--semilla N`
para repetir los mismos datos.

## Pruebas automáticas

```bash
python manage.py test
```

Cubre la conexión, restricciones de los modelos, el CRUD completo en Django Admin,
filtros, búsquedas, acciones, la carga con Faker y el sitio público.
