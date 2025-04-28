# MCP Server

## Yeni Özellikler
- **OCR ve PDF İşleme:** Görüntülerden ve PDF dosyalarından metin çıkarabilirsiniz.
- Yeni endpointler:
  - `/process-image/`: Bir görüntü dosyasından metni çıkarır.
  - `/process-pdf/`: Bir PDF dosyasından metni çıkarır.

## Gereksinimler
- **Tesseract OCR:** Sisteminizde kurulu olmalıdır.
  - **Linux:** `sudo apt install tesseract-ocr`
  - **Mac:** `brew install tesseract`
  - **Windows:** Tesseract OCR [resmi dökümana](https://github.com/tesseract-ocr/tesseract) göre kurulmalıdır.

## Kullanım
1. **Görüntü İşleme:**
   ```bash
   curl -X POST "http://localhost:8000/process-image/" -F "file=@image.jpg"
   ```

2. **PDF İşleme:**
   ```bash
   curl -X POST "http://localhost:8000/process-pdf/" -F "file=@document.pdf"
   ```