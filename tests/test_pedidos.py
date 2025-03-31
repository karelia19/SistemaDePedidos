import sys
import os
import pytest
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from order_processing import Inventario, Pagos, Pedidos


@pytest.fixture
def inventario():
    inventario = Inventario()
    inventario.agregar_producto("Laptop", 5)  # Se agrega stock para la prueba
    return inventario

@pytest.fixture
def pagos():
    return Pagos()

@pytest.fixture
def pedidos(inventario, pagos):
    return Pedidos(inventario, pagos)

def test_realizar_pedido_exitoso(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 2, 500, 100)
    assert resultado.startswith("Pedido confirmado")  #Ahora acepta cualquier ID

def test_realizar_pedido_fallido_stock(pedidos):
    resultado = pedidos.realizar_pedido("Celular", 2, 500, 200)
    assert resultado == "Stock insuficiente"  #No hay stock de "Celular"

def test_realizar_pedido_fallido_pago(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 2, 100, 100)
    assert resultado == "Pago fallido"  #No tiene suficiente saldo
    
def test_realizar_pedido_exitoso_actualiza_stock(pedidos):
    pedidos.realizar_pedido("Laptop", 3, 500, 2000)
    assert pedidos.inventario.productos["Laptop"] == 2  # Quedaban 5 - 3 = 2

def test_realizar_pedido_fallido_pago_no_registra(pedidos):
    pedidos.realizar_pedido("Laptop", 2, 500, 100)  # Pago fallará
    assert len(pedidos.pedidos_realizados) == 0  # No se debe registrar el pedido

def test_notificacion_confirmacion(mocker, pedidos):
    mock_notificar = mocker.patch("order_processing.enviar_notificacion")
    pedidos.realizar_pedido("Laptop", 1, 500, 2000)
    mock_notificar.assert_called_once()  # Confirma que se envió notificación

def comprar(pedidos, resultados):
    resultado = pedidos.realizar_pedido("Laptop", 3, 500, 2000)
    resultados.append(resultado)

def test_manejo_concurrencia(pedidos):
    resultados = []
    t1 = threading.Thread(target=comprar, args=(pedidos, resultados))
    t2 = threading.Thread(target=comprar, args=(pedidos, resultados))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert resultados.count("Pedido confirmado. ID: 1") == 1
    assert resultados.count("Stock insuficiente") == 1  # Solo un pedido debe pasar

def test_pago_con_saldo_exacto(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 500)
    assert resultado.startswith("Pedido confirmado")

def test_pago_con_saldo_mayor(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 600)
    assert resultado.startswith("Pedido confirmado")

def test_pedido_producto_inexistente(pedidos):
    resultado = pedidos.realizar_pedido("TV", 1, 700, 1000)
    assert resultado == "Stock insuficiente"

def test_registro_pedido(pedidos):
    pedidos.realizar_pedido("Laptop", 1, 500, 1000)
    assert pedidos.pedidos_realizados[0]["producto"] == "Laptop"

def test_pago_fallido_saldo_exacto(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 499)
    assert resultado == "Pago fallido"

def test_reduccion_stock_exacta(pedidos):
    pedidos.realizar_pedido("Laptop", 5, 500, 3000)
    assert pedidos.inventario.productos["Laptop"] == 0

def test_pago_saldo_negativo(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, -50)
    assert resultado == "Pago fallido"

def test_ids_pedidos_unicos(pedidos):
    pedidos.realizar_pedido("Laptop", 1, 500, 1000)
    pedidos.realizar_pedido("Laptop", 1, 500, 1000)
    assert pedidos.pedidos_realizados[0]["id"] != pedidos.pedidos_realizados[1]["id"]

def test_cancelacion_pedido_sin_stock(pedidos):
    pedidos.realizar_pedido("Laptop", 5, 500, 3000)
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 1000)
    assert resultado == "Stock insuficiente"

def test_pedido_cantidad_negativa(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", -2, 500, 1000)
    assert resultado == "Stock insuficiente"

def test_realizar_pedido_exitoso(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 1000)
    assert resultado.startswith("Pedido confirmado")

def test_realizar_pedido_fallido_por_stock(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 10, 500, 5000)
    assert resultado == "Stock insuficiente"

def test_realizar_pedido_fallido_por_pago(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 100)
    assert resultado == "Pago fallido"

def test_realizar_pedido_producto_no_existente(pedidos):
    resultado = pedidos.realizar_pedido("TV", 1, 500, 1000)
    assert resultado == "Stock insuficiente"

def test_realizar_pedido_con_descuento(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, 450, 1000)
    assert resultado.startswith("Pedido confirmado")

def test_pedido_sin_cliente(pedidos):
    resultado = pedidos.realizar_pedido("", 1, 500, 1000)
    assert resultado == "Cliente no válido"

def test_pedido_monto_invalido(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 1, -500, 1000)
    assert resultado == "Monto inválido"

def test_pedido_cantidad_cero(pedidos):
    resultado = pedidos.realizar_pedido("Laptop", 0, 500, 1000)
    assert resultado == "Cantidad inválida"

def test_cancelar_pedido_producto_descontinuado(pedidos):
    pedidos.inventario.marcar_como_descontinuado("Laptop")
    resultado = pedidos.realizar_pedido("Laptop", 1, 500, 1000)
    assert resultado == "Producto no disponible"

def test_notificacion_pedido_rechazado(mocker, pedidos):
    mock_notificar = mocker.patch("order_processing.enviar_notificacion")
    pedidos.realizar_pedido("Laptop", 10, 500, 5000)  # Stock insuficiente
    mock_notificar.assert_called_with("Stock insuficiente para Laptop")


