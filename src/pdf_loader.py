import fitz
def load_pdf(pdf_path):
    document = fitz.open(pdf_path)
    return document