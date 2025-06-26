# 🧠 Sistema de Validación Documental OCR Inteligente - Libranzas
Este proyecto tiene como objetivo construir un sistema OCR avanzado para la extracción, validación y generación de reportes a partir de documentos contractuales del proceso de libranzas (Solicitud, Libranza, Cédula, Amortización, etc.).

## 🛠️ Características
- Extracción de texto, imágenes, tablas y firmas desde documentos PDF e imágenes escaneadas.
- OCR inteligente (Tesseract y/o PaddleOCR) para documentos escaneados o con texto no embebido.
- Validación de datos extraídos contra un archivo maestro en Excel (33 columnas).
- Aplicación de reglas específicas por tipo de documento y canal (físico o digital).
- Generación automática de reportes de errores y observaciones por crédito.
- Modular, escalable y preparado para instalación en estaciones locales o backend.
- Preparado para integrar FTP, Web Services o servicios en la nube en el futuro.

## 📂 Estructura de Carpetas Fecha 26/05/2025
Proyecto_OCR/
│
├── app/
│ ├── extractor.py # Coordinador del flujo de extracción
│ └── utils/ # Módulos reutilizables
│ ├── classify_document.py
│ ├── extract_fields.py
│ ├── extract_images.py
│ ├── extract_tables.py
│ ├── extract_tables_ocr.py
│ └── ...
│
├── entrada_pdfs/ # Documentos PDF reales de entrada
├── salida_texto/ # Texto extraído por OCR
├── salida_imagenes/ # Imágenes individuales extraídas
├── salida_tablas/ # Tablas detectadas con Camelot
├── salida_tablas_ocr/ # Tablas vía OCR puro
│
├── validaciones/ # (Opcional) Lógica de validaciones específicas
├── reportes/ # Reportes Excel generados por corrida
│
├── config.py # Parámetros, rutas y configuraciones generales
├── conteo_caracter.py # Script independiente para contar letras OCR
├── requirements.txt # Librerías necesarias para instalar el entorno
└── README.md # Este archivo

## ✅ Requisitos
- Python 3.9 o superior
- Tesseract OCR (instalado en sistema)
- poppler (para pdf2image)
- Dependencias listadas en `requirements.txt`

## Instalación de dependencias:
pip install -r requirements.txt

## Módulos principales
Módulo	                    Función
extractor.py	            Orquestador de extracción completa por documento
extract_fields.py	        Extrae campos específicos según plantilla de JSON/Excel
extract_images.py	        Extrae imágenes y regiones clave de los PDFs
extract_tables.py	        Detecta tablas con texto embebido (Camelot)
extract_tables_ocr.py	    Detecta tablas con OCR puro para escaneos
classify_document.py	    Clasifica el tipo documental usando reglas o IA

▶️ Ejecución general del sistema
python app/extractor.py

🧮 Script Extra: Conteo de Letras por OCR
python conteo_caracter.py

📌 Notas adicionales
Validaciones específicas por tipo documental y canal están contenidas en el documento:
“Validación documental para el modelo Davinci - Anderson”
El formato de salida está basado en una matriz JSON y plantilla en Excel.
Soporta múltiples tipos de documento: Solicitud, Libranza, Cédula, Fianza, etc.

📦 Próximos pasos
Conectar al archivo maestro Excel (33 columnas).
Implementar validaciones por tipo documental.
Generar reporte final por crédito.
Soporte para canal FTP/WebService (ingesta automatizada).
Dockerización y app standalone local.

👨‍💻 Autor / Contacto
Este proyecto ha sido desarrollado por el equipo de automatización documental del área de libranzas.

