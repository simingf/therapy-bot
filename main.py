from llm import chat_with_therapist

def main():
    name = str(input("What is your name?\nUser: "))
    user_question = str(input(f"What would you like to say to your therapist?\n{name}: "))
    while True:
        response = chat_with_therapist(name, user_question)
        print(f"Therapist: {response}\n")
        print(f"{name}: ", end="")
        user_question = str(input())
        if user_question == "exit":
            break

if __name__ == "__main__":
    main()