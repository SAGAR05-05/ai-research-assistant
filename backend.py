from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

app = FastAPI()

# Load pre-trained BERT-based models
qa_pipeline = pipeline("question-answering", model="deepset/bert-base-cased-squad2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Request models
class QARequest(BaseModel):
    question: str
    context: str

class SummaryRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Welcome to the Research Assistant API"}

@app.post("/qa/")
def answer_question(request: QARequest):
    response = qa_pipeline(question=request.question, context=request.context)
    answer = response["answer"]
    score = response["score"]

    # Set a confidence threshold
    if score < 0.4:  # Adjust this threshold if needed
        return {
            "question": request.question,
            "context": request.context,
            "answer": "I'm not confident in my answer. Can you provide more details?",
            "score": score
        }

    # Send back a more detailed response
    return {
        "question": request.question,
        "context": request.context,
        "answer": answer,
        "score": score
    }
    

@app.post("/summarize/")
def summarize_text(request: SummaryRequest):
    summary = summarizer(request.text, max_length=150, min_length=50, do_sample=False)
    
    return {
        "original_text": request.text,
        "summary": summary[0]["summary_text"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
