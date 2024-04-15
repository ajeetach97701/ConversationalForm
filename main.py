from langchain.llms.ollama import Ollama
from langchain.chains import TransformChain, LLMChain, SimpleSequentialChain
from langchain.vectorstores import FAISS
import google.generativeai as genai
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field, EmailStr
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_tagging_chain,create_tagging_chain_pydantic
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# model = Ollama(model = "llama2")
llm = ChatOpenAI(model='gpt-3.5-turbo-0613', temperature=0)
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY GOES HERE"
# model = ChatGoogleGenerativeAI(model = 'gemini-pro', temperature=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# prompt = ChatPromptTemplate.from_template(template=template)
# database = FAISS.load_local("ConversationalFormDemo",embeddings)

class PersonalDetails(BaseModel):
    first_name: str = Field(
        ...,
        description="This is the first name of the user.",
    )
    last_name: str = Field(
        ...,
        description="This is the last name of the user.",
    )
    email: str = Field(
        ...,
        description="This is the email of the user",
    )

chain = create_tagging_chain_pydantic(PersonalDetails,llm)

# test_string = "My last name is acharya and you can contact me at ajeetach@gmail.com."
# test_string_1 = "my first name is Ajeet"
# print(chain.run(test_string_1))

# def get_user_input() -> PersonalDetails:
#     first_name = input("Enter your first name: ")
#     last_name = input("Enter your last name: ")
#     age = input("Enter your Age: ")
#     return PersonalDetails(first_name=first_name,last_name = last_name, age=age)

def check_what_is_empty(user_personal_details):
    ask_for = []
    for field, value in user_personal_details.dict().items():
        if value in [None, "", 0]:
            print(f"Field '{field} is empty.'")
            ask_for.append(f'{field}')
    return ask_for


## checking the response and adding it
def add_non_empty_details(current_details: PersonalDetails, new_details: PersonalDetails):
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details


def ask_for_info(ask_for = ['first_name','last_name', "email"]):
    first_prompt = ChatPromptTemplate.from_template(
        "Below is are some things to ask the user for in a coversation way. \
        you should only ask one question at a time even if you don't get all the info \
        don't ask as a list! Don't greet the user! Don't say Hi.\
        Explain you need to get some info.\
        If the ask_for list is empty then thank \
        them and ask how you can help them \n\n \
        ### ask_for list: {ask_for}"
    )
    
    info_chain = LLMChain(llm = llm, prompt=first_prompt)
    ai_chat= info_chain.run(ask_for = ask_for)
    return ai_chat

def filter_response(text_input, user_details):
    chain = create_tagging_chain_pydantic(PersonalDetails, llm)
    res = chain.run(text_input)
    user_details = add_non_empty_details(user_details, res)
    ask_for = check_what_is_empty(user_details)
    
    return user_details, ask_for

# sender = "abcd"
def filter_response(text_input, user_details,sender):
    chain = create_tagging_chain_pydantic(PersonalDetails, llm)
    res = chain.run(text_input)
    user_details = add_non_empty_details(user_details, res)
    ask_for = check_what_is_empty(user_details)
    print(user_details)
    return user_details, ask_for

def main():
    user_details = PersonalDetails(first_name="",
                                last_name="",
                                email="",
    )
    sender = 'abc'
    ask_for=  ['first_name','last_name', "email"]
    while True:
        if ask_for:
            ques = ask_for_info(ask_for)
            text_input = input(ques)
            user_details, ask_for = filter_response(text_input, user_details, sender)
            print(ask_for)
        else:
            break


if __name__ == "__main__":
    main()
