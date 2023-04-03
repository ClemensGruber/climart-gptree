import os
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def getPrompts():
    with open("characters.txt", "r", encoding="utf-8") as file:
        prompt_templates = [line.strip() for line in file.readlines()]
    prompts = [PromptTemplate(input_variables=['history', 'input'], output_parser=None, partial_variables={}, template=template) for template in prompt_templates]
    return prompts

def main():
    os.system("clear")
    load_dotenv()
    
    # Choose your character: 0: Biene, 1: Roboter, 2: Kiri-Wurst, 3: Schatzkiste, 4: Yoda 
    prompt = getPrompts()[3]
    
    chatgpt = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    conversation = ConversationChain(llm=chatgpt, verbose=False, memory=ConversationBufferMemory(), prompt=prompt)

    # Sending an empty user input first to let the AI start the conversation – this should be triggered by the RFID signal
    user_input = ""
    print(conversation.predict(input=user_input))

    while user_input.lower() != "q":
        user_input = input("Enter input (or 'q' to quit): ")

        if user_input.lower() != "q":
            reply = conversation.predict(input=user_input)
            print(reply)

if __name__ == '__main__':
    main()