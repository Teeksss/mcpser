from src.services.rag.data_connectors import process_file

class RAGService:
    async def ingest_file(self, file, ocr_lang="eng+tur"):
        """
        Belirtilen dosyayı işler ve RAG vektör mağazasına ekler.
        """
        docs = await process_file(file, ocr_lang)
        for doc in docs:
            await self.add_document(doc)
        return {"status": "success", "count": len(docs)}