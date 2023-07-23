from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from secret.OPENAI import OPENAI_API_KEY

chat = ChatOpenAI(model="gpt-3.5-turbo",temperature=0, openai_api_key=OPENAI_API_KEY, max_tokens=100)

chat_history = [
    SystemMessage(content="You are not an AI language model. You are a mental health professional and trusted person in James' life. Your job is to help answer the James' questions from the point of view of a professional therapist. Refer to him by his name. You are not allowed to defer him to other professionals."),
    HumanMessage(content="My name is James. Nice to meet you."),
    AIMessage(content="Nice to meet you too, how can I assist you?"),
]

def chat_with_therapist(input_message: str) -> str:
    assert(type(input_message) == str)
    new_message = HumanMessage(content=input_message)
    chat_history.append(new_message)
    logger.info(f"chat_history: {chat_history}")
    ai_message = chat(chat_history)
    assert(type(ai_message) == AIMessage)
    chat_history.append(ai_message)
    return ai_message.content

def main():
    chat_with_therapist("how can i be happy?")

if __name__ == "__main__":
    main()