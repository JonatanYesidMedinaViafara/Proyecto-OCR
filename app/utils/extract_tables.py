import camelot
import os
import pandas as pd
import re

# Limpieza básica del nombre (usamos misma lógica que en imágenes)
def normalizar_nombre(nombre):
    nombre = nombre.strip()
    nombre = re.sub(r'\s+', ' ', nombre)
    nombre = nombre.replace(" ", "_")
    nombre = re.sub(r'[^\w\-_\.]', '', nombre)
    return nombre

def extraer_tablas_de_pdf(ruta_pdf, carpeta_salida_tablas):
    nombre_pdf_original = os.path.splitext(os.path.basename(ruta_pdf))[0]
    nombre_pdf = normalizar_nombre(nombre_pdf_original)

    # Crear carpeta individual para tablas
    carpeta_pdf = os.path.join(carpeta_salida_tablas, nombre_pdf)
    os.makedirs(carpeta_pdf, exist_ok=True)

    print(f"Buscando tablas en: {nombre_pdf_original}")

    try:
        # Extraemos todas las tablas (stream trabaja mejor para PDFs sin líneas)
        tablas = camelot.read_pdf(ruta_pdf, pages='all', flavor='stream')

        if tablas:
            for i, tabla in enumerate(tablas, start=1):
                archivo_salida = os.path.join(carpeta_pdf, f"{nombre_pdf}_tabla_{i}.csv")
                tabla.df.to_csv(archivo_salida, index=False, encoding="utf-8-sig")
                print(f"Tabla {i} extraída y guardada: {archivo_salida}")
        else:
            print("No se detectaron tablas en este PDF.")
    except Exception as e:
        print(f"Error al extraer tablas de {nombre_pdf_original}: {e}")
