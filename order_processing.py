import random

class Inventario:
    def __init__(self):
        self.stock = {}

    def agregar_producto(self, producto, cantidad):
        self.stock[producto] = cantidad

    def verificar_stock(self, producto, cantidad):
        return self.stock.get(producto, 0) >= cantidad

    def reducir_stock(self, producto, cantidad):
        if self.verificar_stock(producto, cantidad):
            self.stock[producto] -= cantidad
            return True
        return False

class Pagos:
    def procesar_pago(self, saldo_cliente, monto):
        return saldo_cliente >= monto  # Retorna True si el pago es exitoso

class Pedidos:
    def __init__(self, inventario, pagos):
        self.pedidos = {}  # ✅ Usamos un diccionario en lugar de una lista
        self.inventario = inventario
        self.pagos = pagos

    def realizar_pedido(self, producto, cantidad, saldo_cliente, precio_unitario):
        if self.inventario.verificar_stock(producto, cantidad):
            total = cantidad * precio_unitario
            if self.pagos.procesar_pago(saldo_cliente, total):
                self.inventario.reducir_stock(producto, cantidad)
                order_id = random.randint(1000, 9999)
                self.pedidos[order_id] = {"producto": producto, "cantidad": cantidad, "estado": "En proceso"}
                return f"Pedido confirmado. ID: {order_id}"
            return "Pago fallido"
        return "Stock insuficiente"

    def process_order(self, product, quantity, card_number, saldo_cliente, precio_unitario):
        if not product or quantity <= 0 or len(card_number) != 16:
            return "Error: Datos inválidos. Verifica la información ingresada."

        if self.inventario.verificar_stock(product, quantity):
            total = quantity * precio_unitario
            if self.pagos.procesar_pago(saldo_cliente, total):
                self.inventario.reducir_stock(product, quantity)
                order_id = random.randint(1000, 9999)
                self.pedidos[order_id] = {"producto": product, "cantidad": quantity, "estado": "En proceso"}
                return f"Pedido realizado con éxito. ID de pedido: {order_id}"
            return "Pago fallido"
        return "Stock insuficiente"

    def check_order_status(self, order_id):
        if order_id in self.pedidos:
            return f"Estado del pedido {order_id}: {self.pedidos[order_id]['estado']}"
        return "Error: Pedido no encontrado."
