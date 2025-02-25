import flet as ft
from ui.componentes import crear_tabla_datos_scrapeados

def cargar_datos_scrapeados(page):
    """Carga los datos scrapeados y genera una tabla solo con los activos seguidos."""

    # Obtener datos guardados
    datos_scrapeados = page.client_storage.get("datos_scrapeados")

    # Si no es un diccionario, reiniciar almacenamiento
    if not isinstance(datos_scrapeados, dict):
        print("⚠️ Error: datos_scrapeados no es un diccionario. Reiniciando almacenamiento...")
        page.client_storage.set("datos_scrapeados", {})
        return ft.Text("⚠️ No se encontraron datos válidos.")

    # Obtener inversiones seguidas por el usuario
    inversiones_seguidas = page.client_storage.get("inversiones") or []
    tickers_seguidos = {inv["ticker"] for inv in inversiones_seguidas}

    # Filtrar solo los activos seguidos
    datos_filtrados = [
        activo for categoria in datos_scrapeados.values()
        for activo in categoria if activo["ticker"] in tickers_seguidos
    ]

    # Si no hay datos seguidos, mostrar mensaje
    if not datos_filtrados:
        return ft.Text("⚠️ No se encontraron datos para las inversiones seguidas.")

    # Crear y devolver tabla con los datos filtrados
    return crear_tabla_datos_scrapeados(datos_filtrados)

def crear_tabla_datos_scrapeados(datos):
    """Crea una tabla de datos filtrados."""

    # Si no hay datos, devolver mensaje
    if not datos:
        return ft.Text("⚠️ No hay datos disponibles.")

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Ticker")),
            ft.DataColumn(ft.Text("Último Precio")),
            ft.DataColumn(ft.Text("Variación")),
            ft.DataColumn(ft.Text("Apertura")),
            ft.DataColumn(ft.Text("Mínimo")),
            ft.DataColumn(ft.Text("Máximo")),
            ft.DataColumn(ft.Text("Cierre Anterior")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(d["ticker"])),
                    ft.DataCell(ft.Text(d["ultimo_precio"])),
                    ft.DataCell(ft.Text(d["variacion"])),
                    ft.DataCell(ft.Text(d["apertura"])),
                    ft.DataCell(ft.Text(d["minimo"])),
                    ft.DataCell(ft.Text(d["maximo"])),
                    ft.DataCell(ft.Text(d["cierre_anterior"])),
                ]
            ) for d in datos
        ]
    )

def agregar_a_seguimiento(page: ft.Page, inversion):
    """Agrega una inversión seleccionada a la lista de seguimiento."""
    inversiones = page.client_storage.get("inversiones") or []
    inversiones.append(inversion)
    page.client_storage.set("inversiones", inversiones)
    print(f"✅ {inversion['ticker']} agregado a seguimiento.")
    page.update()
