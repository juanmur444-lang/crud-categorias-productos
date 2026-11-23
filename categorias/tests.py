from django.test import TestCase
from django.urls import reverse

from productos.models import Producto
from .models import Categoria


class CategoriasTests(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Bebidas')

    def test_el_listado_muestra_las_categorias(self):
        respuesta = self.client.get(reverse('categorias:lista'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Bebidas')

    def test_crear_una_categoria(self):
        respuesta = self.client.post(reverse('categorias:crear'), {'nombre': 'Snacks'})
        self.assertRedirects(respuesta, reverse('categorias:lista'))
        self.assertTrue(Categoria.objects.filter(nombre='Snacks').exists())

    def test_una_categoria_sin_nombre_no_se_guarda(self):
        self.client.post(reverse('categorias:crear'), {'nombre': ''})
        self.assertEqual(Categoria.objects.count(), 1)

    def test_editar_una_categoria(self):
        self.client.post(reverse('categorias:editar', args=[self.categoria.id]), {'nombre': 'Bebidas frías'})
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Bebidas frías')

    def test_la_confirmacion_avisa_cuantos_productos_se_borraran(self):
        Producto.objects.create(nombre='Jugo', precio=7000, categoria=self.categoria)
        respuesta = self.client.get(reverse('categorias:eliminar', args=[self.categoria.id]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context['total_productos'], 1)
        self.assertContains(respuesta, 'CASCADE')

    def test_eliminar_una_categoria_borra_sus_productos(self):
        Producto.objects.create(nombre='Jugo', precio=7000, categoria=self.categoria)
        Producto.objects.create(nombre='Gaseosa', precio=4000, categoria=self.categoria)
        self.client.post(reverse('categorias:eliminar', args=[self.categoria.id]))
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())
        self.assertEqual(Producto.objects.count(), 0)

    def test_eliminar_una_categoria_no_toca_los_productos_de_otras(self):
        otra = Categoria.objects.create(nombre='Snacks')
        Producto.objects.create(nombre='Papas', precio=3000, categoria=otra)
        self.client.post(reverse('categorias:eliminar', args=[self.categoria.id]))
        self.assertTrue(Producto.objects.filter(nombre='Papas').exists())
