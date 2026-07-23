from langchain_chroma import Chroma

db = Chroma.from_documents(

    documents,

    embeddings,

    persist_directory="vectorstore"

)

db = Chroma(

    persist_directory="vectorstore",

    embedding_function=embeddings

)

retriever = db.as_retriever(

    search_kwargs={

        "k":5

    }

)