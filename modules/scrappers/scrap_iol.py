import requests
from bs4 import BeautifulSoup

def obtener_cotizaciones_iol():
    """Scrapea las cotizaciones de InvertirOnline y devuelve una lista de diccionarios."""
    url = "https://iol.invertironline.com/mercado/cotizaciones"
    headers = {"User-Agent": "Mozilla/5.0"}  # Para evitar bloqueos

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Error al acceder a la página de IOL")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscar la tabla de cotizaciones
    tabla = soup.find("table", {"id": "cotizaciones"})
    if not tabla:
        print("❌ No se encontró la tabla de cotizaciones.")
        return []

    cotizaciones = []
    
    # Iterar sobre las filas de la tabla
    for fila in tabla.find("tbody").find_all("tr"):
        columnas = fila.find_all("td")
        if len(columnas) < 12:  # Asegurarse de que tenga suficientes datos
            continue

        ticker = columnas[0].find("b").text.strip()
        ultimo_precio = columnas[1].text.strip()
        variacion = columnas[2].text.strip()
        apertura = columnas[7].text.strip()
        minimo = columnas[8].text.strip()
        maximo = columnas[9].text.strip()
        cierre_anterior = columnas[10].text.strip()

        cotizacion = {
            "ticker": ticker,
            "ultimo_precio": ultimo_precio,
            "variacion": variacion,
            "apertura": apertura,
            "minimo": minimo,
            "maximo": maximo,
            "cierre_anterior": cierre_anterior
        }
        
        cotizaciones.append(cotizacion)

    return cotizaciones

# Prueba del scraper
if __name__ == "__main__":
    datos = obtener_cotizaciones_iol()
    for dato in datos[:50]:  # Mostrar solo las primeras 5 cotizaciones
        print(dato)
