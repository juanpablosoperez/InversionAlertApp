from modules.scrappers.scrap_yahoo import obtener_datos_yahoo
from modules.scrappers.scrap_google import obtener_datos_google
from modules.scrappers.scrap_iol import obtener_datos_iol  # ✅ Nuevo Import

def obtener_datos(ticker, fuente="yahoo"):
    """
    Obtiene los datos financieros según la fuente seleccionada.
    """
    if fuente == "yahoo":
        return obtener_datos_yahoo(ticker)
    elif fuente == "google":
        return obtener_datos_google(ticker)
    elif fuente == "iol":
        return obtener_datos_iol()  # ✅ Retorna la lista completa de inversiones de IOL
    else:
        return None
