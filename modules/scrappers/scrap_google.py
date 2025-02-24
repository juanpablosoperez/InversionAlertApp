import requests
from bs4 import BeautifulSoup

def obtener_datos_google(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    precio = soup.find("div", {"class": "YMlKec fxKbKc"}).text
    
    return {
        "ticker": ticker,
        "precio_actual": precio
    }
