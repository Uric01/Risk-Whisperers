import getpass
import os

if not os.environ.get("MISTRAL_API_KEY"):
  os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI:")

from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(model="mistral-large-latest")