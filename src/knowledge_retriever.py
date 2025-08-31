import os
import pickle
import sys

from sentence_transformers import SentenceTransformer

# Garante que o script encontre outros módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import faiss
    import numpy as np
except ImportError:
    print(
        "Bibliotecas FAISS ou NumPy não encontradas. Por favor, instale com: pip install faiss-cpu numpy"
    )
    sys.exit(1)


class KnowledgeRetriever:
    """
    Gerencia o carregamento e a busca na base de conhecimento indexada.
    """

    def __init__(self, project_root):
        self.project_root = project_root
        self.index = None
        self.metadata = None
        self.model = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Carrega o índice FAISS, os metadados e o modelo de linguagem."""
        index_file = os.path.join(self.project_root, "knowledge_base_index.faiss")
        metadata_file = os.path.join(self.project_root, "knowledge_base_metadata.pkl")

        if not os.path.exists(index_file) or not os.path.exists(metadata_file):
            print(
                "AVISO: Arquivos da base de conhecimento não encontrados. Execute 'process_knowledge.py' primeiro."
            )
            return

        print("Carregando base de conhecimento e modelo de linguagem...")
        self.index = faiss.read_index(index_file)
        with open(metadata_file, "rb") as f:
            self.metadata = pickle.load(f)

        # Carrega o mesmo modelo usado para criar o índice
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Base de conhecimento carregada com sucesso.")

    def search(self, query: str, k: int = 5) -> list:
        """
        Busca na base de conhecimento os 'k' resultados mais relevantes para a consulta.
        """
        if self.index is None or self.model is None:
            return []  # Retorna vazio se a base de conhecimento não foi carregada

        print(f"Buscando na base de conhecimento por: '{query}'")
        # Transforma a consulta do usuário em um vetor
        query_embedding = self.model.encode([query])

        # Faz a busca no índice FAISS
        distances, indices = self.index.search(query_embedding, k)

        # Coleta os resultados
        results = []
        for i in indices[0]:
            if i != -1:  # FAISS retorna -1 se não encontrar resultados suficientes
                results.append(
                    {
                        "text": self.metadata["texts"][i],
                        "source": self.metadata["sources"][i],
                    }
                )

        return results


if __name__ == "__main__":
    # Exemplo de como usar o retriever
    project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    retriever = KnowledgeRetriever(project_root=project_root_path)

    # Testa com uma busca
    if retriever.index:
        search_results = retriever.search(
            "Qual é o procedimento para solicitar férias?"
        )
        if search_results:
            print("\nResultados da busca:")
            for res in search_results:
                print(f"- Fonte: {res['source']}\n  Texto: {res['text']}\n")
        else:
            print("Nenhum resultado encontrado.")
