from VectorStore.LLMEmbeddings.llmEmbeddings import llmO
from rredis import getData,setData
from langchain.chains import create_tagging_chain,create_tagging_chain_pydantic
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import TransformChain, LLMChain, SimpleSequentialChain

from pydantic import BaseModel, Field

def update_dict(previous_state, new_state):
    if previous_state == new_state:
        for key in new_state.keys():
            if new_state[key] == "":
                new_state[key] = "Not Provided"
                break
    return new_state


class ProductDetails(BaseModel):
    dummy:str = Field(
        ...,
        description="Dummy field",
    )
    productName: str = Field(
        ...,
        description="Name of the product",
    )
    productDimension: str = Field(
        ...,
        description="Dimension of the product",
    )
    brand: str = Field(
        ...,
        description="Brand of the product",
    )

class PersonalDetails(BaseModel):
    name: str = Field(
        ...,
        description="Name of the user",
    )
    email: str = Field(
        ...,
        description="Email of the user",
    )
    quantity: str = Field(
        ...,
        description="Quantity of required product",
    )

chain = create_tagging_chain_pydantic(ProductDetails,llmO)

test_string = "i want to buy door spring that can fit in the box of 50*50."

print(chain.run(test_string))

# user = ProductDetails(productName="",productDimension="")

def check_what_is_empty(user_detail):
    ask_for = []
    for field, value in user_detail.items():
        if value in [None,"",0]:
            print(f"Field '{field}' is empty.")
            ask_for.append(f'{field}')
    return ask_for

# ask_for = check_what_is_empty(user)
# print(ask_for)

def add_non_empty_details(current_details: ProductDetails, new_details: ProductDetails):
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, "", 0]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details

# user1 = add_non_empty_details(user, chain.run("i want to buy door spring that can fit in the box of 50*50."))
# print(user1)

def ask_for_info(ask_for = ["productName","productDimension","brand"]):
    first_prompt = ChatPromptTemplate.from_template(
        "Below are some things to ask the user for in a conversational way.\
         You shoud ask one question at a time even if you don't get all the info, don't ask as a list! \
         Don't greet the user! Don't say Hi. Explain you need to get some info. \
         If the ask_for list is empty then thank them and ask how you can help them. \
        ### ask_for list : {ask_for}"
    )
    info_gathering_chain = LLMChain(llm=llmO, prompt=first_prompt)
    ai_chat = info_gathering_chain.run(ask_for=ask_for)
    return ai_chat

def filter_response_Product(text_input, user_details, sender,form):
    if form == "ProductDetails": 
        chain = create_tagging_chain_pydantic(pydantic_schema=ProductDetails, llm=llmO)
        res = chain.run(text_input)
        user_details = add_non_empty_details(user_details, res)
        print("======",user_details.dict())
        print("======",getData(sender).get("ProductDetails"))
        user_details = update_dict(getData(sender).get("ProductDetails"), user_details.dict())
        ask_for = check_what_is_empty(user_details)
        return user_details, ask_for
    
    
    
    if form == "PersonalDetails":
        chain = create_tagging_chain_pydantic(pydantic_schema=PersonalDetails, llm=llmO)
        res = chain.run(text_input)
        user_details = add_non_empty_details(user_details, res)
        print("======", user_details.dict())
        print("======", getData(sender).get("PersonalDetails"))
        # user_details = update_dict(getData(sender).get("PersonalDetails"), user_details.dict())
        ask_for = check_what_is_empty(user_details.dict())
        return user_details, ask_for
# user_details, ask_for = filter_response_Product("i want to buy door spring.", user)
# print(user_details,"==",ask_for)
