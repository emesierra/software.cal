import reflex as rx

# 🧠 Estado global de la app — Aquí guardamos datos y lógica de negocio
class Estado(rx.State):
    # Variables que controlan los inputs y el resultado
    numero1: str = ""
    numero2: str = ""
    resultado: float = 0.0
    historial: list[str] = []

    # ⚙️ Función que realiza las operaciones básicas
    def operar(self, operacion: str):
        try:
            # Convertimos los inputs a float si existen, si no, se toma como 0.0
            n1 = float(self.numero1) if self.numero1 else 0.0
            n2 = float(self.numero2) if self.numero2 else 0.0

            # Procesamos según el tipo de operación
            if operacion == "suma":
                res = n1 + n2
                op = f"{n1} + {n2} = {res}"
            elif operacion == "resta":
                res = n1 - n2
                op = f"{n1} - {n2} = {res}"
            elif operacion == "multiplicacion":
                res = n1 * n2
                op = f"{n1} * {n2} = {res}"
            elif operacion == "division":
                if n2 == 0:
                    op = "Error: división entre 0"
                    res = 0.0
                else:
                    res = n1 / n2
                    op = f"{n1} / {n2} = {res}"
            else:
                op = "Operación desconocida"
                res = 0.0

            # Guardamos el resultado y la operación en el historial
            self.resultado = res
            self.historial.append(op)
        except Exception as e:
            # En caso de error (por ejemplo conversión fallida), lo agregamos al historial
            self.historial.append(f"Error: {e}")

    # 🧹 Función para limpiar los campos y el historial
    def limpiar(self):
        self.numero1 = ""
        self.numero2 = ""
        self.resultado = 0.0
        self.historial = []

# 📄 Página principal de la app
def index():
    return rx.center(
        rx.vstack(
            rx.heading("Calculadora Reflex", size="6"),

            # Input para el número 1
            rx.input(
                type_="number",
                placeholder="Número 1",
                value=Estado.numero1,
                on_change=lambda v: Estado.set_numero1(v),
            ),

            # Input para el número 2
            rx.input(
                type_="number",
                placeholder="Número 2",
                value=Estado.numero2,
                on_change=lambda v: Estado.set_numero2(v),
            ),

            # Botones de operaciones aritméticas
            rx.hstack(
                rx.button("➕", on_click=lambda: Estado.operar("suma")),
                rx.button("➖", on_click=lambda: Estado.operar("resta")),
                rx.button("✖️", on_click=lambda: Estado.operar("multiplicacion")),
                rx.button("➗", on_click=lambda: Estado.operar("division")),
            ),

            # Resultado mostrado
            rx.text("Resultado:", weight="bold", size="4"),
            rx.text(Estado.resultado, color="green", size="5"),

            # Historial de operaciones
            rx.divider(),
            rx.heading("Historial", size="3"),
            rx.foreach(Estado.historial, lambda item: rx.text(item)),

            # Botón para limpiar
            rx.button("Limpiar", color_scheme="red", on_click=Estado.limpiar),

            spacing="4",
        ),
        padding="4",
        min_height="100vh"
    )

# 🚀 Arranque de la app
app = rx.App()
app.add_page(index)
