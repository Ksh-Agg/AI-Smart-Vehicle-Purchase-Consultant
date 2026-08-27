"""Index a reviewed manifest of official PDF documents into PGVector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.core.config import settings


def _allowed(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(
        host == domain or host.endswith(f".{domain}")
        for domain in settings.allowed_research_domains
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path, help="JSON list of official PDF sources")
    args = parser.parse_args()
    sources = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(sources, list):
        raise SystemExit("Manifest must be a JSON list")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1_200, chunk_overlap=150)
    documents: list[Document] = []
    ids: list[str] = []
    for source in sources:
        path = Path(source["path"])
        source_url = str(source["source_url"])
        if path.suffix.lower() != ".pdf" or not path.is_file():
            raise SystemExit(f"Not a readable PDF: {path}")
        if not _allowed(source_url):
            raise SystemExit(f"Source domain is not approved: {source_url}")
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        reader = PdfReader(path)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for chunk_number, chunk in enumerate(splitter.split_text(text)):
                metadata = {
                    "source_url": source_url,
                    "title": source["title"],
                    "effective_date": source.get("effective_date"),
                    "model": source.get("model"),
                    "page": page_number,
                    "checksum": checksum,
                }
                documents.append(Document(page_content=chunk, metadata=metadata))
                ids.append(
                    hashlib.sha256(
                        f"{source_url}|{page_number}|{chunk_number}".encode()
                    ).hexdigest()
                )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.GEMINI_EMBEDDING_MODEL,
        api_key=settings.GEMINI_API_KEY,
    )
    store = PGVector(
        embeddings=embeddings,
        collection_name=settings.RAG_COLLECTION_NAME,
        connection=settings.database_url,
        use_jsonb=True,
    )
    store.add_documents(documents, ids=ids)
    print(f"Indexed {len(documents)} chunks from {len(sources)} official documents.")


if __name__ == "__main__":
    main()
