<Upload
  accept=".pdf,.png,.jpg,.jpeg,.bmp,.tiff,.webp"
  customRequest={async ({ file }) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("ocr_lang", "eng+tur");
    const resp = await fetch("/api/v1/rag/documents/upload", {
      method: "POST",
      body: formData,
    });
    if (resp.ok) {
      message.success("Dosya başarıyla yüklendi!");
    } else {
      message.error("Yükleme başarısız oldu.");
    }
  }}
>
  <Button icon={<UploadOutlined />}>Dosya Yükle</Button>
</Upload>