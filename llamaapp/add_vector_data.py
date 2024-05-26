import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()

#os.environ['OPENAI_API_KEY'] = '<YOUR_OPENAI_API_KEY>'
#os.environ['PINECONE_API_KEY'] = '<YOUR_PINECONE_API_KEY>'

#Read the documents
def read_doc(directory):
    file_loader= PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents

#Read chunk data
def chunk_data(docs,chunk_size=800,chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc = text_splitter.split_documents(docs)
    return doc

index_name = "langchainindex"
api_key =  os.environ['OPENAI_API_KEY']
embeddings = OpenAIEmbeddings(api_key=api_key)

    # path to an example text file
documents = read_doc("../pdfs/")
final_doc=chunk_data(documents,chunk_size=800,chunk_overlap=50)

vectorstore = PineconeVectorStore.from_documents(final_doc,index_name=index_name,embedding=embeddings)

#Similarity Search
query ="What is Pradhan Mantri Matsya Sampada"
result = vectorstore.similarity_search(query)
print(result)



#texts = ["Tonight, I call on the Senate to: Pass the Freedom to Vote Act.", "ne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.", "One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence."]

# vectorstore_from_texts = PineconeVectorStore.from_texts(
#         texts,
#         index_name=index_name,
#         embedding=embeddings
#     )





