import reflex as rx

# 🧠 Estado global de la app — Aquí guardamos datos y lógica de negocio
class Estado(rx.State):
    # Variables reactivas para los inputs y resultado
    numero1: rx.Var[str] = rx.var("")
    numero2: rx.Var[str] = rx.var("")
    resultado: rx.Var[float] = rx.var(0.0)
    historial: rx.Var[list[str]] = rx.var([])

    # ⚙️ Método que realiza las operaciones básicas
    def operar(self, operacion: str):
        try:
            # Convertimos las entradas de texto a float para operar
            n1 = float(self.numero1.get()) if self.numero1.get() else 0.0
            n2 = float(self.numero2.get()) if self.numero2.get() else 0.0

            # Elegimos operación según la entrada
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
                # Control de división por cero
                if n2 == 0:
                    op = "Error: división entre 0"
                    res = 0.0
                else:
                    res = n1 / n2
                    op = f"{n1} / {n2} = {res}"
            else:
                op = "Operación desconocida"
                res = 0.0

            # Actualizamos el resultado reactivo
            self.resultado.set(res)

            # Añadimos la operación realizada al historial, creando una nueva lista para reactividad
            historial_actual = self.historial.get()
            self.historial.set(historial_actual + [op])
        except Exception as e:
            # En caso de error (por ejemplo en la conversión), se añade al historial
            historial_actual = self.historial.get()
            self.historial.set(historial_actual + [f"Error: {e}"])

    # 🧹 Método para limpiar todos los valores y el historial
    def limpiar(self):
        self.numero1.set("")
        self.numero2.set("")
        self.resultado.set(0.0)
        self.historial.set([])

# 📄 Definición de la página principal de la app con UI
def index():
    return rx.center(
        rx.vstack(
            rx.heading("Calculadora Reflex", size="6"),

            # Input para el primer número, reactivo con el estado
            rx.input(
                type_="number",
                placeholder="Número 1",
                value=Estado.numero1,
                on_change=lambda ev: Estado.numero1.set(ev.target.value),
            ),

            # Input para el segundo número
            rx.input(
                type_="number",
                placeholder="Número 2",
                value=Estado.numero2,
                on_change=lambda ev: Estado.numero2.set(ev.target.value),
            ),

            # Botones para seleccionar la operación a realizar
            rx.hstack(
                rx.button("➕", on_click=lambda: Estado.operar("suma")),
                rx.button("➖", on_click=lambda: Estado.operar("resta")),
                rx.button("✖️", on_click=lambda: Estado.operar("multiplicacion")),
                rx.button("➗", on_click=lambda: Estado.operar("division")),
            ),

            # Mostrar el resultado en pantalla
            rx.text("Resultado:", weight="bold", size="4"),
            rx.text(Estado.resultado, color="green", size="5"),

            # División visual
            rx.divider(),

            # Título y listado del historial de operaciones
            rx.heading("Historial", size="3"),
            rx.foreach(Estado.historial, lambda item: rx.text(item)),

            # Botón para limpiar inputs y resultados
            rx.button("Limpiar", color_scheme="red", on_click=Estado.limpiar),

            spacing="4",
        ),
        padding="4",
        min_height="100vh",
    )

# 🚀 Arranque de la app y registro de la página principal
app = rx.App()
app.add_page(index)
