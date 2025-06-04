import os

# Carpeta principal (queda relativo al proyecto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpetas de entrada y salida
CARPETA_PDFS = os.path.join(BASE_DIR, "entrada_pdfs")
CARPETA_SALIDA = os.path.join(BASE_DIR, "salida_texto")

# Ruta a Tesseract OCR (cambiar solo aquí si es necesario)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
