import os
from app.utils.extract_fields import FieldExtractor
from app.utils.extract_images import ImageExtractor
from app.utils.extract_tables import TableExtractor
from app.utils.extract_tables_ocr import TableOCRExtractor
from app.utils.classify_document import classify_document
from app.extractor import TextExtractor
from app.utils.organize_by_reference import organizar_por_referencia

class DocumentProcessor:
    def __init__(self, ruta_origen, ruta_destino):
        self.ruta_origen = ruta_origen
        self.ruta_destino = ruta_destino
        self._organizar_documentos()
        self.documentos = self._listar_pdfs()

    def _organizar_documentos(self):
        organizar_por_referencia(self.ruta_origen, self.ruta_destino)

    def _listar_pdfs(self):
        documentos = []
        for carpeta in os.listdir(self.ruta_destino):
            carpeta_path = os.path.join(self.ruta_destino, carpeta)
            if os.path.isdir(carpeta_path):
                for archivo in os.listdir(carpeta_path):
                    if archivo.lower().endswith('.pdf'):
                        documentos.append(os.path.join(carpeta_path, archivo))
        return documentos

    def procesar(self):
        for ruta_pdf in self.documentos:
            print(f"\n📄 Procesando: {os.path.basename(ruta_pdf)}")
            tipo_doc = classify_document(ruta_pdf)
            texto = TextExtractor.extract_text(ruta_pdf)
            campos = FieldExtractor.extract(texto, tipo_doc)
            print(f"→ Tipo: {tipo_doc}")
            print(f"→ Campos extraídos: {campos}")
            # Aquí puedes agregar validación, exportación, imágenes, tablas, etc.

class TableExtractor:
    @staticmethod
    def extract(pdf_path):
        """
        Método simulado para extracción de tablas embebidas.
        Futuro uso con Camelot o pdfplumber.

        Args:
            pdf_path (str): Ruta del archivo PDF.

        Returns:
            list: Lista vacía (simulación).
        """
        print(f"[TableExtractor] Extracción simulada de tablas en: {pdf_path}")
        return []


def run_pipeline():
    ruta_origen = r"C:/Users/jhona/Desktop/Documentos juntos"
    ruta_destino = r"C:/Users/jhona/Desktop/Documentos por credito"
    processor = DocumentProcessor(ruta_origen, ruta_destino)
    processor.procesar()
