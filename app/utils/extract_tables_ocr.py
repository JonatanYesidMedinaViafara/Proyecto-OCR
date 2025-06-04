import os
import cv2
import pytesseract
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
import re

# Reutilizamos nuestra normalización de nombres
def normalizar_nombre(nombre):
    nombre = nombre.strip()
    nombre = re.sub(r'\s+', ' ', nombre)
    nombre = nombre.replace(" ", "_")
    nombre = re.sub(r'[^\w\-_\.]', '', nombre)
    return nombre

def extraer_tablas_ocr_pdf(ruta_pdf, carpeta_salida_tablas_ocr):
    nombre_pdf_original = os.path.splitext(os.path.basename(ruta_pdf))[0]
    nombre_pdf = normalizar_nombre(nombre_pdf_original)

    carpeta_pdf = os.path.join(carpeta_salida_tablas_ocr, nombre_pdf)
    os.makedirs(carpeta_pdf, exist_ok=True)

    print(f"Buscando tablas OCR en: {nombre_pdf_original}")

    try:
        paginas = convert_from_path(ruta_pdf, dpi=300)

        for num_pagina, imagen_pil in enumerate(paginas, start=1):
            imagen_np = np.array(imagen_pil)
            gris = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2GRAY)
            _, binaria = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY_INV)

            # Detección de líneas horizontales
            kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
            horizontal = cv2.erode(binaria, kernel_horizontal)
            horizontal = cv2.dilate(horizontal, kernel_horizontal)

            # Detección de líneas verticales
            kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
            vertical = cv2.erode(binaria, kernel_vertical)
            vertical = cv2.dilate(vertical, kernel_vertical)

            # Combinamos líneas
            tabla_mask = cv2.add(horizontal, vertical)

            # Encontramos contornos (celdas)
            contornos, _ = cv2.findContours(tabla_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            celdas = sorted(contornos, key=lambda ctr: (cv2.boundingRect(ctr)[1], cv2.boundingRect(ctr)[0]))

            datos_tabla = []

            for cnt in celdas:
                x, y, w, h = cv2.boundingRect(cnt)
                if w > 50 and h > 20:  # filtro de tamaño mínimo de celda
                    region = imagen_np[y:y+h, x:x+w]
                    texto = pytesseract.image_to_string(region, lang="spa")
                    datos_tabla.append((y, x, texto.strip()))

            # Armamos DataFrame básico
            df = pd.DataFrame(datos_tabla, columns=["y", "x", "contenido"])
            df = df.sort_values(by=["y", "x"]).reset_index(drop=True)
            df.drop(columns=["y", "x"], inplace=True)

            archivo_salida = os.path.join(carpeta_pdf, f"{nombre_pdf}_p{num_pagina}_tabla_ocr.csv")
            df.to_csv(archivo_salida, index=False, encoding="utf-8-sig")

            print(f"Tabla OCR extraída y guardada: {archivo_salida}")

    except Exception as e:
        print(f"Error al procesar OCR en {nombre_pdf_original}: {e}")
