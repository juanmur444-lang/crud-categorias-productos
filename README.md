# CRUD de categorías y productos

Aplicación web hecha con Django para administrar el catálogo de una tienda: permite crear, listar, editar y eliminar categorías y productos. Cada producto pertenece a una categoría y puede tener una imagen.

Práctica académica del Tecnólogo en Análisis y Desarrollo de Software (ADSO), SENA.

## Funcionalidades

- Listado de productos con su precio, imagen y categoría.
- Crear y editar productos con nombre, precio, imagen opcional y categoría.
- Vista previa de la imagen antes de guardar el producto.
- Eliminar con página de confirmación y aviso antes de borrar.
- Gestión completa de categorías (crear, listar, editar y eliminar).
- Si se elimina una categoría, sus productos se eliminan con ella (`on_delete=CASCADE`).
- Panel de administración de Django en `/admin/`.

## Tecnologías

- Python
- Django
- SQLite
- Pillow (para las imágenes)
- HTML, CSS y JavaScript (plantillas y archivos estáticos de Django)

## Estructura

```
crud-categorias-productos/
├── tienda_config/   # configuración general y rutas principales
├── categorias/      # modelo, formulario, vistas y plantillas de las categorías
└── productos/       # modelo, formulario, vistas y plantillas de los productos
```

Cada aplicación tiene sus propias plantillas y archivos estáticos (`css`, `js`, `img`), y sus rutas usan *namespace* (`productos:lista`, `categorias:lista`).

## Rutas

| Ruta | Qué hace |
|---|---|
| `/` | Redirige al listado de productos |
| `/productos/` | Listado de productos |
| `/productos/crear/` | Formulario para crear un producto |
| `/productos/editar/<id>/` | Formulario para editar un producto |
| `/productos/eliminar/<id>/` | Confirmación para eliminar un producto |
| `/categorias/` | Listado y gestión de categorías (mismas acciones) |
| `/admin/` | Panel de administración de Django |

## Cómo ejecutarlo

```
git clone https://github.com/juanmur444-lang/crud-categorias-productos.git
cd crud-categorias-productos
python -m venv venv
venv\Scripts\activate
pip install django pillow
python manage.py migrate
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000` en el navegador.

Para usar el panel de administración, crea primero un usuario con `python manage.py createsuperuser`.

## Qué aprendí

- Dividir un proyecto Django en aplicaciones independientes.
- Relacionar dos modelos con una llave foránea y entender el borrado en cascada.
- Usar `ModelForm` para crear y editar con el mismo formulario.
- Subir imágenes con `ImageField` y servirlas en modo de desarrollo.
- Optimizar la consulta del listado con `select_related`.

## Mejoras pendientes

- Agregar pruebas automatizadas (los archivos `tests.py` están vacíos).
- Proteger la creación, edición y eliminación con inicio de sesión.
- Validar que el precio no sea negativo.

## Autor

Juan Andrés Mur Bermúdez · [github.com/juanmur444-lang](https://github.com/juanmur444-lang)
