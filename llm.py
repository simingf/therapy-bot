from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from loguru import logger

from secret.OPENAI import OPENAI_API_KEY
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

chat = ChatOpenAI(
    model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=1, max_tokens=1000
)
# streaming=True, callbacks=[StreamingStdOutCallbackHandler()]


def sys_message_base(name: str):
    return f"You are not an AI language model. You are a mental health professional and trusted person in {name}'s life. Your job is to help answer {name}'s questions from the point of view of a professional therapist. You should not defer him to other professionals. Respond to all messages in the following way.\nThoughts: your thoughts go here\nReasoning: explanation and conclusion for your thoughts \nCriticism: what do you have to be careful of? what could go wrong?\nMessage: what do you want to say to your client?"


def get_chat_history(name: str):
    return [
        SystemMessage(content=sys_message_base(name)),
        HumanMessage(content=f"My name is {name}. Nice to meet you."),
        AIMessage(
            content=f"Thoughts: It's important to create a safe and supportive environment for {name} to express their feelings and concerns. I should listen actively and attentively, providing empathetic responses that show I understand their emotions.\nReasoning: {name} needs a space where he feels comfortable sharing their thoughts and emotions. As their trusted mental health professional, I can offer guidance and support while helping him explore their thoughts and feelings in a constructive way.\nCriticism: I need to be cautious about not imposing my own beliefs or solutions onto {name}. It's important to let him lead the conversation and reach their own conclusions. Additionally, I should be aware of potential ethical boundaries and my limitations in providing therapy.\nMessage: Hi {name}, I'm here to listen and support you. Feel free to share what's on your mind, and I'll do my best to provide guidance and understanding. Remember, our conversations are confidential and focused on your well-being. What's on your mind today?"
        ),
    ]


summary_prompt = [
    SystemMessage(
        content="You are a summarizer. You should summarize the given human-therapist conversation. Only return the summary."
    ),
]

summary_update_prompt = [
    SystemMessage(
        content="You are a summarizer. You should produce a new summary given a previous summary and a new human-therapist conversation. Only return the new summary."
    ),
]

summary = ""


def format_chat_history(name: str) -> str:
    res = ""
    for obj in get_chat_history(name):
        if type(obj) == SystemMessage:
            res += "System:\n" + obj.content + "\n\n"
        elif type(obj) == HumanMessage:
            res += f"{name}: " + obj.content + "\n\n"
        elif type(obj) == AIMessage:
            res += "Therapist:\n" + obj.content + "\n\n"
    return res


def chat_with_therapist(name: str, input_message: str) -> str:
    global summary_prompt
    global summary_update_prompt
    global summary
    chat_history = get_chat_history(name)
    if len(chat_history) == 5:
        human_content = chat_history[1].content
        ai_content = chat_history[2].content
        if summary == "":
            full_content = "{name}: " + human_content + "\nTherapist: " + ai_content
            summary_prompt.append(HumanMessage(content=full_content))
            aimessage = chat(summary_prompt)
            summary = aimessage.content
            new_sys_message = sys_message_base(name) + "\nContext:\n" + summary
            chat_history = [SystemMessage(content=new_sys_message)] + chat_history[3:]
        else:
            full_content = (
                "Previous Summary: "
                + summary
                + "\nNew {name}-therapist conversation:\n{name}: "
                + human_content
                + "\nTherapist: "
                + ai_content
            )
            summary_update_prompt.append(HumanMessage(content=full_content))
            aimessage = chat(summary_update_prompt)
            summary = aimessage.content
            new_sys_message = sys_message_base(name) + "\nContext:\n" + summary
            chat_history = [SystemMessage(content=new_sys_message)] + chat_history[3:]
    assert type(input_message) == str
    new_message = HumanMessage(content=input_message)
    chat_history.append(new_message)
    ai_message = chat(chat_history)
    assert type(ai_message) == AIMessage
    chat_history.append(ai_message)
    content = ai_message.content
    ai_thoughts = content.split("Message: ")[0]
    user_message = content.split("Message: ")[1]
    logger.info(
        f"CHAT HISTORY\n{format_chat_history(name)}\n--------------------------------------\n"
    )
    logger.info(f"AI THOUGHTS\n{ai_thoughts}\n--------------------------------------\n")
    return user_message


def main():
    chat_with_therapist("how can i be happy?")


if __name__ == "__main__":
    main()
