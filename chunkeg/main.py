from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader

from typing import Dict, List, Optional

from langchain.text_splitter import (
    Language,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

import os 
load_dotenv()

if __name__ == "__main__":
    OPENAI_API_KEY =  os.environ['OPENAI_API_KEY']
    
    web_loader = WebBaseLoader(
        [
            "https://peps.python.org/pep-0483/",
            "https://peps.python.org/pep-0008/",
            "https://peps.python.org/pep-0257/",
        ]
    )
    
    pages = web_loader.load()
    print(len(pages))
                       
       
                              