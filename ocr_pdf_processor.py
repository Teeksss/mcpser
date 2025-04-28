import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
import os

# OCR İşlevi
def extract_text_from_image(image_path):
    """
    Verilen bir görüntü dosyasından metni çıkarır.
    
    Args:
        image_path (str): Görüntü dosyasının yolu.
        
    Returns:
        str: Çıkarılan metin veya hata mesajı.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error processing image: {e}"

# PDF İşleme İşlevi
def extract_text_from_pdf(pdf_path):
    """
    Verilen bir PDF dosyasından metni çıkarır.
    
    Args:
        pdf_path (str): PDF dosyasının yolu.
        
    Returns:
        str: Çıkarılan metin veya hata mesajı.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error processing PDF: {e}"