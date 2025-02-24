import flet as ft

def crear_modal(page):
    """Crea y retorna el modal para agregar una inversión."""
    
    def cerrar_modal(e):
        modal.open = False
        page.update()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Nueva Inversión", weight="bold"),
        content=ft.Column(
            [
                ft.Text("Ticker"),
                ft.TextField(hint_text="Ej: AAPL", bgcolor="white"),
                ft.Container(height=15),  # Espacio adicional
                ft.Text("Precio Objetivo"),
                ft.TextField(hint_text="0.00", bgcolor="white"),
                ft.Container(height=15),  # Espacio adicional
                ft.Text("Frecuencia de Revisión"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("1 min"),
                        ft.dropdown.Option("5 min"),
                        ft.dropdown.Option("15 min"),
                    ],
                    hint_text="Seleccionar frecuencia",
                    bgcolor="white",
                    item_height=30
                ),
            ],
            spacing=20,# Aumenta el espaciado entre filas
            width=250,
            height= 400
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(bgcolor="#E9ECEF", color="black")),
            ft.TextButton("Agregar", on_click=cerrar_modal, style=ft.ButtonStyle(bgcolor="#34A853", color="white")),
        ],
    )

    # Agregamos el modal a `page.overlay` para que siempre esté disponible
    page.overlay.append(modal)
    return modal

def crear_encabezado(page, modal):
    """Crea y retorna el encabezado con métricas y botón para agregar inversión."""

    def abrir_modal(e):
        """Función para abrir el modal al hacer clic en el botón."""
        modal.open = True  # Ahora el modal se activa desde `page.overlay`
        page.update()

    return ft.Row(
        [
            ft.Text("Inversion Alert", size=24, weight="bold"),
            ft.Row([
                ft.Text("3 inversiones monitoreadas", size=14, color="black"),
                ft.Text(" • 0 alcanzaron objetivo", size=14, color="black"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.ElevatedButton(
                "+ Agregar Inversión",
                bgcolor="#34A853",
                color="white",
                on_click=abrir_modal,  # ✅ Ahora pasa la función correctamente
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=10,
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

def crear_barra_busqueda():
    """Crea y retorna la barra de búsqueda y filtros."""
    return ft.Row(
        [
            ft.TextField(hint_text="Buscar por ticker...", expand=True),
            ft.Dropdown(
                options=[
                    ft.dropdown.Option("Ticker [A->Z]"),
                    ft.dropdown.Option("Precio Actual"),
                    ft.dropdown.Option("Precio Objetivo"),
                ],
                hint_text="Ordenar por",
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

def crear_tarjetas():
    """Crea y retorna las tarjetas de inversiones en una fila."""
    inversiones = [
        {"ticker": "AAPL", "pct": "1.23%", "color": "#34A853", "precio_actual": "$185.92", "precio_objetivo": "$200", "distancia": "-7.04%", "ultima_actualizacion": "Hace 1 min"},
        {"ticker": "GOOGL", "pct": "0.78%", "color": "#34A853", "precio_actual": "$142.89", "precio_objetivo": "$150", "distancia": "-4.74%", "ultima_actualizacion": "Hace 12 min"},
        {"ticker": "MELI", "pct": "-0.45%", "color": "#EA4335", "precio_actual": "$1456.78", "precio_objetivo": "$1500", "distancia": "-2.88%", "ultima_actualizacion": "Hace 3 min"},
    ]

    tarjetas = []
    for inv in inversiones:
        tarjeta = ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text(inv["ticker"], size=16, weight="bold"),
                        ft.Text(inv["pct"], color=inv["color"]),
                    ]),
                    ft.Container(height=10),  # Espacio adicional entre elementos
                    ft.Text(f"Precio actual: {inv['precio_actual']}", size=14),
                    ft.Text(f"Precio objetivo: {inv['precio_objetivo']}", size=14),
                    ft.Text(f"Distancia al objetivo: {inv['distancia']}", size=14, color=inv["color"]),
                    ft.Text(f"Última actualización: {inv['ultima_actualizacion']}", size=12, color="gray"),
                    ft.Container(height=10),  # Espacio antes del botón
                    ft.ElevatedButton("Ver detalles", bgcolor="#34A853", color="white"),
                ],
                tight=True,
                spacing=15  # Aumenta el espaciado dentro de cada tarjeta
            ),
            padding=20,
            border_radius=12,
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=10, color="#0000001A"),
            width=350,  # Ajustar tamaño de cada tarjeta
        )
        tarjetas.append(tarjeta)

    return ft.Row(tarjetas, alignment=ft.MainAxisAlignment.CENTER, spacing=30)

def main(page: ft.Page):
    """Función principal que gestiona la página."""
    page.title = "Inversion Alert"
    page.bgcolor = "#FFFFFF"
    page.theme_mode = "light"
    
    modal = crear_modal(page)  # Crear el modal y pasarlo a `page.overlay`

    # Agregar elementos a la página
    page.add(
        ft.Column(
            [
                crear_encabezado(page, modal),
                ft.Container(content=crear_barra_busqueda(), padding=10),
                ft.Container(content=crear_tarjetas(), padding=20),
            ],
            spacing=20
        )
    )

ft.app(target=main)
