from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


class UserInput(BaseModel):
    text: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "EduGenie is running successfully"
    }


@app.post("/qa")
async def qa(data: UserInput):
    result = answer_question(data.text)
    return {"result": result}


@app.post("/explain")
async def explain(data: UserInput):
    result = explain_concept(data.text)
    return {"result": result}


@app.post("/quiz")
async def quiz(data: UserInput):
    result = generate_quiz(data.text)
    return {"result": result}


@app.post("/summarize")
async def summarize(data: UserInput):
    result = summarize_text(data.text)
    return {"result": result}


@app.post("/learn/recommendations")
async def learning_recommendations(data: UserInput):
    result = get_learning_recommendations(data.text)
    return {"result": result}