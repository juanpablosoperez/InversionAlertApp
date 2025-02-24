import pandas as pd
from datetime import datetime
from pathlib import Path
from modules.scrappers.scrap_iol import obtener_datos_iol

def exportar_a_excel():
    """Genera un archivo Excel con los datos scrapeados de InvertirOnline, dividiendo en Acciones y Cedears."""
    
    # Obtener los datos scrapeados
    datos = obtener_datos_iol()
    
    if not datos:
        print("❌ No hay datos para exportar.")
        return
    
    # Obtener la carpeta de Descargas del usuario
    downloads_path = Path.home() / "Downloads"

    # Nombre del archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"inversiones_iol_{timestamp}.xlsx"
    filepath = downloads_path / filename

    # Crear un archivo Excel con los datos
    with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for categoria, valores in datos.items():
            if valores:
                df = pd.DataFrame(valores)
                df.to_excel(writer, sheet_name=categoria, index=False)

    print(f"✅ Archivo Excel generado en: {filepath}")

# Ejecutar la exportación
if __name__ == "__main__":
    exportar_a_excel()
