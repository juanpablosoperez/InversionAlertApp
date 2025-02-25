import flet as ft
from ui.componentes import crear_tabla_datos_scrapeados

def cargar_datos_scrapeados(page):
    """Carga los datos scrapeados y genera una tabla solo con los activos seguidos."""

    # Obtener datos guardados
    datos_scrapeados = page.client_storage.get("datos_scrapeados")

    # Si no es un diccionario, reiniciamos
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

    # Crear tabla con los datos filtrados
    return crear_tabla_datos_scrapeados(datos_filtrados)




