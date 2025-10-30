from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
system_prompt = "You are a helpful assistant called Zeta."

#  prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{query}"),
])

# pipeline
from langchain_core.output_parsers import StrOutputParser
pipeline = prompt_template | llm | StrOutputParser()

# Chat history management
chat_map = {}

def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_map:
        chat_map[session_id] = InMemoryChatMessageHistory()
    return chat_map[session_id]

# pipeline with history
pipeline_with_history = RunnableWithMessageHistory(
    pipeline,
    get_session_history=get_chat_history,
    input_messages_key="query",
    history_messages_key="history"
)

# Test the conversation
# print("=== First message ===")
# result1 = pipeline_with_history.invoke(
#     {"query": "my name is richard"},
#     config={"session_id": "id_123"}
# )
# print(f"Response: {result1}")

# print("\n=== Second message (should remember context) ===")
# result2 = pipeline_with_history.invoke(
#     {"query": "whats my name?"},
#     config={"session_id": "id_123"}
# )
# print(f"Response: {result2}")

print("\n=== Third message (testing memory) ===")
result3 = pipeline_with_history.invoke(
    {"query": "what did I say my name was?"},
    config={"session_id": "id_123"}
)
print(f"Response: {result3}")