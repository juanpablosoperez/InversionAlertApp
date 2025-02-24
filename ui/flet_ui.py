import flet as ft
import pandas as pd
from pathlib import Path
import datetime

def crear_modal(page, agregar_inversion):
    """Crea y retorna el modal para agregar una inversión."""

    ticker_input = ft.TextField(hint_text="Ej: AAPL", bgcolor="white")
    precio_objetivo_input = ft.TextField(hint_text="0.00", bgcolor="white")
    frecuencia_input = ft.Dropdown(
        options=[
            ft.dropdown.Option("1 min"),
            ft.dropdown.Option("5 min"),
            ft.dropdown.Option("15 min"),
        ],
        hint_text="Seleccionar frecuencia",
        bgcolor="white",
        item_height=30
    )

    def limpiar_campos_modal():
        """Limpia los campos del modal después de agregar una inversión."""
        ticker_input.value = ""
        precio_objetivo_input.value = ""
        frecuencia_input.value = None
        page.update()

    def cerrar_modal(e):
        modal.open = False
        page.update()

    def confirmar_agregar(e):
        """Función para agregar la inversión y limpiar los campos."""
        if ticker_input.value and precio_objetivo_input.value:
            agregar_inversion(ticker_input.value, precio_objetivo_input.value, frecuencia_input.value)
            limpiar_campos_modal()  # ✅ Limpia los campos después de agregar
            modal.open = False
            page.update()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Nueva Inversión", weight="bold"),
        content=ft.Column(
            [
                ft.Text("Ticker"),
                ticker_input,
                ft.Container(height=15),
                ft.Text("Precio Objetivo"),
                precio_objetivo_input,
                ft.Container(height=15),
                ft.Text("Frecuencia de Revisión"),
                frecuencia_input,
            ],
            spacing=20,
            width=250,
            height=400
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(bgcolor="#E9ECEF", color="black")),
            ft.TextButton("Agregar", on_click=confirmar_agregar, style=ft.ButtonStyle(bgcolor="#34A853", color="white")),
        ],
    )

    page.overlay.append(modal)
    return modal

def crear_tarjetas(page):
    """Crea y retorna un contenedor dinámico de tarjetas de inversiones."""

    if not page.client_storage.contains_key("inversiones"):
        page.client_storage.set("inversiones", [])

    tarjetas_container = ft.ResponsiveRow()

    def actualizar_tarjetas():
        """Función para actualizar la visualización de las inversiones."""
        tarjetas_container.controls.clear()
        inversiones = page.client_storage.get("inversiones")

        for inv in inversiones:
            tarjeta = ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Text(inv["ticker"], size=16, weight="bold"),
                            ft.Text(inv["pct"], color=inv["color"]),
                        ]),
                        ft.Container(height=10),
                        ft.Text(f"Precio actual: {inv['precio_actual']}", size=14),
                        ft.Text(f"Precio objetivo: {inv['precio_objetivo']}", size=14),
                        ft.Text(f"Distancia al objetivo: {inv['distancia']}", size=14, color=inv["color"]),
                        ft.Text(f"Última actualización: {inv['ultima_actualizacion']}", size=12, color="gray"),
                        ft.Container(height=10),
                        ft.Row([
                            ft.ElevatedButton("Ver detalles", bgcolor="#34A853", color="white"),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, inv=inv: eliminar_inversion(inv)),
                        ]),
                    ],
                    tight=True,
                    spacing=15
                ),
                padding=20,
                border_radius=12,
                bgcolor="white",
                shadow=ft.BoxShadow(blur_radius=10, color="#0000001A"),
                width=300,  # Tamaño de cada tarjeta
            )

            tarjetas_container.controls.append(
                ft.Container(
                    tarjeta,
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3}  # ✅ Hasta 4 tarjetas por fila
                )
            )

        page.update()

    def agregar_inversion(ticker, precio_objetivo, frecuencia):
        """Función para agregar una nueva inversión a la lista."""
        inversiones = page.client_storage.get("inversiones")
        nueva_inversion = {
            "ticker": ticker.upper(),
            "pct": "0.00%",
            "color": "#34A853",
            "precio_actual": "$0.00",
            "precio_objetivo": f"${precio_objetivo}",
            "distancia": "-",
            "ultima_actualizacion": "Ahora",
            "frecuencia": frecuencia
        }
        inversiones.append(nueva_inversion)
        page.client_storage.set("inversiones", inversiones)
        actualizar_tarjetas()

    def eliminar_inversion(inversion):
        """Función para eliminar una inversión de la lista."""
        inversiones = page.client_storage.get("inversiones")
        inversiones.remove(inversion)
        page.client_storage.set("inversiones", inversiones)
        actualizar_tarjetas()

    actualizar_tarjetas()
    return ft.Container(
        content=ft.Column([tarjetas_container], scroll=ft.ScrollMode.ALWAYS, height=800)
    ), agregar_inversion

def exportar_excel(page):
    """Exporta las inversiones a un archivo Excel en la carpeta Documentos y muestra un mensaje de éxito."""

    # ✅ Obtener las inversiones almacenadas en memoria
    inversiones = page.client_storage.get("inversiones") or []  # Si no hay datos, devuelve una lista vacía

    if not inversiones:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("No hay inversiones para exportar."),
            bgcolor=ft.Colors.RED_400
        )
        page.snack_bar.open = True
        page.update()
        return

    # ✅ Ruta de exportación
    documentos_path = Path.home() / "Downloads"
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"inversiones_{timestamp}.xlsx"
    filepath = documentos_path / filename

    # ✅ Crear DataFrame con las inversiones
    df = pd.DataFrame(inversiones, columns=["ticker", "precio_actual", "precio_objetivo", "distancia", "ultima_actualizacion"])
    df.to_excel(filepath, index=False)

    def cerrar_popup(e):
        popup_exportacion.open = False
        page.update()

    # ✅ Popup de confirmación
    popup_exportacion = ft.AlertDialog(
        modal=True,
        title=ft.Text("Exportación Exitosa", size=20),
        content=ft.Column([
            ft.Text("El archivo se ha guardado en:"),
            ft.Container(
                content=ft.Text(
                    str(filepath),
                    color=ft.Colors.BLUE_400,
                    weight=ft.FontWeight.BOLD,
                    selectable=True
                ),
                padding=10,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                border_radius=5
            ),
            ft.Text("Revisa tu carpeta de Documentos."),
        ], tight=True),
        actions=[
            ft.TextButton("Aceptar", on_click=cerrar_popup),
        ],
    )

    # ✅ Agregar el popup a `page.overlay` y mostrarlo
    page.overlay.append(popup_exportacion)
    popup_exportacion.open = True
    page.update()



def main(page: ft.Page):
    """Función principal que gestiona la página."""
    page.title = "Inversion Alert"
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = "light"

    tarjetas_container, agregar_inversion = crear_tarjetas(page)
    modal = crear_modal(page, agregar_inversion)

    # ✅ Función para abrir el modal
    def abrir_modal(e):
        modal.open = True
        page.update()

    # ✅ UI Principal
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Inversion Alert", size=24, weight="bold"),
                        ft.Row([
                            ft.Text("3 inversiones monitoreadas", size=14, color=ft.Colors.BLACK),
                            ft.Text(" • 0 alcanzaron objetivo", size=14, color=ft.Colors.BLACK),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            ft.ElevatedButton(
                                "+ Agregar Inversión",
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                on_click=abrir_modal,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=10,
                                ),
                            ),
                            ft.ElevatedButton(
                                "Exportar a Excel",
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                on_click=lambda e: exportar_excel(page),  # ✅ Llama a la función correctamente
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=10,
                                ),
                            )
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(content=ft.Row([
                    ft.TextField(hint_text="Buscar por ticker...", expand=True),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("Ticker [A->Z]"),
                            ft.dropdown.Option("Precio Actual"),
                            ft.dropdown.Option("Precio Objetivo"),
                        ],
                        hint_text="Ordenar por",
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=10),
                tarjetas_container,
            ],
            spacing=20
        )
    )

ft.app(target=main)