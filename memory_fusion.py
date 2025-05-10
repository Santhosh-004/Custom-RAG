from embedding_manager import EmbeddingManager
from rag_memory_manager import RAGMemoryManager
from ollama_client import OllamaClient
from enums import PromptType
import prompts

class MemoryFusionEngine:
    def __init__(self):
        self.embed_mgr = EmbeddingManager()
        self.rag_mgr = RAGMemoryManager()
        self.ollama = OllamaClient()

    def process_user_input(self, text: str):
        emb = self.embed_mgr.embed([text])[0]
        doc_id = f"doc_{hash(text)}"
        prompt_type = self.ollama.infoOrQuestion(text)
        if prompt_type == PromptType.INFO:
            self.rag_mgr.memoryExtender(text, doc_id, emb)
        
        return self.answer_query(text, emb)
            
    def answer_query(self, query: str, emb):
        mem = self.rag_mgr.memoryRetriever(emb, 5)
        full_prompt = prompts.queryAnswer(query, mem)
        res = self.ollama.generate(full_prompt, thinkingModel=True)
        return res