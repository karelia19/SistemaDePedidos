import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Simulación de base de datos
discounts = {"Camiseta": 10, "Pantalón": 15, "Zapatos": 5}
order_history = []
cart = []

class OnlineOrderSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pedidos en Línea")
        self.root.geometry("900x700")
        self.root.configure(bg="#f8f8f8")

        # Estilo
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Verdana", 12), background="#f8f8f8", foreground="black")
        self.style.configure("TButton", font=("Verdana", 12), background="#0078D4", foreground="black", padding=10, width=15)
        self.style.map("TButton", background=[("active", "#005EB8")])
        self.style.configure("TEntry", font=("Verdana", 12), background="white", foreground="black", padding=5)
        self.style.configure("TCombobox", font=("Verdana", 12), background="white", foreground="black", padding=5)
        self.style.configure("TFrame", background="#f8f8f8")

        # Cargar iconos e imágenes de productos
        self.load_images()

        # Interfaz
        self.create_widgets()

    def load_images(self):
        self.images = {}
        for product in ["Camiseta", "Pantalón", "Zapatos"]:
            path = os.path.join(os.path.dirname(__file__), "assets", f"{product.lower()}.jpg")
            if os.path.exists(path):
                try:
                    self.images[product] = ImageTk.PhotoImage(Image.open(path).resize((120, 120)))
                except Exception as e:
                    print(f"Error al cargar la imagen {path}: {e}")
                    self.images[product] = None
            else:
                self.images[product] = None
                print(f"Error: No se encontró la imagen en {path}")

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=15, relief="groove")
        frame.pack(pady=20, padx=20, fill="both")

        ttk.Label(frame, text="Producto:", style="TLabel").grid(row=0, column=0, sticky="w")
        self.product_var = tk.StringVar()
        self.product_menu = ttk.Combobox(frame, textvariable=self.product_var, values=["Camiseta", "Pantalón", "Zapatos"], state="readonly", style="TCombobox")
        self.product_menu.grid(row=0, column=1, pady=5)
        self.product_menu.bind("<<ComboboxSelected>>", self.update_product_image)

        self.product_image_label = ttk.Label(frame)
        self.product_image_label.grid(row=0, column=2, rowspan=4, padx=10, pady=5)

        ttk.Label(frame, text="Cantidad:", style="TLabel").grid(row=1, column=0, sticky="w")
        self.quantity_var = tk.IntVar()
        ttk.Entry(frame, textvariable=self.quantity_var, style="TEntry").grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Número de Tarjeta:", style="TLabel").grid(row=2, column=0, sticky="w")
        self.card_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.card_var, show="*", style="TEntry").grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="ID de Pedido:", style="TLabel").grid(row=3, column=0, sticky="w")
        self.order_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.order_id_var, style="TEntry").grid(row=3, column=1, pady=5)

        buttons_frame = ttk.Frame(self.root, padding=10)
        buttons_frame.pack()

        ttk.Button(buttons_frame, text="Añadir al Carrito", command=self.add_to_cart, style="TButton").grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Eliminar del Carrito", command=self.remove_from_cart, style="TButton").grid(row=0, column=1, padx=5, pady=24)
        ttk.Button(buttons_frame, text="Vaciar Carrito", command=self.clear_cart, style="TButton").grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Ver Carrito", command=self.view_cart, style="TButton").grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Realizar Pedido", command=self.handle_order, style="TButton").grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Ver Historial", command=self.view_history, style="TButton").grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Aplicar Descuento", command=self.apply_discount, style="TButton").grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Ver Estado del Pedido", command=self.handle_check_status, style="TButton").grid(row=0, column=7, padx=5, pady=24)

        self.result_text = tk.Text(self.root, height=10, width=100, bg="white", fg="black", font=("Verdana", 10))
        self.result_text.pack(pady=10)

    def update_product_image(self, event):
        product = self.product_var.get()
        self.product_image_label.configure(image=self.images.get(product, None))

    def view_history(self):
        if not order_history:
            messagebox.showinfo("Historial", "No hay pedidos en el historial.")
        else:
            history_text = "\n".join(order_history)
            messagebox.showinfo("Historial de Pedidos", f"Historial de pedidos:\n{history_text}")

    def add_to_cart(self):
        product = self.product_var.get()
        quantity = self.quantity_var.get()
        if product and quantity > 0:
            cart.append((product, quantity))
            messagebox.showinfo("Carrito", f"{product} x{quantity} añadido al carrito.")
        else:
            messagebox.showerror("Error", "Seleccione un producto y cantidad válida.")

    def remove_from_cart(self):
        if cart:
            cart.pop()
            messagebox.showinfo("Carrito", "Se eliminó el último producto del carrito.")
        else:
            messagebox.showerror("Error", "El carrito está vacío.")

    def clear_cart(self):
        global cart
        cart.clear()
        messagebox.showinfo("Carrito", "Carrito vaciado.")

    def view_cart(self):
        if not cart:
            messagebox.showinfo("Carrito", "El carrito está vacío.")
        else:
            cart_items = "\n".join([f"{product} x{quantity}" for product, quantity in cart])
            messagebox.showinfo("Carrito", f"Contenido del carrito:\n{cart_items}")

    def apply_discount(self):
        product = self.product_var.get()
        if not product:
            messagebox.showerror("Error", "Seleccione un producto.")
            return

        if product in discounts:
            discount = discounts[product]
            messagebox.showinfo("Descuento", f"Descuento del {discount}% aplicado a {product}.")
        else:
            messagebox.showinfo("Descuento", f"No hay descuento disponible para {product}.")

    def handle_order(self):
        result = self.process_order(self.product_var.get(), self.quantity_var.get(), self.card_var.get())
        self.result_text.insert(tk.END, f"\n{result}\n")
        if "éxito" in result:
            order_history.append(result)

    def process_order(self, product, quantity, card_number):
        if not product or not quantity or not card_number:
            return "Error: Datos de pedido incompletos."
        return f"Pedido de {quantity} {product}(s) realizado con éxito con la tarjeta {card_number[-4:]}"

    def check_order_status(self, order_id):
        return f"Estado del pedido {order_id}: En proceso."

    def handle_check_status(self):
        order_id = self.order_id_var.get()
        if not order_id:
            messagebox.showerror("Error", "Ingrese un ID de pedido.")
            return

        status = self.check_order_status(order_id)
        messagebox.showinfo("Estado del Pedido", status)

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineOrderSystemApp(root)
    root.mainloop()