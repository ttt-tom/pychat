import difflib

class ChatBot:
    def __init__(self, database):
        self.db = database

    def get_answer(self, question: str) -> dict:

        faq_data = self.db.get_faq_data()  


        for item in faq_data:
            if question.lower() == item["question"].lower():
                return {
                    "answer": item["answer"],
                    "url": item.get("url", None)  
                }


        questions = [faq["question"] for faq in faq_data]
        closest_matches = difflib.get_close_matches(question, questions, n=1, cutoff=0.6)

        if closest_matches:
            for item in faq_data:
                if item["question"] == closest_matches[0]:
                    explanation = "Whether you want to inquire about the following: "
                    return {
                        "answer": explanation +"  "+ item["answer"],
                        "url": item.get("url", None)
                    }


        return {
            "answer": "Sorry, I don't have an answer for that question. Could you rephrase it?",
            "url": None
        }
