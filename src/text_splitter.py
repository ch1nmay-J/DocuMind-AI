from src.config import CHUNK_SIZE, CHUNK_OVERLAP
def split_text(
        pages,
        chunk_size = CHUNK_SIZE,
        overlap = CHUNK_OVERLAP
):

    chunks = []

    for page in pages:

        text = page["text"]

        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(
                {
                    "chunk_id": len(chunks) + 1,
                    "file": page["file"],
                    "page": page_number,
                    "text": chunk
                }
            )

            start += chunk_size - overlap

    return chunks