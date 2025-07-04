# app/utils/organize_by_reference.py

import os
import shutil

def organizar_por_referencia(ruta_origen, ruta_destino):
    """
    Organiza archivos PDF desde una carpeta de entrada hacia subcarpetas
    nombradas según una referencia extraída del nombre del archivo (posición [2]).
    
    Args:
        ruta_origen (str): Ruta con todos los archivos PDF mezclados.
        ruta_destino (str): Ruta base donde se creará una carpeta por cada referencia.
    """
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)

    for archivo in os.listdir(ruta_origen):
        if archivo.lower().endswith('.pdf'):
            partes = archivo.split('_')
            if len(partes) >= 3:
                referencia = partes[2]  # Toma la parte [2] del nombre
                carpeta_referencia = os.path.join(ruta_destino, referencia)

                # Crear carpeta si no existe
                if not os.path.exists(carpeta_referencia):
                    os.makedirs(carpeta_referencia)

                # Rutas completas de origen y destino
                origen_archivo = os.path.join(ruta_origen, archivo)
                destino_archivo = os.path.join(carpeta_referencia, archivo)

                # Copiar archivo
                shutil.move(origen_archivo, destino_archivo)
                print(f"📁 {archivo} → {referencia}/")
            else:
                print(f"❌ Nombre inválido (menos de 3 segmentos separados por '_'): {archivo}")
