from llm import chat_with_therapist

def main():
    user_question = str(input("What would you like to say to your therapist?\n"))
    while True:
        response = chat_with_therapist(user_question)
        print(f"Therapist: {response}\n")
        user_question = str(input())
        if user_question == "exit":
            break

if __name__ == "__main__":
    main()