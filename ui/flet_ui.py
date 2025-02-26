import flet as ft
import pandas as pd
from pathlib import Path
import datetime
from modules.scrappers.exportar_iol import exportar_a_excel
from modules.scrappers.scrap_iol import obtener_datos_iol
from modules.notifier import enviar_notificacion 


import re

def parse_float(value: str) -> float:
     """
     Tu versión robusta de parse_float que maneja casos como '6.820.00', '6.570,00', etc.
     """
     # 1. Eliminar espacios, símbolo de $, etc. [esta es tu función actual robusta]
     tmp = value.strip().replace('$', '')
     tmp = re.sub(r'[^0-9\.,]+', '', tmp)
     if not tmp:
         return 0.0
     if ',' in tmp and '.' in tmp:
         tmp = tmp.replace('.', '')
         tmp = tmp.replace(',', '.')
     elif ',' in tmp and '.' not in tmp:
         tmp = tmp.replace(',', '.')
     elif '.' in tmp and ',' not in tmp:
         parts = tmp.rsplit('.', 1)
         main = parts[0].replace('.', '')
         decimals = parts[1]
         tmp = main + '.' + decimals
     try:
         return float(tmp)
     except ValueError:
         return 0.0



def variacion_color(variacion_str: str) -> str:
    if variacion_str.strip().startswith('-'):
        return "#EA4335"  # rojo
    return "#34A853"     # verde


def crear_modal_detalle(page):
    """Crea un modal vacío que se llenará con los datos de la inversión seleccionada."""
    
    def cerrar_modal(e):
        modal.open = False
        page.update()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detalles de la Inversión", weight="bold"),
        content=ft.Column(
            [
                ft.Text("Ticker:", weight="bold", size=16),
                ft.Text("", key="detalle_ticker"),
                ft.Text("Precio Actual:", weight="bold", size=16),
                ft.Text("", key="detalle_precio_actual"),
                ft.Text("Precio Objetivo:", weight="bold", size=16),
                ft.Text("", key="detalle_precio_objetivo"),
                ft.Text("Distancia al Objetivo:", weight="bold", size=16),
                ft.Text("", key="detalle_distancia"),
                ft.Text("Última Actualización:", weight="bold", size=16),
                ft.Text("", key="detalle_actualizacion"),
            ],
            spacing=10,
            height= 300,
            width= 300,
        ),
        actions=[ft.TextButton("Cerrar", on_click=cerrar_modal)],
    )

    page.overlay.append(modal)
    return modal

def abrir_modal_detalle(page, datos_inv, inv):
    """Muestra un modal con información detallada del activo, con estilo mejorado."""

    # 1. Intentamos encontrar si ya existe un modal con título "Detalles del Ticker"
    modal = next(
        (m for m in page.overlay
         if isinstance(m, ft.AlertDialog) and m.title.value == "Detalles del Ticker"),
        None
    )

    # 2. Si no existe, lo creamos
    if not modal:
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalles del Ticker", weight="bold", size=18),
            # Contenedor que envuelve la Column interna, para poder estilizar el fondo, padding, bordes, etc.
            content=ft.Container(
                content=ft.Column([], spacing=10),  # Column vacía: la llenaremos más abajo
                padding=ft.padding.all(20),
                bgcolor="#FAFAFA",           # Fondo claro
                border_radius=12,           # Bordes redondeados
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    # Llamamos a la función de cerrar
                    on_click=lambda e: cerrar_modal(e, modal, page),
                    style=ft.ButtonStyle(
                        # Botón color gris claro
                        color="#000000",      # Texto negro
                        bgcolor="#E5E7EB",    # Fondo gris claro
                    ),
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,   # Alinea el botón de acción a la derecha
            shape=ft.RoundedRectangleBorder(radius=12),   # Borde redondeado del AlertDialog en sí
            on_dismiss=lambda e: print("Modal cerrado")   # Callback si se cierra el modal
        )
        page.overlay.append(modal)

    # 3. Obtenemos la Column interna para llenarla con los controles
    contenido_modal = modal.content.content
    contenido_modal.controls.clear()  # Limpiamos por si ya había algo

    # 4. Extraer los datos que quieres mostrar
    precio_actual = datos_inv.get("ultimo_precio", "N/A")
    variacion = datos_inv.get("variacion", "N/A")
    apertura = datos_inv.get("apertura", "N/A")
    minimo = datos_inv.get("minimo", "N/A")
    maximo = datos_inv.get("maximo", "N/A")
    cierre_anterior = datos_inv.get("cierre_anterior", "N/A")
    precio_objetivo = inv.get("precio_objetivo", "N/A")

    # 5. Crear los controles de texto con la información
    contenido_modal.controls.extend([
        ft.Text(f"Ticker: {datos_inv['ticker']}", size=16, weight="bold"),
        ft.Text(f"Precio Actual: {precio_actual}", size=14),
        ft.Text(f"Variación: {variacion}", size=14),
        ft.Text(f"Apertura: {apertura}", size=14),
        ft.Text(f"Mínimo: {minimo}", size=14),
        ft.Text(f"Máximo: {maximo}", size=14),
        ft.Text(f"Cierre Anterior: {cierre_anterior}", size=14),
        ft.Text(f"Precio Objetivo: {precio_objetivo}", size=14),
        # Aquí podrías agregar más controles si lo deseas,
        # por ejemplo: distancia actual vs objetivo, etc.
    ])

    # 6. Mostramos el modal
    modal.open = True
    page.update()


def cerrar_modal(e, modal, page):
    """Cierra el modal."""
    modal.open = False
    page.update()


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
    """Crea y muestra solo las tarjetas de los activos que el usuario sigue."""
    
    inversiones = page.client_storage.get("inversiones") or []
    if not inversiones:
        print("⚠️ No hay inversiones guardadas en client_storage.")
    
    datos_scrapeados = obtener_datos_iol()
    if not datos_scrapeados:
        print("⚠️ No se obtuvieron datos scrapeados.")
        return ft.Column([ft.Text("⚠️ No hay datos disponibles.")]), None
    
    tickers_seguidos = {inv["ticker"].strip().upper() for inv in inversiones}
    print(f"✅ Tickers seguidos normalizados: {tickers_seguidos}")

    # Filtrar datos
    datos_filtrados = [
        dato for categoria in datos_scrapeados.values() for dato in categoria
        if dato["ticker"].strip().upper() in tickers_seguidos
    ]
    
    if not datos_filtrados:
        print("⚠️ Ningún ticker guardado tiene datos en el scrapping.")

    tarjetas_container = ft.ResponsiveRow()
    search_input = ft.TextField(
        hint_text="Buscar por ticker...",
        expand=True,
        on_change=lambda e: actualizar_tarjetas(e.control.value)
    )

    def actualizar_tarjetas(filtro=""):
        tarjetas_container.controls.clear()

        # Recuperar la lista de tickers que ya han recibido notificación
        tickers_notificados = set(page.client_storage.get("tickers_notificados") or [])

        for inv in inversiones:
            # Buscar los datos scrapeados
            datos_inv = next(
                (d for d in datos_filtrados if d["ticker"].strip().upper() == inv["ticker"].strip().upper()),
                None
            )
            if not datos_inv:
                continue

            if filtro.lower() not in inv["ticker"].lower():
                continue

            # Calcular el color de la variación
            color_variacion = variacion_color(datos_inv.get("variacion", "0.00%"))

            # Calcular la diferencia con parse_float
            actual = parse_float(datos_inv["ultimo_precio"])
            objetivo = parse_float(inv["precio_objetivo"])
            diferencia = actual - objetivo

            # 📌 Imprimir valores antes de enviar notificación
            print(f"📊 Ticker: {inv['ticker']} - Actual: {actual} - Objetivo: {objetivo}")
            print(f"🔍 Ya notificado? {'Sí' if inv['ticker'] in tickers_notificados else 'No'}")

            # ✅ Condición correcta
            if actual <= objetivo and inv["ticker"] not in tickers_notificados:
                print(f"🚀 Enviando notificación para {inv['ticker']}...")  # 📌 Mensaje de prueba
                enviar_notificacion(inv["ticker"], actual, objetivo)
                tickers_notificados.add(inv["ticker"])
                page.client_storage.set("tickers_notificados", list(tickers_notificados))  # Guardar como lista
                print(f"✅ Notificación enviada para {inv['ticker']}")

            else:
                print(f"❌ No se envió notificación para {inv['ticker']}")

            # Definir color según la distancia al objetivo
            color_distancia = "#34A853" if diferencia >= 0 else "#EA4335"
            dist_str = f"{diferencia:.2f}"

            # Construir la tarjeta
            tarjeta = ft.Container(
                content=ft.Column(
                    [
                        # Título y variación
                        ft.Row([
                            ft.Text(inv["ticker"], size=16, weight="bold"),
                            ft.Text(datos_inv["variacion"], color=color_variacion)
                        ]),
                        ft.Container(height=10),
                        # Precio actual
                        ft.Text(f"Precio actual: {datos_inv['ultimo_precio']}", size=14),
                        # Precio objetivo
                        ft.Text(f"Precio objetivo: {inv['precio_objetivo']}", size=14),
                        # Distancia al objetivo
                        ft.Text(
                            f"Distancia al objetivo: {dist_str}",
                            size=14,
                            color=color_distancia
                        ),
                        # Última actualización
                        ft.Text("Última actualización: Ahora", size=12, color="gray"),
                        ft.Container(height=10),
                        # Botones de detalle y eliminar
                        ft.Row([
                            ft.ElevatedButton(
                                "Ver detalles",
                                bgcolor="#34A853",
                                color="white",
                                on_click=lambda e, datos_inv=datos_inv, inv=inv: abrir_modal_detalle(page, datos_inv, inv)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                on_click=lambda e, inv=inv: eliminar_inversion(inv),
                            ),
                        ]),
                    ],
                    tight=True,
                    spacing=15
                ),
                padding=20,
                border_radius=12,
                bgcolor="white",
                shadow=ft.BoxShadow(blur_radius=10, color="#0000001A"),
                width=300,
            )
            tarjetas_container.controls.append(
                ft.Container(tarjeta, col={"xs": 12, "sm": 6, "md": 4, "lg": 3})
            )

        page.update()


    def agregar_inversion(ticker, precio_objetivo, frecuencia):
        if any(inv["ticker"] == ticker for inv in inversiones):
            print("⚠️ La inversión ya existe.")
            return

        nueva_inversion = {
            "ticker": ticker.upper(),
            "precio_objetivo": f"${precio_objetivo}",
            "frecuencia": frecuencia
        }
        inversiones.append(nueva_inversion)
        page.client_storage.set("inversiones", inversiones)
        actualizar_tarjetas()

    def eliminar_inversion(inversion):
        inversiones.remove(inversion)
        page.client_storage.set("inversiones", inversiones)
        actualizar_tarjetas()

    actualizar_tarjetas()

    return ft.Column(
        [
            search_input,
            ft.Container(
                content=ft.Column([tarjetas_container], scroll=ft.ScrollMode.ALWAYS, height=800)
            )
        ]
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

    # ✅ Limpiar los tickers notificados al iniciar la app (prueba para ver si soluciona el problema)
    page.client_storage.remove("tickers_notificados")

    # ✅ Verificar inversiones guardadas
    inversiones_guardadas = page.client_storage.get("inversiones")

    # ✅ Verificar datos scrapeados
    datos_scrapeados = obtener_datos_iol()


    # En main()
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
                                "📥 Descargar Data IOL",
                                bgcolor=ft.Colors.ORANGE_600,
                                color=ft.Colors.WHITE,
                                on_click=lambda e: exportar_a_excel(),  # Llama a la función de generación de Excel de IOL
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=10,
                                ),
                            ),
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
                                on_click=lambda e: exportar_excel(page),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=10,
                                ),
                            )
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                tarjetas_container,  # ✅ Ya incluye el buscador
            ],
            spacing=20
        )
    )

ft.app(target=main)
