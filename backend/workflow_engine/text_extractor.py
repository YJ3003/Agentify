import io
import pypdf
import docx
from fastapi import UploadFile

class TextExtractor:
    async def extract(self, file: UploadFile) -> str:
        filename = file.filename.lower()
        content = await file.read()
        file_obj = io.BytesIO(content)
        
        text = ""
        
        if filename.endswith(".pdf"):
            reader = pypdf.PdfReader(file_obj)
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
        elif filename.endswith(".docx"):
            doc = docx.Document(file_obj)
            for para in doc.paragraphs:
                text += para.text + "\n"
                
        elif filename.endswith(".txt") or filename.endswith(".md"):
            text = content.decode("utf-8")
            
        else:
            raise ValueError("Unsupported file format")
            
        return text
