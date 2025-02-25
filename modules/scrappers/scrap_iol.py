# scrap_iol.py
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://iol.invertironline.com"
ENDPOINTS = [
    "/mercado/cotizaciones/argentina/Acciones",
    "/mercado/cotizaciones/argentina/Cedears",
]

def obtener_datos_iol():
    """Scrapea Acciones y Cedears de InvertirOnline y devuelve los datos."""
    resultados = {}

    for endpoint in ENDPOINTS:
        url = BASE_URL + endpoint
        print(f"🔍 Scrapear {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error al acceder a {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        tabla = soup.find("table", {"id": "cotizaciones"})
        if not tabla:
            print(f"⚠ No se encontró la tabla en {url}")
            continue

        filas = tabla.find("tbody").find_all("tr", recursive=False)
        if not filas:
            print(f"⚠ La tabla no tiene filas en {url}")
            continue

        # Nombre de la categoría (Acciones, Cedears, etc.)
        categoria = endpoint.split("/")[-1].capitalize()
        datos_categoria = []

        for fila in filas:
            columnas = fila.find_all("td")
            if len(columnas) < 10:
                continue  # Ignorar filas que no tengan las columnas esperadas

            # EJEMPLO: "AAPL\r\n        Algo mas"
            # Vamos a dividir por espacios, y tomar la primera "palabra"
            # para quedarnos con "AAPL"
            raw_text = columnas[0].text.strip()
            # Dividir por espacios
            partes = raw_text.split()
            # Quedarnos con la primera parte y normalizar
            ticker_limpio = partes[0].upper()

            # Extraer el resto de datos como antes:
            ultimo_precio = columnas[1].text.strip()
            variacion = columnas[2].text.strip()
            apertura = columnas[7].text.strip()
            minimo = columnas[8].text.strip()
            maximo = columnas[9].text.strip()
            cierre_anterior = columnas[10].text.strip()

            datos_categoria.append({
                "ticker": ticker_limpio,
                "ultimo_precio": ultimo_precio,
                "variacion": variacion,
                "apertura": apertura,
                "minimo": minimo,
                "maximo": maximo,
                "cierre_anterior": cierre_anterior,
            })

        resultados[categoria] = datos_categoria

    return resultados
