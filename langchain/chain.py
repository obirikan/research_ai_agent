from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable
from dotenv import load_dotenv
import os
import random

from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate
)

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

system_message_prompt = SystemMessagePromptTemplate.from_template("""
You are a helpful assistant that can answer questions and help with tasks
""")
human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")

prompt = ChatPromptTemplate.from_messages([
system_message_prompt,
human_message_prompt,
])

chain = prompt | llm 

@traceable
def rand_number():
    return random.randint(1, 100)

rand_number()


print(chain.invoke({"input": "What is the weather in Tokyo?"}).content)