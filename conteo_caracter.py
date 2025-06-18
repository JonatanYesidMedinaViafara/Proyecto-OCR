import os
import re
import pandas as pd
import pytesseract
from pdf2image import convert_from_path

# RUTA LOCAL A TESSERACT (ajustar según tu instalación)
# Ejemplo para Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def contar_letras_ocr(ruta_pdf):
    """Extrae texto con OCR y cuenta las letras"""
    try:
        paginas = convert_from_path(ruta_pdf, dpi=300)
        texto_total = ''
        for pagina in paginas:
            texto = pytesseract.image_to_string(pagina, lang='spa')  # OCR en español
            texto_total += texto
        
        # Contar solo letras (A-Z, incluyendo acentos y ñ)
        letras = re.findall(r'[A-Za-zÁÉÍÓÚáéíóúÑñ]', texto_total)
        return len(letras)
    
    except Exception as e:
        print(f"Error procesando {ruta_pdf}: {e}")
        return 0

def procesar_carpeta_pdf(ruta_carpeta):
    resultados = []
    
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith('.pdf'):
            ruta_pdf = os.path.join(ruta_carpeta, archivo)
            total_letras = contar_letras_ocr(ruta_pdf)
            resultados.append({
                'Archivo': archivo,
                'Cantidad_Letras': total_letras
            })
            print(f"Procesado: {archivo} -> {total_letras} letras")
    
    return resultados

if __name__ == "__main__":
    # Ajusta aquí la ruta de tu carpeta:
    ruta_carpeta = r'C:\Users\jhona\Desktop\Ayuda para anderson'
    
    resultados = procesar_carpeta_pdf(ruta_carpeta)
    
    df_resultados = pd.DataFrame(resultados)
    salida_excel = os.path.join(ruta_carpeta, 'resultado_letras_OCR.xlsx')
    df_resultados.to_excel(salida_excel, index=False)
    
    print(f"\nProceso finalizado. Resultados guardados en: {salida_excel}")
