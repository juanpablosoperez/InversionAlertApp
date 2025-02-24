import requests
from bs4 import BeautifulSoup

# URL base
BASE_URL = "https://iol.invertironline.com"

# Diccionario con los tipos de instrumentos a scrapear
INSTRUMENTOS = {
    "Acciones": "/mercado/cotizaciones/argentina/Acciones",
    "Cedears": "/mercado/cotizaciones/argentina/Cedears"
}

def obtener_datos_iol():
    """Scrapea Acciones y Cedears en InvertirOnline y devuelve los datos."""
    resultados = {}

    for categoria, path in INSTRUMENTOS.items():
        url = BASE_URL + path
        print(f"🔍 Scrapear {categoria}: {url}")

        # Obtener el contenido de la página
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error al acceder a {url}")
            continue

        # Parsear la página con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar la tabla de cotizaciones
        tabla = soup.find("table", {"id": "cotizaciones"})
        if not tabla:
            print(f"⚠ No se encontró la tabla en {categoria}, saltando...")
            continue

        # Extraer las filas de la tabla
        filas = tabla.find("tbody").find_all("tr")
        if not filas:
            print(f"⚠ No hay datos en {categoria}, saltando...")
            continue

        datos_categoria = []

        for fila in filas:
            columnas = fila.find_all("td")

            if len(columnas) < 10:  # Si la fila tiene menos columnas de las esperadas, la ignoramos
                continue

            datos = {
                "ticker": columnas[0].text.strip(),
                "ultimo_precio": columnas[1].text.strip(),
                "variacion": columnas[2].text.strip(),
                "apertura": columnas[7].text.strip(),
                "minimo": columnas[8].text.strip(),
                "maximo": columnas[9].text.strip(),
                "cierre_anterior": columnas[10].text.strip(),
            }

            datos_categoria.append(datos)

        resultados[categoria] = datos_categoria

    return resultados

# Ejecutar el scraper y mostrar resultados
if __name__ == "__main__":
    datos = obtener_datos_iol()
    for categoria, valores in datos.items():
        print(f"\n📌 {categoria}: {len(valores)} registros obtenidos")
        for v in valores[:5]:  # Mostrar solo los primeros 5 por categoría
            print(v)
