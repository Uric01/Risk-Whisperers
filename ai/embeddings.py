from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

docs = []

for file in [

    "knowledge/ISO27001.pdf",

    "knowledge/ISO27005.pdf",

    "knowledge/ISO31000.pdf"

]:

    docs.extend(

        PyPDFLoader(file).load()

    )
    

splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,

    chunk_overlap=200

)

documents = splitter.split_documents(docs)


embeddings = HuggingFaceEmbeddings(

    model_name="BAAI/bge-base-en-v1.5"

)