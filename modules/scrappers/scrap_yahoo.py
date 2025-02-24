import requests
from bs4 import BeautifulSoup

def obtener_datos_yahoo(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    precio_actual = soup.find("fin-streamer", {"data-field": "regularMarketPrice"}).text
    variacion = soup.find("fin-streamer", {"data-field": "regularMarketChangePercent"}).text
    
    return {
        "ticker": ticker,
        "precio_actual": precio_actual,
        "variacion": variacion
    }
