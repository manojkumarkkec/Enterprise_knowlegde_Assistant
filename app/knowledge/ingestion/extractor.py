from pathlib import Path

from pypdf import PdfReader
from docx import Document as DocxDocument


class DocumentExtractor:


    async def extract(
        self,
        file_path: str,
    ) -> str:

        path = Path(file_path)

        extension = path.suffix.lower()


        if extension == ".pdf":

            return self._extract_pdf(
                path
            )


        elif extension == ".docx":

            return self._extract_docx(
                path
            )


        elif extension == ".txt":

            return path.read_text(
                encoding="utf-8"
            )


        else:
            raise ValueError(
                "Unsupported file type"
            )



    def _extract_pdf(
        self,
        path: Path,
    ) -> str:

        reader = PdfReader(
            str(path)
        )

        text = []

        for page in reader.pages:

            content = page.extract_text()

            if content:
                text.append(content)


        return "\n".join(text)



    def _extract_docx(
        self,
        path: Path,
    ) -> str:

        doc = DocxDocument(
            str(path)
        )

        paragraphs = [
            p.text
            for p in doc.paragraphs
            if p.text.strip()
        ]

        return "\n".join(
            paragraphs
        )