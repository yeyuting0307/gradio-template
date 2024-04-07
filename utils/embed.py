#%%
import tempfile
from typing import List, Dict, Iterator
from langchain.schema import Document
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from langchain.text_splitter import CharacterTextSplitter

DEFAULT_EMBEDDING = HuggingFaceEmbeddings(
    model_name = "Mike0307/text2vec-base-chinese-crosslingual"
)
DEFAULT_VECTOR_STORE = FAISS

DEFAULT_SPLITTER = CharacterTextSplitter(
            separator = "\n\n",
            chunk_size = 500,
            chunk_overlap  = 200,
            length_function = len
) 

class Embedder:
    def __init__(
            self, 
            documents: Iterator, 
            metadata: List = None,
            embeddings = DEFAULT_EMBEDDING, 
            vector_store = DEFAULT_VECTOR_STORE,
            splitter = DEFAULT_SPLITTER
    ) -> None:
        
        self.embeddings = embeddings
        self.vector_store = vector_store
        self.splitter = splitter

        if not isinstance(documents, Document):
            self.documents = [
                Document(
                    page_content=doc if doc else "", 
                    metadata = metadata[i] if metadata else {}
                ) for i, doc in enumerate(documents)
            ]
        else:
            self.documents = documents
        self._split_docs()
        self._embed_docs()

    def _split_docs(self):
        self.splitted_docs = self.splitter.split_documents(self.documents)
        
    def _embed_docs(self):
        self.db = self.vector_store.from_documents(self.splitted_docs, self.embeddings)
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            self.db_path = tmp.name
            try:
                self.db.save_local(self.db_path)
            except Exception as e:
                print(f"db save failed : {e}")
        return self.db_path
    
    def retrieve_docs(self, question: str, top_k: int = 7):
        if self.db is None:
            self._split_docs()
            self._embed_docs()
        else:
            self.retriever = self.db.as_retriever(
                search_kwargs={'k': top_k}
            )
        return self.retriever.invoke(question)
    
# %%


