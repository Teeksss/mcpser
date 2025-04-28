async def process_file(file, ocr_lang="eng+tur"):
    filename = file.filename.lower()
    content = await file.read()
    docs = []
    if filename.endswith(".pdf"):
        for page_idx, text in enumerate(pdf_to_texts(io.BytesIO(content))):
            docs.append({"content": text, "metadata": {"filename": file.filename, "page": page_idx+1}})
    elif any(filename.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]):
        text = await ocr_image(io.BytesIO(content), ocr_lang)
        docs.append({"content": text, "metadata": {"filename": file.filename}})
    else:
        docs.append({"content": content.decode(), "metadata": {"filename": file.filename}})
    return docs