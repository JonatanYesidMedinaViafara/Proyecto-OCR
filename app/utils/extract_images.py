import fitz  # PyMuPDF
import os
import re

# Función para limpiar nombres de carpetas
def normalizar_nombre(nombre):
    nombre = nombre.strip()  # quita espacios adelante y atrás
    nombre = re.sub(r'\s+', ' ', nombre)  # reemplaza múltiples espacios por uno solo
    nombre = nombre.replace(" ", "_")  # reemplaza espacios por guiones bajos (opcional)
    nombre = re.sub(r'[^\w\-_\.]', '', nombre)  # elimina caracteres raros
    return nombre

def extraer_imagenes_de_pdf(ruta_pdf, carpeta_salida_imagenes):
    doc = fitz.open(ruta_pdf)
    nombre_pdf_original = os.path.splitext(os.path.basename(ruta_pdf))[0]
    nombre_pdf = normalizar_nombre(nombre_pdf_original)

    # Creamos una subcarpeta específica para este PDF (ya limpia)
    carpeta_pdf = os.path.join(carpeta_salida_imagenes, nombre_pdf)
    os.makedirs(carpeta_pdf, exist_ok=True)

    for num_pagina in range(len(doc)):
        pagina = doc.load_page(num_pagina)
        imagenes = pagina.get_images(full=True)

        for img_index, img in enumerate(imagenes, start=1):
            xref = img[0]
            base_imagen = doc.extract_image(xref)
            imagen_bytes = base_imagen['image']
            extension = base_imagen['ext']

            nombre_archivo_imagen = f"{nombre_pdf}_p{num_pagina+1}_img{img_index}.{extension}"
            ruta_imagen_salida = os.path.join(carpeta_pdf, nombre_archivo_imagen)

            with open(ruta_imagen_salida, "wb") as img_file:
                img_file.write(imagen_bytes)

            print(f"Imagen extraída: {nombre_archivo_imagen}")

