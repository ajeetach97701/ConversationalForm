from rredis import getData, setData, deleteData, flushAll
from fastapi import FastAPI
import sys
sys.path.append('/Volumes/Ajeet/LLM Projects/ConversationalForm/')
from main import ask_for_info, filter_response, PersonalDetails

app = FastAPI()

data = {
    "PersonalDetails":"",
    "History":""
}

def Personal(query:str, sender:str):
    if getData(sender) is None:
        setData(sender, data)
    userNull = PersonalDetails(first_name=  "",last_name="", email="" )
    if getData(sender).get("PersonalDetails") == "":
        print(getData(sender))
        setData(sender, {"PersonalDetails":userNull.dict()})
    data = getData(sender).get("PersonalDetails")
    user = PersonalDetails(**data)
    user,ask_for = filter_response(query, user, sender)
    redisData = getData(sender)
    redisData["PersonalDetails"] = user.dict()
    setData(sender, redisData)
    print(getData(sender).get("PersonalDetails"))
    if ask_for:
        ai_response = ask_for_info(ask_for)
        return ai_response
    else:
        return getData(sender)

@app.get("/test")
def output(query:str, sender:str):
    if getData(sender) is None:
        setData(sender, query)
    return getData(sender)
        
        
        
app = FastAPI()
@app.get("/test/")
def form(query: str,sender: str):
    if getData(sender) is None:
        setData(sender, data)
    if getData(sender).get("Form") == "PersonalDetails":
        return Personal(query, sender)