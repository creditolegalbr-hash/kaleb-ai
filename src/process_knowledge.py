import os
import pickle
import sys

from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Garante que o script encontre outros módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config.config_manager import ConfigManager

try:
    import faiss
except ImportError:
    print(
        "Biblioteca FAISS não encontrada. Por favor, instale com: pip install faiss-cpu"
    )
    sys.exit(1)


def extract_text_from_pdf(file_path):
    """Extrai texto de um arquivo PDF."""
    print(f"[REINDEX] Lendo PDF: {os.path.basename(file_path)}...")
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"  [REINDEX] ERRO ao ler o PDF {os.path.basename(file_path)}: {e}")
    return text


def extract_text_from_txt(file_path):
    """Extrai texto de um arquivo .txt."""
    print(f"[REINDEX] Lendo TXT: {os.path.basename(file_path)}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"  [REINDEX] ERRO ao ler o TXT {os.path.basename(file_path)}: {e}")
    return ""


def reindex_knowledge_base():
    """
    Função principal que pode ser chamada por outros scripts para reprocessar a base de conhecimento.
    """
    print("\n[REINDEXAÇÃO AUTOMÁTICA INICIADA]...")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_file_path = os.path.join(project_root, "config", "default.yaml")
    config_manager = ConfigManager(config_paths=[config_file_path])
    kb_path = os.path.join(
        project_root, config_manager.get("knowledge_base.path", "knowledge_base")
    )

    if not os.path.exists(kb_path):
        print("[REINDEX] Diretório da base de conhecimento não encontrado.")
        return False

    print("[REINDEX] Carregando modelo de linguagem...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    all_texts, text_sources = [], []

    for filename in os.listdir(kb_path):
        file_path = os.path.join(kb_path, filename)
        text = ""
        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith(".txt"):
            text = extract_text_from_txt(file_path)

        if text:
            chunks = text.split("\n")
            for chunk in chunks:
                if (
                    len(chunk.strip()) > 10
                ):  # Indexa apenas trechos com mais de 10 caracteres
                    all_texts.append(chunk.strip())
                    text_sources.append(filename)

    if not all_texts:
        print("[REINDEX] Nenhum texto válido encontrado para indexar.")
        return False

    print(f"[REINDEX] Criando embeddings para {len(all_texts)} trechos...")
    embeddings = model.encode(all_texts, show_progress_bar=False)

    print("[REINDEX] Construindo índice FAISS...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    index_file = os.path.join(project_root, "knowledge_base_index.faiss")
    metadata_file = os.path.join(project_root, "knowledge_base_metadata.pkl")

    faiss.write_index(index, index_file)
    with open(metadata_file, "wb") as f:
        pickle.dump({"texts": all_texts, "sources": text_sources}, f)

    print("\n[REINDEXAÇÃO AUTOMÁTICA CONCLUÍDA COM SUCESSO!]\n")
    return True


# Esta parte permite que o script ainda seja executado manualmente, se necessário
if __name__ == "__main__":
    reindex_knowledge_base()
