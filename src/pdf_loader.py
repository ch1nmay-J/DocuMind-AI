import os
import fitz

def load_pdf(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        pages.append(
            {
                "page": page_number,
                "text": page.get_text()
            }
        )

    return pages

def load_all_pdfs(folder_path):

    all_pages = []

    for file_name in os.listdir(folder_path):

        if file_name.endswith(".pdf"):

            pdf_path = os.path.join(folder_path, file_name)

            pages = load_pdf(pdf_path)

            for page in pages:
                page["file"] = file_name

            all_pages.extend(pages)

    return all_pages