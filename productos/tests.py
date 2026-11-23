import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from categorias.models import Categoria
from .models import Producto

# Las imágenes de las pruebas se guardan en una carpeta temporal que se borra al final
MEDIA_TEMPORAL = tempfile.mkdtemp()


def imagen_de_prueba(nombre='prueba.png'):
    """Crea una imagen PNG pequeña en memoria para subirla en el formulario."""
    archivo = BytesIO()
    Image.new('RGB', (10, 10), 'red').save(archivo, 'PNG')
    return SimpleUploadedFile(nombre, archivo.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class ProductosTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Bebidas')
        self.producto = Producto.objects.create(nombre='Bebida con hielo', precio=20000, categoria=self.categoria)

    def test_la_raiz_redirige_al_listado_de_productos(self):
        respuesta = self.client.get('/')
        self.assertRedirects(respuesta, reverse('productos:lista'))

    def test_el_listado_muestra_los_productos(self):
        respuesta = self.client.get(reverse('productos:lista'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Bebida con hielo')

    def test_crear_un_producto_sin_imagen(self):
        respuesta = self.client.post(reverse('productos:crear'), {
            'nombre': 'Café', 'precio': '5000', 'categoria': self.categoria.id,
        })
        self.assertRedirects(respuesta, reverse('productos:lista'))
        self.assertTrue(Producto.objects.filter(nombre='Café').exists())

    def test_crear_un_producto_con_imagen(self):
        self.client.post(reverse('productos:crear'), {
            'nombre': 'Jugo', 'precio': '7000', 'categoria': self.categoria.id,
            'imagen': imagen_de_prueba('jugo.png'),
        })
        producto = Producto.objects.get(nombre='Jugo')
        self.assertTrue(producto.imagen.name.startswith('productos/'))

    def test_un_precio_con_letras_no_se_guarda(self):
        respuesta = self.client.post(reverse('productos:crear'), {
            'nombre': 'Té', 'precio': 'barato', 'categoria': self.categoria.id,
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Producto.objects.filter(nombre='Té').exists())

    def test_un_producto_necesita_categoria(self):
        self.client.post(reverse('productos:crear'), {'nombre': 'Agua', 'precio': '3000'})
        self.assertFalse(Producto.objects.filter(nombre='Agua').exists())

    def test_editar_un_producto(self):
        self.client.post(reverse('productos:editar', args=[self.producto.id]), {
            'nombre': 'Bebida con hielo', 'precio': '25000', 'categoria': self.categoria.id,
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.precio, 25000)

    def test_eliminar_con_get_solo_pide_confirmacion(self):
        respuesta = self.client.get(reverse('productos:eliminar', args=[self.producto.id]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(Producto.objects.filter(id=self.producto.id).exists())

    def test_eliminar_con_post_borra_el_producto(self):
        respuesta = self.client.post(reverse('productos:eliminar', args=[self.producto.id]))
        self.assertRedirects(respuesta, reverse('productos:lista'))
        self.assertFalse(Producto.objects.filter(id=self.producto.id).exists())

    def test_un_producto_que_no_existe_da_404(self):
        respuesta = self.client.get(reverse('productos:editar', args=[9999]))
        self.assertEqual(respuesta.status_code, 404)
