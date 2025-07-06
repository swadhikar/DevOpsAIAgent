import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

dot_env_path = os.path.join(os.getcwd(), "..", "..", ".env")

if load_dotenv(dot_env_path):
    print("Environment variables loaded successfully.")
else:
    raise Exception(f'Unable to find credentials in: {dot_env_path}')

genai_model = ChatGoogleGenerativeAI(model=os.getenv('GEMINI_FLASH'), temperature=0.1)
print(f'Created Gemini model instance!')

openai_model = ChatOpenAI(model=os.getenv('GPT_3.5'), temperature=0.1)
print(f'Created OpenAI model instance!')
