import chromadb
from datetime import datetime
from enums import MemoryType
import ollama_client, embedding_manager
import prompts

class RAGMemoryManager:
    def __init__(self, persist_path='chroma_db'):
        self.embed_mgr = embedding_manager.EmbeddingManager()
        self.ollamaClient = ollama_client.OllamaClient()
        self.client = chromadb.PersistentClient(path=persist_path)
        self.conversation_memory = self.client.get_or_create_collection(name="conversation_memory")
        self.facts = self.client.get_or_create_collection(name="facts")
        self.events = self.client.get_or_create_collection(name="events")

    def add_memory(self, doc_id: str, text: str, embedding):
        print(f"docId: {doc_id}, text: {text}, embedding: {embedding}")
        self.conversation_memory.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding.tolist()],
            metadatas=[{'timestamp': datetime.now().isoformat()}],
        )

    def add_fact(self, doc_id: str, text: str, embedding):
        self.facts.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding.tolist()],
            metadatas=[{'timestamp': datetime.now().isoformat()}],
        )

    def add_event(self, doc_id: str, text: str, embedding):
        self.events.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding.tolist()],
            metadatas=[{'timestamp': datetime.now().isoformat()}],
        )
    
    def allInOneRetriever(self, memoryType, query_embedding, top_k):
        res = memoryType.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=['documents', 'metadatas']
        )

        docs = res['documents'][0]
        metas = res['metadatas'][0]

        combined = list(zip(docs, metas))
        combined.sort(key=lambda x: x[1]['timestamp'], reverse=True)

        return str(combined)

    def memoryRetriever(self, query_embedding, top_k):
        mem = self.allInOneRetriever(self.conversation_memory, query_embedding, top_k)
        fact = self.allInOneRetriever(self.facts, query_embedding, top_k)
        event = self.allInOneRetriever(self.events, query_embedding, top_k)

        return {'Conversation memory': mem, 'stored facts': fact, 'stored events': event}
    

    def memoryExtender(self, prompt: str, doc_id, embedding):        
        response = self.memoryTypeIdentifier(prompts.memoryExtenderMessage(prompt))
        
        if response == MemoryType.SIMPLE_CONVERSATION:
            self.add_memory(doc_id=doc_id, text=prompt, embedding=embedding)
        if response == MemoryType.EVENT:
            self.add_event(doc_id=doc_id, text=prompt, embedding=embedding)
        elif response == MemoryType.FACT:
            self.add_fact(doc_id=doc_id, text=prompt, embedding=embedding)

    def memoryTypeIdentifier(self, prompt: str) -> MemoryType:
        response = self.ollamaClient.generate(prompt, thinkingModel=True)

        if response == "simple_conversation":
            return MemoryType.SIMPLE_CONVERSATION
        elif response == "event":
            return MemoryType.EVENT
        elif response == "fact":
            return MemoryType.FACT
        
