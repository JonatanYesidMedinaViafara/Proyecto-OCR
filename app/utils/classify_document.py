import os
import re

def normalizar_nombre(nombre):
    nombre = nombre.strip()
    nombre = re.sub(r'\s+', ' ', nombre)
    nombre = nombre.replace(" ", "_")
    nombre = re.sub(r'[^\w\-_\.]', '', nombre)
    return nombre

def clasificar_documento(nombre_archivo):
    nombre_archivo = normalizar_nombre(nombre_archivo).lower()

    if "nomina" in nombre_archivo:
        return "DESPRENDIBLE_NOMINA"
    elif "conocimiento" in nombre_archivo:
        return "FORMATO_CONOCIMIENTO"
    elif "recompra" in nombre_archivo:
        return "SOPORTES_RECOMPRA"
    elif "datacredito" in nombre_archivo:
        return "DATACREDITO"
    elif "amortizacion" in nombre_archivo:
        return "AMORTIZACION"
    elif "fianza" in nombre_archivo:
        return "FIANZA"
    elif "cedula" in nombre_archivo:
        return "CEDULA"
    elif "solicitud" in nombre_archivo or "credito" in nombre_archivo:
        return "SOLICITUD_CREDITO"
    elif "seguro" in nombre_archivo or "vida" in nombre_archivo:
        return "SEGURO_DE_VIDA"
    elif "libranza" in nombre_archivo:
        return "LIBRANZA"
    else:
        return "NO_CLASIFICADO"
