from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from secret.OPENAI import OPENAI_API_KEY

def main():
    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    question = "What is the meaning of life?"
    answer = llm_chain.run(question=question)
    print(answer)

if __name__ == "__main__":
    main()