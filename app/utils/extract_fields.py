import re

def extraer_campos_desprendible_nomina(texto):
    datos = {}

    # Cédula de ciudadanía
    cedula = re.search(r"C[eé]dula\s+de\s+Ciudadan[ií]a\s+No\.?\s*([0-9]{5,15})", texto, re.IGNORECASE)
    datos['cedula'] = cedula.group(1) if cedula else None

    # Nombre
    nombre = re.search(r"señor\(a\)\s+([A-ZÑÁÉÍÓÚ ]+?)\s+identificado\(a\)", texto, re.IGNORECASE)
    datos['nombre'] = nombre.group(1).strip() if nombre else None

    # Fecha de pago (expedición)
    fecha = re.search(r"el día (\d{1,2}) de ([a-zA-ZñÑ]+) de (\d{4})", texto, re.IGNORECASE)
    if fecha:
        dia, mes_texto, anio = fecha.groups()
        datos['fecha_pago'] = f"{dia.zfill(2)}/{mes_texto}/{anio}"
    else:
        datos['fecha_pago'] = None

    # Valor pensión
    salario = re.search(r"VALOR PENSION\s*\$\s*([0-9\.,]+)", texto, re.IGNORECASE)
    datos['salario'] = salario.group(1).replace('.', '').replace(',', '.') if salario else None

    # Total deducciones
    deduccion = re.search(r"TOTAL DEDUCIDOS\s*\$\s*([0-9\.,]+)", texto, re.IGNORECASE)
    datos['deducciones'] = deduccion.group(1).replace('.', '').replace(',', '.') if deduccion else None

    # Neto girado
    neto = re.search(r"NETO GIRADO\s*\$\s*([0-9\.,]+)", texto, re.IGNORECASE)
    datos['neto_pagar'] = neto.group(1).replace('.', '').replace(',', '.') if neto else None

    return datos

def extraer_campos_formato_conocimiento(texto):
    datos = {}

    # Nombre
    nombre = re.search(r"Nombre:\s*([A-ZÑÁÉÍÓÚ ]+)", texto, re.IGNORECASE)
    datos['nombre'] = nombre.group(1).strip() if nombre else None

    # Cédula
    cedula = re.search(r"C\.?C\.?\s*([0-9]{5,15})", texto)
    datos['cedula'] = cedula.group(1) if cedula else None

    # Ciudad expedición
    ciudad = re.search(r"expedida en\s+([A-ZÑÁÉÍÓÚ ]+)", texto, re.IGNORECASE)
    datos['ciudad_expedicion'] = ciudad.group(1).strip() if ciudad else None

    # Fecha de firma
    fecha = re.search(r"(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}", texto)
    datos['fecha_firma'] = fecha.group(1) if fecha else None

    # Celular
    celular = re.search(r"Cel\s+([0-9]{7,15})", texto)
    datos['celular'] = celular.group(1) if celular else None

    return datos

def extraer_campos_soportes_recompra(texto):
    datos = {}

    # Buscamos el primer número largo en el documento que corresponde a la cédula
    cedula_match = re.search(r"\b([0-9]{5,15})\b", texto)
    datos['cedula'] = cedula_match.group(1) if cedula_match else None

    # Extraemos el nombre como la línea anterior a la cédula
    nombre = None
    if cedula_match:
        pos_cedula = cedula_match.start()
        texto_antes = texto[:pos_cedula]
        lineas = texto_antes.strip().split('\n')
        if lineas:
            nombre = lineas[-1].strip()
    
    datos['nombre'] = nombre

    # Fecha de corte (YYYY-MM-DD)
    fecha_corte = re.search(r"(\d{4}-\d{2}-\d{2})", texto)
    datos['fecha_corte'] = fecha_corte.group(1) if fecha_corte else None

    # Valor a pagar
    valor_pagar = re.search(r"Valor a Pagar\s*([0-9\.,]+)", texto, re.IGNORECASE)
    if valor_pagar:
        datos['valor_pagar'] = valor_pagar.group(1).replace('.', '').replace(',', '.')
    else:
        datos['valor_pagar'] = None

    return datos

def extraer_campos_datacredito(texto):
    datos = {
        'nombre': None,
        'cedula': None,
        'lugar_expedicion': None,
        'fecha_expedicion': None,
        'fecha_consulta': None,
        'score_acierta': None
    }

    lineas = texto.split('\n')

    for linea in lineas:
        linea = linea.strip()

        if linea.startswith("Nombre:"):
            valor = linea.replace("Nombre:", "").strip()
            if valor:
                datos['nombre'] = valor

        if "Num. Documento:" in linea:
            match = re.search(r"Num\. Documento:\s*([0-9]{5,15})", linea)
            if match:
                datos['cedula'] = match.group(1)

        if "Lugar Expedición:" in linea:
            match = re.search(r"Lugar Expedici[oó]n:\s*([A-ZÑÁÉÍÓÚ ]+)", linea, re.IGNORECASE)
            if match:
                datos['lugar_expedicion'] = match.group(1).strip()

        if "Fecha Exp.:" in linea:
            match = re.search(r"Fecha Exp\.\s*:\s*([0-9]{2}/[0-9]{2}/[0-9]{4})", linea)
            if match:
                datos['fecha_expedicion'] = match.group(1)

        if "Fecha Consulta:" in linea:
            match = re.search(r"Fecha Consulta:\s*([0-9]{2}/[0-9]{2}/[0-9]{4})", linea)
            if match:
                datos['fecha_consulta'] = match.group(1)

        if "Acierta" in linea:
            match = re.search(r"Acierta\s+\+\s*:\s*([0-9]{1,4})", linea)
            if match:
                datos['score_acierta'] = match.group(1)

    return datos
