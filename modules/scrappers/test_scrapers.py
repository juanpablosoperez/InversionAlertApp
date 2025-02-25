from modules.scrappers.scrap_yahoo import obtener_datos_yahoo
from modules.scrappers.scrap_google import obtener_datos_google
from modules.scrappers.scrap_iol import obtener_datos_iol
from modules.scrappers.scrap_stock import obtener_datos

def test_scrapers():
    print("🔍 Probando Scrapers...\n")

    # ✅ Test Yahoo Finance
    print("📌 Probando Yahoo Finance:")
    ticker = "AAPL"
    datos_yahoo = obtener_datos_yahoo(ticker)
    if datos_yahoo:
        print(datos_yahoo)
    else:
        print("❌ No se pudieron obtener datos de Yahoo Finance")

    print("\n-------------------------------------\n")

    # ✅ Test Google Finance
    print("📌 Probando Google Finance:")
    datos_google = obtener_datos_google(ticker)
    if datos_google:
        print(datos_google)
    else:
        print("❌ No se pudieron obtener datos de Google Finance")

    print("\n-------------------------------------\n")

    # ✅ Test InvertirOnline (IOL)
    print("📌 Probando InvertirOnline (IOL):")
    datos_iol = obtener_datos_iol()
    if datos_iol:
        print(datos_iol[:5])  # Muestra solo las primeras 5 inversiones
    else:
        print("❌ No se pudieron obtener datos de IOL")

    print("\n-------------------------------------\n")

    # ✅ Test Scraper General (stock)
    print("📌 Probando Scraper General:")
    datos_stock = obtener_datos(ticker, fuente="yahoo")
    if datos_stock:
        print(datos_stock)
    else:
        print("❌ No se pudieron obtener datos del scraper general")

if __name__ == "__main__":
    test_scrapers()
