import sys
import pytest
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from order_processing import Inventario, Pagos, Pedidos


@pytest.fixture
def inventario():
    inv = Inventario()
    inv.agregar_producto("Laptop", 10)
    return inv

def test_agregar_producto(inventario):
    inventario.agregar_producto("Mouse", 5)
    assert inventario.stock["Mouse"] == 5

def test_verificar_stock_suficiente(inventario):
    assert inventario.verificar_stock("Laptop", 5) is True

def test_verificar_stock_insuficiente(inventario):
    assert inventario.verificar_stock("Laptop", 15) is False

def test_reducir_stock_exitoso(inventario):
    assert inventario.reducir_stock("Laptop", 3) is True
    assert inventario.stock["Laptop"] == 7

def test_reducir_stock_fallido(inventario):
    assert inventario.reducir_stock("Laptop", 15) is False

def test_agregar_producto(inventario):
    inventario.agregar_producto("Mouse", 10)
    assert inventario.productos["Mouse"] == 10

def test_verificar_stock_suficiente(inventario):
    assert inventario.verificar_stock("Laptop", 5) is True

def test_verificar_stock_insuficiente(inventario):
    assert inventario.verificar_stock("Laptop", 10) is False

def test_verificar_stock_producto_no_existente(inventario):
    assert inventario.verificar_stock("Teclado", 1) is False

def test_reducir_stock_producto_no_existente(inventario):
    assert inventario.reducir_stock("Teclado", 1) is False

def test_agregar_producto_existente_incrementa_stock(inventario):
    inventario.agregar_producto("Laptop", 5)
    assert inventario.stock["Laptop"] == 15

def test_remover_producto_existente(inventario):
    inventario.remover_producto("Laptop")
    assert "Laptop" not in inventario.stock

def test_remover_producto_no_existente(inventario):
    assert inventario.remover_producto("Teclado") is False

def test_no_permitir_stock_negativo(inventario):
    assert inventario.reducir_stock("Laptop", -5) is False

def test_marcar_producto_como_descontinuado(inventario):
    inventario.marcar_como_descontinuado("Laptop")
    assert inventario.productos["Laptop"]["disponible"] is False

def test_verificar_producto_descontinuado(inventario):
    inventario.marcar_como_descontinuado("Laptop")
    assert inventario.verificar_stock("Laptop", 1) is False

def test_recuperar_producto_descontinuado(inventario):
    inventario.marcar_como_descontinuado("Laptop")
    inventario.habilitar_producto("Laptop")
    assert inventario.productos["Laptop"]["disponible"] is True

def test_consultar_stock_total(inventario):
    assert inventario.consultar_stock_total() == 10

def test_actualizar_stock(inventario):
    inventario.actualizar_stock("Laptop", 20)
    assert inventario.stock["Laptop"] == 20

def test_actualizar_stock_producto_no_existente(inventario):
    assert inventario.actualizar_stock("Teclado", 5) is False

