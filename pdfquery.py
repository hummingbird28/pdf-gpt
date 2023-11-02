import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader, UnstructuredURLLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI


class PDFQuery:
    def __init__(self, openai_api_key=None) -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key, max_tokens=500)
        self.chain = None
        self.db = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Please, add a document."
        else:
            docs = self.db.get_relevant_documents(question)
            response = self.chain.run(input_documents=docs, question=question)
        return response
    
    def ingest_urls(self, urls: list):
        loader = UnstructuredURLLoader(urls)
        documents = loader.load()
        self.process_documents(documents)

    def ingest(self, file_path: os.PathLike | str) -> None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        self.process_documents(documents)
    
    def process_documents(self, documents):
        splitted_documents = self.text_splitter.split_documents(documents)
        self.db = Chroma.from_documents(
            splitted_documents, self.embeddings,
            persist_directory="chroma"
        ).as_retriever()
        self.chain = load_qa_chain(
            ChatOpenAI(temperature=0, max_tokens=250),
            chain_type="stuff",
        )

    def forget(self) -> None:
        self.db = None
        self.chain = None
