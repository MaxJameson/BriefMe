import os
import openai
import json
import colorama

# store API key
os.environ['OPENAI_API_KEY']

# libary used to customise text
from colorama import Fore


print(Fore.YELLOW + "Importing libraries")

# libararies ues to read files
from pathlib import Path
from llama_index import download_loader
from llama_index import GPTVectorStoreIndex

# class for creating a chatbot
class Chatbot:

    # class constructor
    def __init__(self, api_key, index):

        # stores in index file for contexent
        self.index = index
        # connects to openai
        openai.api_key = api_key
        # stores chat history
        self.chat_history = []

    # sends user input to ai and gains response
    def generate_response(self, user_input):

        # creates and stores prompt from user input
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        # sends prompt to ai
        engine = index.as_query_engine()
        response = engine.query(user_input)
        # formats and stores response
        message = {"role": "assistant", "content": response.response[1:]}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    # loads chat history
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass
    
    # saves chat history
    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)

print(Fore.GREEN +"Libraries imported\n")

validChoice = False

# user is offered the choice between two different PDFs
while validChoice == False:

    file_choice = input(Fore.WHITE + "please choose one of these two files as context (brief or proposal): ")
    # checks which file the user has chosen
    if file_choice == "brief" or file_choice == "Brief":
        path = './brief.pdf'
        history_file = "brief.json"
        validChoice = True

    elif file_choice == "proposal" or file_choice == "Proposal":
        path = './proposal.pdf'
        history_file = "proposal.json"
        validChoice = True

# creates a PDF reader
PDFReader = download_loader("PDFReader")

# loads and indexs PDF
loader = PDFReader()
documents = loader.load_data(file=Path(path))
index = GPTVectorStoreIndex.from_documents(documents)

# creates chatbot
bot = Chatbot(os.environ['OPENAI_API_KEY'], index=index)
bot.load_chat_history(history_file)

# stores current chat history
with open(history_file, 'r') as f:
    history = json.load(f)

# prints chat history
for i in history:
    if i['role'] == "user":
        print(Fore.WHITE + "You: " + i['content'])
    else:
        print(Fore.GREEN + "Bot: " + i['content'] + "\n")
        


# loop allowing users to ask questions to the chatbot
while True:

    # takes user input
    user_input = input(Fore.WHITE + "You: ")
    # chats if user wants to end the session
    if user_input.lower() in ["bye", "goodbye"]:
        print(Fore.GREEN + "Bot: Goodbye!" + Fore.WHITE)
        bot.save_chat_history(history_file)
        break
    # submits user input to chatbot
    response = bot.generate_response(user_input)['content']
    bot.save_chat_history(history_file)
    print(Fore.GREEN + f"Bot: {response}\n")
