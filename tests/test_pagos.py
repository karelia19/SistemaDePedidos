import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from order_processing import Inventario, Pagos, Pedidos


@pytest.fixture
def pagos():
    return Pagos()

def test_pago_exitoso(pagos):
    assert pagos.procesar_pago(100, 50) is True

def test_pago_fallido_por_saldo_insuficiente(pagos):
    assert pagos.procesar_pago(20, 50) is False

def test_pago_exitoso(pagos):
    assert pagos.procesar_pago(100, 200) is True

def test_pago_fallido(pagos):
    assert pagos.procesar_pago(300, 200) is False

def test_pago_cero(pagos):
    assert pagos.procesar_pago(0, 200) is True

def test_pago_monto_cero(pagos):
    assert pagos.procesar_pago(0, 1000) is False

def test_pago_monto_negativo(pagos):
    assert pagos.procesar_pago(-50, 1000) is False

def test_pago_exitoso_exacto(pagos):
    assert pagos.procesar_pago(500, 500) is True

def test_pago_fallido_saldo_menor(pagos):
    assert pagos.procesar_pago(500, 499) is False

def test_pago_tarjeta_credito(pagos):
    assert pagos.procesar_pago(100, 200, metodo="tarjeta_credito") is True

def test_pago_tarjeta_debito(pagos):
    assert pagos.procesar_pago(100, 200, metodo="tarjeta_debito") is True

def test_pago_paypal(pagos):
    assert pagos.procesar_pago(100, 200, metodo="paypal") is True

def test_pago_metodo_invalido(pagos):
    assert pagos.procesar_pago(100, 200, metodo="cripto") is False

def test_procesar_reembolso(pagos):
    assert pagos.procesar_reembolso(100) is True

def test_procesar_reembolso_monto_negativo(pagos):
    assert pagos.procesar_reembolso(-100) is False

def test_reembolso_pago_fallido(mocker, pagos):
    mock_reembolso = mocker.patch("order_processing.procesar_reembolso")
    pagos.procesar_pago(300, 100)  # Pago fallará
    mock_reembolso.assert_called_once()

@pytest.mark.parametrize("metodo_pago", ["tarjeta_credito", "tarjeta_debito", "paypal"])
def test_procesar_pago_con_varios_metodos(pagos, metodo_pago):
    assert pagos.procesar_pago(500, 1000, metodo_pago) is True

def test_registro_intentos_pago_fallidos(mocker, pagos):
    mock_log = mocker.patch("order_processing.registrar_intento_fallido")
    pagos.procesar_pago(300, 100)  # Pago fallará
    mock_log.assert_called_once()