from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot import ChatBot
from database import FAQDatabase
# from app.chatbot import ChatBot
# from app.database import FAQDatabase

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = FAQDatabase()
chatbot = ChatBot(db)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FAQ ChatBot API!"}

@app.get("/ask/")
def ask_question(question: str):
    try:
        response = chatbot.get_answer(question)

        if not response:
            return {"question": question, "answer": "Sorry, I don't have an answer for that question."}
        
        return {
            "question": question,
            "answer": response["answer"],
            "url": response["url"]  
        }
    except Exception as e:
        return {"error": str(e), "message": "An error occurred while processing your question."}
