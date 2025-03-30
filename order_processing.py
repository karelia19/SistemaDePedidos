import random

orders = {}

def process_order(product, quantity, card_number):
    if not product or quantity <= 0 or len(card_number) != 16:
        return "Error: Datos inválidos. Verifica la información ingresada."
    
    order_id = random.randint(1000, 9999)
    orders[order_id] = {"producto": product, "cantidad": quantity, "estado": "En proceso"}
    return f"Pedido realizado con éxito. ID de pedido: {order_id}"

def check_order_status(order_id):
    if order_id in orders:
        return f"Estado del pedido {order_id}: {orders[order_id]['estado']}"
    return "Error: Pedido no encontrado."
