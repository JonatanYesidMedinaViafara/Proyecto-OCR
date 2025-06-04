import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import sys
import warnings
import logging

# Silenciar warnings de pdfminer (usado por pdfplumber, camelot, etc.)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Silenciar posibles warnings de fitz / pymupdf
warnings.filterwarnings("ignore", message=".*CropBox missing.*")

# Permite importar config relativo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.extract_images import extraer_imagenes_de_pdf
from utils.extract_tables import extraer_tablas_de_pdf
from utils.extract_tables_ocr import extraer_tablas_ocr_pdf

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

# Aseguramos que la carpeta de salida exista
os.makedirs(config.CARPETA_SALIDA, exist_ok=True)

CARPETA_IMAGENES = os.path.join(config.BASE_DIR, "salida_imagenes")
os.makedirs(CARPETA_IMAGENES, exist_ok=True)

CARPETA_TABLAS = os.path.join(config.BASE_DIR, "salida_tablas")
os.makedirs(CARPETA_TABLAS, exist_ok=True)

CARPETA_TABLAS_OCR = os.path.join(config.BASE_DIR, "salida_tablas_ocr")
os.makedirs(CARPETA_TABLAS_OCR, exist_ok=True)

# Procesar todos los PDFs
for archivo in os.listdir(config.CARPETA_PDFS):
    if archivo.lower().endswith(".pdf"):
        ruta_pdf = os.path.join(config.CARPETA_PDFS, archivo)
        extraer_tablas_ocr_pdf(ruta_pdf, CARPETA_TABLAS_OCR)
        extraer_imagenes_de_pdf(ruta_pdf, CARPETA_IMAGENES)
        extraer_tablas_de_pdf(ruta_pdf, CARPETA_TABLAS)
        print(f"\nProcesando archivo: {archivo}")
        texto_total = ""

        try:
            doc = fitz.open(ruta_pdf)

            for num_pagina in range(len(doc)):
                pagina = doc.load_page(num_pagina)
                texto = pagina.get_text()

                if texto.strip():  # Si tiene texto embebido
                    texto_total += f"\n--- Página {num_pagina + 1} (texto embebido) ---\n"
                    texto_total += texto
                else:  # Si no tiene texto, hacemos OCR
                    print(f"Aplicando OCR en página {num_pagina + 1}")
                    pix = pagina.get_pixmap(dpi=300)
                    imagen_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                    
                    if imagen_np.shape[2] == 4:
                        imagen_np = cv2.cvtColor(imagen_np, cv2.COLOR_RGBA2RGB)

                    gris = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2GRAY)
                    gris = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                    ocr_texto = pytesseract.image_to_string(gris, lang='spa')
                    texto_total += f"\n--- Página {num_pagina + 1} (OCR) ---\n"
                    texto_total += ocr_texto

            nombre_salida = os.path.splitext(archivo)[0] + ".txt"
            ruta_salida = os.path.join(config.CARPETA_SALIDA, nombre_salida)

            with open(ruta_salida, "w", encoding="utf-8") as f:
                f.write(texto_total)

            print(f"Extracción finalizada para: {archivo}")

        except Exception as e:
            print(f"Error procesando {archivo}: {e}")
