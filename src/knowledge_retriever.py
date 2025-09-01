import os
import sys
import pickle
from sentence_transformers import SentenceTransformer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import faiss
    import numpy as np
except ImportError:
    print("AVISO: FAISS ou NumPy não encontrado.")
    sys.exit(1)

class KnowledgeRetriever:
    def __init__(self, project_root, lazy_load=False):
        self.project_root = project_root
        self.index = None
        self.metadata = None
        self.model = None
        # Se lazy_load for False, carrega tudo imediatamente.
        if not lazy_load:
            self._load_models()

    def _load_models(self):
        """Carrega o índice, os metadados e o modelo de linguagem, somente se ainda não foram carregados."""
        if self.model is not None:
            return # Já está carregado, não faz nada.

        print("Carregando base de conhecimento e modelo de linguagem (Lazy Load)...")
        index_file = os.path.join(self.project_root, 'knowledge_base_index.faiss')
        metadata_file = os.path.join(self.project_root, 'knowledge_base_metadata.pkl')

        if not os.path.exists(index_file) or not os.path.exists(metadata_file):
            print("AVISO: Arquivos da base de conhecimento não encontrados. Execute 'process_knowledge.py' primeiro.")
            return

        try:
            self.index = faiss.read_index(index_file)
            with open(metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
            
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("Modelos carregados com sucesso.")
        except Exception as e:
            print(f"ERRO ao carregar modelos: {e}")

    def search(self, query: str, k: int = 5) -> list:
        """Busca na base de conhecimento."""
        # Garante que os modelos estejam carregados antes de cada busca
        self._load_models()
        
        if self.index is None or self.model is None:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.metadata['texts']):
                results.append({
                    'text': self.metadata['texts'][i],
                    'source': self.metadata['sources'][i]
                })
        return results